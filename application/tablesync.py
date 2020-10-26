# Copyright (c) 2020, David Canaday, All rights reserved.
# TableSync is an open source project designed to help restaurants
# manage their tables digitally by running this program on computers
# like the raspberry pi which is cheap and easy to set up

import tkinter as tk  # Used to provide GUI
from tkinter import messagebox
import logging
import asyncio  # Used to manage both event loops (tkinter and socket)
import socket  # I want direct control over sockets
import json


# Main application class that manager tkinter app and asyncio socket
class Application(tk.Tk):
    def __init__(self, settings, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.loop = asyncio.get_event_loop()
        self.notStopped = True  # Variable for cleaner exits of infinite loops
        self.connected = False
        self.firstTime = True  # We only want to request a full update upon connection if we just joined
        self.sock = None  # Stores the socket object
        self.settings = settings
        self.buttons = settings['buttons']  # Should be dictionary containing all buttons that need to be drawn
        self.uiObjects = {}  # Dictionary to hold all tkinter objects
        if settings['socktype'] == 'server':
            self.socket_loop = self.socket_server
            self.title("TableSync (Server)")
        else:
            self.socket_loop = self.socket_client
            self.title("TableSync")
        self.protocol('WM_DELETE_WINDOW', self.stop)
        self.geometry(f"{settings['width']}x{settings['height']}")
        self.minsize(settings['width'], settings['height'])
        self.create_widgets()

    def create_widgets(self):
        copyright_string = '-- Copyright (c) 2020, All rights reserved. --'
        tk.Label(self, text=copyright_string, bd=2, relief='sunken').pack(side='bottom', fill='x')
        for num in self.buttons:
            self.uiObjects[f'b{num}'] = tk.Button(self, text=str(num), activebackground='grey', bd=3,
                                                  command=lambda n=num: self.send_update(n, self.buttons[n]['val']),
                                                  background=self.settings['colors'][0],
                                                  font=self.settings['fontstring'],
                                                  state='disabled' if self.buttons[num].get('deco') else 'normal')
            self.uiObjects[f'b{num}'].pack()
            self.uiObjects[f'b{num}'].place(x=self.buttons[num]['pos'][0], y=self.buttons[num]['pos'][1],
                                            height=self.buttons[num]['size'][0], width=self.buttons[num]['size'][1])
        for i in range(0, len(self.settings['colors'])):
            self.uiObjects[f'l{i}'] = tk.Label(self,
                                               text=f"{self.settings['colors'][i]} == {self.settings['states'][i]}",
                                               fg=self.settings['colors'][i],
                                               bg="grey", font=self.settings['fontstring'])
            self.uiObjects[f'l{i}'].pack()
            self.uiObjects[f'l{i}'].place(x=self.settings['labelPosX'], y=self.settings['labelPosY'][i])
        self.uiObjects['statusLabel'] = tk.Label(self, text="Waiting for connection...",
                                                 font=self.settings['fontstring'])
        self.uiObjects['statusLabel'].pack()
        self.uiObjects['statusLabel'].place(x=210, y=5)

    async def connected_loop(self, connection):
        self.connected = True
        while self.connected and self.notStopped:
            await asyncio.sleep(0.001)
            try:
                data = connection.recv(8 * 8)  # Receive message header
                data = data.decode()
                size, messageType = int(data[2:]), data[0:2]  # Extract data from header
            except ConnectionResetError:
                connected = False
                print("Scream")
                break
            if not data:
                break
            self.uiObjects['statusLabel'].configure(text='')
            logging.info(f"received {messageType} message")
            if messageType == 'ur':  # Mass Update Request (no message body)
                self.send_full_update()
            else:
                data = connection.recv(size)  # Receive actual message
                message = json.dumps(data.decode())
                if messageType == 'um' or messageType == 'su':  # Mass Update Response (message) or Single Update
                    for num in message:
                        self.updateButton(num, message[num])

    async def socket_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind(self.settings['addr'])
            sock.setblocking(0)
            sock.listen(1)
            while self.notStopped:
                await asyncio.sleep(0.001)
                try:
                    connection, address = sock.accept()
                    with connection:
                        self.sock = connection
                        self.uiObjects['statusLabel'].configure(text='Connected!')
                        if self.firstTime:
                            sock.sendall(f'ur{0:<6}'.encode())
                            self.firstTime = False
                        await self.connected_loop(connection)
                except Exception:
                    pass

    async def socket_client(self):
        while self.notStopped:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                self.sock = sock
                sock.setblocking(0)
                connected = False
                while not connected:
                    await asyncio.sleep(0.001)
                    try:
                        sock.connect(self.settings['addr'])
                        connected = True
                        self.uiObjects['statusLabel'].configure(text='Connected!')
                        if self.firstTime:
                            sock.sendall(f'ur{0:<6}'.encode())
                            self.firstTime = False
                    except Exception:
                        pass
                await self.connected_loop(sock)

    async def gui_loop(self):
        while self.notStopped:
            self.update()  # Take control of tkinter mainloop
            await asyncio.sleep(0.001)

    def send_full_update(self):
        update = {}
        for num in self.buttons:
            update[num] = self.buttons[num]['val']
        message = json.dumps(update)
        self.sock.sendall(f'um{len(message):<6}{message}'.encode())
        logging.info('sent full update')

    def send_update(self, num, val):
        logging.info(f'requested that table {num} be updated to {self.settings["states"][val]}')
        newval = (self.buttons[num]['val'] + 1) % 3
        self.uiObjects[f'b{num}'].configure(bg=self.settings['colors'][newval])
        self.buttons[num]['val'] = newval
        message = json.dumps({num: newval})
        try:
            self.sock.sendall(f'su{len(message):<6}{message}'.encode())
        except Exception as e:
            logging.error(f"Failed to send message: {e}")
            self.connected = False

    def updateButton(self, num, val):
        self.buttons[num]['val'] = val
        self.uiObjects[f'b{num}'].configure(bg=self.settings['colors'][val])

    def stop(self):
        prompt = messagebox.askquestion(title="Exit and Shutdown", message="Do you really want to exit the program "
                                                                           "and shutdown?", icon="warning")
        if prompt == "yes":
            self.notStopped = False
            self.loop.stop()

    def start_loop(self):
        # Create async io loop to run tkinter and async socket
        self.loop.create_task(self.gui_loop())
        self.loop.create_task(self.socket_loop())
        try:
            self.loop.run_forever()
        except Exception as e:
            logging.warning(f"Exception occurred while running mainloop: {e}")
        finally:
            self.loop.close()
            self.destroy()

# Copyright (c) 2020, David Canaday, All rights reserved.

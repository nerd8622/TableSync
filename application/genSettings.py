# Use this template to generate the settings file to run with the application

import json

settings = {
    'addr': ('localhost', 4444),  # Address-port pair
    'socktype': 'server',  # Whether to act as client or server
    'height': 600,
    'width': 800,
    'fontcolor': 'black',
    'fontstring': 'Verdana 12 bold',
    'colors': ['white', 'red', 'blue'],
    'states': ['clean', 'occupied', 'dirty'],
    'labelPosY': [10, 33, 56],
    'labelPosX': 10,
    'buttons': {  # Dictionaries to represent each
        1: {'val': 0, 'size': (60, 60), 'pos': (210, 30)},
        2: {'val': 0, 'size': (60, 60), 'pos': (300, 30)},
        3: {'val': 0, 'size': (60, 60), 'pos': (390, 30)},
        4: {'val': 0, 'size': (60, 60), 'pos': (500, 5)},
        5: {'val': 0, 'size': (60, 60), 'pos': (615, 25)},
        6: {'val': 0, 'size': (60, 60), 'pos': (715, 5)},
        101: {'val': 0, 'size': (100, 80), 'pos': (5, 110)},
        102: {'val': 0, 'size': (100, 80), 'pos': (5, 220)},
        103: {'val': 0, 'size': (100, 80), 'pos': (5, 330)},
        104: {'val': 0, 'size': (100, 80), 'pos': (5, 440)},
        201: {'val': 0, 'size': (100, 80), 'pos': (95, 160)},
        202: {'val': 0, 'size': (100, 80), 'pos': (95, 270)},
        203: {'val': 0, 'size': (100, 80), 'pos': (95, 380)},
        301: {'val': 0, 'size': (100, 80), 'pos': (200, 100)},
        302: {'val': 0, 'size': (100, 80), 'pos': (200, 210)},
        303: {'val': 0, 'size': (100, 80), 'pos': (200, 320)},
        304: {'val': 0, 'size': (100, 80), 'pos': (185, 450)},
        401: {'val': 0, 'size': (100, 80), 'pos': (290, 100)},
        402: {'val': 0, 'size': (100, 80), 'pos': (290, 210)},
        403: {'val': 0, 'size': (100, 80), 'pos': (290, 320)},
        404: {'val': 0, 'size': (100, 80), 'pos': (275, 450)},
        501: {'val': 0, 'size': (100, 80), 'pos': (380, 100)},
        502: {'val': 0, 'size': (100, 80), 'pos': (380, 210)},
        503: {'val': 0, 'size': (100, 80), 'pos': (380, 320)},
        504: {'val': 0, 'size': (100, 80), 'pos': (365, 450)},
        601: {'val': 0, 'size': (100, 80), 'pos': (490, 90)},
        602: {'val': 0, 'size': (100, 80), 'pos': (490, 200)},
        603: {'val': 0, 'size': (100, 80), 'pos': (490, 320)},
        701: {'val': 0, 'size': (90, 75), 'pos': (605, 90)},
        702: {'val': 0, 'size': (90, 75), 'pos': (610, 200)},
        703: {'val': 0, 'size': (90, 75), 'pos': (610, 320)},
        801: {'val': 0, 'size': (90, 75), 'pos': (705, 100)},
        802: {'val': 0, 'size': (90, 75), 'pos': (705, 200)},
        803: {'val': 0, 'size': (90, 75), 'pos': (705, 300)},
        804: {'val': 0, 'size': (90, 75), 'pos': (705, 400)},
        'Tortilla\nStation': {'size': (100, 80), 'pos': (460, 450), 'deco': 1}
    }
}
with open('settings.conf', 'w') as f:
    json.dump(settings, f)

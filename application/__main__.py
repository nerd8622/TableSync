import json
import tablesync

with open("settings.conf", "r") as sfile:
    settings = json.load(sfile)
    settings['addr'] = tuple(settings['addr'])

app = tablesync.Application(settings)
app.start_loop()

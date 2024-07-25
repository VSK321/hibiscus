import argparse
import uvicorn
from server import app, build
from peewee import *
import importlib
import glob

"""
Capture all command arguments and compare to functions from .commands and rose.commands
"""

parser = argparse.ArgumentParser(description='Rose framework management')
parser.add_argument("command", nargs="+")  # Capture optional argument after "command"
#parser.add_argument("--o", type=str)
#parser.add_argument('runserver', nargs="2", type=str, help="Runserver and ")
#parser.add_argument('--port', type=int)
#parser.add_argument('--migrate', type=str)
try:
    args = parser.parse_args()
except Exception as e:
    print(f"Error parsing arguments: {e}")

argsdict = vars(args)

commands = glob.glob('./commands/*.py')

#importlib.import_module()

#parser.add_argument('migrate', type=str, help="")
#args = parser.parse_args(['MIGRATE'])
#argsdict += vars(args)

# if argsdict['migrate']:
#     settings: dict = json.loads('dev_appsettings.json')
    
#     db = SqliteDatabase(settings['database'])
#     db.connect()
    
#     db.create_tables([Models.User, Post])

#for com in getattr(locals().get("commands") or globals().get("commands"))

if 'runserver' in argsdict['command']:
    if len(argsdict['command']) == 2:
        port = int(argsdict['command'][1])
    else:
        port = 8000
    build()
    try:
        uvicorn.run(
            app,
            host='127.0.0.1',
            port=port)
    except KeyboardInterrupt:
        pass
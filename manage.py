import argparse
import subprocess
import uvicorn
from server import app, build
from peewee import *
import json
import os
import importlib
import glob

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
#parser.add_argument('migrate', type=str, help="")
#args = parser.parse_args(['MIGRATE'])
#argsdict += vars(args)

# if argsdict['migrate']:
#     settings: dict = json.loads('dev_appsettings.json')
    
#     db = SqliteDatabase(settings['database'])
#     db.connect()
    
    #db.create_tables([Models.User, Post])

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
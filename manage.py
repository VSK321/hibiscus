import argparse
import subprocess
import uvicorn
from server import app

parser = argparse.ArgumentParser(description='Rose framework management')
parser.add_argument('runserver', type=str, help="")
args = parser.parse_args()
argsdict = vars(args)

if 'runserver' in argsdict:
    try:
        uvicorn.run(
            app,
            host='127.0.0.1',
            port=8080)
    except KeyboardInterrupt:
        pass
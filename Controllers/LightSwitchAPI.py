import controller
from AppLoc import *
import json
import socket

@app.set_route("/lightapi")
class Controller(controller.Controller):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def main(self):
        request = json.loads(self.http_data)
        if (request["request"]):
            #print("success: open")
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
            sock.connect(('192.168.0.50', 4444))
            sock.send(b'on')
            sock.close()
        else:
            #print("success: close")
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
            sock.connect(('192.168.0.50', 4444))
            sock.send(b'off')
            sock.close()
        val = { "status" : True }
        await self.return_data(json.dumps(val))


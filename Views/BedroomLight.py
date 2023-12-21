import socket
import view
from AppLoc import *
import Views.Calculator

@app.set_route("/BedroomLight")
class Page(view.View):

    def __init__(self):
        self.calc = Views.Calculator.Page()

    async def TurnOn(self):
        #sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        #sock.connect(('192.168.0.50', 4444))
        #sock.send(b'on')
        #sock.close()
        print("On")
        return True

    async def TurnOff(self):
        #sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        #sock.connect(('192.168.0.50', 4444))
        #sock.send(b'off')
        #sock.close()
        print("Off")
        return True

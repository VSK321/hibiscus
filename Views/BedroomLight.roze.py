import socket

class Page:

    def __init__(self):
        pass

    def TurnOn(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        sock.connect(('192.168.0.50', 666))
        sock.send(b'on')
        sock.close()
        return True

    def TurnOff(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        sock.connect(('192.168.0.50', 666))
        sock.send(b'off')
        sock.close()
        return True

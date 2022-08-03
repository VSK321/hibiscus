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

    def main(self):
        temp = ""
        temp = temp + '<button class="btn btn-primary" rozeclick="TurnOn">Turn On</button>\n' 
        temp = temp + '<div class="row">\n' 
        temp = temp + '		<button class="btn btn-primary" rozeclick="TurnOff">Turn Off</button>\n' 
        temp = temp + '</div>\n' 
        return temp
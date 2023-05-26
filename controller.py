import httpheaders
import uuid

class Controller:

    def __init__(self, conn, addr, http_headers, http_data, Critical_View):
        self.conn = conn
        self.addr = addr
        self.http_headers = http_headers
        self.http_data = http_data
        self.Critical_View = Critical_View

    def reroute(self, path):
        sentData = "HTTP/1.1 302 Found\r\n"
        sentData += httpheaders.HTTP_Headers_Constructor({"Location": path, "Server": "Roze", "X-Frame-Options": "SameOrigin", "Cache-Control": "no-cache", "connection": "close"})
        self.conn.send(sentData.encode())
        self.conn.close()

    def return_data(self, data):
        sentData = "HTTP/1.1 200 OK\r\n"
        sentData += httpheaders.HTTP_Headers_Constructor({"Server": "Roze", "X-Frame-Options": "SameOrigin", "Cache-Control": "no-cache", "connection": "close"})
        sentData += data
        self.conn.send(sentData.encode())
        self.conn.close()

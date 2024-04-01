import httpheaders
import uuid

class Controller:

    def __init__(self, send, receive, scope, Critical_View):
        self.send = send
        self.receive = receive
        self.scope = scope
        self.Critical_View = Critical_View

    async def reroute(self, path):
        headers = httpheaders.HTTP_Headers_Uvicorn_Constructor({"Location": path, "Server": "Rose", "X-Frame-Options": "SameOrigin", "Cache-Control": "no-cache", "connection": "close"})
        await self.send({"type": "http.response.start", "status": 302, "headers": headers})
        await self.send({"type": "http.response.body", "body": b''})

    async def return_data(self, data):
        headers = httpheaders.HTTP_Headers_Uvicorn_Constructor({"Server": "Rose", "X-Frame-Options": "SameOrigin", "Cache-Control": "no-cache", "connection": "close"})
        await self.send({"type": "http.response.start", "status": 200, "headers": headers})
        await self.send({"type": "http.response.body", "body": data.encode()})

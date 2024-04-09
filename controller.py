import httpheaders
import uuid
import rose_compiler
import view
from jinja2 import BaseLoader, Environment, FileSystemLoader, PackageLoader
from os import getcwd
import importlib

class Controller(view.View):

    def __init__(self, send, receive, scope, Critical_View):
        self.send = send
        self.receive = receive
        self.scope = scope
        self.Critical_View = Critical_View
        self.path = None

    async def reroute(self, path):
        headers = httpheaders.HTTP_Headers_Uvicorn_Constructor({"Location": path, "Server": "Rose", "X-Frame-Options": "SameOrigin", "Cache-Control": "no-cache", "connection": "close"})
        await self.send({"type": "http.response.start", "status": 302, "headers": headers})
        await self.send({"type": "http.response.body", "body": b''})

    async def return_data(self, data):
        headers = httpheaders.HTTP_Headers_Uvicorn_Constructor({"Server": "Rose", "X-Frame-Options": "SameOrigin", "Cache-Control": "no-cache", "connection": "close"})
        await self.send({"type": "http.response.start", "status": 200, "headers": headers})
        await self.send({"type": "http.response.body", "body": data.encode()})

    async def return_page(self, path: str, params: dict):
        if self.path == path:
            await self.return_data(await self.page())
            return
        cwd = getcwd()
        #chdir(path)
        with open(path, 'r') as file:
            data = file.read()
        env = Environment(loader=FileSystemLoader(cwd+"/templates/"), line_statement_prefix="%", variable_start_string="${", variable_end_string="}", enable_async=True)
        tmpl = env.from_string(data)
        await self.return_data(await tmpl.render_async(**params))
        #compiled_page = rose_compiler.ConvertFile(data)
        #page = 'async def page(self, page_change=None):\n    rose_line = ""' + compiled_page + '\n    if page_change != None:    rose_line = self._pageChange(rose_line, page_change)\n    return rose_line'
        #importlib.import_module
        #c = compile(page, 'x', 'exec')
        #setattr(self, c, c)
        #await self.return_data(await self.page())
        
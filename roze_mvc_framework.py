from types import ModuleType
import roze_server_framework
import roze_compiler
import importlib
import httpheaders
import mimetypes
import os
import glob
from AppLoc import *
import asyncio
import socket

class MVC(roze_server_framework.HTTP_Server):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Critical_View: dict[str, ModuleType] = {}

    async def HTML_Manager(self, page_view, softpath) -> str:
        page_model = await self.Critical_View['MainLayout'].Page().main()
        return page_model

    async def ViewHandlerAsync(self, softpath: str) -> bytes:
        sentData = ""
        headers = {'Server': 'Roze', 'X-Frame-Options': 'SameOrigin', 'Cache-Control': 'no-cache', 'Content-Type': 'text/html', 'connection': 'close'}
        sentData = httpheaders.HTTP_Headers_Constructor(headers)
        sentData = sentData + await self.HTML_Manager(await app.funcs[softpath]['module']().main(), softpath)
        sentData = sentData.encode()
        return sentData

    async def ControllerHandlerAsync(self, conn: socket.socket, addr, http_headers: httpheaders.HTTP_Headers, http_data: str, softpath: str) -> None:
        await app.funcs[softpath]['module'](**{'conn':conn, 'addr':addr, 'http_headers':http_headers, 'http_data':http_data, 'Critical_View':self.Critical_View}).main()

    def PublicHandler(self, softpath: str) -> bytes:
        headers = {'Server': 'Roze', 'X-Frame-Options': 'SameOrigin', 'Cache-Control': 'no-cache', 'Content-Type': mimetypes.guess_type(softpath)[0], 'connection': 'close'}
        cwd = os.getcwd()
        sentData = httpheaders.HTTP_Headers_Constructor(headers)
        os.chdir(app.funcs[softpath]['hardpath'])
        f = open(app.funcs[softpath]['file'], 'rb')
        sentData = sentData.encode() + f.read()
        f.close()
        os.chdir(cwd)
        return sentData

    async def HTTPRequestManagerAsync(self, conn: socket.socket, addr, http_headers: httpheaders.HTTP_Headers, http_data: str) -> None:
        loop = asyncio.get_event_loop()
        softpath = http_headers.Url###Check if softpath exists
        try:
            softpath_Type = app.funcs[softpath]['type']
            if softpath_Type == 'view':
                sentData = "HTTP/1.1 200 OK\r\n"
                sentData = sentData.encode() + await self.ViewHandlerAsync(softpath)
                await loop.sock_sendall(conn, sentData)
                conn.close()
            elif softpath_Type == 'controller':
                await self.ControllerHandlerAsync(conn, addr, http_headers, http_data, softpath)
            elif softpath_Type == 'public':
                sentData = "HTTP/1.1 200 OK\r\n"
                sentData = sentData.encode() + self.PublicHandler(softpath)
                await loop.sock_sendall(conn, sentData)
                conn.close()
        except KeyError:
            sentData = "HTTP/1.1 404 Not Found\r\n"
            sentData = sentData.encode() + await self.ViewHandlerAsync('/_error')
            await loop.sock_sendall(conn, sentData)
            conn.close()

    def Build(self) -> None:
        print('Building...')
        cwd = os.getcwd()
        for f in os.listdir(os.getcwd()+'/Shared'):
            if f.endswith('.roze'):
                roze_compiler.Convert(os.getcwd()+'/Shared', f)
        for f in os.listdir(os.getcwd()+'/Shared'):
            if f.endswith('.roze'):
                #os.chdir(cwd + "/g")
                self.Critical_View[f[0:-5]] = importlib.import_module(f[0:-5])
                os.remove(f[0:-5] + ".py")
               # os.chdir(cwd)
        #Discover all files within cwd and check for .roze and .py
        views = glob.glob('./**/*.roze', recursive=True)
        controllers = glob.glob('./*/**/*.py', recursive=True)
        controllers = [controller for controller in controllers if not controller.endswith(".roze.py")]
        os.chdir(cwd + "/root")
        public = glob.glob("./**/*.*", recursive=True)
        os.chdir(cwd)

        for obj in public:
            path = obj.split("\\")
            divider = "\\"
            if len(path) == 1:
                path = path[0].split("/")
                divider = "/"
            name = path[-1]
            app.funcs["/" + "/".join(path[1:])] = {'type': 'public', 'file': (name), 'hardpath': (cwd + "/root" + "/".join(path[1:-1]))}

        #Import and check for implementations of View or Controller
        for view in views:
            if view.startswith(".\\Shared") or view.startswith("./Shared"):
                continue
            path = view.split("\\")
            divider = "\\"
            if len(path) == 1:
                path = path[0].split("/")
                divider = "/"
            roze_compiler.Convert(divider.join(path[0:-1]), path[-1]);

        for view in views:
            if view.startswith(".\\Shared") or view.startswith("./Shared"):
                continue
            path = view.split("\\")
            divider = "\\"
            if len(path) == 1:
                path = path[0].split("/")
                divider = "/"
            name = path[-1][0:-5]
            #os.chdir(cwd + "/g")
            importlib.import_module(name)
            os.remove(name + ".py")

        for controller in controllers:
            path = controller.split("\\")
            divider = "\\"
            if len(path) == 1:
                path = path[0].split("/")
                divider = "/"
            name = path[-1][0:-3]
            os.chdir(cwd + "/" + divider.join(path[1:-1]))
            controllerCode = open(path[-1], 'r')
            data = controllerCode.read()
            controllerCode.close()
            os.chdir(cwd)
            currControllerCode = open(path[-1], 'w')
            currControllerCode.write(data)
            currControllerCode.close()
            importlib.import_module(name)
            os.remove(path[-1])
            
        for task in backgroundtasks.funcs:
            task.main()


        os.chdir(cwd)
        print('Build successful.')

#socket.gethostbyname(socket.gethostname())
#instance = MVC(socket.gethostbyname(socket.gethostname()), 80, 50)
instance = MVC("127.0.0.1", 80, 50)
instance.Build()
#instance.Start_Server()
try:
    asyncio.run(instance.run_server())
except:
    pass


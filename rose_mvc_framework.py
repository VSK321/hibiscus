from builtins import KeyError
from types import ModuleType
import rose_server_framework
import rose_compiler
import importlib
import httpheaders
import mimetypes
import os
import glob
from AppLoc import *
import AppLoc
import asyncio
import socket
import sys
import pickle
import traceback

class MVC(rose_server_framework.HTTP_Server):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Critical_View: dict[str, ModuleType] = {}

    async def ViewHandlerAsync(self) -> bytes:
        headers = {'Server': 'Roze', 'X-Frame-Options': 'SameOrigin', 'Cache-Control': 'no-cache', 'Content-Type': 'text/html', 'connection': 'close'}
        sentData = httpheaders.HTTP_Headers_Constructor(headers)
        sentData = sentData + await self.Critical_View['MainLayout'].Page().main()
        sentData = sentData.encode()
        return sentData

    async def ControllerHandlerAsync(self, conn: socket.socket, addr, http_headers: httpheaders.HTTP_Headers, http_data: str, softpath: str, recognised_pattern: str, subs: dict[str, object]) -> None:
        await app.funcs[recognised_pattern]['module'](**{'conn':conn, 'addr':addr, 'http_headers':http_headers, 'http_data':http_data, 'Critical_View':self.Critical_View}).main()

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
            #Match softpath pattern
            found_pattern = None
            subs = {}
            for path_to_re in app.paths_to_re:
                if bool(path_to_re[0].fullmatch(softpath)):
                    found_pattern = path_to_re[1]
                    subs = {tup[0][0]: getattr(sys.modules['builtins'], tup[0][1])(tup[1]) for tup in zip(path_to_re[2], softpath.split("/")[1:]) if tup[0] != None}
                    break
            if found_pattern == None:
                softpath_Type = app.funcs[softpath]['type']
            else:
                softpath_Type = app.funcs[found_pattern]['type']
            if softpath_Type == 'view':
                sentData = "HTTP/1.1 200 OK\r\n"
                sentData = sentData.encode() + await self.ViewHandlerAsync()
                await loop.sock_sendall(conn, sentData)
                conn.close()
            elif softpath_Type == 'controller':
                await self.ControllerHandlerAsync(conn, addr, http_headers, http_data, softpath, found_pattern, subs)
            elif softpath_Type == 'public':
                if found_pattern != None:
                    raise KeyError
                sentData = "HTTP/1.1 200 OK\r\n"
                sentData = sentData.encode() + self.PublicHandler(softpath)
                await loop.sock_sendall(conn, sentData)
                conn.close()
        except KeyError as e:
            print('Page not found: ' + str(e))
            sentData = "HTTP/1.1 404 Not Found\r\n"
            sentData = sentData.encode() + await self.ViewHandlerAsync()
            await loop.sock_sendall(conn, sentData)
            conn.close()

    def Build(self) -> None:
        print('Building...')
        cwd = os.getcwd()
        for f in os.listdir(os.getcwd()+'/Shared'):
            if f.endswith('.rose'):
                rose_compiler.Convert(os.getcwd()+'/Shared', f)
        for f in os.listdir(os.getcwd()+'/Shared'):
            if f.endswith('.rose'):
                #os.chdir(cwd + "/g")
                self.Critical_View[f[0:-5]] = importlib.import_module(f[0:-5])
                os.remove(f[0:-5] + ".py")
               # os.chdir(cwd)
        #Discover all files within cwd and check for .rose and .py
        views = glob.glob('./**/*.rose', recursive=True)
        controllers = glob.glob('./*/**/*.py', recursive=True)
        controllers = [controller for controller in controllers if not controller.endswith(".rose.py")]
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
            rose_compiler.Convert(divider.join(path[0:-1]), path[-1], True)
            
        for view in views:
            if view.startswith(".\\Shared") or view.startswith("./Shared"):
                continue
            path = view.split("\\")
            divider = "\\"
            if len(path) == 1:
                path = path[0].split("/")
                divider = "/"
            value = '.'.join(view.split("\\")[1:])[:-5]
            full_val = divider.join(path[0:-1])+divider+path[-1][:-5]+".py"
            importlib.import_module(value)
            os.remove(full_val)

        # for view in views:
        #     if view.startswith(".\\Shared") or view.startswith("./Shared"):
        #         continue
        #     path = view.split("\\")
        #     divider = "\\"
        #     if len(path) == 1:
        #         path = path[0].split("/")
        #         divider = "/"
        #     name = path[-1][0:-5]
        #     #os.chdir(cwd + "/g")
        #     importlib.import_module(name)
        #     os.remove(name + ".py")

        for controller in controllers:
            value = '.'.join(controller.split("\\")[1:])[:-3]
            importlib.import_module(value)
            
        for task in backgroundtasks.funcs:
            task.main()


        os.chdir(cwd)
        try:
            file = open("./models/EMCPG.txt", 'rb')
            AppLoc.EMCPG = pickle.loads(file.read())
            file.close()
        except:
            file = open("./models/EMCPG.txt", 'w')
            file.close()
            AppLoc.EMCPG.fill_funcs_matrix(list(app.funcs.keys()))
            #Check to extend funcs list ---------------------------------------------------------------
        print('Build successful.')

#socket.gethostbyname(socket.gethostname())
#instance = MVC(socket.gethostbyname(socket.gethostname()), 80, 50)
instance = MVC("192.168.0.24", 80, 50)
instance.Build()
#instance.Start_Server()
try:
    asyncio.run(instance.run_server())
except:
    file = open("./models/EMCPG.txt", 'wb')
    file.write(pickle.dumps(AppLoc.EMCPG))
    file.close()


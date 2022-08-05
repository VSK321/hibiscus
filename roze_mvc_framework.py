import roze_server_framework
import roze_compiler
import importlib
import httpheaders
import mimetypes
import os
import glob
from AppLoc import *

class MVC(roze_server_framework.HTTP_Server):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Critical_View = {}

    def HTML_Manager(self, page_view, softpath):
        page_model = self.Critical_View['MainLayout'].Page().main()
        return page_model

    def ViewHandler(self, softpath):
        sentData = ""
        headers = {'Server': 'Roze', 'X-Frame-Options': 'SameOrigin', 'Cache-Control': 'no-cache', 'Content-Type': 'text/html', 'connection': 'close'}
        sentData = httpheaders.HTTP_Headers_Constructor(headers)
        sentData = sentData + self.HTML_Manager(app.funcs[softpath]['module']().main(), softpath)
        sentData = sentData.encode()
        return sentData

    def ControllerHandler(self, conn, addr, http_headers, http_data, softpath):
        app.funcs[softpath]['module'](**{'conn':conn, 'addr':addr, 'http_headers':http_headers, 'http_data':http_data, 'Critical_View':self.Critical_View}).main()

    def PublicHandler(self, softpath):
        headers = {'Server': 'Roze', 'X-Frame-Options': 'SameOrigin', 'Cache-Control': 'no-cache', 'Content-Type': mimetypes.guess_type(softpath)[0], 'connection': 'close'}
        cwd = os.getcwd()
        sentData = httpheaders.HTTP_Headers_Constructor(headers)
        os.chdir(app.funcs[softpath]['hardpath'])
        file = open(app.funcs[softpath]['file'], 'rb')
        sentData = sentData.encode() + file.read()
        file.close()
        os.chdir(cwd)
        return sentData

    def HTTP_Request_Manager(self, conn, addr, http_headers, http_data):
        softpath = http_headers.Url###Check if softpath exists
        try:
            softpath_Type = app.funcs[softpath]['type']
            if softpath_Type == 'view':
                sentData = "HTTP/1.1 200 OK\r\n"
                sentData = sentData.encode() + self.ViewHandler(softpath)
                conn.send(sentData)
                conn.close()
            elif softpath_Type == 'controller':
                self.ControllerHandler(conn, addr, http_headers, http_data, softpath)
            elif softpath_Type == 'public':
                sentData = "HTTP/1.1 200 OK\r\n"
                sentData = sentData.encode() + self.PublicHandler(softpath)
                conn.send(sentData)
                conn.close()
        except KeyError:
            sentData = "HTTP/1.1 404 Not Found\r\n"
            sentData = sentData.encode() + self.ViewHandler('/_error')
            conn.send(sentData)
            conn.close()

    def inheritors(klass):
        subclasses = set()
        work = [klass]
        while work:
            parent = work.pop()
            for child in parent.__subclasses__():
                if child not in subclasses:
                    subclasses.add(child)
                    work.append(child)
        return subclasses

    def Build(self):
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

        os.chdir(cwd)
        print('Build successful.')

instance = MVC('192.168.0.135', 80, 50, 50)
instance.Build()
instance.Start_Server()
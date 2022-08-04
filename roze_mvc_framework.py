import roze_server_framework
import roze_compiler
import importlib
import httpheaders
import mimetypes
from lxml import etree
import os
import json
import glob
import functools
from AppLoc import *

class MVC(roze_server_framework.HTTP_Server):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Critical_View = {}
        self.Module_Discovery = {}

    def HTML_Manager(self, page_view, softpath):
        page_model = self.Critical_View['MainLayout'].Page().main()
        return page_model

    def ViewHandler(self, softpath):
        sentData = ""
        headers = {'Server': 'Roze', 'X-Frame-Options': 'SameOrigin', 'Cache-Control': 'no-cache', 'Content-Type': 'text/html', 'connection': 'close'}
        sentData = httpheaders.HTTP_Headers_Constructor(headers)
        sentData = sentData + self.HTML_Manager(self.Module_Discovery[softpath]['module'].Page().main(), softpath)
        sentData = sentData.encode()
        return sentData

    def ControllerHandler(self, conn, addr, http_headers, http_data, softpath):
        self.Module_Discovery[softpath]['module'].Controller(**{'conn':conn, 'addr':addr, 'http_headers':http_headers, 'http_data':http_data, 'Critical_View':self.Critical_View, 'Module_Discovery':self.Module_Discovery}).main()

    def PublicHandler(self, softpath):
        headers = {'Server': 'Roze', 'X-Frame-Options': 'SameOrigin', 'Cache-Control': 'no-cache', 'Content-Type': mimetypes.guess_type(softpath)[0], 'connection': 'close'}
        cwd = os.getcwd()
        sentData = httpheaders.HTTP_Headers_Constructor(headers)
        os.chdir(self.Module_Discovery[softpath]['hardpath'])
        file = open(self.Module_Discovery[softpath]['file'], 'rb')
        sentData = sentData.encode() + file.read()
        file.close()
        os.chdir(cwd)
        return sentData

    def HTTP_Request_Manager(self, conn, addr, http_headers, http_data):
        softpath = http_headers.Url###Check if softpath exists
        try:
            softpath_Type = self.Module_Discovery[softpath]['type']
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
                os.chdir(cwd + "/g")
                importlib.__path__.append(cwd + "/g")
                self.Critical_View[f[0:-5]] = importlib.import_module(f[0:-5])
                os.chdir(cwd)
        #Discover all files within cwd and check for .roze and .py
        views = glob.glob('./**/*.roze', recursive=True)
        controllers = glob.glob('./**/*.py', recursive=True)
        controllers = [controller for controller in controllers if not controller.endswith("_g.py") and not controller.endswith(".roze.py")]
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
            self.Module_Discovery["/" + "/".join(path[1:])] = {'type': 'public', 'file': (name), 'hardpath': (cwd + "/root" + "/".join(path[1:-1]))}

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
            name = path[-1][0:-5]
            os.chdir(cwd + "/g")
            module = importlib.import_module(name)
            os.chdir(cwd)
            try:
                softPath = module.Page().path;
            except:
                softPath = "/" + name
            self.Module_Discovery[softPath] = {'type': 'view', 'module': module}

        for controller in controllers:
            path = controller.split("\\")
            divider = "\\"
            if len(path) == 1:
                path = path[0].split("/")
                divider = "/"
            name = path[-1][0:-5]
            os.chdir(cwd + divider.join(path[0:-1]))
            module = importlib.import_module(name)
            os.chdir(cwd)
            softPath = module.Controller().path;
            self.Module_Discovery["/" + "/".join(path[1:])] = {'type': 'controller', 'module': module}

        #file = open('urls.json', 'r')
        #data = file.read()
        #file.close()
        #urls = json.loads(data)
        #for url in urls:
        #    if urls[url]['type'] == 'view':
        #        roze_compiler.Convert(urls[url]['hardpath'], urls[url]['name'])
        #        #os.chdir(urls[url]['hardpath'])
        #        #os.remove(os.getcwd() + '/' + urls[url]['name'][0:-5] + '.py')
        #    elif urls[url]['type'] == 'controller':
        #        os.chdir(urls[url]['hardpath'])
        #        file = open(urls[url]['name'], 'r')
        #        data = file.read()
        #        file.close()
        #        os.chdir(cwd)
        #        file = open(urls[url]['name'], 'w')
        #        file.write(data)
        #        file.close()
        #        #os.remove(os.getcwd() + '/' + urls[url]['name'])
        #    elif urls[url]['type'] == 'public':
        #        self.Module_Discovery[urls[url]['softpath']] = {'type': 'public', 'file': (urls[url]['name']), 'hardpath': (urls[url]['hardpath'])}

        #for url in urls:
        #    if urls[url]['type'] == 'view':
        #        temp = urls[url]['name'][0:-5]
        #        self.Module_Discovery[urls[url]['softpath']] = {'type': 'view', 'module': importlib.import_module(temp)}
        #    elif urls[url]['type'] == 'controller':
        #        self.Module_Discovery[urls[url]['softpath']] = {'type': 'controller', 'module': importlib.import_module(urls[url]['name'][0:-3])}
        print(app.funcs)
        os.chdir(cwd)
        print('Build successful.')

instance = MVC('192.168.0.135', 80, 50, 50)
instance.Build()
instance.Start_Server()
import roze_server_framework
import roze_compiler
import importlib
import httpheaders
import mimetypes
from lxml import etree
import os
import json

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

    def Build(self):
        print('Building...')
        cwd = os.getcwd()
        for file in os.listdir(os.getcwd()+'/Shared'):
            if file.endswith('.roze'):
                roze_compiler.Convert(os.getcwd()+'/Shared', file)
        for file in os.listdir(os.getcwd()+'/Shared'):
            if file.endswith('.roze'):
                self.Critical_View[file[0:-5]] = importlib.import_module(file[0:-5])
        file = open('urls.json', 'r')
        data = file.read()
        file.close()
        urls = json.loads(data)
        for url in urls:
            if urls[url]['type'] == 'view':
                roze_compiler.Convert(urls[url]['hardpath'], urls[url]['name'])
                #os.chdir(urls[url]['hardpath'])
                #os.remove(os.getcwd() + '/' + urls[url]['name'][0:-5] + '.py')
            elif urls[url]['type'] == 'controller':
                os.chdir(urls[url]['hardpath'])
                file = open(urls[url]['name'], 'r')
                data = file.read()
                file.close()
                os.chdir(cwd)
                file = open(urls[url]['name'], 'w')
                file.write(data)
                file.close()
                #os.remove(os.getcwd() + '/' + urls[url]['name'])
            elif urls[url]['type'] == 'public':
                self.Module_Discovery[urls[url]['softpath']] = {'type': 'public', 'file': (urls[url]['name']), 'hardpath': (urls[url]['hardpath'])}

        for url in urls:
            if urls[url]['type'] == 'view':
                temp = urls[url]['name'][0:-5]
                self.Module_Discovery[urls[url]['softpath']] = {'type': 'view', 'module': importlib.import_module(temp)}
            elif urls[url]['type'] == 'controller':
                self.Module_Discovery[urls[url]['softpath']] = {'type': 'controller', 'module': importlib.import_module(urls[url]['name'][0:-3])}
        os.chdir(cwd)
        print('Build successful.')

instance = MVC('192.168.0.135', 80, 50, 50)
instance.Build()
instance.Start_Server()
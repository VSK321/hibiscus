import websocket
import json
import threading
from lxml import etree
from lxml.html import fromstring, tostring
from lxml.html.diff import htmldiff, html_annotate
import difflib
import controller
from AppLoc import *
import asyncio
import sys

@app.set_route("/_rose", True)
class Controller(controller.Controller):

    def __init__(self, conn, addr, http_headers, http_data, Critical_View):
        self.conn = conn
        self.addr = addr
        self.http_headers = http_headers
        self.http_data = http_data
        self.Critical_View = Critical_View
        self.Lock = threading.Lock()
        self.SoftPath = http_headers.Url
        self.paths = {}
        self.page_view = ""
        self.app_view = ""
        self.original_doc = ""

    def HTML_Manager(self, page_view, app_view):
        paths = {}
        self.paths = {}
        #print(page_view)
        page_view = app_view.replace("~appView~", page_view)
        page_view = fromstring(page_view)
        tree = etree.ElementTree(page_view)
        for el in page_view.xpath("//*"):
            for attr in el.attrib:
                if attr.startswith("rose"):# and not attr.startswith("roseid"):
                    #print(attr)
                    
                    self.paths['/HTML/BODY/APP' + tree.getpath(el).upper().replace("[1]", "") + '/' + attr[4:]] = el.get(attr)
                    el.attrib.pop(attr)
                    try:
                        paths['/HTML/BODY/APP' + tree.getpath(el).upper().replace("[1]", "")]
                        paths['/HTML/BODY/APP' + tree.getpath(el).upper().replace("[1]", "")].append(attr[4:])
                    except:
                        paths['/HTML/BODY/APP' + tree.getpath(el).upper().replace("[1]", "")] = [attr[4:]]
                    #paths['/HTML/BODY/APP' + tree.getpath(el).upper()] = attr[4:]
                #elif attr.startswith("roseid"):
                #    pass
        page_view = (tostring(page_view)).decode()
        #print(self.paths)
        return page_view, paths

    async def WebSocketRequestHandlerAsync(self, data):
        if data['type'] == 'info':
            sentData = await self.InfoWebSocketAsync(data)
        elif data['type'] == 'update':
            sentData = await self.UpdateWebSocketAsync(data)
        return sentData

    async def InfoWebSocketAsync(self, data):
        try:
            found_pattern = None
            subs = {}
            for path_to_re in app.paths_to_re:
                if bool(path_to_re[0].fullmatch(data['softpath'])):
                    found_pattern = path_to_re[1]
                    subs = {tup[0][0]: getattr(sys.modules['builtins'], tup[0][1])(tup[1]) for tup in zip(path_to_re[2], data['softpath'].split("/")[1:]) if tup[0] != None}
                    break
            self.page_view = app.funcs[found_pattern]['module'](**subs)
            #self.page_view = app.funcs[data['softpath'].lower()]['module']()
        except:
            self.page_view = app.funcs['/_error']['module']()
        temp, data['paths'] = self.HTML_Manager(await self.page_view.main(), await self.app_view.main())
        self.original_doc = temp
        data['insert'] = {"/HTML/BODY/APP": temp}
        return data

    async def UpdateWebSocketAsync(self, data):
        method = self.paths[data['path'] + '/' + data['event']]
        if data['path'].find('/MAIN') != -1:
            if data['event'] == "input":
                #print(data['vars'][data['path']])
                methods = method.split(".")
                update = self.page_view
                for method in range(len(methods)):
                    if method == len(methods) - 1:
                        update = getattr(update, methods[method])(data['vars'][data['path']])
                        continue
                    if methods[method].endswith("()"):
                        update = getattr(update, methods[method][:-2])()
                        continue
                    update = getattr(update, methods[method])
            else:
                methods = method.split(".")
                update = self.page_view
                for method in range(len(methods)):
                    if method == len(methods) - 1:
                        update = getattr(update, methods[method])()
                        continue
                    if methods[method].endswith("()"):
                        update = getattr(update, methods[method][:-2])()
                        continue
                    update = getattr(update, methods[method])
        else:
            if data['event'] == "input":
                methods = method.split(".")
                update = self.app_view
                for method in range(len(methods)):
                    if method == len(methods) - 1:
                        update = getattr(update, methods[method])(data['vars'][data['path']])
                        continue
                    if methods[method].endswith("()"):
                        update = getattr(update, methods[method][:-2])()
                        continue
                    update = getattr(update, methods[method])
            else:
                methods = method.split(".")
                update = self.app_view
                for method in range(len(methods)):
                    if method == len(methods) - 1:
                        update = getattr(update, methods[method])()
                        continue
                    if methods[method].endswith("()"):
                        update = getattr(update, methods[method][:-2])()
                        continue
                    update = getattr(update, methods[method])
        if update:
            temp, data['paths'] = self.HTML_Manager(await self.page_view.main(), await self.app_view.main())
            page_view = fromstring(temp)
            tree = etree.ElementTree(page_view)
            #for i,s in enumerate(difflib.ndiff(self.original_doc, temp)):
            #    if s[0] == " ": continue
            #    elif s[0] == "-":
            #        print(u'Delete "{}" from position {}'.format(s[-1], i))
            #    elif s[0] == "+":
            #        print(u'Add "{}" from position {}'.format(s[-1], i))
            diff = htmldiff(self.original_doc, temp)
            #print(diff)
            diff_view = fromstring(diff)
            self.original_doc = temp
            data['insert'] = {"/HTML/BODY/APP": temp}
        data['vars'] = {}
        return data

    async def WebSocketPing(self):
        loop = asyncio.get_event_loop()
        data = "Current"
        data = websocket.WebSocketDataEncoder(data, 1, 9)
        await loop.sock_sendall(self.conn, data.encode('utf8'))

    async def WebSocketHandlerAsync(self):
        loop = asyncio.get_event_loop()
        try:
            data = (await loop.sock_recv(self.conn, 4096))
            data, fin, opcode = websocket.WebSocketDataDecoder(data)
            while opcode != "1000":
                temp = data
                while fin != "1":
                    data = (await loop.sock_recv(self.conn, 4096))
                    data, fin, opcode = websocket.WebSocketDataDecoder(data)
                    temp = temp + data
                data = temp
                if opcode == "1001":
                    data = websocket.WebSocketDataEncoder(data, 1, 10)
                    await loop.sock_sendall(self.conn, data)
                else:
                    data = json.loads(data)
                    #print(data)
                    sendData = await self.WebSocketRequestHandlerAsync(data)
                    #print(sendData)
                    if sendData['insert'] == {}:
                        pass
                    else:
                        sendData = json.dumps(sendData).encode()
                        sendData = websocket.WebSocketDataEncoder(sendData, 1, 1)
                        await loop.sock_sendall(self.conn, sendData)
                data = (await loop.sock_recv(self.conn, 4096))
                data, fin, opcode = websocket.WebSocketDataDecoder(data)
            self.conn.close()
        except Exception as e:
            print(e)


    async def main(self):
        connectiontype, seckey = websocket.VerifyWebSocketRequest(self.http_headers)
        if connectiontype:
            self.app_view = self.Critical_View['App'].Page()
            websocket.AcceptWebSocketRequest(self.conn, seckey)
            #self.t = threading.Thread(target = self.WebSocketHandler, daemon = True)
            #self.t.start()
            #self.t.join()
            await self.WebSocketHandlerAsync()
        else:
            self.conn.close()

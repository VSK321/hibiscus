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
import traceback

from starlette.websockets import WebSocket
from starlette.websockets import WebSocketDisconnect
from starlette.websockets import WebSocketState

@app.set_route("/_rose", True)
class Controller(controller.Controller):

    def __init__(self, send, receive, scope, Critical_View):
        self.send = send
        self.receive = receive
        self.scope = scope
        self.Critical_View = Critical_View
        self.Lock = threading.Lock()
        self.SoftPath = scope['raw_path'].decode()
        self.paths = {}
        self.path_values: dict = {}
        self.page_view = ""
        self.app_view = ""
        self.original_doc = ""
        self.access_paths: list[tuple[str, str]] = []
        self.websocket = None

    def HTML_Manager(self, page_view, app_view):
        paths = {}
        self.paths = {}
        self.path_values = {}
        #print(page_view)
        page_view = app_view.replace("~appView~", page_view)
        page_view = fromstring(page_view)
        tree = etree.ElementTree(page_view)
        for el in page_view.xpath("//*"):
            for attr in el.attrib:
                if attr.startswith("rose") and not attr.startswith("roseid"):
                    #print(attr)
                    
                    self.paths['/HTML/BODY/APP' + tree.getpath(el).upper().replace("[1]", "") + '/' + attr[4:]] = el.get(attr)
                    el.attrib.pop(attr)
                    try:
                        paths['/HTML/BODY/APP' + tree.getpath(el).upper().replace("[1]", "")]
                        paths['/HTML/BODY/APP' + tree.getpath(el).upper().replace("[1]", "")].append(attr[4:])
                    except:
                        paths['/HTML/BODY/APP' + tree.getpath(el).upper().replace("[1]", "")] = [attr[4:]]
                    #paths['/HTML/BODY/APP' + tree.getpath(el).upper()] = attr[4:]
                elif attr.startswith("roseid"):
                    self.path_values['/HTML/BODY/APP' + tree.getpath(el).upper().replace("[1]", "")] = [el.get(attr)]
                    el.attrib.pop(attr)
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
            data['softpath'] = data['softpath'].lower()
            self.access_paths.append((self.SoftPath, data['softpath']))
            self.SoftPath = data['softpath']
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
            update = self.page_view
        else:
            update = self.app_view
        if data['event'] == "input":
            #print(data['vars'][data['path']])
            methods = method.split(".")
            for method in range(len(methods)):
                if method == len(methods) - 1:
                    update = await getattr(update, methods[method])(data['vars'][data['path']])
                    continue
                if methods[method].endswith("()"):
                    if self.path_values.get(data['path']) != None:
                        update = await getattr(update, methods[method][:-2])(self.path_values[data['path']])
                    else:
                        update = await getattr(update, methods[method][:-2])()
                    continue
                update = getattr(update, methods[method])
        else:
            methods = method.split(".")
            for method in range(len(methods)):
                if method == len(methods) - 1:
                    if self.path_values.get(data['path']) != None:
                        update = await getattr(update, methods[method])(*self.path_values[data['path']])
                    else:
                        update = await getattr(update, methods[method])()
                    continue
                if methods[method].endswith("()"):
                    if self.path_values.get(data['path']) != None:
                        update = await getattr(update, methods[method][:-2])(*self.path_values[data['path']])
                    else:
                        update = await getattr(update, methods[method][:-2])()
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

    async def WebSocketHandlerAsync(self):
        try:
            while self.websocket.client_state == WebSocketState.CONNECTED:
                request = await self.websocket.receive_text()
                request = json.loads(request)
                sendData = await self.WebSocketRequestHandlerAsync(request)
                if sendData['insert'] == {}:
                    pass
                else:
                    #sendData = json.dumps(sendData).encode()
                    await self.websocket.send_json(sendData)
        except WebSocketDisconnect:
            pass
        self.websocket.close()
        EMCPG.update_probabilities(self.access_paths)


    async def main(self):
        self.websocket = WebSocket(scope=self.scope, receive=self.receive, send=self.send)
        self.app_view = self.Critical_View['App'].Page()
        await self.websocket.accept()
        await self.WebSocketHandlerAsync()
        

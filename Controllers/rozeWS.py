import websocket
import json
import threading
from lxml import etree
from lxml.html import fromstring, tostring
import difflib
import controller
from AppLoc import *

@app.set_route("/_roze", True)
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
                if attr.startswith("roze"):
                    #print(attr)
                    self.paths['/HTML/BODY/APP' + tree.getpath(el).upper() + '/' + attr[4:]] = el.get(attr)
                    el.attrib.pop(attr)
                    try:
                        paths['/HTML/BODY/APP' + tree.getpath(el).upper()]
                        paths['/HTML/BODY/APP' + tree.getpath(el).upper()].append(attr[4:])
                    except:
                        paths['/HTML/BODY/APP' + tree.getpath(el).upper()] = [attr[4:]]
                    #paths['/HTML/BODY/APP' + tree.getpath(el).upper()] = attr[4:]
        page_view = (tostring(page_view)).decode()
        #print(self.paths)
        return page_view, paths

    def WebSocketRequestHandler(self, data):
        if data['type'] == 'info':
            sentData = self.InfoWebSocket(data)
        elif data['type'] == 'update':
            sentData = self.UpdateWebSocket(data)
        return sentData

    def InfoWebSocket(self, data):
        try:
            self.page_view = app.funcs[data['softpath']]['module']()
        except:
            self.page_view = app.funcs['/_error']['module']()
        temp, data['paths'] = self.HTML_Manager(self.page_view.main(), self.app_view.main())
        self.original_doc = temp
        data['insert'] = {"/HTML/BODY/APP": temp}
        return data

    def UpdateWebSocket(self, data):
        method = self.paths[data['path'] + '/' + data['event']]
        if data['path'].find('/MAIN') != -1:
            if data['event'] == "input":
                #print(data['vars'][data['path']])
                update = getattr(self.page_view, method)(data['vars'][data['path']])
            else:
                update = getattr(self.page_view, method)()
        else:
            if data['event'] == "input":
                update = getattr(self.app_view, method)(*data['vars'][data['path']])
            else:
                update = getattr(self.app_view, method)()
        if update == True:
            temp, data['paths'] = self.HTML_Manager(self.page_view.main(), self.app_view.main())
            page_view = fromstring(temp)
            tree = etree.ElementTree(page_view)
            for i,s in enumerate(difflib.ndiff(self.original_doc, temp)):
                pass
                #if s[0] == " ": continue
                #elif s[0] == "-":
                #    print(u'Delete "{}" from position {}'.format(s[-1], i))
                #elif s[0] == "+":
                #    print(u'Add "{}" from position {}'.format(s[-1], i))
            data['insert'] = {"/HTML/BODY/APP": temp}
        data['vars'] = {}
        return data

    def WebSocketPing(self):
        data = "Current"
        data = websocket.WebSocketDataEncoder(data, 1, 9)
        self.conn.send(data)

    def WebSocketHandler(self):
        try:
            data = self.conn.recv(4096)
            data, fin, opcode = websocket.WebSocketDataDecoder(data)
            while opcode != "1000":
                temp = data
                while fin != "1":
                    data = self.conn.recv(4096)
                    data, fin, opcode = websocket.WebSocketDataDecoder(data)
                    temp = temp + data
                data = temp
                if opcode == "1001":
                    data = websocket.WebSocketDataEncoder(data, 1, 10)
                    self.conn.send(data)
                else:
                    data = json.loads(data)
                    #print(data)
                    sendData = self.WebSocketRequestHandler(data)
                    #print(sendData)
                    if sendData['insert'] == {}:
                        pass
                    else:
                        sendData = json.dumps(sendData).encode()
                        sendData = websocket.WebSocketDataEncoder(sendData, 1, 1)
                        self.conn.send(sendData)
                data = self.conn.recv(4096)
                data, fin, opcode = websocket.WebSocketDataDecoder(data)
            self.conn.close()
        except Exception as e:
            print(e)


    def main(self):
        connectiontype, seckey = websocket.VerifyWebSocketRequest(self.http_headers)
        if connectiontype:
            self.app_view = self.Critical_View['App'].Page()
            websocket.AcceptWebSocketRequest(self.conn, seckey, self.http_headers)
            #self.t = threading.Thread(target = self.WebSocketHandler, daemon = True)
            #self.t.start()
            #self.t.join()
            self.WebSocketHandler()
        else:
            self.conn.close()

from collections import deque
from enum import Enum
import json
import threading
from lxml import etree
from lxml.html import HtmlElement, fromstring, tostring
from lxml.html.diff import htmldiff, html_annotate
import difflib
import controller
from AppLoc import *
import sys
import traceback

from starlette.websockets import WebSocket
from starlette.websockets import WebSocketDisconnect
from starlette.websockets import WebSocketState

class Change_Status(Enum):
    Removed = 0
    Added = 1
    Updated = 2

@app.set_route("/_rose")
class Controller:

    def __init__(self, send, receive, scope, Critical_View):
        self.send = send
        self.receive = receive
        self.scope = scope
        self.Critical_View = Critical_View
        self.Lock = threading.Lock()
        self.SoftPath = scope['path']
        self.paths = {}
        self.path_values: dict = {}
        self.page_view = ""
        self.app_view = ""
        self.original_doc = ""
        self.access_paths: list[tuple[str, str]] = []
        self.websocket = None
        
    def remove_optional_end(self, value: str):
        value = value.split('/')
        for v in range(len(value)):
            if value[v].endswith('[1]'):
                value[v] = value[v][:-3]
        return '/'.join(value)
        
    def find_changes(self, old_page: str, new_page: str) -> list[tuple[str, Change_Status]]:
        old_tree = fromstring(old_page)
        new_tree = fromstring(new_page)

        def compare_elements(old_element: HtmlElement, new_element: HtmlElement, root: etree.ElementTree, old_root: etree.ElementTree) -> list[tuple[str, Change_Status]]:

            changed_elements = []
            
            if tostring(old_element) == tostring(new_element):
                return changed_elements

            if old_element.tag != new_element.tag:
                changed_elements.append((root.getpath(new_element), Change_Status.Updated))
                
            elif len(old_element.getchildren()) == 0 and len(new_element.getchildren()) == 0:
                            old_text = old_element.text_content().strip()
                            new_text = new_element.text_content().strip()
                            if old_text != new_text:
                                changed_elements.append((root.getpath(new_element), Change_Status.Updated))

            else:
                old_attrs = dict(old_element.attrib)
                new_attrs = dict(new_element.attrib)
                added_attrs = set(new_attrs) - set(old_attrs)
                removed_attrs = set(old_attrs) - set(new_attrs)
                changed_attrs = {(attr, old_attrs[attr], new_attrs[attr]) for attr in set(old_attrs) & set(new_attrs) if old_attrs[attr] != new_attrs[attr]}

                if added_attrs or removed_attrs or changed_attrs:
                    changed_elements.append((root.getpath(new_element), Change_Status.Updated))
                else:
                    ordered_old_element_xpaths = [self.remove_optional_end(old_root.getpath(x)) for x in old_element.getchildren()]
                    old_element_xpaths = set(ordered_old_element_xpaths)
                    ordered_new_element_xpaths = [self.remove_optional_end(root.getpath(x)) for x in new_element.getchildren()]
                    new_element_xpaths = set(ordered_new_element_xpaths)
                    added_elements = new_element_xpaths - old_element_xpaths
                    deleted_elements = old_element_xpaths - new_element_xpaths
                    
                    all_xpaths = old_element_xpaths.union(new_element_xpaths)
                    
                    possible_updated_elements = all_xpaths - added_elements - deleted_elements
                    
                    changed_elements += [(x, Change_Status.Removed) for x in deleted_elements]
                    
                    added_dict = dict.fromkeys(ordered_new_element_xpaths)
                    for value in added_elements:
                        added_dict[value] = 1
                        
                    for key in added_dict:
                        if added_dict[key] == 1:
                            changed_elements.append((key, Change_Status.Added))

                    for xpath in possible_updated_elements:
                        old_elem = old_root.xpath(xpath)[0]
                        new_elem = root.xpath(xpath)[0]
                        sub_changes = compare_elements(old_elem, new_elem, root, old_root)
                        changed_elements += sub_changes

            return changed_elements

        return compare_elements(old_tree, new_tree, etree.ElementTree(new_tree), etree.ElementTree(old_tree))

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
        data = json.loads(data)
        if data['type'] == 'info':
            sentData = await self.InfoWebSocketAsync(data)
        elif data['type'] == 'update':
            sentData = await self.UpdateWebSocketAsync(data)
        await self.websocket.send_json(sentData)

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
        page, data['paths'] = self.HTML_Manager(await self.page_view.main(), await self.app_view.main())
        self.original_doc = page
        data['insert'] = {"/HTML/BODY/APP": [page, Change_Status.Updated.value]}
        return data

    async def UpdateWebSocketAsync(self, data):
        data['insert'] = {}
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
            page, data['paths'] = self.HTML_Manager(await self.page_view.main(), await self.app_view.main())
            curr_page = fromstring(page)
            curr_tree = etree.ElementTree(curr_page)
            changes = self.find_changes(self.original_doc, page)
            changes = sorted(changes, key=lambda x: x[1].value)
            for change, change_type in changes:
                root_removed = '/'.join(change.split('/')[2:])
                if change_type == Change_Status.Removed:
                    data['insert']["/HTML/BODY/APP"+change] = ['', Change_Status.Removed.value]
                elif change_type == Change_Status.Added:
                    p: HtmlElement = curr_page.xpath(root_removed)[0]
                    next_elem = p.getnext()
                    if next_elem != None:
                        next_elem = "/HTML/BODY/APP" + curr_tree.getpath(next_elem)
                    if '/HTML/BODY/APP'+'/'.join(change.split('/')[:-1]) in data['insert']:
                        data['insert']['/HTML/BODY/APP'+'/'.join(change.split('/')[:-1])][0].append((tostring(p).decode(), next_elem))
                    else:
                        data['insert']['/HTML/BODY/APP'+'/'.join(change.split('/')[:-1])] = [[(tostring(p).decode(), next_elem)], change_type.value]
                else:
                    data['insert']["/HTML/BODY/APP"+change] = [tostring(curr_page.xpath(root_removed)[0]).decode(), change_type.value]
            self.original_doc = page
        #data['insert'] = {"/HTML/BODY/APP": page}
        data['vars'] = {}
        return data

    async def WebSocketHandlerAsync(self):
        try:
            while self.websocket.client_state == WebSocketState.CONNECTED:
                request = await self.websocket.receive_text()
                await self.WebSocketRequestHandlerAsync(request)
        except WebSocketDisconnect:
            pass
        #await self.websocket.close()
        EMCPG.update_probabilities(self.access_paths)


    async def main(self):
        self.websocket = WebSocket(scope=self.scope, receive=self.receive, send=self.send)
        self.app_view = self.Critical_View['App'].Page()
        await self.websocket.accept()
        await self.WebSocketHandlerAsync()
        

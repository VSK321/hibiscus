import functools
from ctypes import Union
import re
import uuid
from threading import Lock

class Logger:
    def __init__(self, logFunc) -> None:
        self.log = logFunc

    def log(self, funcParam):
        def wrapper(func):
            self.log(func)


            @functools.wraps(func)
            def inner_wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return inner_wrapper
        return wrapper


def partial_implementation(klass):
    def wrapper(func):
        setattr(klass, func.__name__, func)
        return func
    return wrapper

class Singletons:
    def __init__(self):
        self.singletons: list = []
        self.access_lock: Lock = Lock()

    def register_singleton(self):
        def wrapper(klass):
            self.singletons.append(klass())
            
            @functools.wraps(klass)
            def inner_wrapper(*args, **kwargs):
                return klass(*args, **kwargs)
            return inner_wrapper
        return wrapper

    def get_singleton(self, obj_type):
        for singleton in self.singletons:
            if type(singleton) == obj_type:
                return singleton
        raise KeyError


class BackgroundTasks:
    def __init__(self):
        self.funcs: list[function] = []

    def register_task(self):
        def wrapper(func):
            self.funcs.append(func())
            
            @functools.wraps(func)
            def inner_wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return inner_wrapper
        return wrapper

def convert_path(path: str):
    #Convention shall be /value/{x:str}/{y:int,3}/{z:str,} and should be converted to /value/[a-z]+/[0-9]{3}[/]?[a-z]*
    converted_path = ""
    substitions = []
    path = path.split("/")[1:]
    for p in path:
        if len(p) > 2 and p[0] == "{" and p[-1] == "}":
            split_val = (p[1:-1]).split(":")
            if split_val[1].find(",") != -1:
                split_val[1] = split_val[1].split(",")[0]
            substitions.append(tuple(split_val))
            p = (p[1:-1]).split(":")[1]
            length = "-1"
            if p.find(",") != -1:
                split_str = p.split(",")
                length = split_str[1]
                p = split_str[0]
            if p == "str":
                converted_path += "/[a-z]"
            elif p == "int":
                converted_path += "/[0-9]"


            if length == "":
                converted_path += "*"
                converted_path = converted_path[0:-7] + "[/]?" + converted_path[-6:]
            elif length != "-1":
                converted_path += "{" + length + "}"
            else:
                converted_path += "+"
        else:
            converted_path += "/" + p
            substitions.append(None)

    return converted_path, substitions


class App:
    def __init__(self):
        self.paths_to_re: list[tuple[function, str]] = []
        self.funcs: dict[function, dict[object]] = {}

    def set_route(self, path: str, iscontroller: bool = False, metadata = None):
        def wrapper(func):
            converted_path, subs = convert_path(path.lower())
            compiled_re = re.compile(converted_path)
            self.paths_to_re.append((compiled_re, path.lower(), subs))
            self.funcs[path.lower()] = {'type': (lambda: "controller" if iscontroller else "view")(), 'module' : func, 'metadata': metadata}            
            @functools.wraps(func)
            def inner_wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return inner_wrapper
        return wrapper


app = App()
backgroundtasks = BackgroundTasks()
singletons = Singletons()
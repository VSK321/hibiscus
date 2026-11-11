import functools
import re
from types import ModuleType
from typing import Any, Callable
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
    def wrapper(func: ModuleType):
        names = {}
        for n in app.funcs:
            if app.funcs[n]['type'] == 'view' and not hasattr(app.funcs[n]['module'], 'main'):
                names[(app.funcs[n]['module'])] = n
        if names:
            setattr(list(names.keys())[-1], func.__name__, func)
        else:
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
        self.funcs: list[object] = []

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
    split_path = path.split("/")[1:]
    for p in split_path:
        if len(p) > 2 and p.startswith("{") and p.endswith("}"):
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
                converted_path += "/[.]"
            elif p == "int":
                converted_path += "/[-]?[0-9]"
            #elif p == "float":
            #    converted_path += ""


            if length == "":
                last_split = converted_path.rfind("/")
                converted_path += "*"
                converted_path = converted_path[0:last_split] + "[/]?" + converted_path[last_split+1:]
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
        self.paths_to_re: list[tuple[re.Pattern[str], str, list]] = []
        self.funcs: dict[str, dict[str, Any]] = {}

    def set_route(self, path: str, metadata = None):
        def wrapper(func: Callable):
            converted_path, subs = convert_path(path.lower())
            compiled_re = re.compile(converted_path)
            self.paths_to_re.append((compiled_re, path.lower(), subs))
            self.funcs[path.lower()] = {'type': (lambda: "controller" if func.__name__ == "Controller" else "view")(), 'module' : func, 'metadata': metadata}            
            @functools.wraps(func)
            def inner_wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return inner_wrapper
        return wrapper

class AppModels:
    def __init__(self):
        self.registered_models: dict[str, dict[str, object]] = {}
    
    def register(self, metadata = None):
        def wrapper(func: Callable):
            self.registered_models[func.__name__] = {'metadata': metadata, 'module': func}
            @functools.wraps(func)
            def inner_wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return inner_wrapper
        return wrapper

class ProbabilityGeneralizerHelper:
    def __init__(self, length):
        self.ratios: list[int|float] = [0 for x in range(length)]
        self.curr_max = 0
        self.curr_max_position = 0
        
    def update_ratio(self, position: int):
        #self.ratios = [x * self.curr_max for x in self.ratios]
        if (self.ratios[position] * self.curr_max) + 1 > self.curr_max:
            self.curr_max_position = position
        if position == self.curr_max_position:
            self.curr_max += 1
        self.ratios[position] += 1/self.curr_max

app = App()
backgroundtasks = BackgroundTasks()
singletons = Singletons()
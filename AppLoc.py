import functools
from ctypes import Union

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


class BackgroundTasks:
    def __init__(self):
        self.funcs: list[function] = []

    def register_task(self):
        def wrapper(func):
            self.funcs.append(func)
            
            @functools.wraps(func)
            def inner_wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return inner_wrapper
        return wrapper

class App:
    def __init__(self):
        self.funcs: dict[str, dict[object]] = {}

    def set_route(self, path: str, iscontroller: bool = False, metadata = None):
        def wrapper(func):
            if iscontroller:
                self.funcs[path.lower()] = {'type': 'controller', 'module' : func, 'metadata': metadata}
            else:
                self.funcs[path.lower()] = {'type': 'view', 'module' : func, 'metadata': metadata}
            
            @functools.wraps(func)
            def inner_wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return inner_wrapper
        return wrapper

app = App()
backgroundtasks = BackgroundTasks()
import functools

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


class App:
    def __init__(self):
        self.funcs: dict[str, dict[str]] = {}

    def set_route(self, path: str, iscontroller: bool = False):
        def wrapper(func):
            if iscontroller:
                self.funcs[path.lower()] = {'type': 'controller', 'module' : func}
            else:
                self.funcs[path.lower()] = {'type': 'view', 'module' : func}
            
            @functools.wraps(func)
            def inner_wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return inner_wrapper
        return wrapper

app = App()

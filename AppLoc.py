import functools

class App:
    def __init__(self):
        self.funcs = {}

    def set_route(self, path, iscontroller = False):
        def wrapper(func):
            if iscontroller:
                self.funcs[path] = {'type': 'controller', 'module' : func}
            else:
                self.funcs[path] = {'type': 'view', 'module' : func}
            
            @functools.wraps(func)
            def inner_wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return inner_wrapper
        return wrapper

app = App()

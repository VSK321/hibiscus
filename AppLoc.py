import functools

#class Logger:
#    def __init__(self, logFunc) -> None:
#        self.log = logFunc

#    def log(self, func: function):
#        def wrapper(func):
#            self.log(func)
#            @functools.wraps(func)
#            def inner_wrapper(*args, **kwargs):
#                return func(*args, **kwargs)
#            return inner_wrapper
#        return wrapper


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

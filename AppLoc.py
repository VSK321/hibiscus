import functools

class App:
    def __init__(self):
        self.funcs = {}

    def set_route(self, path):
        #functools.update_wrapper(self, _func)
        def wrapper(func):
            self.funcs[path] = func
            
            @functools.wraps(func)
            def inner_wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return inner_wrapper
        return wrapper

app = App()

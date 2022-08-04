import controller

class Controller(controller.Controller):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path = "/r"

    def main(self):
        self.reroute("/")
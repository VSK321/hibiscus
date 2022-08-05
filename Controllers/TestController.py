import controller
from AppLoc import *

@app.set_route("/r", True)
class Controller(controller.Controller):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def main(self):
        self.reroute("/")
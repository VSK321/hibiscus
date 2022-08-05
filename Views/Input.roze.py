import view
from AppLoc import *

@app.set_route("/input")
class Page(view.View):

    def __init__(self):
        self.val = ""

    def InputVal(self, val=""):
        self.val = val

    def ReturnTrue(self):
        return True


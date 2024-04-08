import view
from AppLoc import *

@app.set_route("/input")
class Page(view.View):

    def __init__(self):
        self.val = ""

    async def InputVal(self, val=""):
        self.val = val
        return True

    async def ReturnTrue(self):
        return True


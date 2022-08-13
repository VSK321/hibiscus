import view
from AppLoc import *

@app.set_route("/counter")
class Page(view.View):

    def __init__(self):
        self.x = 0

    def AddOne(self):
        self.x += 1
        return True
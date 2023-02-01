import view
from AppLoc import *
import BedroomLight

@app.set_route("/counter")
class Page(view.View):

    def __init__(self):
        self.x = 0
        self.first = BedroomLight.Page()

    def AddOne(self):
        self.x += 1
        return True
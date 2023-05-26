import view
from AppLoc import *
import BedroomLight

@app.set_route("/counter/{x:int,}")
class Page(view.View):

    def __init__(self, x=0):
        self.x = x
        self.first = BedroomLight.Page()

    def AddOne(self):
        self.x += 1
        return True

    def SubOne(self):
        self.x -= 1
        return True

    #~(await self.first.main("first"))~
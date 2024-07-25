import view
from AppLoc import *
import Views.BedroomLight
import asyncio

@app.set_route("/counter/{x:int,}")
class Page(view.View):

    def __init__(self, x=0):
        self.x = x
        self.first = Views.BedroomLight.Page()

    async def AddOne(self):
        self.x += 1
        await asyncio.sleep(5)
        return True

    async def SubOne(self):
        self.x -= 1
        return True
    
    async def test(self, val=""):
        self.x += int(val)
        return True

    #~(await self.first.main("first"))~
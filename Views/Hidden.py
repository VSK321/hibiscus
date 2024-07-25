import random
import view
from AppLoc import *

@app.set_route("/a")
class Page(view.View):

    def __init__(self):
        pass

    async def RandomValue(self):
        x = random.randint(0, 100)
        return x

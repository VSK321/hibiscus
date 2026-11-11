from hibiscus import view, app

@app.set_route("/counter/{x:int,}")
class Page(view.View):
    def __init__(self, x=0):
        self.x = x

    async def AddOne(self):
        self.x += 1
        return True

    async def SubOne(self):
        self.x -= 1
        return True

    async def add_self(self, val=""):
        self.x += int(val)
        return True

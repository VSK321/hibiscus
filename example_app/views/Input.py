from hibiscus import view, app


@app.set_route("/input")
class Page(view.View):
    def __init__(self):
        self.val = ""

    async def InputVal(self, val=""):
        val = val.replace("<", "&lt;").replace(">", "&gt;")
        self.val = val
        return True

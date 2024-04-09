import controller
from AppLoc import *

@app.set_route("/template")
class Controller(controller.Controller):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def main(self):
        await self.return_page("templates/template.html", {})
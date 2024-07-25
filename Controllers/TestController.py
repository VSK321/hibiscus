import controller
from AppLoc import *

@app.set_route("/r")
class Controller(controller.Controller):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def main(self):
        await self.reroute("/bedroomlight")
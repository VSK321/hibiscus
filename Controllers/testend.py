import controller
from AppLoc import *
import json
import socket

@app.set_route("/test123", True)
class Controller(controller.Controller):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def main(self):
        print(self.http_data)
        self.reroute("/bedroomlight")


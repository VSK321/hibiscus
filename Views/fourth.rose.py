import view
from AppLoc import *
import random

@app.set_route("/fourth")
class Page(view.View):

    def __init__(self):
        self.val = 0

    def clicker(self):
        self.val = random.randint(0, 20)
        return True


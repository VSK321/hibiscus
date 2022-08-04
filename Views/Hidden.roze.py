import random
import view

class Page(view.View):

    def __init__(self):
        self.path = "/a"
    
    def RandomValue(self):
        x = random.randint(0, 100)
        return x

import view

class Page(view.View):

    def __init__(self):
        self.x = 0
        self.path = "/counter"

    def AddOne(self):
        self.x += 1
        return True
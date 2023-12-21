import view

class Page(view.View):

    def __init__(self, test2=0):
        self.test2 = test2

    def Add(self):
        self.test2 = self.test2 + 1
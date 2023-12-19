import view
import Views.Counter


class Page(view.View):

    def __init__(self, test2=0):
        self.test2 = test2
        self.counter = Views.Counter.Page()

    def Add(self):
        self.test2 = self.test2 + 1
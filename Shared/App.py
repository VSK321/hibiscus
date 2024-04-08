import Views.NavMenu
import view

class Page(view.View):
    def __init__(self, dis=False, int2=0):
        #import NavMenu
        self.dis = dis
        self.int2 = int2
        self.menu = Views.NavMenu.Page()

    def display(self):
        self.dis = True
    

import Shared.NavMenu

class Page(Shared.NavMenu.Page):
    def __init__(self, dis=False, int2=0):
        #import NavMenu
        self.dis = dis
        self.int2 = int2
        self.menu = Shared.NavMenu.Page()

    def display(self):
        self.dis = True
    

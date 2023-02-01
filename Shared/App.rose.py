import NavMenu

class Page(NavMenu.Page):
    def __init__(self, dis=False, int2=0):
        #import NavMenu
        self.dis = dis
        self.int2 = int2
        self.menu = NavMenu.Page()

    def display(self):
        self.dis = True
    

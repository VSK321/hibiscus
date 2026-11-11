from hibiscus import view
import views


class Page(view.View):
    def __init__(self, dis=False, int2=0):
        # import NavMenu
        self.dis = dis
        self.int2 = int2
        self.menu = views.NavMenu.Page()

    # def display(self):
    #     self.dis = True

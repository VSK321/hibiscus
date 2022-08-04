import NavMenu

class Page(NavMenu.Page):
    def __init__(self, dis=False, int2=0):
        #import NavMenu
        self.dis = dis
        self.int2 = int2
        self.menu = NavMenu.Page()

    def display(self):
        self.dis = True
    

    def main(self):
        temp = ""
        temp = temp + '<div class="page">\n' 
        temp = temp + '    <div class="sidebar">\n' 
        temp = temp + '        ' + str(self.menu.main()) + '\n' 
        temp = temp + '    </div>\n' 
        temp = temp + '\n' 
        temp = temp + '    <div class="main">\n' 
        temp = temp + '        <div class="content px-4">\n' 
        temp = temp + '            <main>\n' 
        temp = temp + '                ~appView~\n' 
        temp = temp + '            </main>\n' 
        temp = temp + '        </div>\n' 
        temp = temp + '    </div>\n' 
        temp = temp + '</div>\n' 
        return temp
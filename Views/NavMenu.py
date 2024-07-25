import view

class Page(view.View):

    def __init__(self, num=0):
        self.num = num

    async def Add(self):
        self.num = self.num + 1
        return True
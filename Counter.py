class Page:

    def __init__(self):
        self.x = 0

    def AddOne(self):
        self.x += 1
        return True
    def main(self):
        temp = ""
        temp = temp + '<p>Counter is at ' + str(self.x) + '</p>\n' 
        temp = temp + '\n' 
        temp = temp + '<div>\n' 
        temp = temp + '    <button class="btn btn-primary" rozeclick="AddOne">Add</button>\n' 
        temp = temp + '</div>\n' 
        return temp
class Page:

    def __init__(self):
        self.val = ""

    def InputVal(self, val=""):
        self.val = val

    def ReturnTrue(self):
        return True


    def main(self):
        temp = ""
        temp = temp + '<p>Length of "' + str(self.val) + '" is ' + str(len(self.val)) + '</p>\n' 
        temp = temp + '<input rozefocusout="ReturnTrue" rozeinput="InputVal" />\n' 
        return temp
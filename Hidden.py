import random

class Page:

    def __init__(self):
        pass
    
    def RandomValue(self):
        x = random.randint(0, 100)
        return x

    def main(self):
        temp = ""
        x = self.RandomValue()
        if x < 50:
            temp = temp + '<p>x is not greater than 50. x is ' + str(x) + '. x is ' + str(x) + '</p>\n' 
        
        else:
            temp = temp + '<p>x is greater than 50. x is ' + str(x) + '</p>\n' 
        
        import Home
        temp = temp + '<p>' + str(Home.Page().main()) + '</p>\n' 
        return temp
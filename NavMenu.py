class Page:

    def __init__(self, test2=0):
        self.test2 = test2

    def Add(self):
        self.test2 = self.test2 + 1
    def main(self):
        temp = ""
        temp = temp + '<nav class="navbar navbar-expand-lg navbar-light bg-light">\n' 
        temp = temp + '  <a class="navbar-brand" href="/">Example Site</a>\n' 
        temp = temp + '  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">\n' 
        temp = temp + '    <span class="navbar-toggler-icon"></span>\n' 
        temp = temp + '  </button>\n' 
        temp = temp + '\n' 
        temp = temp + '  <div class="collapse navbar-collapse" id="navbarSupportedContent">\n' 
        temp = temp + '    <ul class="navbar-nav mr-auto">\n' 
        temp = temp + '      <li class="nav-item">\n' 
        temp = temp + '        <a class="nav-link" href="/counter">Counter</a>\n' 
        temp = temp + '      </li>\n' 
        temp = temp + '      <li class="nav-item">\n' 
        temp = temp + '        <a class="nav-link" href="/input">Input Example</a>\n' 
        temp = temp + '      </li>\n' 
        temp = temp + '      <li class="nav-item">\n' 
        temp = temp + '        <a class="nav-link" href="/BedroomLight">Bedroom Light</a>\n' 
        temp = temp + '      </li>\n' 
        temp = temp + '    </ul>\n' 
        temp = temp + '  </div>\n' 
        temp = temp + '</nav>\n' 
        return temp
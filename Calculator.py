
class Page:

    def __init__(self):
        pass

    def main(self):
        temp = ""
        temp = temp + '<style>\n' 
        temp = temp + '    .btn{\n' 
        temp = temp + '    width:50px;\n' 
        temp = temp + '    min-width:50px;\n' 
        temp = temp + '}\n' 
        temp = temp + '</style>\n' 
        temp = temp + '<div class ="btn-group-vertical" role="group" aria-label="Vertical button group">\n' 
        temp = temp + '    <div class="btn-group btn-group-lg" role="group" aria-label="First Row">\n' 
        temp = temp + '        <input type="button" class="btn btn-secondary btn-outline-dark" waves-effect value="7"></input>\n' 
        temp = temp + '        <input type="button" class="btn btn-secondary btn-outline-dark" waves-effect value="8"></input>\n' 
        temp = temp + '        <input type="button" class="btn btn-secondary btn-outline-dark" waves-effect value="9"></input>\n' 
        temp = temp + '        <input type="button" class="btn btn-secondary btn-outline-dark" waves-effect value="+"></input>\n' 
        temp = temp + '    </div>\n' 
        temp = temp + '    <div class="btn-group btn-group-lg" role="group" aria-label="Second Row">\n' 
        temp = temp + '        <input type="button" class="btn btn-secondary btn-outline-dark" waves-effect value="4"></input>\n' 
        temp = temp + '        <input type="button" class="btn btn-secondary btn-outline-dark" waves-effect value="5"></input>\n' 
        temp = temp + '        <input type="button" class="btn btn-secondary btn-outline-dark" waves-effect value="6"></input>\n' 
        temp = temp + '        <input type="button" class="btn btn-secondary btn-outline-dark" waves-effect value="-"></input>\n' 
        temp = temp + '    </div>\n' 
        temp = temp + '    <div class="btn-group btn-group-lg" role="group" aria-label="Third Row">\n' 
        temp = temp + '\n' 
        temp = temp + '        <input type="button" class="btn btn-secondary btn-outline-dark" waves-effect value="1"></input>\n' 
        temp = temp + '        <input type="button" class="btn btn-secondary btn-outline-dark" waves-effect value="2"></input>\n' 
        temp = temp + '        <input type="button" class="btn btn-secondary btn-outline-dark" waves-effect value="3"></input>\n' 
        temp = temp + '        <input type="button" class="btn btn-secondary btn-outline-dark" waves-effect value="*"></input>\n' 
        temp = temp + '    </div>\n' 
        temp = temp + '    <div class="btn-group btn-group-lg" role="group" aria-label="Fourth Row">\n' 
        temp = temp + '        <input type="button" class="btn btn-secondary btn-outline-dark" waves-effect value="0"></input>\n' 
        temp = temp + '        <input type="button" class="btn btn-secondary btn-outline-dark" waves-effect value="."></input>\n' 
        temp = temp + '        <input type="button" class="btn btn-secondary btn-outline-dark" waves-effect value="+/-"></input>\n' 
        temp = temp + '        <input type="button" class="btn btn-secondary btn-outline-dark" waves-effect value="/"></input>\n' 
        temp = temp + '    </div>\n' 
        temp = temp + '    <div class="btn-group btn-group-lg" role="group" aria-label="Basic example">\n' 
        temp = temp + '        <input type="button" class="btn btn-secondary btn-outline-dark" waves-effect value="="></input>\n' 
        temp = temp + '    </div>\n' 
        temp = temp + '</div>\n' 
        return temp
class Page:
    def __init__(self):
        pass

    def main(self):
        temp = ""
        temp = temp + '<html>\n' 
        temp = temp + '    <head>\n' 
        temp = temp + '        <meta charset="utf-8">\n' 
        temp = temp + '        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">\n' 
        temp = temp + '        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">\n' 
        temp = temp + '        <title>Hello World</title>\n' 
        temp = temp + '    </head>\n' 
        temp = temp + '    <body>\n' 
        temp = temp + '        <app>\n' 
        temp = temp + '            Loading...\n' 
        temp = temp + '        </app>\n' 
        temp = temp + '        <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>\n' 
        temp = temp + '        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>\n' 
        temp = temp + '        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>\n' 
        temp = temp + '        <script src="/scripts/roze.server.js"></script>\n' 
        temp = temp + '    </body>\n' 
        temp = temp + '</html>\n' 
        return temp
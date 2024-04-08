import uuid
import re

class View(object):
    
    def __init__(self, inner_pages: list):
        self.path = "/" + str(uuid.uuid4())
        self.inner_pages = inner_pages

    def _pageChange(self, main:str, change:str):
        main = main.splitlines()
        new_main = ""
        for line in main:
            l = re.findall("\srose[a-z]+=\"[a-zA-Z0-9]+\"", line)
            for v in l:
                if v.startswith("roseid"):
                    continue
                code = v.split("\"")[-2]
                line = line.replace(code, change+"."+code, 1)
            new_main += line + "\n"
        return new_main

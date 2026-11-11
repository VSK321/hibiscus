import uuid
import re


class View(object):
    def __init__(self, inner_pages: list):
        self.path = "/" + str(uuid.uuid4())
        self.inner_pages = inner_pages

    def _pageChange(self, main: str, change: str):
        split_main = main.splitlines()
        new_main = ""
        for line in split_main:
            l = re.findall('hbs[a-z]+="[a-zA-Z0-9]+"', line)
            for v in l:
                if v.startswith("hbsid"):
                    continue
                code = v.split('"')[-2]
                line = line.replace(code, change + "." + code, 1)
            new_main += line + "\n"
        return new_main

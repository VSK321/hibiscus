import os

from lxml.html import fromstring, tostring


def convert_single_line(line: str) -> str:
    if line.replace("\t", "").replace(" ", "").startswith("~exe~"):
        line = line[(line.find("~exe~") + 5) : len(line)]
    else:
        line = line.replace("~(", "' + str(")
        line = line.replace(")~", ") + '")
        line = "hbs_line += '" + line + "\\n' "
    return line


def convert_file(temp: str) -> str:
    splitTemp = temp.splitlines()
    num = 1
    for lineNum in range(len(splitTemp)):
        if splitTemp[lineNum].replace("\t", "").replace(" ", "").startswith(
            "~"
        ) and splitTemp[lineNum].endswith("{"):
            tempTwo = ""
            for x in range(num):
                tempTwo = tempTwo + "    "
            start = splitTemp[lineNum].find("~")
            splitTemp[lineNum] = tempTwo + splitTemp[lineNum][start + 1 : -1] + ":"
            num = num + 1
        elif (
            splitTemp[lineNum].replace("\t", "").replace(" ", "").startswith("}")
            and num > 1
        ):
            num = num - 1
            tempTwo = ""
            for x in range(num):
                tempTwo = tempTwo + "    "
            splitTemp[lineNum] = tempTwo + ""
        else:
            tempTwo = ""
            for x in range(num):
                tempTwo = tempTwo + "    "
            splitTemp[lineNum] = tempTwo + convert_single_line(splitTemp[lineNum])
    temp = ""
    for x in splitTemp:
        temp = temp + "\n" + x
    return temp


def convert_page(page: str):
    page = fromstring(page)


def convert(path: str, fileName: str) -> None:
    microcontrollerData = ""
    cwd = os.getcwd()
    os.chdir(path)
    file = open(fileName, "r")
    data = file.read()
    file.close()
    compiledFile = convert_file(data)
    try:
        file = open(fileName[:-9] + ".py", "r")
        microcontrollerData = file.read()
        file.close()
    except FileNotFoundError:
        file = open(fileName[:-9] + ".py", "w")
        microcontrollerData = "import view\nclass Page(view.View):\n    def __init__(self):\n        pass\n"
        file.write(microcontrollerData)
        file.close()
    os.chdir(cwd)
    # if not os.listdir().__contains__("g"):
    #    os.mkdir("g")
    # os.chdir(cwd + "/g")
    # print(microcontrollerData)
    file = open(path + "/" + (fileName[:-9] + "c.py"), "w")
    linked_mod = path[2:].replace("/", ".").replace("\\", ".") + "." + fileName[:-9]
    compiledFile = (
        "from hibiscus.core.apploc import *\nimport "
        + linked_mod
        + "\n@partial_implementation("
        + linked_mod
        + '.Page)\nasync def main(self, page_change=None):\n    hbs_line = ""'
        + compiledFile
        + "\n    if page_change != None:    hbs_line = self._pageChange(hbs_line, page_change)\n    return hbs_line"
    )
    file.write((compiledFile))
    file.close()
    # os.chdir(cwd)
    # os.chdir(cwd)

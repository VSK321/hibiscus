import os #Convert("C:\\Users\\shrik.HOME-PC02\\OneDrive\\Documents\\PythonTests\\Roze", "Test.roze")
import uuid

def ConvertSingleLine(line: str) -> str:
    if line.replace('\t', '').replace(' ', '').startswith("~exe~"):
        line = line[(line.find("~exe~")+5):len(line)]        
    else:
        #if line.find("~(") != -1:
        #    position = line.find(">")
        #    if position != -1:
        #        line = line[:position] + " rozeid=\""+ uuid.uuid4().hex +"\"" + line[position:]
        line = line.replace("~(", "' + str(")
        line = line.replace(")~", ") + '")
        line = "temp = temp + '" + line + "\\n' "
    return line

def ConvertFile(temp: str) -> str:
    splitTemp = temp.splitlines()
    num = 2
    for lineNum in range(len(splitTemp)):
        if splitTemp[lineNum].replace('\t', '').replace(' ', '').startswith('~') and splitTemp[lineNum].endswith('{~'):
            tempTwo = ""
            for x in range(num):
                tempTwo = tempTwo + '    '
            start = splitTemp[lineNum].find('~')
            splitTemp[lineNum] = tempTwo + splitTemp[lineNum][start+1:-2] + ":"
            num = num + 1
        elif splitTemp[lineNum].replace('\t', '').replace(' ', '').startswith('~}'):
            num = num - 1
            tempTwo = ""
            for x in range(num):
                tempTwo = tempTwo + '    '
            splitTemp[lineNum] = tempTwo + ""
        else:
            tempTwo = ""
            for x in range(num):
                tempTwo = tempTwo + '    '
            splitTemp[lineNum] = tempTwo + ConvertSingleLine(splitTemp[lineNum])
    temp = ""
    for x in splitTemp:
        temp = temp + '\n' + x
    return temp

def Convert(path: str, fileName: str) -> None:
    microcontrollerData = ""
    cwd = os.getcwd()
    os.chdir(path)
    file = open(fileName, 'r')
    data = file.read()
    file.close()
    compiledFile = ConvertFile(data)
    try:
        file = open(fileName+'.py', 'r')
        microcontrollerData = file.read()
        file.close()
    except:
        file = open(fileName+'.py', 'w')
        microcontrollerData = 'import view\nclass Page(view.View):\n    def __init__(self):\n        pass\n'
        file.write(microcontrollerData)
        file.close()
    os.chdir(cwd)
    #if not os.listdir().__contains__("g"):
    #    os.mkdir("g")
    #os.chdir(cwd + "/g")
    #print(microcontrollerData)
    file = open((fileName[:-5]+".py"), 'w')
    compiledFile = microcontrollerData + '\n    async def main(self, page_change=None):\n        temp = ""' + compiledFile + '\n        if page_change != None:    temp = super()._pageChange(temp, page_change)\n        return temp'
    file.write((compiledFile))
    file.close()
    #os.chdir(cwd)
    #os.chdir(cwd)


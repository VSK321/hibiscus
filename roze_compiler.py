import os #Convert("C:\\Users\\shrik.HOME-PC02\\OneDrive\\Documents\\PythonTests\\Roze", "Test.roze")

def ConvertSingleLine(line):
    if line.replace('\t', '').replace(' ', '').startswith("~exe~") == True:
        line = line[(line.find("~exe~")+5):len(line)]        
    else:
        line = line.replace("~(", "' + str(")
        line = line.replace(")~", ") + '")
        #if line.find(" ~onclick=") != -1:
        line = line.replace("~onclick=", "rozeclick=")
        line = line.replace("~onhover=", "rozehover=")
            #end = line.find("]~") + 2
            #start = line.find(" ~[onclick=")
            #line = line[0:start] + line[end:len(line)]
        line = "temp = temp + '" + line + "\\n' "
    return line

def ConvertFile(temp):
    splitTemp = temp.splitlines()
    num = 2
    for lineNum in range(len(splitTemp)):
        if splitTemp[lineNum].replace('\t', '').replace(' ', '').startswith('~') == True and splitTemp[lineNum].endswith('{~') == True:
            tempTwo = ""
            for x in range(num):
                tempTwo = tempTwo + '    '
            start = splitTemp[lineNum].find('~')
            splitTemp[lineNum] = tempTwo + splitTemp[lineNum][start+1:-2] + ":"
            num = num + 1
        elif splitTemp[lineNum].replace('\t', '').replace(' ', '').startswith('~}') == True:
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

def Convert(path, fileName):
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
    if not os.listdir().__contains__("g"):
        os.mkdir("g")
    os.chdir(cwd + "/g")
    #print(microcontrollerData)
    file = open((fileName[:-5]+".py"), 'w')
    compiledFile = microcontrollerData + '\n    def main(self):\n        temp = ""' + compiledFile + '\n        return temp'
    file.write((compiledFile))
    file.close()
    os.chdir(cwd)
    #os.chdir(cwd)


import os
from shutil import copy
import shutil
from searchStr import SearchStr
import sys
class AutoOCD:
    installDir = ""
    cwd = ""
    gdbPort = 1234
    telnetPort = 1235
    mainPath =""
    mainHeaderPath = ""
    interruptsPath = ""
    openOCDPath = ""
    def __init__(self,args,installDir) -> None:
        self.installDir = installDir
        self.cwd = os.getcwd()
        if args.init:
            print("in main")
            self.init()
    def init(self):
        ans = input(f"You are about to initalize a new auto-ocd project in the directory \"{self.cwd}\". This will overwrite existing files.  Are you sure? (y or n) ")
        if not ans == "y":
            print("aborting....")
            sys.exit() 
        while True:
            projectName = input(f"enter a new project name: ")
            if not projectName:
                print(f'Invalid project name')
            else:
                break
        cubeMXPath = f'''{self.cwd}/CubeMX'''
        print(f'''Open STM32CubeMX and create a new project.  Select {self.cwd} as the project directory and name the project "CubeMX". Do not change the Toolchain folder location. Select "CMake" as the "toolchain / IDE", then click generate code.  When this step is completed, return to this terminal and press enter''')
        input()
        if not os.path.exists(f'''{cubeMXPath}/Core/Src'''):
            print(f'''Error: Cannot read {cubeMXPath}/Core/Src/main.c, manually delete CubeMX directories and try again''')
            sys.exit()

        cmakePath = f'''{cubeMXPath}/CMakeLists.txt'''
        oldStr = SearchStr.CMakeUserIncludes
        newStr = f'''{SearchStr.CMakeUserIncludes}\n"../src/includes"'''
        fileStringReplace(cmakePath,oldStr,newStr)
        oldStr = SearchStr.CMakeUserSources
        startStr = f'''FILE(GLOB SOURCES "../src/*.cpp")'''
        endStr = "${SOURCES}"
        newStr = f'''{startStr}\n{oldStr}\n{endStr}'''
        fileStringReplace(cmakePath,oldStr,newStr)
        self.copyDefaultFiles(projectName)


    def copyDefaultFiles(self,projectName):
        os.makedirs("./src")
        os.makedirs("./src/includes")
        defaultPrePath = "/usr/share/auto-ocd"
        defaultMainPath = f'''{defaultPrePath}/default1234.cpp'''
        defaultMainHeaderPath = f'''{defaultPrePath}/default1234.hpp'''
        defaultInterruptsPath = f'''{defaultPrePath}/interrupts.cpp'''
        defaultOpenOCDPath = f'''{defaultPrePath}/openocd.cfg'''

        newSrcPath = f'''{self.cwd}/src'''
        self.mainPath = f'''{newSrcPath}/default1234.cpp'''
        self.mainHeaderPath = f'''{newSrcPath}/includes/default1234.hpp'''
        self.interruptsPath = f'''{newSrcPath}/interrupts.cpp'''
        self.openOCDPath = f'''{self.cwd}/openocd.cfg'''

        copyNewPermissions(defaultMainPath,self.mainPath)
        copyNewPermissions(defaultMainHeaderPath,self.mainHeaderPath)
        copyNewPermissions(defaultInterruptsPath,self.interruptsPath)
        copyNewPermissions(defaultOpenOCDPath,self.openOCDPath)

        fileStringReplace(self.mainPath,"default1234",projectName)
        fileStringReplace(self.mainHeaderPath,"default1234",projectName)
        tmpMainPath = f'''{getParentDir(self.mainPath)}{projectName}.cpp'''
        tmpHeaderPath = f'''{getParentDir(self.mainHeaderPath)}{projectName}.hpp'''
        shutil.move(self.mainPath,tmpMainPath)
        shutil.move(self.mainHeaderPath,tmpHeaderPath)

        self.mainPath = tmpMainPath
        self.mainHeaderPath = tmpHeaderPath


        
        
        
def copyNewPermissions(srcPath,newPath):
    shutil.copy(srcPath,newPath)
    os.chmod(newPath,0o666)


def getParentDir(path): #removes filename from end of path, leaving a trailing /
    path = path[::-1]
    for curChar in path:
        if curChar == '/':
            break
        else:
            path = path[1:]
    return path[::-1]

def checkFileExists(path): #returns file path if it exists, exits program with message otherwise
    if not os.path.exists(path):
        print(f'''Error: Cannot read {path}....Aborting''')
    return path

def fileStringReplace(filePath,oldStr,newStr):
    filePath = checkFileExists(filePath)
    data = ''
    with open(filePath,"r") as file:
        data = file.read()
    data = data.replace(oldStr,newStr)
    with open(filePath,"w") as file:
        file.write(data)


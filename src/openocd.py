import threading
import os
import telnetlib
import time
class Openocd:
    tn:telnetlib.Telnet
    upld:str
    verify:str
    def __init__(self) -> None:
        self.verify = "flash verify_image ./build/CubeMX.elf 0 elf"
        self.upld = "flash write_image erase unlock ./build/CubeMX.elf 0 elf"
        self.createOpenocd()
    def createOpenocd(self):

        self.thread = threading.Thread(target=os.system,args=('openocd > /dev/null ',))
        self.thread.start()
        time.sleep(0.5)
        print("we in")
    def sendNC(self,command):
        command = f'''echo "{command}" | nc localhost 1235 -w1'''
        os.system(command)
    def upload(self):
        self.sendNC(self.upld)
        self.sendNC(self.verify)


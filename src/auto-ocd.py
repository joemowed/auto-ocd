#!/usr/bin/env python3
import argparse
import os
import sys
installDir = "/usr/share/auto-ocd"
tmpDir = "/tmp/auto-ocd"

def clrDir(path):

    try:
        os.removedirs(path)
    except FileNotFoundError:
        pass
        os.makedirs(path)

if __name__ == "__main__": 
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--init", action="store_true",
                    help="Initialize a new auto-ocd project.  Use with no other arguments.")
    parser.add_argument("-u","--upload",action="store_true",help="Uploads program and verifies upload using openocd script located at auto-ocd/openocd.cfg.  Resets and halts processor upon completion of upload.  Does not build program before uploading when used without \"--build\" option")
    parser.add_argument("-b","--build",action="store_true",help="Builds program. Defaults to debug build.")

    parser.add_argument("-g","--gdb",action="store_true",help="Creates openocd instance and calls gdb-multiarch on project executable.")
    parser.add_argument("--update",action="store_true",help=" Requires sudo.  Downloads newest version from github and adds \"auto-ocd.py\" to \"/usr/bin\" and copies nessasarry files to \"/usr/share/auto-ocd/*\". Overwrites existing open-ocd installation")
    args = parser.parse_args()
    print(args)
    if(args.update):
        if not os.getenv("SUDO_USER"):
            print("Installation requries sudo privileges.")
            sys.exit()
         
        cloneCommand = f"git clone \"https://github.com/joemowed/auto-ocd\" {tmpDir}"
        clrDir(tmpDir)
        os.system(cloneCommand)

#!/usr/bin/env python3
import argparse
import glob
import os
from posix import system
import sys
import shutil
installDir = "/usr/share/auto-ocd"
tmpDir = "/tmp/auto-ocd"

def rmDir(path):
    try:
        shutil.rmtree(path)
    except FileNotFoundError:
        pass

def clrDir(path):
    rmDir(path)
    os.makedirs(path)

if __name__ == "__main__":  
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--init", action="store_true",
                    help="Initialize a new auto-ocd project.  Use with no other arguments.")
    parser.add_argument("-u","--upload",action="store_true",help="Uploads program and verifies upload using openocd script located at auto-ocd/openocd.cfg.  Resets and halts processor upon completion of upload.  Does not build program before uploading when used without \"--build\" option")

    parser.add_argument("-b","--build",action="store_true",help="Builds program. Defaults to debug build.")
    parser.add_argument("-g","--gdb",action="store_true",help="Creates openocd instance and calls gdb-multiarch on project executable.")
    parser.add_argument("--update",action="store_true",help=" Requires sudo.  Downloads newest version from github and adds \"auto-ocd.py\" to \"/usr/bin\" and copies nessasarry files to \"/usr/share/auto-ocd/*\". Overwrites existing open-ocd installation")
    parser.add_argument("--update-local",action="store_true",help="Same as \"--update\", but uses the local src files instead of cloning from github.  Useful for development.")
    parser.add_argument("-d","--dev",action="store_true",help="Uses local src files instead of the ones installed at \"/usr/share\".  Useful for development. Note: Installs auto-ocd as if \"--update-local\" was called.")
    args = parser.parse_args()
    cwd = os.path.dirname(__file__)
    if args.dev:
        args.update_local = True
    if(args.update or args.update_local):
        if not os.getenv("SUDO_USER"):
            print("Installation requries sudo privileges.")
            sys.exit()
        if args.update_local:
            print(cwd)
            if -1 == cwd.find("auto-ocd/src"):
                if -1 == cwd.find("auto-ocd/test"):
                    print("Error:  Cannot run \"--update-local\" from the installed version of auto-ocd.  To update, try \"--update\" instead.")
                    sys.exit()
            rmDir(tmpDir)
            shutil.copytree(cwd,f"{tmpDir}/src")
            rmDir("/tmp/auto-ocd/__pycache__")

        else:   
            print("Downloading latest version...")
            clrDir(tmpDir)
            cloneCommand = f"git clone \"https://github.com/joemowed/auto-ocd\" {tmpDir}"
            os.system(cloneCommand)


        print("Creating \"/usr/share/auto-ocd\"...")
        clrDir(installDir)
        copyCommand = f"cp {tmpDir}/src/* {installDir}/"
        print("Copying dependencies...")
        os.system(copyCommand)
        copyBinCommand = f"cp {tmpDir}/src/auto-ocd.py /usr/bin"
        print("Creating executable...")
        try:
            os.remove("/usr/bin/auto-ocd")
        except FileNotFoundError:
            pass
        try:
            os.remove("/usr/bin/auto-ocd.py")
        except FileNotFoundError:
            pass
        os.system(copyBinCommand)
        renameBinCommand = f"mv /usr/bin/auto-ocd.py /usr/bin/auto-ocd"
        os.system(renameBinCommand)
        print("Removing temporary files...")
        rmDir(tmpDir)
        green_text = "\033[32m"
        reset_color = "\033[0m"

        print(f"{green_text}auto-ocd Successfully Installed{reset_color}")
        #drop root privlages
        callerUID = int(os.getenv("SUDO_UID"))

        os.setuid(callerUID)
    if args.dev:
        sys.path.append(cwd)
        from main import AutoOCD
        newCWD = os.getcwd()
        if not newCWD.find("auto-ocd/test"):
            print("local directories not valid for development, aborting")
            sys.exit()
        files = glob.glob(f'{newCWD}/**/**',recursive=True)
        for file in files:
            if os.path.isfile(file):
                os.remove(file)
                files.remove(file)
        files = glob.glob(f'{newCWD}/**/**',recursive=True)
        for dir in files:
            if dir.endswith('test'):
                continue
            try:
            
                shutil.rmtree(dir)
            except FileNotFoundError:
                pass
        shutil.copytree(f"../testSource",newCWD)
        os.chdir(newCWD)
    else:
        sys.path.append("/usr/share/auto-ocd")
        from main import AutoOCD
    AutoOCD(args,installDir)


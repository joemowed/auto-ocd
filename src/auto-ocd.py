#!/usr/bin/env python3
import argparse
import os
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
    args = parser.parse_args()
    print(args)
    if(args.update or args.update_local):
        if not os.getenv("SUDO_USER"):
            print("Installation requries sudo privileges.")
            sys.exit()
        if args.update_local:
            cwd = os.path.dirname(__file__)
            if -1 == cwd.find("auto-ocd/src"):
                print("Error:  Cannot run \"--update-local\" from the installed version of auto-ocd.  To update, try \"--update\" instead.")
                sys.exit()
            rmDir(tmpDir)
            shutil.copytree(cwd,f"{tmpDir}/src")

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
        print("git update test")

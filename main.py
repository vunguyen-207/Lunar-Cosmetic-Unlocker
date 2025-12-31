import os
import sys
import colorama
import pystyle
import shutil
import time 
from time import sleep
import tempfile
import urllib.request

reqfile = "https://github.com/prometheusreengineering/lunar/releases/download/1.2.0/prometheus-1.2.0-lunar.jar" # Just maybe, use the jar that i put in the same directory with this script instead of the link for safety purposes..
mainfile = os.path.basename(reqfile)

VERSIONS = [
    "1.16.5",
    "1.17.1",
    "1.18.2",
    "1.19.2",
    "1.19.3",
    "1.19.4",
]

VERSIONS.append("1.20")
VERSIONS.extend([f"1.20.{i}" for i in range(1, 7)])
VERSIONS.append("1.21")
VERSIONS.extend([f"1.21.{i}" for i in range(1, 11)])

def choose_version(): # I didn't filter 1.21.2. While making this I changed my mind and make the script paste the jar into EVERY folder in the directory instead of just the specified version.
    os.system('cls')
    print("\033[1;39m[\033[0;31mvu\033[1;39m] Pick your favourite version (Make sure it was installed!)")
    for i, v in enumerate(VERSIONS, start=1):
        print(f"{i}. {v}")
    choice = input("Choose one: ").strip()
    try:
        idx = int(choice) - 1
        if idx < 0 or idx >= len(VERSIONS):
            raise ValueError()
        return VERSIONS[idx]
    except Exception:
        os.system('cls')
        print("Number not exists.")
        time.sleep(2)

def download_file(reqfile, dst_path):
    print(f"Applying.. Please stand by.")
    try:
        urllib.request.urlretrieve(reqfile, dst_path)
        print(f"\033[1;39m[\033[0;31mvu\033[1;39m] Applied.")
    except Exception as e:
        os.system('cls')
        print("\033[1;39m[\033[0;31mvu\033[1;39m] Exception while installing required mod.")
        print("\033[1;39m[\033[0;31mvu\033[1;39m] Consider checking your internet.")
        raise


version = choose_version()
parts = version.split('.')
major_minor = '.'.join(parts[:2])

home = os.path.expanduser("~")

mods_path = os.path.join(home, ".lunarclient", "profiles", "lunar", major_minor, "mods")
print("\033[1;39m[\033[0;31mvu\033[1;39m] We got your mods directory.")

if not os.path.exists(mods_path):
    try:
        os.makedirs(mods_path, exist_ok=True)
        print(f"\033[1;39m[\033[0;31mvu\033[1;39m] We just created the directory for you. Make sure you didn't enable 'Override Global Setting' for 'Game Directory' in the Fabric settings. ", mods_path)
    except Exception as e:
        os.system('cls')
        print("\033[1;39m[\033[0;31mvu\033[1;39m] Exception while creating missing directory. Consider running the file as Administrator.")
        time.sleep(5)
        sys.exit(1)

moddirectory = os.path.join(mods_path, f"fabric-{version}") # Only for fabrics, yes.
if not os.path.exists(moddirectory):
    try:
        os.makedirs(moddirectory, exist_ok=True)
        print(f"\033[1;39m[\033[0;31mvu\033[1;39m] Created missing mods directory: {moddirectory}")
    except Exception:
        os.system('cls')
        print("\033[1;39m[\033[0;31mvu\033[1;39m] Exception while creating Fabric directory. Consider running the unlocker as Administrator.")
        time.sleep(5)
        sys.exit(1)

tmp_file = os.path.join(tempfile.gettempdir(), mainfile)
try:
    download_file(reqfile, tmp_file)
except Exception:
    os.system('cls')
    print("\033[1;39m[\033[0;31mvu\033[1;39m] Exception while downloading required mod. Consider checking your internet.")
    time.sleep(5)
    sys.exit(1)

allentries = os.listdir(mods_path)
subfolders = [d for d in allentries if os.path.isdir(os.path.join(mods_path, d))]
targets = []
if subfolders:
    targets = [os.path.join(mods_path, d) for d in subfolders]
else:
    targets = [moddirectory]
if moddirectory not in targets:
    targets.append(moddirectory)
copied = 0
    
for t in targets:
    dst = os.path.join(t, mainfile)
    try:
        shutil.copy2(tmp_file, dst)
        copied += 1
        print(f"\033[1;39m[\033[0;31mvu\033[1;39m] Done.")
    except Exception as e:
        print(f"\033[1;39m[\033[0;31mvu\033[1;39m] Exception while applying the required mod into the directory {dst}:", e)
            
os.system('cls')
print(f"\033[1;39m[\033[0;31mvu\033[1;39m] Everything's done! You are good to go :)")
time.sleep(5)
sys.exit(1)

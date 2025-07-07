import time
import os
import requests
import json
import sys
from InquirerPy import inquirer
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# === Config ===
try:
    with open('settings.json') as f:
        config = json.load(f)
except:
    os.system('cls' if os.name == 'nt' else 'clear')
    print ("\nHello & Welcome To Psyncer !")
    print ("This is A pilot CLI project to sync documents between devices connected to PSYCHO-SYNC\n")

    choice = "Yes"
    choice = inquirer.select(
        message="Are You Using The PSYCHO-SYNC's IP :",
        choices=["Yes", "No"],
    ).execute()
    tmpIP = "https://40.0.0.4/"
    if choice == "No" :
        tmpIP = input("Enter Your Host IP : ")

    choice = inquirer.select(
        message="Use `C: → Psyncer` : ",
        choices=["Yes", "No"],
    ).execute()
    tmpDIR = "C:\\Psyncer"
    if choice == "No" :
        tmpDIR = input("Enter The Psyncer Directory : ")

    if not os.path.isdir(tmpDIR):
        os.makedirs(tmpDIR)

    data = {
        "dir": tmpDIR,
        "host": tmpIP
    }

    with open("settings.json", 'w') as json_file:
        json.dump(data, json_file, indent=2)
    
    print("Everything Done !")
    print(f"Now Files in ({tmpDIR}) Are Sync with PSYCHO-SYNC Device & Devices Connected To It .")

    with open('settings.json') as f:
        config = json.load(f)

    time.sleep(7)

    
path = config['dir']
api_url = config['host']

# === Global Variables ===
flg = True

# === File Watch Handler ===
class WatchHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if flg :
            if not event.is_directory:
                print(f"File Changed → {event.src_path.replace(path, '.')}")

    def on_created(self, event):
        if flg :
            if not event.is_directory:
                print(f"File Created → {event.src_path.replace(path, '.')}")

    def on_deleted(self, event):
        if flg :
            if not event.is_directory:
                print(f"File Deleted → {event.src_path.replace(path, '.')}")

    def on_moved(self, event):
        if flg :
            if not event.is_directory:
                print(f"Filename Changed → {event.src_path.replace(path, '.')} → {event.dest_path.replace(path, '.')}")

# === Functions ===
def clr():
    os.system('cls' if os.name == 'nt' else 'clear')

# === Main Program ===
if __name__ == "__main__":
    # Start file watcher
    event_handler = WatchHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        while True:
            try:
                try: 
                    response = requests.get(api_url, timeout=3)
                    if response.status_code == 200:
                        clr()
                        print(f"🔌 PSYCHO-SYNC is Connected. → {api_url}")
                        print(f"📂 Psyncing Directory → {path}")
                        flg = True
                    else:
                        raise requests.RequestException
                except requests.RequestException:
                    raise RuntimeError("❌ PSYCHO-SYNC is not Connected.")
            except RuntimeError as e:
                clr()
                print(e)
                print("🔗 Check https://github.com/aliamdevs/psycho-sync")
                print("🔗 Psyncer Needs To Connect To PSYCHO-SYNC")
                print("🔗 More Information Check https://github.com/aliamdevs/psyncer")
                flg = False
            time.sleep(3)
    except KeyboardInterrupt:
        print("❌ Stopping Observer & Exit ...")
        observer.stop()

    observer.join()

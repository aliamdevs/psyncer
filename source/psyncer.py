import time
import os
import requests
import json
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# === Config ===
try:
    with open('settings.json') as f:
        config = json.load(f)
except:
    print("❌ Settigns Not Declared Correctly. ")
    print("🔗 Check https://github.com/aliamdevs/psyncer")   
    sys.exit(1)
    
path = config['dir']
api_url = config['host']
delay = config['delay']

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
            time.sleep(delay)
    except KeyboardInterrupt:
        print("❌ Stopping Observer & Exit ...")
        observer.stop()

    observer.join()

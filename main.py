from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
from datetime import datetime


class handler(FileSystemEventHandler):

    def on_created(self, event):
        if event.is_directory:
            return
        print(f'File Created: {event.src_path}')
    

if __name__ == "__main__":
    path = "watched_folder"
    event_handler = handler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive = False)
    observer.start()

    try:
        while True: 
            time.sleep(1) 
    except KeyboardInterrupt:
        observer.stop()  
    observer.join() 
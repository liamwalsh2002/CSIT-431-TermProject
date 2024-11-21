from watchdog.observers import Observer
from watchdog.events import DirModifiedEvent, FileModifiedEvent, FileSystemEventHandler
import time
from datetime import datetime
import random
import os


class handler(FileSystemEventHandler):

    def on_modified(self, event):
        if event.is_directory:
            return
        
        with open('./journal_folder/jl_abc_txt_81247.DAT', 'a') as journalFile:
            # journal_entry = f"File Created: {event.src_path} - Random Number: {randomNumber} - Date/Time: {datetime.now()}\n"
            journal_entry = "testing that it picks up modfied"
            journalFile.write(journal_entry)
        # return super().on_modified(event)
    
    def on_created(self, event):
        if event.is_directory:
            return
        
        print(f'File Created: {event.src_path}')

        watchedFolder = os.path.abspath('watched_folder')  
        journalFolder = os.path.abspath('journal_folder')  

        filenameWithoutExtension = os.path.splitext(os.path.basename(event.src_path))[0]
        randomNumber = random.randint(10000, 99999)
        journalFileName = f'jl_{filenameWithoutExtension}_txt_{randomNumber}.DAT'

        journalFilePath = os.path.join(journalFolder, journalFileName)

        with open(journalFilePath, 'a') as journalFile:
            journal_entry = f"File Created: {event.src_path} - Random Number: {randomNumber} - Date/Time: {datetime.now()}\n"
            journalFile.write(journal_entry)

    

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
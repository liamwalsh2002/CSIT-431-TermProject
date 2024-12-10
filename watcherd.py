import os
import time
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

WATCHED_FOLDER = "./watched_folder"
JOURNAL_FOLDER = "./journal_folder"

os.makedirs(JOURNAL_FOLDER, exist_ok=True)

def get_journal_file(file_name):
    """Generate a unique journal file path for the given file."""
    base_name = file_name.replace('.', '_')
    random_suffix = str(int(time.time()))
    return os.path.join(JOURNAL_FOLDER, f"j1_{base_name}_{random_suffix}.DAT")

def write_to_journal(journal_path, action, line_number, content):
    """Write a log entry to the journal file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_entry = f"{timestamp},{action},l{line_number}:{content}\n"

    with open(journal_path, "a") as journal:
        journal.write(new_entry)

def track_file(file_path):
    """Track the changes in a file."""
    journal_path = get_journal_file(os.path.basename(file_path))
    with open(file_path, "r") as file:
        lines = file.readlines()
    # Log all current lines as added
    for idx, line in enumerate(lines, start=1):
        write_to_journal(journal_path, "+", idx, line.strip())
    return journal_path

class FileChangeHandler(FileSystemEventHandler):
    """Custom event handler for file changes."""

    def __init__(self):
        super().__init__()
        self.tracked_files = {}

    def on_created(self, event):
        if not event.is_directory:
            print(f"File created: {event.src_path}")
            self.tracked_files[event.src_path] = track_file(event.src_path)

    def on_modified(self, event):
        if not event.is_directory and event.src_path in self.tracked_files:
            print(f"File modified: {event.src_path}")
            journal_path = self.tracked_files[event.src_path]

            with open(event.src_path, "r") as file:
                new_lines = file.readlines()

            # Create journal if not exists
            if not os.path.exists(journal_path):
                with open(journal_path, 'w') as journal:
                    pass

            # Read existing journal to get the last state of the file
            with open(journal_path, "r") as journal:
                current_lines = {}
                for entry in journal.readlines():
                    parts = entry.strip().split(",")
                    action, line_content = parts[1], parts[2]
                    line_number, content = line_content[1:].split(":")
                    current_lines[int(line_number)] = content if action == "+" else None

            # Detect changes
            for idx, new_line in enumerate(new_lines, start=1):
                if idx not in current_lines or current_lines[idx] != new_line.strip():
                    # Remove old line (if it exists)
                    if idx in current_lines and current_lines[idx]:
                        write_to_journal(journal_path, "-", idx, current_lines[idx])
                    # Add new line
                    write_to_journal(journal_path, "+", idx, new_line.strip())

            # Detect removed lines
            for idx in list(current_lines.keys()):
                if idx > len(new_lines) or current_lines[idx] is None:
                    write_to_journal(journal_path, "-", idx, current_lines[idx])

    def on_deleted(self, event):
        if not event.is_directory and event.src_path in self.tracked_files:
            print(f"File deleted: {event.src_path}")
            del self.tracked_files[event.src_path]

if __name__ == "__main__":
    # Ensure the watched folder exists
    os.makedirs(WATCHED_FOLDER, exist_ok=True)

    # Initialize the observer and handler
    event_handler = FileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCHED_FOLDER, recursive=False)

    print(f"Monitoring folder: {WATCHED_FOLDER}")
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

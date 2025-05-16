import os
import sys

count = 0

def base_directory():
    """Returns the base directory of the script or executable."""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

def delete_desktop_ini_files(directory):
    """Deletes all 'desktop.ini' files in the specified directory and subdirectories."""
    global count
    if not os.path.exists(directory):
        print(f"Error: Directory '{directory}' does not exist.")
        return
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower() == "desktop.ini":
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    count += 1
                    print(f"Deleted: {file_path} (Total: {count})")
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")

directories = [
    r"C:\Users\angry\My Drive",
    r"S:\My Drive",
    r"Z:\My Drive"
]

for dir_path in directories:
    print(f"Cleaning directory: {dir_path}")
    delete_desktop_ini_files(dir_path)

print(f"Finished cleaning. Total files deleted: {count}")

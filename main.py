import shutil
import time
import sys
from pathlib import Path
from datetime import datetime

# 1. HANDLING THE INPUT ARGUMENTS
# checking the number of command line arguments
if len(sys.argv) != 5:
    print("""Invalid number of command line arguments. Expected 4 arguments:
    1: path of the folder
    2: path of the synchronised copy folder
    3: path of the log file
    4: synchronisation interval in seconds""")
    sys.exit(1)

# transforming value types of the arguments
try:
    MAIN_DIRECTORY = Path(sys.argv[1])
    COPY_DIRECTORY_NAME = Path(sys.argv[2])
    LOG_PATH = Path(sys.argv[3])
    SYNCHRONIZATION_INTERVAL = int(sys.argv[4])
except ValueError as e:
    print("Invalid argument:", e)
    sys.exit(1)

# checking if the original directory exists
if not MAIN_DIRECTORY.is_dir():
    print(f"The directory {MAIN_DIRECTORY} does not exist")
    sys.exit(1)

# creating the copy directory
if not COPY_DIRECTORY_NAME.exists():
    COPY_DIRECTORY_NAME.mkdir()


# 2. DEFINING FUNCTIONS
def action_record(path_name: Path, action: str, log_file: Path = LOG_PATH):
    message = f"{datetime.now()} {action}: {path_name}"
    print(message)
    with open(log_file, mode="a", encoding="utf-8") as file:
        file.write(f"{message}\n")


def moved_subpath(old_path: Path, new_parent: Path) -> Path:
    """Creates path from original path with new parent directory."""
    sub_path = Path(*Path(old_path).parts[1:])
    new_path = Path(new_parent, sub_path)
    return new_path


def delete_path(to_del_path: Path):
    for child in to_del_path.glob('*'):
        if child.is_file():
            child.unlink()
        else:
            delete_path(child)
        action_record(child, "deleted")
    if to_del_path.is_file():
        to_del_path.unlink()
    else:
        to_del_path.rmdir()
    action_record(to_del_path, "deleted")


def replace_updated_file(original: Path, copy: Path):
    if original.stat().st_mtime > copy.stat().st_mtime:
        destination_path = Path(*copy.parts[:-1])
        copy.unlink()
        shutil.copy2(original, destination_path)
        action_record(original, "updated")


def create_copy_path(original: Path, copy: Path):
    if original.is_dir():
        copy.mkdir()
    elif original.is_file():
        copy_destination = Path(*copy.parts[:-1])
        shutil.copy2(original, copy_destination)
    action_record(copy, "created")


# 3. RUNNING THE SCRIPT
while True:

    # deleting and updating files and directories in copy
    for copy_path_1 in COPY_DIRECTORY_NAME.rglob("*"):
        original_path_1 = moved_subpath(copy_path_1, MAIN_DIRECTORY)

        # updating files in copy
        if original_path_1.is_file():
            replace_updated_file(original_path_1, copy_path_1)

        # deleting files and directories in copy
        elif not original_path_1.is_dir():
            delete_path(copy_path_1)

    # creating files and directories in copy
    for original_path_2 in MAIN_DIRECTORY.rglob("*"):
        copy_path_2 = moved_subpath(original_path_2, COPY_DIRECTORY_NAME)
        if not copy_path_2.exists():
            create_copy_path(original_path_2, copy_path_2)

    time.sleep(SYNCHRONIZATION_INTERVAL)

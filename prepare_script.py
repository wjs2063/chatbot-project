import re
import os
import shutil



def move_and_rename():
    wmv_files = [file for file in os.listdir() if file.endswith('.wmv')]

    for wmv_file in wmv_files:
        _match = re.match(r'^(\d+)_',wmv_file)
        if _match:
            prefix = _match.group(1)
            new_folder_name = wmv_file.replace(f"{prefix}_", "")
            new_folder_name = new_folder_name.replace(".wmv","")
            os.makedirs(new_folder_name, exist_ok=True)
            shutil.move(wmv_file, os.path.join(new_folder_name, new_folder_name + ".wmv"))
            print(f"Moved {wmv_file} to {new_folder_name}/{wmv_file}")

if __name__ == "__main__":
    move_and_rename()
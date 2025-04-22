from os import listdir
from os.path import isfile, join
import os
import json
from pathlib import Path

# List all valid files in a directory that don't match ignored extensions
def get_files_in_directory(directory_path, files_to_ignore):
    file_paths = []
    
    for file_path in listdir(directory_path):
        if isfile(join(directory_path, file_path)) and file_path[-4:] not in files_to_ignore:
            file_paths.append(join(directory_path, file_path).replace("\\", "/"))
            
    return file_paths


# List all folders in a directory
def get_folders_in_directory(directory_path):
    folder_paths = []
    
    for folder_path in listdir(directory_path):
        if isfile(join(directory_path, folder_path)) == False:
            folder_paths.append(join(directory_path, folder_path).replace("\\", "/"))
            
    return folder_paths


# Save content to file, as JSON if appropriate
def save_file_to_directory(directory_path, file_name, content):
    directory_path = Path(directory_path)
    directory_path.mkdir(parents=True, exist_ok=True)
    output_file = directory_path / file_name
    file_extension = output_file.suffix

    with open(output_file, 'w', encoding='utf-8') as file:
        if file_extension == ".json":
            json.dump(content, file, indent=4)
        else:
            file.write(content)

# Count files in a given directory
def count_files_in_directory(directory):
    return len([f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))])

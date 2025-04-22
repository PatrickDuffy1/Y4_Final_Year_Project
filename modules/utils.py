from os import listdir
from os.path import isfile, join
import os
import json
from pathlib import Path

# Returns a list of all the file paths in the given folder
def get_files_in_directory(directory_path, files_to_ignore):
    
    file_paths = []
    
    # Loop through all of the files in the given directory
    for file_path in listdir(directory_path):
    
        # Ignore anything that is a directory or text file
        if isfile(join(directory_path, file_path)) and file_path[-4:] not in files_to_ignore:
            
            # Add the file to the list of valid files
            file_paths.append(join(directory_path, file_path).replace("\\", "/"))
        
    return file_paths
    
    
def get_folders_in_directory(directory_path):
    
    folder_paths = []
    
    # Loop through all of the files in the given directory
    for folder_path in listdir(directory_path):
    
        # Ignore anything that is a directory or text file
        if isfile(join(directory_path, folder_path)) == False:
            
            # Add the file to the list of valid files
            folder_paths.append(join(directory_path, folder_path).replace("\\", "/"))
        
    return folder_paths
    
    
def save_file_to_directory(directory_path, file_name, content):
    directory_path = Path(directory_path)  # Ensure it's a Path object
    directory_path.mkdir(parents=True, exist_ok=True)  # Create dirs if needed

    output_file = directory_path / file_name
    file_extension = output_file.suffix

    with open(output_file, 'w', encoding='utf-8') as file:
        if file_extension == ".json":
            json.dump(content, file, indent=4)
        else:
            file.write(content)
            

def count_files_in_directory(directory):
    return len([f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))])
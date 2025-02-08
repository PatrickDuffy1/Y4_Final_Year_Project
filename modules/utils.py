from os import listdir, getcwd
from os.path import isfile, join

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
def read_file(file_path):
    
    try:
        # Check if the file is an epub file or a txt file. Raise exception if not either
        if file_path[-5:] == ".epub":
            text = read_epub_file(file_path)
        elif file_path[-4:] == ".txt":
            text = read_text_file(file_path)
        else:
            raise Exception("Invalid file type")
    except:
        raise Exception("Error reading file")
        
    return text
    
    
def read_text_file(file_path):

    print("Reading .txt file:", file_path)
    
    # Read text file
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

        

def read_epub_file(file_path):
    
    print("Reading .epub file:", file_path)
    
    # TODO: Implement epub_file_reader
    #text = epub_file_reader.read_epub_file(file_path)
    
    raise Exception("Not yet implemented")
    
    return ""
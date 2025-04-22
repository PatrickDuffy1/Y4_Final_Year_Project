# Import the ebub reader module
import epub_file_reader

def read_file(file_path):
    """
    Reads the content of a .txt or .epub file based on its extension.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The textual content of the file.

    Raises:
        ValueError: If the file extension is not .txt or .epub.
        Exception: If an error occurs during reading.
    """
    try:
        # Check file extension and delegate to appropriate function
        if file_path.endswith(".epub"):
            text = read_epub_file(file_path)
        elif file_path.endswith(".txt"):
            text = read_text_file(file_path)
        else:
            # Raise an error for unsupported file types
            raise ValueError(f"Invalid file type: {file_path}")
    except Exception as e:
        # Raise a new exception with additional context if reading fails
        raise Exception(f"Error reading file: {e}")
    
    return text


def read_text_file(file_path):
    """
    Reads the contents of a plain text (.txt) file.

    Args:
        file_path (str): The path to the .txt file.

    Returns:
        str: The textual content of the file.
    """
    print("Reading .txt file:", file_path)
    
    # Open and read the file using UTF-8 encoding
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def read_epub_file(file_path):
    """
    Reads the contents of an EPUB file using the epub_file_reader module.

    Args:
        file_path (str): The path to the .epub file.

    Returns:
        str: The textual content of the EPUB file.
    """
    print("Reading .epub file:", file_path)
    
    # Delegate to the custom EPUB file reader module
    return epub_file_reader.read_epub_file(file_path)

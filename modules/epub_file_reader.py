import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import re

def read_epub_file(file_path):

    # Load the EPUB file
    book = epub.read_epub(file_path)

    # Access the spine items (the main content of the EPUB)
    spine_items = book.get_items_of_type(ebooklib.ITEM_DOCUMENT)

    chapters = []

    # Loop through the spine items and print their content
    for item in spine_items:
        # Get the chapter title from the item (if available)
        title = item.get_name()  # Gets the chapter name
        
        # Read the content of the chapter
        content = item.get_body_content()  # Get as a string
        content = content.decode('utf-8')  # Decode bytes to string
        
        # Remove <a>, <em>, and <i> tags using regex
        content = re.sub(r'<(a|em|i)[^>]*>', '', content)  # Remove opening tags
        content = re.sub(r'</(a|em|i)>', '', content)      # Remove closing tags

        # Use Beautiful Soup to parse the HTML content
        soup = BeautifulSoup(content, 'html.parser')
        
        # Attempt to extract chapter titles from all <h1> tags
        title = None
        h1_tags = soup.find_all('h1')  # Find all <h1> tags

        # If there are multiple <h1> tags, join them with a separator
        if h1_tags:
            title = " - ".join(h1.get_text(strip=True) for h1 in h1_tags)

        # If no title is found or the title is empty, set a default title ("New Chapter")
        if not title or title == "":
            title = "New Chapter"  # Default title for empty <h1> tags
            
        plain_text = title + ".\n"
        
        # Extract and clean plain text from the HTML
        sections = soup.find_all('p')
        plain_text += "\n".join(section.get_text(strip=True) for section in sections)
        
        # Normalize whitespace
        plain_text = "\n".join(line.strip() for line in plain_text.splitlines() if line.strip())
        
        chapters.append(plain_text)

    print(f"\nTotal chapters extracted: {len(chapters)}")
    
    return chapters

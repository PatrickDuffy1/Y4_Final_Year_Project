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

    # Loop through the spine items
    for item in spine_items:
        # Read and decode the content of the chapter
        content = item.get_body_content()
        content = content.decode('utf-8')

        # Remove <a>, <em>, and <i> tags using regex
        content = re.sub(r'<(a|em|i)[^>]*>', '', content)
        content = re.sub(r'</(a|em|i)>', '', content)

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(content, 'html.parser')
        
        print(f"Inspecting: {item.get_name()}")
        print(soup.prettify()[:1000])  # Show the first 1000 characters of cleaned HTML

        # Extract chapter title from <h1> tags if available
        title = None
        h1_tags = soup.find_all('h1')
        if h1_tags:
            title = " - ".join(h1.get_text(strip=True) for h1 in h1_tags)

        if not title or title.strip() == "":
            title = "New Chapter"

        # Remove scripts and styles
        for tag in soup(['script', 'style']):
            tag.decompose()

        # Extract all visible text
        visible_text = soup.get_text(separator="\n", strip=True)

        # Clean and normalize the text
        visible_text = "\n".join(line.strip() for line in visible_text.splitlines() if line.strip())

        # Combine title and visible text
        plain_text = f"{title}.\n{visible_text}"

        # Append to chapters list
        chapters.append(plain_text)

    return chapters

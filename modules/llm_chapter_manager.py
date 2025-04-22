import json
import os
import glob
from datetime import datetime
from file_reader import read_file
from llm_line_identifier import identify_lines_in_chapter
from utils import save_file_to_directory
from pathlib import Path

# Get the directory where this script is located
script_dir = Path(__file__).resolve().parent

# Default output folder for saving results
DEFAULT_OUTPUT_FILE_FOLDER = script_dir / ".." / "multi_speaker_outputs"

def identify_book_character_lines(llm, user_input, is_file, start_section, end_section, output_folder, max_retries_if_no_narrator):
    """
    Identifies character lines in a book or text input using an LLM and saves the results.
    Can resume from a previous run if the output folder already contains processed sections.
    """

    # Determine output directory based on user input or timestamp
    if output_folder == "":
        # If no output folder is provided, generate one with a timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S_%f")
        book_directory_path = DEFAULT_OUTPUT_FILE_FOLDER / timestamp
    elif not os.path.exists(output_folder):
        # If folder does not exist, create new one
        book_directory_path = Path(output_folder)
    else:
        # If folder exists, continue from last completed section
        book_directory_path = Path(output_folder)
        start_section = len(os.listdir(book_directory_path))
        print("Some sections already complete\nContinuing from section", start_section)
        
    # Load input text, either from file or directly from input
    if is_file:
        text = read_file(user_input)
    else:
        text = [user_input]
        start_section = 0
        end_section = len(text)
        
    if end_section == -1:
        # If end_section is -1, process till the end of the input
        end_section = len(text)
        
    print(text)
            
    # Process each chapter or section
    for i in range(start_section, end_section):
        # Identify character lines using the LLM
        character_lines = identify_lines_in_chapter(text[i], llm, max_retries_if_no_narrator)
        
        # Save identified lines to file
        chapter_dir = Path(book_directory_path) / "chapter_lines"
        filename = f"chapter_{i}_lines.json"
        save_file_to_directory(chapter_dir, filename, character_lines)
        
        # Extract and save character metadata (e.g., speaker names)
        chapter_dir = Path(book_directory_path) / "book_characters"
        filename = f"book_characters_chapter_{i}.json"
        save_file_to_directory(chapter_dir, filename, identify_characters(character_lines))

        # Merge all character files into one combined JSON
        merge_character_json_files(book_directory_path / "book_characters")
    
    print("\n\nLine identification complete")
    
    return book_directory_path
    
    
def identify_characters(input_data):
    """
    Extracts and returns a list of unique speakers with default voice assignments.
    Ensures 'Narrator' appears first if present.
    """

    # Normalize speaker names to lowercase
    speakers = [line["speaker"].lower() for line in input_data["lines"]]
    
    # Get unique speakers
    unique_speakers = set(speakers)

    # Create speaker records with default voice assignment
    speakers_with_voice = [{"speaker": speaker.capitalize(), "voice": "unassigned"} for speaker in unique_speakers]

    # Prioritize narrator (if present) to appear first
    if any(speaker == "narrator" for speaker in speakers):
        narrator = next(speaker for speaker in speakers_with_voice if speaker["speaker"].lower() == "narrator")
        speakers_with_voice.remove(narrator)
        speakers_with_voice.insert(0, narrator)

    return speakers_with_voice
    
    
import os
import glob
import json

def merge_character_json_files(folder_path, output_filename="merged_book_characters.json"):
    """
    Merges character JSON files from multiple chapters into one consolidated file.
    Tracks the sections in which each character appears.
    Ensures 'Narrator' appears first if present.
    """

    merged_data = {}

    # Find all relevant chapter character files
    files = glob.glob(os.path.join(folder_path, "book_characters_chapter_*.json"))

    for file in files:
        # Extract chapter number from filename
        chapter_num = int(os.path.splitext(os.path.basename(file))[0].split("_")[-1])
        
        with open(file, 'r') as f:
            data = json.load(f)
            
            for entry in data:
                speaker = entry["speaker"]
                
                # Add or update speaker record
                if speaker not in merged_data:
                    merged_data[speaker] = {
                        "speaker": speaker,
                        "voice": entry.get("voice", "unassigned"),
                        "sections": [chapter_num]
                    }
                else:
                    if chapter_num not in merged_data[speaker]["sections"]:
                        merged_data[speaker]["sections"].append(chapter_num)
                        merged_data[speaker]["sections"].sort()

    # Convert dict to sorted list for output
    merged_list = list(merged_data.values())
    merged_list.sort(key=lambda x: x["speaker"].lower())

    # Prioritize narrator to appear first if present
    narrator_entry = next((entry for entry in merged_list if entry["speaker"].lower() == "narrator"), None)
    if narrator_entry:
        merged_list.remove(narrator_entry)
        merged_list.insert(0, narrator_entry)

    # Save the merged file one level above the input folder
    output_dir = os.path.abspath(os.path.join(folder_path, os.pardir))
    output_path = os.path.join(output_dir, output_filename)

    with open(output_path, "w") as outfile:
        json.dump(merged_list, outfile, indent=4)

    print(f"Merged JSON created: {output_path}")

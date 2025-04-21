import json
import os
import glob
from datetime import datetime
from text_generator import generate_json_text
from llm_model_loader import load_llm_model
from file_reader import read_file
from llm_line_identifier import identify_lines_in_chapter
from utils import save_file_to_directory
from pathlib import Path

script_dir = Path(__file__).resolve().parent

DEFAULT_OUTPUT_FILE_FOLDER = script_dir / ".." / "multi_speaker_outputs"

def indentify_book_character_lines(llm, user_input, is_file, start_section, end_section, output_folder):
    
    if output_folder != "":
        book_directory_path = output_folder
        start_section = len(os.listdir(book_directory_path))
        print("Some sections already complete\nContinuing from section", start_section)
    else:
        # Set the output audio folder name to the current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S_%f")
        book_directory_path = DEFAULT_OUTPUT_FILE_FOLDER / timestamp
        
    if is_file:
        # Read the given file
        text = read_file(user_input)
    else:
        text = list()
        text.append(user_input)
        start_section = 0
        end_section = len(text)
        
        
    if end_section == -1:
        end_section = len(text)
        
        
    print(text)
            
    for i in range(start_section, end_section):
        character_lines = identify_lines_in_book(text[i], llm, is_file)
        save_file_to_directory(book_directory_path + "/chapter_lines", "chapter_" + str(i) + "_lines.json", character_lines)
        
        save_file_to_directory(book_directory_path + "/book_characters", "book_characters_chapter_" + str(i) + ".json", identify_characters(character_lines))
        identify_characters(character_lines)
        merge_character_json_files(book_directory_path + "/book_characters")
    
    print("\n\nLine identification complete")
    
    return character_lines
    
    
def identify_characters(input_data):
    
    # Convert all speaker names to lowercase to ensure case does not matter
    speakers = [line["speaker"].lower() for line in input_data["lines"]]
    
    # Extract unique speakers from the data
    unique_speakers = set(speakers)

    # Create a list of dictionaries with each speaker and the voice attribute set to "unnasigned"
    speakers_with_voice = [{"speaker": speaker.capitalize(), "voice": "unnasigned"} for speaker in unique_speakers]

    # Find the "narrator" entry (if it exists) and move it to the first position
    if any(speaker == "narrator" for speaker in speakers):
        narrator = next(speaker for speaker in speakers_with_voice if speaker["speaker"].lower() == "narrator")
        speakers_with_voice.remove(narrator)
        speakers_with_voice.insert(0, narrator)

    return speakers_with_voice


def identify_lines_in_book(user_input, llm, is_file):

    resulting_chapters = []

    #if is_file == False:
    return identify_lines_in_chapter(user_input, llm)
    #else:
     #   chapters = read_file(user_input)
           
    resulting_chapters.append(identify_lines_in_chapter(chapters[0], llm))
    
    for i in range(1, len(chapters)):
    
        resulting_chapters.append(identify_lines_in_chapter(chapters[i], llm))
        print(resulting_chapters[i])
        
    return resulting_chapters
    
    
def merge_character_json_files(folder_path, output_filename="merged_book_characters.json"):
    merged_data = {}

    files = glob.glob(os.path.join(folder_path, "book_characters_chapter_*.json"))

    for file in files:
        chapter_num = int(os.path.splitext(os.path.basename(file))[0].split("_")[-1])
        
        with open(file, 'r') as f:
            data = json.load(f)
            
            for entry in data:
                speaker = entry["speaker"]
                
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

    merged_list = list(merged_data.values())
    merged_list.sort(key=lambda x: x["speaker"].lower())

    output_dir = os.path.abspath(os.path.join(folder_path, os.pardir))
    output_path = os.path.join(output_dir, output_filename)

    with open(output_path, "w") as outfile:
        json.dump(merged_list, outfile, indent=4)

    print(f"Merged JSON created: {output_path}")

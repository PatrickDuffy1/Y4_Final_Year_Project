from datetime import datetime
import torch
import re
from TTS.api import TTS
import os
from file_reader import read_file

DEFAULT_OUTPUT_FILE_FOLDER = "./outputs"
DEFAULT_AUDIO_FILE_EXTENSION = ".mp3"
MAX_LINE_LENGTH = 600


# Load TTS model
def load_model():
    
    # Use cuda if available, otherwise use the cpu
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    print("Using device:", device)
    
    # Load TTS model
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
    
    return tts
    

def generate_audio(text, voice, tts, output_path, ouput_file_type):
    
    # Limit the sentence length in the text if a max length has been set
    if MAX_LINE_LENGTH > 0:
        text = limit_sentence_length(text, MAX_LINE_LENGTH)
        
    # Clean the text
    text = clean_text(text)
        
    # Run TTS
    tts.tts_to_file(text, speaker_wav=voice, language="en", file_path=output_path)
    
    # Return the path to the created audio file
    return output_path
    
 
def generate_audio_from_text(text, voice, ouput_file_type=DEFAULT_AUDIO_FILE_EXTENSION):
    
    # Load the tts model
    tts = load_model()

    # Set the output audio file name to the current timestamp
    output_file_path = DEFAULT_OUTPUT_FILE_FOLDER + "/" + str(datetime.now()).replace(":", "_").replace(".", "_").replace(" ", "_") + ouput_file_type
    
    return generate_audio(text, voice, tts, output_file_path, ouput_file_type)


def generate_audio_from_file(file_path, voice, ouput_file_type=DEFAULT_AUDIO_FILE_EXTENSION):
        
    # Read the given file
    text = read_file(file_path) 
    
    # Check if there are multiple sections/chapters
    if isinstance(text, list) == False:
    
        # Use the generate_audio_from_text function if there is not multiple sections
        return generate_audio_from_text(text, voice) 
    
    # Load the tts model
    tts = load_model()
    
    chapter_paths = []
    
    # Set the output audio folder name to the current timestamp
    output_folder_path = DEFAULT_OUTPUT_FILE_FOLDER + "/" + str(datetime.now()).replace(":", "_").replace(".", "_").replace(" ", "_") + "/"
    
    # Create output folder if it does not exist
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)
    
    # Call the generate_audio function for every section/chapter in the text
    for i, chapter in enumerate(text):
        output_file_path = output_folder_path + str(i) + ouput_file_type
        chapter_paths.append(generate_audio(text[i], voice, tts, output_file_path))
    
    # Return the audio file path of the first section of the text
    return chapter_paths[0]
    

# Clean unwanted characters from text
def clean_text(text):
    
    # Replace certain special characters or edge cases with valid characters
    text = text.replace("—", "-").replace(". . .", "...")
    text = text.replace("”", '"').replace("“", '"').replace("’", "'").replace("''", "'").replace('""', '"')
    text = text.replace("Mr.", "Mr").replace("Mrs.", "Mrs").replace("Dr.", "Dr").replace("Co.", "Co")
    text = text.replace("!.", "!").replace("?.", "?").replace("'.", "'").replace("\".", "\"")
    text = text.replace(" .", "")
    
    # Remove double periods '..' but keep '...' and '.'
    text = re.sub(r'(?<!\.)\.\.(?!\.)', '', text)
    
    # Remove any characters that are not letters or certain special characters
    text = re.sub(r'[^a-zA-Z0-9\s,.\'"!?()\[\]:;&\n-]', '', text)
    
    # Ensure every line ends with a full stop
    place_holder = "PLACE_HOLDER_STRING"
    text = re.sub(r'(?<![.,;:])\n(?=[A-Z])', place_holder, text)
    text = re.sub(r'(?<!\.)\n', ' ', text)
    text = re.sub(place_holder, '. ', text)
    
    return text
    

# Split sentences that are over max_line_length characters in length
def limit_sentence_length(text, max_line_length):
    
    # Split text by new lines
    text = text.split("\n")
    
    # Loop through all lines
    for i, line in enumerate(text):
        
        print("\n\nline:\n", line)
        
        # Limit the size of the words in the text
        line = limit_word_size(line)
        
        # Check if the current line is greater than max_line_length
        if len(line) > max_line_length:
            
            # Split the line
            line = split_line(line)
            
            # Recursive call this function to limit the size of the split lines 
            line = limit_sentence_length(line, max_line_length)
        
        # Add new lines back into the list of lines
        line = line + "\n"
        line = os.linesep.join([s for s in line.splitlines() if s])
        text[i] = line.replace("\n\n", "\n").lstrip(" ").rstrip(" ")
    
    filtered_text = [line for line in text if line]
    
    # Convert the lines back into a single string and return it
    return '\n'.join(filtered_text) + '\n' if filtered_text else ''
    

# Split a line
def split_line(line):
    
    # Find the halfway point of the line
    half_index = round(len(line) / 2)
    
    # Half the line and create two strings
    first_half_string = line[:half_index]
    second_half_string = line[half_index:]
    
    # Find the closest full stop the the halfway point of the original line
    first_full_stop_index = first_half_string.rfind(".")
    second_full_stop_index = second_half_string.find(".")
    
    # Find the closest space the the halfway point of the original line
    first_space_index = first_half_string.rfind(" ")
    second_space_index = second_half_string.find(" ")
    
    # Find the closest full stop to the halfway point (if it exists), and split the line at that point.
    # If a full stop is not in the line, split at the closest space to the halfway point.
    # Otherwise, split line in half
    if first_full_stop_index >= 0 and second_full_stop_index >= 0:
        
        if (len(first_half_string) - first_full_stop_index) < second_full_stop_index:
            space_index = first_full_stop_index
            
        elif (len(first_half_string) - first_full_stop_index) >= second_full_stop_index:
            space_index = second_full_stop_index + len(first_half_string)
                                
    elif first_full_stop_index >= 0:
        space_index = first_full_stop_index
        
    elif second_full_stop_index >= 0:
        space_index = second_full_stop_index + len(first_half_string)
        
    elif (len(first_half_string) - first_space_index) < second_space_index:
        space_index = first_space_index
        
    elif (len(first_half_string) - first_space_index) >= second_space_index:
        space_index = second_space_index + len(first_half_string)
    
    else:
        space_index = half_index
    
    # Insert a newline at the split point to split the lines
    line = line[:space_index] + "\n" + line[space_index + 1:]
    
    return line
    

# Split words that are over max_line_length characters in length
def limit_word_size(line):
    
    # Split the line into individual words
    line = line.split()
    result = []
    
    # Set the maximum word length
    max_word_size = 19
    
    # Loop through every word in the line
    for word in line:
    
        # Check if the current word is greater than max_word_size
        if len(word) > max_word_size:
            # Split the long word into chunks of max_word_size characters
            chunks = [word[i:i + max_word_size] for i in range(0, len(word), max_word_size)]
            result.append("\n".join(chunks))
        else:
            result.append(word)
    
    # Convert the words back into a single string
    final_result = " ".join(result)
    
    return final_result
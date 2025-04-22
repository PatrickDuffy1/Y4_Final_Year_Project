# Import the TTS (Text-to-Speech) API from Coqui
from TTS.api import TTS
import re
import os

# Maximum allowed line length for audio generation
MAX_LINE_LENGTH = 600


# Main function to generate audio using the specified model type
def generate_audio(text, voice, tts, output_path, model_type):
    
    # Currently, only the 'coqui' model is supported
    if model_type == "coqui":
        return coqui_generate_audio(text, voice, tts, output_path)
        
    # Raise an error for unsupported model types
    raise ValueError(f"Invalid model type: {model_type}")
    
    
# Audio generation specifically for the Coqui TTS model
def coqui_generate_audio(text, voice, tts, output_path):

    # Shorten long sentences if a max line length is set
    if MAX_LINE_LENGTH > 0:
        text = limit_sentence_length(text, MAX_LINE_LENGTH)
        
    # Clean up unwanted or problematic characters in the text
    text = clean_text(text)
        
    if len(text) > 0:
        # Use Coqui TTS to generate audio from text
        tts.tts_to_file(text, speaker_wav=voice, language="en", file_path=output_path)
    
    # Return the path where the audio file was saved
    return output_path


# Function to clean text from special characters and formatting issues
def clean_text(text):
    
    # Replace various special and problematic characters with standard ones
    text = text.replace("—", "-").replace(". . .", "...")
    text = text.replace("”", '"').replace("“", '"').replace("’", "'").replace("''", "'").replace('""', '"')
    text = text.replace("Mr.", "Mr").replace("Mrs.", "Mrs").replace("Dr.", "Dr").replace("Co.", "Co")
    text = text.replace("!.", "!").replace("?.", "?").replace("'.", "'").replace("\".", "\"")
    text = text.replace(" .", "")
    
    # Replace double periods '..' with a single period, unless it's an ellipsis
    text = re.sub(r'(?<!\.)\.\.(?!\.)', '', text)
    
    # Remove characters that aren't alphanumeric or selected punctuation
    text = re.sub(r'[^a-zA-Z0-9\s,.\'"!?()\[\]:;&\n-]', '', text)
    
    # Add periods where a newline starts a new sentence without punctuation
    place_holder = "PLACE_HOLDER_STRING"
    text = re.sub(r'(?<![.,;:])\n(?=[A-Z])', place_holder, text)
    text = re.sub(r'(?<!\.)\n', ' ', text)
    text = re.sub(place_holder, '. ', text)
    
    # Convert quatation marks and periods to new lines to reduce the TTS modules problems with splitting
    text = text.replace(".", "\n")
    text = text.replace('"', "\n")
    
    return text


# Function to break down text lines exceeding the maximum length
def limit_sentence_length(text, max_line_length):
    
    # Break text into lines using newlines
    text = text.split("\n")
    
    for i, line in enumerate(text):
        print("\n\nLine:\n", line)
        
        # Limit overly long words in the line
        line = limit_word_size(line)
        
        # If the line exceeds the maximum length, split and recursively process it
        if len(line) > max_line_length:
            line = split_line(line)
            line = limit_sentence_length(line, max_line_length)  # Recursively shorten
        
        # Reformat the lines and clean extra whitespace
        line = line + "\n"
        line = os.linesep.join([s for s in line.splitlines() if s])
        text[i] = line.replace("\n\n", "\n").lstrip(" ").rstrip(" ")
    
    # Remove any empty lines
    filtered_text = [line for line in text if line]
    
    # Reconstruct the processed lines into a single string
    return '\n'.join(filtered_text) + '\n' if filtered_text else ''


# Function to split a line near the middle (by period if possible, space if not)
def split_line(line):
    
    # Determine halfway point of the line
    half_index = round(len(line) / 2)
    
    # Create two parts around the midpoint
    first_half_string = line[:half_index]
    second_half_string = line[half_index:]
    
    # Look for the nearest full stop and space in each half
    first_full_stop_index = first_half_string.rfind(".")
    second_full_stop_index = second_half_string.find(".")
    first_space_index = first_half_string.rfind(" ")
    second_space_index = second_half_string.find(" ")
    
    # Choose the best splitting point based on proximity to midpoint
    if first_full_stop_index >= 0 and second_full_stop_index >= 0:
        if (len(first_half_string) - first_full_stop_index) < second_full_stop_index:
            space_index = first_full_stop_index
        else:
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
    
    # Insert a newline at the chosen split point
    line = line[:space_index] + "\n" + line[space_index + 1:]
    
    return line


# Function to split very long words into smaller chunks
def limit_word_size(line):
    
    # Break line into individual words
    line = line.split()
    result = []
    
    # Define maximum word length
    max_word_size = 19
    
    # Process each word
    for word in line:
        if len(word) > max_word_size:
            # Break long word into chunks
            chunks = [word[i:i + max_word_size] for i in range(0, len(word), max_word_size)]
            result.append("\n".join(chunks))  # Add line breaks within long word
        else:
            result.append(word)
    
    # Recombine words into a single line
    final_result = " ".join(result)
    
    return final_result

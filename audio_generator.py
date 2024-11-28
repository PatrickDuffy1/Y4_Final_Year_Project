from datetime import datetime
import torch
import re
from TTS.api import TTS

DEFAULT_OUTPUT_FILE_FOLDER = "./outputs"
AUDIO_FILE_EXTENSION = ".wav"
DEFAULT_OUTPUT_FILE_NAME = "output"

def generate_audio(text, file, voice):
    
    # Set the output audio file name to the current timestamp
    output_file_path = DEFAULT_OUTPUT_FILE_FOLDER + "/" + str(datetime.now()).replace(":", "_") + AUDIO_FILE_EXTENSION
    
    # Use cuda if available, otherwise use the cpu
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    print("Using device:", device)
    
    # Load TTS model
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
    
    # Clean the text
    text = clean_text(text)
        
    # Run TTS
    tts.tts_to_file(text, speaker_wav=voice, language="en", file_path=output_file_path)
    
    # Return the path to the created audio file
    return output_file_path
    

# Clean unwanted characters from text
def clean_text(text):
    
    # Replace certain special characters or edge cases with valid characters
    text = text.replace("—", "-").replace(". . .", "...")
    text = text.replace("”", '"').replace("“", '"').replace("’", "'").replace("''", "'").replace('""', '"')
    text = text.replace("Mr.", "Mr").replace("Mrs.", "Mrs").replace("Dr.", "Dr").replace("Co.", "Co")
    text = text.replace("!.", "!").replace("?.", "?").replace("'.", "'").replace("\".", "\"")
    
    # Remove any characters that are not letters or certain special characters
    text = re.sub(r'[^a-zA-Z0-9\s,.\'"!?():;&\n-]', '', text)
    
    # Ensure every line ends with a full stop
    place_holder = "PLACE_HOLDER_STRING"
    text = re.sub(r'(?<![.,;:])\n(?=[A-Z])', place_holder, text)
    text = re.sub(r'(?<!\.)\n', ' ', text)
    text = re.sub(place_holder, '. ', text)
    
    return text
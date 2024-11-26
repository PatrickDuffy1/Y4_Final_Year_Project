from datetime import datetime
import torch
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
        
    # Run TTS
    tts.tts_to_file(text, speaker_wav=voice, language="en", file_path=output_file_path)
    
    # Return the path to the created audio file
    return output_file_path
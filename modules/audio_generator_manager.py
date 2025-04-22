import os
import json
import shutil
from datetime import datetime
from file_reader import read_file
from tts_model_loader import load_tts_model
from tts_audio_generator import generate_audio
from utils import count_files_in_directory
from pathlib import Path
from pydub import AudioSegment

script_dir = Path(__file__).resolve().parent

DEFAULT_OUTPUT_FILE_FOLDER = script_dir / ".." / "single_speaker_outputs"
DEFAULT_AUDIO_FILE_EXTENSION = ".wav"


def tts_generate_audio(user_input, voice, output_folder, ouput_file_type=DEFAULT_AUDIO_FILE_EXTENSION, tts_model_type="coqui"):
    
    if output_folder is not None and isinstance(user_input, list) == False:
        # Read the given file
        text = read_file(user_input)
    else:
        text = user_input
    
    # Load the tts model
    tts = load_tts_model(tts_model_type)
    
    # Check if there are multiple sections/chapters
    if isinstance(text, list) == False:
    
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S_%f")
        output_file_path = DEFAULT_OUTPUT_FILE_FOLDER / f"{timestamp}{ouput_file_type}"
        
        return generate_audio(text, voice, tts, output_file_path, tts_model_type)
    
    chapter_paths = []
    
    using_existing_folder = False
    
    if output_folder != "":
        output_folder_path = output_folder
        using_existing_folder = True
    else:
        # Set the output audio folder name to the current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S_%f")
        output_folder_path = DEFAULT_OUTPUT_FILE_FOLDER / timestamp
    
    
    # Create output folder if it does not exist
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)
        using_existing_folder = False
        
    start_index = 0
        
    if using_existing_folder:
        start_index = len(os.listdir(output_folder_path))
        print("Some sections already complete\nContinuing from section", start_index)
        print("Folder: ", output_folder_path)
        print("LENGTH: ", len(os.listdir(output_folder_path)), "\n\n\n\n")
        #raise Exception()
    
    # Call the generate_audio function for every section/chapter in the text
    for i in range(start_index, len(text)):
        output_file_path = output_folder_path + str(i) + ouput_file_type
        chapter_paths.append(generate_audio(text[i].encode('ascii', 'ignore').decode(), voice[i], tts, output_file_path, tts_model_type))
    
    # Return the audio file path of the first section of the text
    return chapter_paths
    

def tts_generate_multi_speaker_audio(folder_path):
        
    folder_path = folder_path.replace("\\", "/")
    number_of_chapters = count_files_in_directory(folder_path + "/chapter_lines")
    
    for i in range(0, number_of_chapters):
        
        lines, voices = extract_lines_and_voices(folder_path + "/chapter_lines/chapter_" + str(i) + "_lines.json", folder_path + "/merged_book_characters.json")
        
        temp_files_path = folder_path + "/temp_audio_" + str(i)
        os.makedirs(temp_files_path, exist_ok=True)
        tts_generate_audio(lines, voices, temp_files_path + "/")
        stitch_wav_files(folder_path + "/temp_audio_" + str(i), i)
        
    return "Audio generation complete"


def extract_lines_and_voices(line_file, voice_file):
    with open(line_file, 'r') as f1, open(voice_file, 'r') as f2:
        line_data = json.load(f1)
        voice_data = json.load(f2)

    lines = []
    voices = []

    # Create a speaker-to-voice mapping from the second file
    speaker_to_voice = {entry['speaker'].lower(): entry['voice'] for entry in voice_data}

    # Check if Narrator voice is defined
    narrator_voice = speaker_to_voice.get("narrator")
    if not narrator_voice or narrator_voice.lower() == "unassigned":
        raise Exception("Narrator voice is unassigned or missing. Cannot proceed.")

    # Extract lines and find corresponding voices
    for entry in line_data['lines']:
        line = entry['line']
        speaker = entry['speaker'].lower()
        lines.append(line)

        # Attempt to get voice for speaker
        voice = speaker_to_voice.get(speaker)
        if not voice or voice.lower() == "unassigned":
            print(f"Voice for speaker '{speaker}' is unassigned. Using Narrator voice instead.")
            voice = narrator_voice

        voices.append(voice)

    return lines, voices
    

def stitch_wav_files(folder_path, index, delete_originals=True):
    # Get a list of .wav files and sort them numerically based on the number in the filename
    audio_files = sorted(
        [f for f in os.listdir(folder_path) if f.endswith('.wav')],
        key=lambda x: int(os.path.splitext(x)[0])
    )

    combined_audio = AudioSegment.empty()

    # Stitch the audio files in the correct order
    for file_name in audio_files:
        file_path = os.path.join(folder_path, file_name)
        audio = AudioSegment.from_wav(file_path)
        combined_audio += audio

    # Ensure final_outputs directory exists
    output_dir = os.path.join(folder_path, "..", "final_outputs")
    os.makedirs(output_dir, exist_ok=True)

    # Save stitched audio as index.wav
    output_path = os.path.join(output_dir, f"{index}.wav")
    combined_audio.export(output_path, format="wav")

    print(f"Audio files stitched successfully! Saved as: {output_path}")

    # Delete original files and folder if requested
    if delete_originals:
        try:
            shutil.rmtree(folder_path)
            print(f"Deleted temp folder and original audio files: {folder_path}")
        except Exception as e:
            print(f"Error deleting folder: {e}")

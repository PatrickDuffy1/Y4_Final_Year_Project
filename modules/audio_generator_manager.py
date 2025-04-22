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

# Define the directory where output audio files will be stored
script_dir = Path(__file__).resolve().parent
DEFAULT_OUTPUT_FILE_FOLDER = script_dir / ".." / "single_speaker_outputs"
DEFAULT_AUDIO_FILE_EXTENSION = ".wav"


# Generate audio using a TTS model for either a single block of text or multiple sections/chapters
def tts_generate_audio(user_input, voice, output_folder, output_file_type=DEFAULT_AUDIO_FILE_EXTENSION, tts_model_type="coqui"):
    
    # If a file path is passed instead of a list of text sections, read the file content
    if output_folder is not None and isinstance(user_input, list) == False:
        text = read_file(user_input)
    else:
        text = user_input
    
    # Load the specified TTS model
    tts = load_tts_model(tts_model_type)
    
    # If the input is not a file, use the current timestamp as a name
    if isinstance(text, list) == False:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S_%f")
        output_file_path = DEFAULT_OUTPUT_FILE_FOLDER / f"{timestamp}{output_file_type}"
        return generate_audio(text, voice, tts, output_file_path, tts_model_type)
    
    chapter_paths = []  # Stores paths to generated chapter audio files
    using_existing_folder = False

    # Set the output folder path
    if output_folder != "":
        output_folder_path = output_folder
        using_existing_folder = True
    else:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S_%f")
        output_folder_path = DEFAULT_OUTPUT_FILE_FOLDER / timestamp
    
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)
        using_existing_folder = False
        
    start_index = 0
    
    # If folder already has audio files, continue from where it left off
    if using_existing_folder:
        start_index = len(os.listdir(output_folder_path))
        print("Some sections already complete\nContinuing from section", start_index)
        print("Folder: ", output_folder_path)
        print("LENGTH: ", len(os.listdir(output_folder_path)), "\n\n\n\n")

    # Generate audio for each section of text
    for i in range(start_index, len(text)):
        output_file_path = Path(output_folder_path) / f"{i}{output_file_type}"
        # Clean non-ASCII characters before generating audio
        cleaned_text = text[i].encode('ascii', 'ignore').decode()
        chapter_paths.append(generate_audio(cleaned_text, voice[i], tts, output_file_path, tts_model_type))
    
    return chapter_paths  # Return paths of all generated audio chapters


# Generate audio for a multi-speaker audiobook using character voice and line data
def tts_generate_multi_speaker_audio(folder_path):
    folder_path = folder_path.replace("\\", "/")
    number_of_chapters = count_files_in_directory(folder_path + "/chapter_lines")
    
    # Iterate through each chapter and generate audio
    for i in range(0, number_of_chapters):
        lines, voices = extract_lines_and_voices(
            folder_path + "/chapter_lines/chapter_" + str(i) + "_lines.json",
            folder_path + "/merged_book_characters.json"
        )
        
        temp_files_path = folder_path + "/temp_audio_" + str(i)
        os.makedirs(temp_files_path, exist_ok=True)
        
        # Generate audio for each chapter and then stitch the files together
        tts_generate_audio(lines, voices, temp_files_path + "/")
        stitch_wav_files(folder_path + "/temp_audio_" + str(i), i)
        
    return "Audio generation complete"


# Extract dialogue lines and assign the appropriate voice for each speaker
def extract_lines_and_voices(line_file, voice_file):
    with open(line_file, 'r') as f1, open(voice_file, 'r') as f2:
        line_data = json.load(f1)
        voice_data = json.load(f2)

    lines = []
    voices = []

    # Build a mapping of speaker names to voice models
    speaker_to_voice = {entry['speaker'].lower(): entry['voice'] for entry in voice_data}

    # Validate that Narrator voice is present
    narrator_voice = speaker_to_voice.get("narrator")
    if not narrator_voice or narrator_voice.lower() == "unassigned":
        raise Exception("Narrator voice is unassigned or missing. Cannot proceed.")

    # Assign voices to each line of dialogue
    for entry in line_data['lines']:
        line = entry['line']
        speaker = entry['speaker'].lower()
        lines.append(line)

        voice = speaker_to_voice.get(speaker)
        if not voice or voice.lower() == "unassigned":
            print(f"Voice for speaker '{speaker}' is unassigned. Using Narrator voice instead.")
            voice = narrator_voice

        voices.append(voice)

    return lines, voices


# Combine multiple .wav files into one and optionally delete the original temp files
def stitch_wav_files(folder_path, index, delete_originals=True):
    # Get list of .wav files sorted by their numeric filename (0.wav, 1.wav, etc.)
    audio_files = sorted(
        [f for f in os.listdir(folder_path) if f.endswith('.wav')],
        key=lambda x: int(os.path.splitext(x)[0])
    )

    combined_audio = AudioSegment.empty()

    # Merge audio files in order
    for file_name in audio_files:
        file_path = os.path.join(folder_path, file_name)
        audio = AudioSegment.from_wav(file_path)
        combined_audio += audio

    # Create output folder if not already present
    output_dir = os.path.join(folder_path, "..", "final_outputs")
    os.makedirs(output_dir, exist_ok=True)

    # Export the combined audio as a single .wav file
    output_path = os.path.join(output_dir, f"{index}.wav")
    combined_audio.export(output_path, format="wav")

    print(f"Audio files stitched successfully! Saved as: {output_path}")

    # Optionally remove temporary folder and files
    if delete_originals:
        try:
            shutil.rmtree(folder_path)
            print(f"Deleted temp folder and original audio files: {folder_path}")
        except Exception as e:
            print(f"Error deleting folder: {e}")

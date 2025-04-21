import json
import os
import glob
from pydub import AudioSegment
from text_generator import generate_json_text
from llm_model_loader import load_llm_model
from file_reader import read_file
from llm_line_identifier import identify_lines_in_chapter
    
    
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
    
    
def extract_lines_and_voices(file1, file2):

    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        data1 = json.load(f1)
        data2 = json.load(f2)

    lines = []
    voices = []

    # Create a speaker-to-voice mapping from the second file
    speaker_to_voice = {entry['speaker'].lower(): entry['voice'] for entry in data2}

    # Extract lines and find corresponding voices
    for entry in data1['lines']:
        line = entry['line']
        speaker = entry['speaker'].lower()

        lines.append(line)

        # Find the corresponding voice or use "unassigned" if not found
        voice = speaker_to_voice.get(speaker, "unassigned")
        voices.append(voice)

    return lines, voices
    

def stitch_wav_files(folder_path, index):
    # Get a list of .wav files and sort them numerically based on the number in the filename
    audio_files = sorted([f for f in os.listdir(folder_path) if f.endswith('.wav')], key=lambda x: int(os.path.splitext(x)[0]))

    combined_audio = AudioSegment.empty()

    # Stitch the audio files in the correct order
    for file_name in audio_files:
        file_path = os.path.join(folder_path, file_name)
        audio = AudioSegment.from_wav(file_path)
        combined_audio += audio

    # Export the combined audio as WAV
    output_path = os.path.join(folder_path, "..", "chapter_" + str(index) + "_combined_audio.wav")
    combined_audio.export(output_path, format="wav")

    print(f"Audio files for chapter", str(index), "have been stitched together successfully! Saved as: ", output_path)
    
    
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

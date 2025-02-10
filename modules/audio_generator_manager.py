from datetime import datetime
import os
from file_reader import read_file
from tts_model_loader import load_tts_model
from tts_audio_generator import generate_audio

DEFAULT_OUTPUT_FILE_FOLDER = "../outputs"
DEFAULT_AUDIO_FILE_EXTENSION = ".wav"
    
 
def generate_audio_from_text(text, voice, ouput_file_type=DEFAULT_AUDIO_FILE_EXTENSION, tts_model_type = "coqui"):
    
    # Load the tts model
    tts = load_tts_model(tts_model_type)

    # Set the output audio file name to the current timestamp
    output_file_path = DEFAULT_OUTPUT_FILE_FOLDER + "/" + str(datetime.now()).replace(":", "_").replace(".", "_").replace(" ", "_") + ouput_file_type
    
    return generate_audio(text, voice, tts, output_file_path, tts_model_type)


def generate_audio_from_file(file_path, voice, output_folder, ouput_file_type=DEFAULT_AUDIO_FILE_EXTENSION, tts_model_type="coqui"):
       
    # Read the given file
    text = read_file(file_path) 
    
    # Load the tts model
    tts = load_tts_model(tts_model_type)
    
    # Check if there are multiple sections/chapters
    if isinstance(text, list) == False:
        return generate_audio_from_text(text, voice, output_file_path)
    
    chapter_paths = []
    
    using_existing_folder = False
    
    if output_folder != "":
        output_folder_path = output_folder
        using_existing_folder = True
    else:
        # Set the output audio folder name to the current timestamp
        output_folder_path = DEFAULT_OUTPUT_FILE_FOLDER + "/" + str(datetime.now()).replace(":", "_").replace(".", "_").replace(" ", "_") + "/"
    
    
    # Create output folder if it does not exist
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)
        using_existing_folder = False
        
    start_index = 0
        
    if using_existing_folder:
        start_index = len(os.listdir(output_folder_path))
        print("Folder: ", output_folder_path)
        print("LENGTH: ", len(os.listdir(output_folder_path)), "\n\n\n\n")
        #raise Exception()
    
    # Call the generate_audio function for every section/chapter in the text
    for i in range(start_index, len(text)):
        output_file_path = output_folder_path + str(i) + ouput_file_type
        chapter_paths.append(generate_audio(text[i], voice, tts, output_file_path, tts_model_type))
    
    # Return the audio file path of the first section of the text
    return chapter_paths[0]
    


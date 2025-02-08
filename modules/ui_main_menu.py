import gradio as gr
from audio_generator import generate_audio_from_text, generate_audio_from_file
from os import getcwd
from utils import get_files_in_directory, get_folders_in_directory

class UiMainPage:
    def __init__(self, session):
        self._session = session
    

    # Generate the audio using the chosen text/file, and the chosen voice
    def gradio_generate_audio(input_text, input_file, voice, output_file_type, existing_ouput_folder, new_output_folder):

        output_folder = ""
        output_file_type = "." + output_file_type
        
        if new_output_folder:
            output_folder = getcwd() + "../outputs/" + new_output_folder + "/"
        elif existing_ouput_folder:
            output_folder = existing_ouput_folder  + "/"
            
        output_folder = output_folder.replace("\\", "/")
            
        print("folder: " + output_folder)
        
        # Use textbox as default. If there is no text in the textbox, use file, If there is neither, print message
        if input_text:
            audio = generate_audio_from_text(input_text, voice, output_file_type)
        elif input_file:
            audio = generate_audio_from_file(input_file.name, voice, output_folder, output_file_type)
        else:
            return "Please provide either text or a file."
        
        return audio
        

    main_menu = gr.Interface(
        fn=gradio_generate_audio,
        inputs=[
            "text", # Input box for text
            "file", # Input box for files
            
            # Dropdown menu for voices
            gr.Dropdown(
                    choices=set(["../voices/voice_1.wav"] + get_files_in_directory("../voices", [".txt"])), # Get all of the available voices
                    label="Voice", 
                    value="../voices/voice_1.wav" # Default voice
                ),
                
            gr.Radio(["mp3", "wav"], label="Output file type", value="wav"), # Radio button for output file type
            
            gr.Dropdown(
                    choices=get_folders_in_directory("../outputs"), # Get all of the available folders
                    label="Outputs"
                ),
            "text",
        ],
        outputs=["audio"], # Output box for audio file
        allow_flagging="never",  # Disables the flagging functionality
    )
        
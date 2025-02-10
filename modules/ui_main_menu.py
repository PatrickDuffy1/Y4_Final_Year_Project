import gradio as gr
from os import getcwd
from utils import get_files_in_directory, get_folders_in_directory

class UiMainPage:
    def __init__(self, session):
        self._session = session
        self.main_menu = self.get_gradio_page()
    

    # Generate the audio using the chosen text/file, and the chosen voice
    def gradio_generate_audio(self, input_text, input_file, voice, output_file_type, existing_ouput_folder, new_output_folder):

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
            user_input = input_text
            output_folder = None
        elif input_file:
            user_input = input_file.name
        else:
            return "Please provide either text or a file."
        
        return self._session.generate_audio(user_input, voice, output_folder, output_file_type)
        
    
    def get_gradio_page(self):
    
        return gr.Interface(
            fn=self.gradio_generate_audio,
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
        
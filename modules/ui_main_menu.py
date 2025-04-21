import gradio as gr
import os
from utils import get_files_in_directory, get_folders_in_directory
from pathlib import Path

script_dir = Path(__file__).resolve().parent
voices_path = script_dir / ".." / "voices"
outputs_path = script_dir / ".." / "single_speaker_outputs"

class UiMainPage:
    def __init__(self, session):
        self._session = session
        self.main_menu = self.get_gradio_page()
    

    # Generate the audio using the chosen text/file, and the chosen voice
    def gradio_generate_audio(self, input_text, input_file, voice, existing_ouput_folder, new_output_folder):

        output_folder = ""
        
        if new_output_folder:
            output_folder = os.path.abspath(
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "single_speaker_outputs", new_output_folder)
            )

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
        
        return self._session.generate_audio(user_input, voice, output_folder)
        
    
    def get_gradio_page(self):
    
        return gr.Interface(
            fn=self.gradio_generate_audio,
            inputs=[
                "text", # Input box for text
                "file", # Input box for files
                
                # Dropdown menu for voices
                gr.Dropdown(
                        choices=set(get_files_in_directory(str(voices_path), [".txt"])), # Get all of the available voices
                        label="Voice"
                    ),
                gr.Dropdown(
                        choices=get_folders_in_directory(str(outputs_path)), # Get all of the available folders
                        label="Outputs"
                    ),
                "text",
            ],
            outputs=["audio"], # Output box for audio file
            allow_flagging="never",  # Disables the flagging functionality
        )
        
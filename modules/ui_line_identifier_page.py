import gradio as gr
import os
from pathlib import Path
from utils import get_files_in_directory, get_folders_in_directory

script_dir = Path(__file__).resolve().parent
outputs_path = script_dir / ".." / "multi_speaker_outputs"

class UiLineIdentifierPage:
    def __init__(self, session):
        self._session = session
        self.line_identifier_page = self.get_gradio_page()

    def indentify_character_lines(self, input_text, input_file, start_section, end_section, existing_ouput_folder, new_book_folder_path):
        
        book_folder_path = ""
        
        if new_book_folder_path:
            book_folder_path = os.path.abspath(
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "multi_speaker_outputs", new_book_folder_path)
            )

        elif existing_ouput_folder:
            book_folder_path = existing_ouput_folder  + "/"
            
        book_folder_path = book_folder_path.replace("\\", "/")
            
        print("folder: " + book_folder_path)
    
        if input_text:
            user_input = input_text
            is_file = False
        elif input_file:
            user_input = input_file.name
            is_file = True
        else:
            return "Please provide either text or a file."
            
        print(user_input)
            
        return self._session.indentify_character_lines(user_input, is_file, book_folder_path, int(start_section), int(end_section))

    
    def get_gradio_page(self):
    
        return gr.Interface(
            fn=self.indentify_character_lines,
            inputs=[
                "text",
                "file",
                gr.Textbox("0"),
                gr.Textbox("-1"),
                gr.Dropdown(
                        choices=get_folders_in_directory(str(outputs_path)), # Get all of the available folders
                        label="Outputs"
                    ),
                "text",
            ],
            outputs=["text"], # Output box for audio file
            allow_flagging="never",  # Disables the flagging functionality
        )
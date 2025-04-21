import gradio as gr
from pathlib import Path
from utils import get_files_in_directory, get_folders_in_directory

script_dir = Path(__file__).resolve().parent
outputs_path = script_dir / ".." / "multi_speaker_outputs"

class UiMultiSpeakerPage:
    def __init__(self, session):
        self._session = session
        self.multi_speaker_page = self.get_gradio_page()

    def generate_multi_speaker_audio(self, existing_ouput_folder, new_book_folder_path):
        
        book_folder_path = ""
        
        if new_book_folder_path:
            book_folder_path = os.path.abspath(
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "multi_speaker_outputs", new_book_folder_path)
            )

        elif existing_ouput_folder:
            book_folder_path = existing_ouput_folder  + "/"
            
        book_folder_path = book_folder_path.replace("\\", "/")
            
        print("folder: " + book_folder_path)
            
        return self._session.generate_multi_speaker_audio(book_folder_path)

    
    def get_gradio_page(self):
    
        return gr.Interface(
            fn=self.generate_multi_speaker_audio,
            inputs=[
                gr.Dropdown(
                        choices=get_folders_in_directory(str(outputs_path)), # Get all of the available folders
                        label="Outputs"
                    ),
                "text",
            ],
            outputs=["audio"], # Output box for audio file
            allow_flagging="never",  # Disables the flagging functionality
        )
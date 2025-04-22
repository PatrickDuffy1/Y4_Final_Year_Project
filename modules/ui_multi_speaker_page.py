import gradio as gr
from pathlib import Path
from utils import get_folders_in_directory

script_dir = Path(__file__).resolve().parent
outputs_path = script_dir.parent / "multi_speaker_outputs"

class UiMultiSpeakerPage:
    def __init__(self, session):
        self._session = session
        self.multi_speaker_page = self.get_gradio_page()

    def generate_multi_speaker_audio(self, folder_choice_type, existing_output_folder, absolute_folder_path):
        if folder_choice_type == "From Project Outputs":
            if not existing_output_folder:
                return "Please select a folder from the outputs list.", None
            book_folder_path = Path(existing_output_folder)
        elif folder_choice_type == "Use Absolute Path":
            if not absolute_folder_path.strip():
                return "Please enter a valid absolute folder path.", None
            book_folder_path = Path(absolute_folder_path)
        else:
            return "Invalid folder selection type.", None

        if not book_folder_path.exists():
            return f"Folder does not exist: {book_folder_path}", None

        print(f"Generating audio from: {book_folder_path}")
        audio_path = self._session.generate_multi_speaker_audio(str(book_folder_path))

        return f"Multi-speaker audio generated from: {book_folder_path}", audio_path

    def refresh_folder_choices(self):
        updated_folders = get_folders_in_directory(str(outputs_path))
        return gr.update(choices=updated_folders)

    def get_gradio_page(self):
        with gr.Blocks() as demo:
            gr.Markdown("## Multi-Speaker Audio Generator")

            folder_source = gr.Radio(
                choices=["From Project Outputs", "Use Absolute Path"],
                value="From Project Outputs",
                label="Select Folder Source"
            )

            existing_folder = gr.Dropdown(
                choices=get_folders_in_directory(str(outputs_path)),
                label="Choose from Output Folders",
                visible=True
            )

            absolute_path = gr.Textbox(
                label="Absolute Path to Folder",
                placeholder="C:/Users/YourName/Documents/Project/folder_name",
                visible=False
            )

            # Auto-refresh button
            refresh_button = gr.Button("🔄 Refresh Folder List")

            # Show/hide dropdown or text input based on radio choice
            folder_source.change(
                lambda choice: (
                    gr.update(visible=choice == "From Project Outputs"),
                    gr.update(visible=choice == "Use Absolute Path")
                ),
                inputs=folder_source,
                outputs=[existing_folder, absolute_path]
            )

            # Refresh the dropdown list when button clicked
            refresh_button.click(
                self.refresh_folder_choices,
                outputs=[existing_folder]
            )

            generate_button = gr.Button("Generate Multi-Speaker Audio")
            status_text = gr.Textbox(label="Status")

            generate_button.click(
                self.generate_multi_speaker_audio,
                inputs=[folder_source, existing_folder, absolute_path],
                outputs=[status_text]
            )

        return demo

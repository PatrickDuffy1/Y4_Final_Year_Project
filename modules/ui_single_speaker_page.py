import gradio as gr
from pathlib import Path
from utils import get_files_in_directory, get_folders_in_directory

script_dir = Path(__file__).resolve().parent
voices_path = script_dir.parent / "voices"
outputs_path = script_dir.parent / "single_speaker_outputs"

class UiSingleSpeakerPage:
    def __init__(self, session):
        self._session = session
        self.single_speaker_page = self.get_gradio_page()

    def gradio_generate_audio(self, input_text, input_file, voice, existing_output_folder, new_output_folder):
        output_folder = None
        if new_output_folder:
            output_folder = outputs_path / new_output_folder
        elif existing_output_folder:
            output_folder = Path(existing_output_folder)

        if output_folder is not None:
            output_folder.mkdir(parents=True, exist_ok=True)

        if input_text:
            user_input = input_text
            output_folder = None
        elif input_file:
            user_input = input_file.name
        else:
            return "Please provide either text or a file.", None

        audio_path = self._session.generate_audio(user_input, voice, str(output_folder) if output_folder else None)
        
        if output_folder:
            status_msg = f"Audio saved in folder: {output_folder}"
        else:
            status_msg = "Audio generated from text input (no folder used)."
        return status_msg, audio_path



    def get_gradio_page(self):
        voice_choices = get_files_in_directory(str(voices_path), [".txt"])
        output_folders = get_folders_in_directory(str(outputs_path))

        with gr.Blocks() as demo:
            gr.Markdown("## Single Speaker Audio Generator")

            # Input Method Selection
            input_choice = gr.Radio(
                choices=["Text Input", "File Upload"],
                value="Text Input",
                label="Choose Input Type"
            )
            input_text = gr.Textbox(label="Text Input", lines=4, visible=True)
            input_file = gr.File(label="Upload File", visible=False)

            def toggle_input(choice):
                return (
                    gr.update(visible=choice == "Text Input"),
                    gr.update(visible=choice == "File Upload")
                )
            input_choice.change(toggle_input, inputs=input_choice, outputs=[input_text, input_file])

            # Voice Selection
            voice = gr.Dropdown(choices=voice_choices, label="Select Voice")

            # Output Folder Selection
            folder_choice = gr.Radio(
                choices=["Existing Folder", "New Folder"],
                value="Existing Folder",
                label="Choose Output Folder Type"
            )
            existing_output = gr.Dropdown(
                choices=output_folders,
                label="Select Existing Output Folder",
                visible=True
            )
            new_output = gr.Textbox(
                label="Name for New Output Folder",
                placeholder="e.g. my_custom_folder",
                visible=False
            )

            def toggle_folder(choice):
                return (
                    gr.update(visible=choice == "Existing Folder"),
                    gr.update(visible=choice == "New Folder")
                )
            folder_choice.change(toggle_folder, inputs=folder_choice, outputs=[existing_output, new_output])

            # Generate Button
            generate_button = gr.Button("Generate Audio")
            status = gr.Textbox(label="Status")
            output_audio = gr.Audio(label="Generated Audio")

            generate_button.click(
                self.gradio_generate_audio,
                inputs=[input_text, input_file, voice, existing_output, new_output],
                outputs=[status, output_audio]
            )

        return demo

import gradio as gr
from pathlib import Path
from utils import get_files_in_directory, get_folders_in_directory

# Paths to voice options and single-speaker outputs
script_dir = Path(__file__).resolve().parent
voices_path = script_dir.parent / "voices"
outputs_path = script_dir.parent / "single_speaker_outputs"

class UiSingleSpeakerPage:
    def __init__(self, session):
        self._session = session
        self.single_speaker_page = self.get_gradio_page()  # Initialize UI

    def gradio_generate_audio(self, input_text, input_file, voice, new_output_folder, existing_output_folder):
        output_folder = None

        # Make sure a voice is selected
        if not voice:
            return "Please select a voice.", None

        # Determine output folder (existing or new)
        if new_output_folder:
            output_folder = outputs_path / new_output_folder
        elif existing_output_folder:
            output_folder = Path(existing_output_folder)

        if output_folder is not None:
            output_folder.mkdir(parents=True, exist_ok=True)

        # Decide input source (text or file)
        if input_text:
            user_input = input_text
            output_folder = None  # Do not use folder if just using text input
            is_file = False
        elif input_file:
            user_input = input_file.name
            is_file = True
        else:
            return "Please provide either text or a file.", None

        # Generate audio via session
        audio_path = self._session.generate_audio(user_input, voice, is_file, str(output_folder) if output_folder else None)

        # Return result status
        if output_folder:
            status_msg = f"Audio saved in folder: {output_folder}"
        else:
            status_msg = "Audio generated from text input (no folder used)."
        return status_msg, audio_path

    def refresh_folder_choices(self):
        updated_folders = get_folders_in_directory(str(outputs_path))
        return gr.update(choices=updated_folders)

    def refresh_voice_choices(self):
        updated_voices = get_files_in_directory(str(voices_path), [".txt"])
        return gr.update(choices=updated_voices)

    def get_gradio_page(self):
        voice_choices = get_files_in_directory(str(voices_path), [".txt"])
        output_folders = get_folders_in_directory(str(outputs_path))

        with gr.Blocks() as demo:
            gr.Markdown("## Single Speaker Audio Generator")

            # Input method selection
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

            # Choose voice file
            voice = gr.Dropdown(choices=voice_choices, label="Select Voice")
            refresh_voices_button = gr.Button("🔄 Refresh Voices List")

            # Output folder handling
            folder_choice = gr.Radio(
                choices=["New Folder", "Existing Folder"],
                value="New Folder",
                label="Choose Output Folder Type"
            )

            new_output = gr.Textbox(
                label="Name for New Output Folder",
                placeholder="e.g. my_custom_folder",
                visible=False
            )

            existing_output = gr.Dropdown(
                choices=output_folders,
                label="Select Existing Output Folder",
                visible=True
            )
            refresh_folders_button = gr.Button("🔄 Refresh Folder List")

            def toggle_folder(choice):
                return (
                    gr.update(visible=choice == "Existing Folder"),
                    gr.update(visible=choice == "New Folder")
                )
            folder_choice.change(toggle_folder, inputs=folder_choice, outputs=[existing_output, new_output])

            # Hook refresh buttons
            refresh_voices_button.click(
                self.refresh_voice_choices,
                outputs=[voice]
            )

            refresh_folders_button.click(
                self.refresh_folder_choices,
                outputs=[existing_output]
            )

            # Output components
            generate_button = gr.Button("Generate Audio")
            status = gr.Textbox(label="Status")
            output_audio = gr.Audio(label="Generated Audio")

            generate_button.click(
                self.gradio_generate_audio,
                inputs=[input_text, input_file, voice, new_output, existing_output],
                outputs=[status, output_audio]
            )

        return demo

import gradio as gr
from pathlib import Path
from utils import get_folders_in_directory

# Location of multi-speaker outputs
script_dir = Path(__file__).resolve().parent
outputs_path = script_dir.parent / "multi_speaker_outputs"

class UiLineIdentifierPage:
    def __init__(self, session):
        self._session = session
        self.line_identifier_page = self.get_gradio_page()

    def indentify_character_lines(
        self, input_type, input_text, input_file,
        start_section, end_section,
        output_type, new_book_folder_path, existing_output_folder,
        max_retries
    ):
        # Handle user input source
        if input_type == "Text":
            if not input_text.strip():
                return "Please enter some text."
            user_input = input_text
            is_file = False
            start = end = None
        elif input_type == "File":
            if not input_file:
                return "Please upload a file."
            user_input = input_file.name
            is_file = True
            try:
                start = int(start_section)
                end = int(end_section)
            except ValueError:
                return "Start and End Section must be integers."
        else:
            return "Invalid input type selected."

        # Determine output folder
        if output_type == "New":
            if new_book_folder_path != "":
                book_folder_path = outputs_path / new_book_folder_path
            else:
                book_folder_path = ""
        elif output_type == "Existing":
            if not existing_output_folder:
                return "Please select an existing output folder."
            book_folder_path = Path(existing_output_folder)
        else:
            return "Invalid output folder selection."

        if book_folder_path != "":
            book_folder_path.mkdir(parents=True, exist_ok=True)

        # Parse max retries
        try:
            retries = int(max_retries)
        except ValueError:
            return "Max retries must be an integer."

        # Call session to process lines
        result = self._session.indentify_character_lines(
            user_input, is_file,
            str(book_folder_path),
            start if is_file else 0,
            end if is_file else -1,
            retries
        )

        return f"Lines identified and saved in: {book_folder_path or 'timestamped folder (auto-named)'}\n\n{result}"

    def refresh_folder_choices(self):
        updated_folders = get_folders_in_directory(str(outputs_path))
        return gr.update(choices=updated_folders)

    def get_gradio_page(self):
        folders = get_folders_in_directory(str(outputs_path))

        with gr.Blocks() as demo:
            gr.Markdown("## Multi-Speaker Line Identifier")

            # Input method
            input_type = gr.Radio(["Text", "File"], value="Text", label="Select Input Type")
            input_text = gr.Textbox(label="Text Input", lines=4, visible=True)
            input_file = gr.File(label="Upload File", visible=False)
            start_section = gr.Textbox(value="0", label="Start Section", visible=False)
            end_section = gr.Textbox(value="-1", label="End Section (-1 for all)", visible=False)

            output_type = gr.Radio(["New"], value="New", label="Select Output Folder Type")
            new_output = gr.Textbox(label="New Output Folder Name", placeholder="Leave blank to auto-name using timestamp", visible=True)
            existing_output = gr.Dropdown(choices=folders, label="Choose Existing Output Folder", visible=False)

            # Refresh button for folder list
            refresh_button = gr.Button("🔄 Refresh Folder List", visible=False)

            def on_input_type_change(choice):
                is_file = choice == "File"
                return (
                    gr.update(visible=choice == "Text"),
                    gr.update(visible=choice == "File"),
                    gr.update(visible=choice == "File"),
                    gr.update(visible=choice == "File"),
                    gr.update(choices=["New", "Existing"] if is_file else ["New"], value="New"),
                    gr.update(visible=is_file)  # Toggle refresh button
                )

            input_type.change(
                on_input_type_change,
                inputs=input_type,
                outputs=[input_text, input_file, start_section, end_section, output_type, refresh_button]
            )

            output_type.change(
                lambda choice: (
                    gr.update(visible=choice == "New"),
                    gr.update(visible=choice == "Existing")
                ),
                inputs=output_type,
                outputs=[new_output, existing_output]
            )

            # Hook up refresh button
            refresh_button.click(
                self.refresh_folder_choices,
                outputs=[existing_output]
            )

            max_retries = gr.Textbox(
                value="5",
                label="Max Retries If No Narrator",
                info="Number of times to retry if there is no narrator in the output. May not want to be too high, as while no narrator in the output is usually a mistake, this is not always the case. Small chunk sizes have a higher chance of having no narrator and without it being a mistake"
            )

            run_button = gr.Button("Identify Character Lines")
            result_text = gr.Textbox(label="Status")

            run_button.click(
                self.indentify_character_lines,
                inputs=[
                    input_type, input_text, input_file,
                    start_section, end_section,
                    output_type, new_output, existing_output,
                    max_retries
                ],
                outputs=[result_text]
            )

        return demo

import gradio as gr
from pathlib import Path
from utils import get_files_in_directory
from llm_model_loader import Model_Type

# Define the path to the models folder
script_dir = Path(__file__).resolve().parent
models_path = script_dir.parent / "models"

class UiModelPage:
    def __init__(self, session):
        self._session = session
        self.model_page = self.get_gradio_page()  # Initialize the Gradio UI

    def load_model(self, model_source, model_dropdown, model_path_str, repo_id, context_length, gpu_layers, temperature, seed):
        # Determine model path and type based on selected input method
        model_path = None
        model_type = None

        if model_source == "Choose from models folder":
            if not model_dropdown or model_dropdown == "--- Select a model ---":
                return "Error: Please select a model from the dropdown.",
            model_path = model_dropdown
            model_type = Model_Type.LOCAL_FILE
            repo_id = None

        elif model_source == "Enter local model path":
            if not model_path_str.strip():
                return "Error: Local model path is required.",
            model_path = model_path_str.strip()
            model_type = Model_Type.LOCAL_FILE
            repo_id = None

        elif model_source == "Use HuggingFace repo":
            if not model_path_str.strip():
                return "Error: Model path for HuggingFace is required.",
            if not repo_id.strip():
                return "Error: HuggingFace repo ID is required.",
            model_path = model_path_str.strip()
            model_type = Model_Type.HUGGING_FACE
            repo_id = repo_id.strip()

        # Convert seed to integer, default to -1 if invalid
        try:
            seed = int(seed)
        except ValueError:
            seed = -1

        # Load model using session handler
        llm = self._session.set_and_load_llm(
            model_path, model_type, repo_id, context_length, gpu_layers, temperature, seed
        )

        return f"Loaded model: {llm}"

    def get_gradio_page(self):
        # Get list of available model files
        available_models = get_files_in_directory(str(models_path), [".txt"])
        available_models.insert(0, "--- Select a model ---")

        with gr.Blocks() as demo:
            gr.Markdown("## Load Language Model")

            # Model source radio buttons
            model_source = gr.Radio(
                choices=["Choose from models folder", "Enter local model path", "Use HuggingFace repo"],
                value="Choose from models folder",
                label="Select model source"
            )

            # Inputs for different source types
            model_dropdown = gr.Dropdown(choices=available_models, label="Select model file", visible=True)
            model_path_str = gr.Textbox(label="Model path (local or HuggingFace)", visible=False)
            repo_id = gr.Textbox(label="HuggingFace Repo ID (required for HF models)", visible=False)

            # Dynamically show/hide inputs based on source type
            def toggle_model_fields(choice):
                return (
                    gr.update(visible=choice == "Choose from models folder"),
                    gr.update(visible=choice in ["Enter local model path", "Use HuggingFace repo"]),
                    gr.update(visible=choice == "Use HuggingFace repo")
                )

            model_source.change(toggle_model_fields, inputs=model_source, outputs=[model_dropdown, model_path_str, repo_id])

            # Model settings
            context_length = gr.Slider(0, 131072, value=4096, step=1, label="Context size")
            gpu_layers = gr.Slider(0, 100, value=0, label="GPU layers to offload")
            temperature = gr.Slider(0, 2, value=0.7, label="Temperature")
            seed = gr.Textbox(value="-1", label="Seed")

            # Button and output
            load_button = gr.Button("Load Model")
            result = gr.Textbox(label="Status")

            # Load model when button clicked
            load_button.click(
                self.load_model,
                inputs=[model_source, model_dropdown, model_path_str, repo_id, context_length, gpu_layers, temperature, seed],
                outputs=[result]
            )

        return demo

import gradio as gr
from pathlib import Path
from utils import get_files_in_directory
from llm_model_loader import Model_Type

script_dir = Path(__file__).resolve().parent
models_path = script_dir.parent / "models"

class UiModelPage:
    def __init__(self, session):
        self._session = session
        self.model_page = self.get_gradio_page()

    def load_model(self, model_source, model_dropdown, model_path_str, repo_id, context_length, gpu_layers, temperature, seed):
        model_path = None
        model_type = None

        if model_source == "Choose from models folder":
            model_path = model_dropdown
            model_type = Model_Type.LOCAL_FILE
            repo_id = None
        elif model_source == "Enter local model path":
            model_path = model_path_str
            model_type = Model_Type.LOCAL_FILE
            repo_id = None
        elif model_source == "Use HuggingFace repo":
            model_path = model_path_str
            model_type = Model_Type.HUGGING_FACE
            if not repo_id:
                return "Error: HuggingFace repo ID is required.",

        # Handle empty seed safely
        try:
            seed = int(seed)
        except ValueError:
            seed = -1

        llm = self._session.set_and_load_llm(
            model_path, model_type, repo_id, context_length, gpu_layers, temperature, seed
        )

        return f"Loaded model: {llm}"

    def get_gradio_page(self):
        available_models = get_files_in_directory(str(models_path), [".txt"])

        with gr.Blocks() as demo:
            gr.Markdown("## Load Language Model")

            model_source = gr.Radio(
                choices=["Choose from models folder", "Enter local model path", "Use HuggingFace repo"],
                value="Choose from models folder",
                label="Select model source"
            )

            model_dropdown = gr.Dropdown(choices=available_models, label="Select model file", visible=True)
            model_path_str = gr.Textbox(label="Model path (local or HuggingFace)", visible=False)
            repo_id = gr.Textbox(label="HuggingFace Repo ID (required for HF models)", visible=False)

            def toggle_model_fields(choice):
                return (
                    gr.update(visible=choice == "Choose from models folder"),
                    gr.update(visible=choice in ["Enter local model path", "Use HuggingFace repo"]),
                    gr.update(visible=choice == "Use HuggingFace repo")
                )

            model_source.change(toggle_model_fields, inputs=model_source, outputs=[model_dropdown, model_path_str, repo_id])

            # Common model parameters
            context_length = gr.Slider(0, 131072, value=4096, step=1, label="Context size")
            gpu_layers = gr.Slider(0, 100, value=0, label="GPU layers to offload")
            temperature = gr.Slider(0, 2, value=0.7, label="Temperature")
            seed = gr.Textbox(value="-1", label="Seed")

            load_button = gr.Button("Load Model")
            result = gr.Textbox(label="Status")

            load_button.click(
                self.load_model,
                inputs=[model_source, model_dropdown, model_path_str, repo_id, context_length, gpu_layers, temperature, seed],
                outputs=[result]
            )

        return demo

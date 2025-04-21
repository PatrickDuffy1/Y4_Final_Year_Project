import gradio as gr
from text_generator import generate_json_text
from utils import get_files_in_directory
from llm_model_loader import Model_Type

class UiModelPage:
    def __init__(self, session):
        self._session = session
        self.model_page = self.get_gradio_page()
        
    # Load the LLM
    def load_model(self, local_model_path, huggingface_model_path, repo_id, context_length, gpu_layers, temperature, seed):
        
        if huggingface_model_path != "":
            model_path = huggingface_model_path
        else:
            model_path = local_model_path
        
        if repo_id == "":
            repo_id = None
            model_type = Model_Type.LOCAL_FILE
        else:
            model_type = Model_Type.HUGGING_FACE
        
        llm = self._session.set_and_load_llm(model_path, model_type, repo_id, context_length, gpu_layers, temperature, int(seed))
        
        return "Loaded model: " + str(llm)

    
    def get_gradio_page(self):
    
        return gr.Interface(
            fn=self.load_model,
            inputs=[
                
                # Dropdown menu for models
                gr.Dropdown(
                        choices=set(get_files_in_directory("../models", [".txt"])), # Get all of the available models
                        label="Model"
                    ),
                "text", # Text box for model paths
                "text", # Text box for repo ids
                gr.Slider(0, 131072, value=4096, label="Context size", info="Context size of model. Suggested to leave at default"),
                gr.Slider(0, 100, value=0, label="GPU layers to offload", info="Number of GPU layers to offload. Requires a compatible GPU"),
                gr.Slider(0, 2, value=0.7, label="Temperature", info="Temperature of model. Higher values have more randomness"),
                gr.Textbox("-1"), # Text box for seed
            ],
            outputs=["text"], # Output box for audio file
            allow_flagging="never",  # Disables the flagging functionality
        )
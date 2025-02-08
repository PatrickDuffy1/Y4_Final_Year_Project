import gradio as gr
from text_generator import generate_json_text
from utils import get_files_in_directory
from llm import Llm

class UiModelPage:
    def __init__(self, session):
        self._session = session

    llm = None
        
    # Load the LLM
    def load_model(local_model_path, huggingface_model_path, repo_id, context_length, gpu_layers, temperature, seed):

        global llm
        
        if huggingface_model_path != "":
            model_path = huggingface_model_path
        else:
            model_path = local_model_path
        
        if repo_id == "":
            repo_id = None
        
        llm = Llm(model_path, repo_id, context_length, gpu_layers, temperature, int(seed))
        llm.load_model()
        
        return "Loaded model: " + str(llm)


    model_page = gr.Interface(
        fn=load_model,
        inputs=[
            
            # Dropdown menu for models
            gr.Dropdown(
                    choices=set(get_files_in_directory("../models", [".txt"])), # Get all of the available models
                    label="Model"
                ),
            "text", # Text box for model paths
            "text", # Text box for repo ids
            gr.Slider(0, 131072, value=16384, label="Context size", info="Context size of model. Suggested to leave at default"),
            gr.Slider(0, 100, value=0, label="GPU layers to offload", info="Number of GPU layers to offload. Requires a compatible GPU"),
            gr.Slider(0, 1, value=0.7, label="Temperature", info="Temperature of model. Higher values have more randomness"),
            gr.Textbox("-1"), # Text box for seed
        ],
        outputs=["text"], # Output box for audio file
        allow_flagging="never",  # Disables the flagging functionality
    )


# The following code is for testing purposes only

from llm_chapter_manager import identify_characters_in_chapter

class UiTestChapterPage:
    def __init__(self, session):
        self._session = session

    def indentify_chapter_characters(chapter):

        global llm
        characters = ""
        
        if llm is not None:
            characters = identify_characters_in_chapter(chapter, llm)
        
        return characters



    test_chapter_interface = gr.Interface(
        fn=indentify_chapter_characters,
        inputs=[

            "text",
        ],
        outputs=["text"], # Output box for audio file
        allow_flagging="never",  # Disables the flagging functionality
    )
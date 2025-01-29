import gradio as gr
from text_generator import generate_json_text
from llm_model_loader import load_llm_model
from os import listdir, getcwd
from os.path import isfile, join

llm = None

# Returns a list of all the file paths in the given folder
def get_files_in_directory(directory_path, files_to_ignore):
    
    file_paths = []
    
    # Loop through all of the files in the given directory
    for file_path in listdir(directory_path):
    
        # Ignore anything that is a directory or text file
        if isfile(join(directory_path, file_path)) and file_path[-4:] not in files_to_ignore:
            
            # Add the file to the list of valid files
            file_paths.append(join(directory_path, file_path).replace("\\", "/"))
        
    return file_paths
    

# Load the LLM
def load_model(local_model_path, huggingface_model_path, repo_id, context_length, gpu_layers):
    
    if local_model_path:
        model_path = local_model_path
        repo_id = None
    elif huggingface_model_path:
        model_path = huggingface_model_path
    else:
        return "Invalid model path"
    
    model_info = {
        "file_name": model_path,
        "repo_id": repo_id,
        "n_gpu_layers": gpu_layers,
        "n_ctx": context_length
    }
    
    global llm
    
    llm = load_llm_model(model_info)
    
    return "Loaded model: " + str(model_info)


model_page = gr.Interface(
    fn=load_model,
    inputs=[
        
        # Dropdown menu for models
        gr.Dropdown(
                choices=set(get_files_in_directory("./models", [".txt"])), # Get all of the available models
                label="Model"
            ),
        "text", # Text box for model paths
        "text", # Text box for repo ids
        gr.Slider(0, 131072, value=16384, label="Context size", info="Context siz of model. Suggested to leave at default"),
        gr.Slider(0, 100, value=0, label="GPU layers to offload", info="Number of GPU layers to offload. Requires a compatible GPU"),
    ],
    outputs=["text"], # Output box for audio file
    allow_flagging="never",  # Disables the flagging functionality
)


# The following code is for testing purposes only

from llm_chapter_manager import identify_characters_in_chapter

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

gr.TabbedInterface(
    [model_page, test_chapter_interface], ["Model", "Test Chapter"]
).launch()
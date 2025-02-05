from llama_cpp import Llama

# Load LLM model
def load_llm_model(model_settings):
    
    llm = None
    
    # If the model was manually downloaded, load it based on its file path
    if model_settings["repo_id"] is None:
        llm = load_model_from_file(model_settings)
    
    # Load model from Hugging Face
    else:
        llm = load_model_from_huggingface(model_settings)
    
    return llm
    

# Load a model from a file path
def load_model_from_file(model_settings):

    llm = Llama(
        model_path = model_settings["file_name"], # Path to model
        n_gpu_layers = model_settings["n_gpu_layers"],
        n_ctx = model_settings["n_ctx"]
    )
    
    return llm
    

# Load model from Hugging Face
def load_model_from_huggingface(model_settings):

    from llama_cpp import Llama

    llm = Llama.from_pretrained(
        repo_id = model_settings["repo_id"],
        filename = model_settings["file_name"],
        n_gpu_layers = model_settings["n_gpu_layers"],
        n_ctx = model_settings["n_ctx"]
    )
    
    return llm

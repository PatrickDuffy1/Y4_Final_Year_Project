from llama_cpp import Llama

# Load LLM model
def load_llm_model(model_info):
    
    llm = None
    
    # If the model was manually downloaded, load it based on its file path
    if model_info["repo_id"] is None:
        llm = load_model_from_file(model_info)
    
    # Load model from Hugging Face
    else:
        llm = load_model_from_huggingface(model_info)
    
    return llm
    

# Load a model from a file path
def load_model_from_file(model_info):

    llm = Llama(
        model_path = model_info["file_name"], # Path to model
        n_gpu_layers = model_info["n_gpu_layers"],
        n_ctx = model_info["n_ctx"]
    )
    
    return llm
    

# Load model from Hugging Face
def load_model_from_huggingface(model_info):

    from llama_cpp import Llama

    llm = Llama.from_pretrained(
        repo_id = model_info["repo_id"],
        filename = model_info["file_name"],
        n_gpu_layers = model_info["n_gpu_layers"],
        n_ctx = model_info["n_ctx"]
    )
    
    return llm

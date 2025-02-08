from llama_cpp import Llama

# Load LLM model
def load_llm_model(llm):
    
    loaded_llm = None
    
    # If the model was manually downloaded, load it based on its file path
    if llm._repo_id is None:
        loaded_llm = load_model_from_file(llm)
    
    # Load model from Hugging Face
    else:
        loaded_llm = load_model_from_huggingface(llm)
    
    return loaded_llm
    

# Load a model from a file path
def load_model_from_file(llm):

    loaded_llm = Llama(
        model_path = llm._model_path,
        n_gpu_layers = llm._gpu_layers,
        n_ctx = llm._context_length,
        seed = llm.seed,
        temperature = llm.temperature
    )
    
    return loaded_llm
    

# Load model from Hugging Face
def load_model_from_huggingface(llm):

    loaded_llm = Llama.from_pretrained(
        repo_id = llm._repo_id,
        filename = llm._model_path,
        n_gpu_layers = llm._gpu_layers,
        n_ctx = llm._context_length,
        seed = llm.seed,
        temperature = llm.temperature
    )
    
    return loaded_llm

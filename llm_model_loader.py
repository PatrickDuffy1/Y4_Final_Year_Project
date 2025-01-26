from llama_cpp import Llama

# Load LLM model
def load_llm_model(model_path, load_from_huggingface):
    
    llm = None
    
    # If the model was manually downloaded, load it based on its file path
    if load_from_huggingface is False:
        llm = load_model_from_file(model_path)
    
    return llm
    

# Load a model from a file path
def load_model_from_file(model_path):

    llm = Llama(
          model_path=model_path, # Path to model
          n_gpu_layers=1, # Layers to offload to GPU
          n_ctx=8192, # Context length
    )
    
    return llm
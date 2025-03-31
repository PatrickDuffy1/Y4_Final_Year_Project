from enum import Enum
from llama_cpp import Llama

class Model_Type(Enum):
    LOCAL_FILE = 1
    HUGGING_FACE = 2
    OPEN_AI = 3
    GEMINI = 4

# Load LLM model
def load_llm_model(llm):
    
    loaded_llm = None
    model_type = llm.model_config['model_type']
    
    if model_type is Model_Type.LOCAL_FILE:
        return load_model_from_file(llm)

    elif model_type is Model_Type.HUGGING_FACE:
        return load_model_from_huggingface(llm)
        
    else:
        raise Exception("Invalid Model Type:", model_type)
    

# Load a model from a file path
def load_model_from_file(llm):

    loaded_llm = Llama(
        model_path = llm.model_config['model_path'],
        n_gpu_layers = llm.model_config['gpu_layers'],
        n_ctx = llm.model_config['context_length'],
        seed = llm.model_config['seed'],
        temperature = llm.model_config['temperature']
    )
    
    return loaded_llm
    

# Load model from Hugging Face
def load_model_from_huggingface(llm):

    loaded_llm = Llama.from_pretrained(
        repo_id = llm.model_config['repo_id'],
        filename = llm.model_config['model_path'],
        n_gpu_layers = llm.model_config['gpu_layers'],
        n_ctx = llm.model_config['context_length'],
        seed = llm.model_config['seed'],
        temperature = llm.model_config['temperature']
    )
    
    return loaded_llm

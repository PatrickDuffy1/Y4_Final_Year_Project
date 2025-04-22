from llama_cpp import Llama  # Import the Llama class from the llama_cpp python library
from text_generator import Model_Type  # Import the Model_Type enum for model source identification

# Load LLM model based on the specified model type in the configuration
def load_llm_model(llm):
    
    loaded_llm = None  # Placeholder for the model once loaded
    model_type = llm.model_config['model_type']  # Get the model type from configuration

    # If the model is stored locally, load it from file
    if model_type == Model_Type.LOCAL_FILE:
        return load_model_from_file(llm)

    # If the model is hosted on Hugging Face, download and then load it from there
    elif model_type == Model_Type.HUGGING_FACE:
        return load_model_from_huggingface(llm)
        
    # Raise an error if the model type is invalid or unsupported
    else:
        raise ValueError(f"Invalid Model Type: {model_type}")
    

# Load a model from a local file path using Llama class
def load_model_from_file(llm):

    # Create a Llama instance using configuration details
    loaded_llm = Llama(
        model_path = llm.model_config['model_path'],       # Path to the local model file
        n_gpu_layers = llm.model_config['gpu_layers'],     # Number of layers to run on GPU
        n_ctx = llm.model_config['context_length'],        # Context window size
        seed = llm.model_config['seed'],                   # Seed for reproducibility
        temperature = llm.model_config['temperature']      # Sampling temperature for generation
    )
    
    return loaded_llm  # Return the loaded model instance
    

# Load a model hosted on Hugging Face using from_pretrained method
def load_model_from_huggingface(llm):

    # Load the model from a Hugging Face repo using its ID and file name
    loaded_llm = Llama.from_pretrained(
        repo_id = llm.model_config['repo_id'],             # Hugging Face repository ID
        filename = llm.model_config['model_path'],         # File name of the model in the repo
        n_gpu_layers = llm.model_config['gpu_layers'],     # Number of GPU layers
        n_ctx = llm.model_config['context_length'],        # Context window size
        seed = llm.model_config['seed'],                   # Seed
        temperature = llm.model_config['temperature']      # Sampling temperature
    )
    
    return loaded_llm  # Return the model instance

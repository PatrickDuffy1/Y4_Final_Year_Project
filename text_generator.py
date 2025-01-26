from llm_model_loader import load_llm_model

# The following code is currently for testing purposes only

test_model_info = {
    "file_name": "./models/DeepSeek-R1-Distill-Llama-8B-Q4_K_M.gguf",
    "repo_id": None,
    "n_gpu_layers": 1, # Layers to offload to GPU
    "n_ctx": 8192 # Context length
}

load_llm_model(test_model_info)

test_model_info = {
    "file_name": "Llama-3.2-3B-Instruct-Q4_K_M.gguf",
    "repo_id": "bartowski/Llama-3.2-3B-Instruct-GGUF",
    "n_gpu_layers": 1, # Layers to offload to GPU
    "n_ctx": 8192 # Context length
}

load_llm_model(test_model_info)
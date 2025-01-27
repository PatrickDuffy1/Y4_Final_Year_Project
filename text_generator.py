from llm_model_loader import load_llm_model
import json

# Generate response based on an initial input
def generate_text(initial_prompt, llm):

    response = llm.create_chat_completion(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that outputs in JSON.",
            },
            {"role": "user", "content": "Who won the world series in 2020"},
        ],
        response_format={
            "type": "json_object",
        },
        temperature=0.7,
    )
    
    return response
    


# The following code is currently for testing purposes only

test_model_info = {
    "file_name": "./models/DeepSeek-R1-Distill-Llama-8B-Q4_K_M.gguf",
    "repo_id": None,
    "n_gpu_layers": 1, # Layers to offload to GPU
    "n_ctx": 8192 # Context length
}

#load_llm_model(test_model_info)

test_model_info = {
    "file_name": "Llama-3.2-3B-Instruct-Q4_K_M.gguf",
    "repo_id": "bartowski/Llama-3.2-3B-Instruct-GGUF",
    "n_gpu_layers": 1, # Layers to offload to GPU
    "n_ctx": 8192 # Context length
}

llm = load_llm_model(test_model_info)
response = generate_text("", llm)

# Extract the answer from the response
content = response['choices'][0]['message']['content']
result_dict = json.loads(content)
result = result_dict['result']

print(result)
# Import necessary libraries for interacting with different LLMs (OpenAI)
import openai
from enum import Enum


# Define an Enum to categorize different model sources/types
class Model_Type(Enum):
    LOCAL_FILE = 1       # Local or self-hosted model
    HUGGING_FACE = 2     # Model from Hugging Face
    OPEN_AI = 3          # OpenAI's API model


# Main function to generate a JSON-formatted response from a given prompt and LLM
def generate_json_text(initial_prompt, llm, schema):
    model_type = llm.model_config['model_type']

    # Call corresponding generation method for the model type
    if model_type == Model_Type.LOCAL_FILE or model_type == Model_Type.HUGGING_FACE:
        return generate_local_json_text(initial_prompt, llm, schema)
    elif model_type == Model_Type.OPEN_AI:
        return generate_open_ai_json_text(initial_prompt, llm, schema)
    else:
        # Raise an error if model type is unsupported here
        raise ValueError(f"Invalid Model Type: {model_type}")


# Function to handle text generation using a local model
def generate_local_json_text(initial_prompt, llm, schema):
    # Construct the chat completion request with system and user messages
    response = llm.model.create_chat_completion(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that outputs in JSON.",
            },
            {"role": "user", "content": initial_prompt},
        ],
        response_format = {
            "type": "json_object",
            "schema": schema,  # Enforce schema for the output format
        },
        temperature = llm.model_config['temperature'],  # Control randomness
        seed = llm.model_config['seed']  # For deterministic output
    )
    
    return response

# Function to handle text generation using OpenAI's ChatCompletion API
def generate_open_ai_json_text(initial_prompt, llm, schema):
    openai.api_key = llm.model_config['api_key']  # Set API key

    # Make a chat completion call to OpenAI's API
    response = openai.ChatCompletion.create(
        model=llm.model_config['model_name'],
        messages=[
            {"role": "user", "content": initial_prompt}
        ],
        functions=[
            {
                "name": "generate_response",
                "description": "Generate output following a specific JSON schema.",
                "parameters": schema
            }
        ],
        function_call={"name": "generate_response"},  # Force function call with schema
        temperature = llm.model_config['temperature'],
        max_tokens = llm.model_config['max_tokens']
    )

    # Extract the structured JSON arguments from the function call
    arguments_json = response["choices"][0]["message"]["function_call"]["arguments"]
    
    return arguments_json

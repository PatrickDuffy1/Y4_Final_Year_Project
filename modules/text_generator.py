from llm_model_loader import Model_Type
import openai

# Generate response based on an initial input
def generate_json_text(initial_prompt, llm, schema):
    
    model_type = llm.model_config['model_type']
    
    if model_type is Model_Type.LOCAL_FILE or model_type is Model_Type.HUGGING_FACE:
        return generate_local_json_text(initial_prompt, llm, schema)
        
    else:
        raise Exception("Invalid Model Type:", model_type)
    
    
def generate_local_json_text(initial_prompt, llm, schema):
    
    # Use LLM to generate text and get the result in the correct (JSON) format
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
            "schema": schema,
        },
        temperature = llm.model_config['temperature'],
        seed = llm.model_config['seed']
    )
    
    return response
    
    
def generate_open_ai_json_text(initial_prompt, llm, schema):

    openai.api_key = llm.model_config['api_key']
    
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
        function_call={"name": "generate_response"},
        temperature = llm.model_config['temperature'],
        max_tokens = llm.model_config['max_tokens']
    )

    arguments_json = response["choices"][0]["message"]["function_call"]["arguments"]
    
    return arguments_json
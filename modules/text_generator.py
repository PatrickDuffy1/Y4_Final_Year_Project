from llm_model_loader import Model_Type

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
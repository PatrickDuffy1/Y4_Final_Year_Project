# Generate response based on an initial input
def generate_json_text(initial_prompt, llm, schema):
    
    # Use LLM to generate text and get the result in the correct (JSON) format
    response = llm._model.create_chat_completion(
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
        temperature = llm._temperature,
        seed = llm._seed
    )
    
    return response
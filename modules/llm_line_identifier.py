import json
from text_generator import generate_json_text

def identify_lines_in_chapter(chapter, llm):

    print("Start")
    
    # Get the JSON schema from the file
    with open('../llm_json_schemas/line_identifier_schema.json', 'r') as file:
        schema = json.load(file)
        
    user_query = "Identify all of the lines in the text that are spoken by a character, and the character who spoke the line.\nDo not include any lines by the narrator.\n. Do not skip any lines spoken by a character.\nDo not make up any line that does not exist.\nThe line should be the full line, not just part of it. Identify the lines in order:\n\n"
    
    #temp = generate_json_text(user_query + chapter, llm, schema)['choices'][0]['message']['content']
    
    chunks = split_text_into_chunks(chapter, 5000)
    identified_chunks = []
    
    for chunk in chunks:
        identified_chunks.append(generate_json_text(user_query + chunk, llm, schema)['choices'][0]['message']['content'])
    
    combined_lines = []
    
    for chunk in identified_chunks:
        data = json.loads(chunk)
        combined_lines.extend(data["lines"])
        
    combined_data = {"lines": combined_lines}

    combined_json = json.dumps(combined_data, indent=4)

    print(combined_json)
    
    return combined_json


def split_text_into_chunks(text, chunk_size):

    text = text.split("\n\n")
    chunks = [""]
    counter = 0
    
    for paragraph in text:
    
        if len(paragraph) + len(chunks[counter]) < chunk_size:
            chunks[counter] += " " + paragraph
        else:
            counter += 1
            chunks.append("")
        
    return chunks
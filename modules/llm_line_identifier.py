import json
import re
import os
from text_generator import generate_json_text

def identify_lines_in_chapter(chapter, llm):
    print("Start")
    
    # Get the JSON schema from the file
    with open('../llm_json_schemas/line_identifier_schema.json', 'r') as file:
        schema = json.load(file)
        
    user_query = "Identify all of the lines in the text that are spoken by a character, and the character who spoke the line.\nAlso include any lines by the narrator.\n. Do not skip any lines.\nDo not make up any line that does not exist.\nThe line should be the full line, not just part of it.\nIdentify the lines in order.\nEnsure that each line is exactly written exactly as it is in the text, including the punctuation.\nEnsure you include the narrator's lines as well.\nEnsure you do not misclassify character and narrator lines. For example the line '\"Hello!\" John said' should be have the 'Hello!' part labeled as a line by John, and the 'John said' part labled as a narrator line. This is important.\n DO NOT skip any lines. DO NOT skip a single word. Every word in the text should be in your final output\nDo not leave anything out. Do not skip a line. Ensure all characters and narrator lines are correctly assigned:\n\n"

    max_retries = 3  # Maximum retries for each chunk

    # Split text into chunks
    chunks = split_text_into_chunks(chapter, 2000)
    identified_chunks = []

    # Process each chunk with retry on JSON errors
    for i, chunk in enumerate(chunks):
        for attempt in range(max_retries):
            try:
                # Generate JSON text
                response = generate_json_text(user_query + chunk, llm, schema)
                content = response['choices'][0]['message']['content']

                # Attempt to parse JSON
                parsed_chunk = json.loads(content)
                identified_chunks.append(parsed_chunk)
                break  # Exit retry loop on success

            except json.JSONDecodeError as e:
                print(f"JSON error for chunk: {chunk[:100]}... (Attempt {attempt + 1}/{max_retries})")
                print(f"Error: {e}")

            except Exception as e:
                print(f"Unexpected error for chunk: {chunk[:100]}... (Attempt {attempt + 1}/{max_retries})")
                print(f"Error: {e}")

        else:
            print("Max retries reached for a chunk. Skipping it.")
            continue  # Skip this chunk if all retries fail
            
        print(i + 1, "of", len(chunks), "chunks completed")

    # Extract and combine lines directly using list comprehension
    combined_lines = [line for chunk in identified_chunks for line in chunk["lines"]]

    # Create the combined JSON directly
    combined_json = json.dumps({"lines": combined_lines}, indent=4)

    combined_json_dict = json.loads(combined_json)

    merged_json = merge_consecutive_lines(combined_json_dict)
    print(merged_json)
    
    return merged_json
    

def merge_consecutive_lines(data):
    merged_lines = []
    previous = None

    # Iterate through the lines
    for entry in data['lines']:
        if previous and entry['speaker'].lower() == previous['speaker'].lower():
            # Merge line if the speaker is the same as previous
            previous['line'] += " " + entry['line']
        else:
            # Append previous to merged_lines if speaker changes
            if previous:
                merged_lines.append(previous)
            previous = entry

    # Append the last entry
    if previous:
        merged_lines.append(previous)

    # Replace original lines with merged ones
    data['lines'] = merged_lines
    
    #output_dir = "../../test_json"
    #os.makedirs(output_dir, exist_ok=True)

    # Save the updated JSON file
    #with open(output_dir + "/" + "output.json", 'w') as file:
        #json.dump(data, file, indent=4)

    print("Merging complete.")
    return data  # Return the merged data


def split_text_into_chunks(text, chunk_size):
    # Split text into paragraphs
    text = text.split("\n\n")
    chunks = [""]
    counter = 0
    
    file_path="../../chunk_test.txt"
    
    # Create chunks
    for paragraph in text:
        if len(paragraph) + len(chunks[counter]) < chunk_size:
            if chunks[counter]:
                chunks[counter] += " "
            chunks[counter] += paragraph
        else:
            counter += 1
            chunks.append(paragraph)
    
    # Write chunks to file
    #with open(file_path, "w", encoding="utf-8") as file:
        #for i, chunk in enumerate(chunks):
            #file.write(f"--- Chunk {i + 1} ---\n")
            #file.write(chunk + "\n\n")
    
    #print(f"Successfully wrote {len(chunks)} chunks to '{file_path}'")
    print(f"Successfully created {len(chunks)} chunks")
    
    return chunks

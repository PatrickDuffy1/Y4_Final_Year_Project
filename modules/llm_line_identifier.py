import json
import re
import os
from text_generator import generate_json_text

def identify_lines_in_chapter(chapter, llm):
    print("Start")
    
    # Get the JSON schema from the file
    with open('../llm_json_schemas/line_identifier_schema.json', 'r') as file:
        schema = json.load(file)
        
    user_query = "Identify all of the lines in the text that are spoken by a character, and the character who spoke the line.\nAlso include any lines by the narrator.\n. Do not skip any lines.\nDo not make up any line that does not exist.\nThe line should be the full line, not just part of it.\nIdentify the lines in order.\nEnsure that each line is exactly written exactly as it is in the text, including the punctuation.\nEnsure you include the narrator's lines as well.\nEnsure you do not misclassify character and narrator lines. For example the line '\"Hello!\" John said' should be have the 'Hello!' part labeled as a line by John, and the 'John said' part labled as a narrator line. This is important.\n DO NOT skip any lines. DO NOT skip a single word. Every word in the text should be in your final output\nDo not leave anything out. Do not skip a line. Ensure all characters and narrator lines are correctly assigned.\nIf you are unsure of the speaker of a line, label it as a Narrator line. Do not skip it. NEVER return an empty lines array. Ensure you include the non speaker (Narrator) lines in your output. Ensure that ALL Narrator lines are included:\n\n"

    max_retries = 500  # Maximum retries for each chunk
    retry_if_no_narrator = True
    max_retries_if_no_narrator = 5
    current_no_narrator_retries = 0

    # Split text into chunks
    chunks = split_text_into_chunks(chapter, 2000)
    identified_chunks = []

    # Process each chunk with retry on JSON errors or empty arrays
    for i, chunk in enumerate(chunks):
        current_no_narrator_retries = 0  # Reset per chunk
        for attempt in range(max_retries):
            try:
                # Generate JSON text
                response = generate_json_text(user_query + chunk, llm, schema)
                content = response['choices'][0]['message']['content']

                #print("\n\n\nCONTENT:\n", content, "\n\n\n")

                # Attempt to parse JSON
                parsed_chunk = json.loads(content)
                
                # Check for error and print message if exists
                if parsed_chunk.get("was_error"):
                    print(f"MODEL ERROR: {parsed_chunk.get('error_message')}")
                    raise Exception("Error")

                # Check if the 'lines' array is empty
                if not parsed_chunk.get("lines"):
                    print(f"Empty 'lines' array for chunk: {chunk[:100]}... (Attempt {attempt + 1}/{max_retries})")
                    continue  # Retry if 'lines' is empty

                # Check if there's a speaker called "Narrator" (case-insensitive)
                has_narrator = any(
                    line.get("speaker", "").strip().lower() == "narrator"
                    for line in parsed_chunk["lines"]
                )

                if not has_narrator and retry_if_no_narrator:
                    if current_no_narrator_retries < max_retries_if_no_narrator:
                        current_no_narrator_retries += 1
                        print(f"No 'Narrator' found, retrying chunk... (Narrator retry {current_no_narrator_retries}/{max_retries_if_no_narrator})")
                        continue
                    else:
                        print(f"No 'Narrator' found after {max_retries_if_no_narrator} retries. Accepting chunk.")
                
                # Add parsed chunk to results
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
    text = text.replace("\r", "\n")

    # Step 1: Normalize and split into paragraphs
    paragraphs = re.split(r'\n\s*\n', text.strip())

    # Step 2: Split large paragraphs
    processed_paragraphs = []
    for para in paragraphs:
        if len(para) <= chunk_size:
            processed_paragraphs.append(para)
        else:
            # If paragraph is too large, split it into smaller parts
            processed_paragraphs.extend(split_large_paragraph(para, chunk_size))

    # Step 3: Group paragraphs into chunks
    chunks = []
    current_chunk = ""

    for para in processed_paragraphs:
        if len(current_chunk) + len(para) + 2 <= chunk_size:
            current_chunk += ("\n\n" if current_chunk else "") + para
        else:
            chunks.append(current_chunk)
            current_chunk = para

    if current_chunk:
        chunks.append(current_chunk)

    print(f"Successfully created {len(chunks)} chunks")
    return chunks


def split_large_paragraph(paragraph, chunk_size):
    # Split by sentence
    sentences = re.split(r'(?<=[.!?]) +', paragraph)
    
    parts = []
    current = ""

    for sentence in sentences:
        if len(current) + len(sentence) + 1 <= chunk_size:
            current += (" " if current else "") + sentence
        else:
            if current:
                parts.append(current)
            # Handle case where a single sentence is larger than chunk_size
            if len(sentence) > chunk_size:
                parts.extend(split_long_sentence(sentence, chunk_size))
                current = ""
            else:
                current = sentence

    if current:
        parts.append(current)

    return parts


def split_long_sentence(sentence, chunk_size):
    # Split a too-long sentence into smaller chunks by word
    words = sentence.split()
    parts = []
    current = ""

    for word in words:
        if len(current) + len(word) + 1 <= chunk_size:
            current += (" " if current else "") + word
        else:
            parts.append(current)
            current = word

    if current:
        parts.append(current)

    return parts

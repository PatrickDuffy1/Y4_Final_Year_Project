import json
import re
import os
from text_generator import generate_json_text

# Main function to identify spoken and narrator lines in a given chapter
def identify_lines_in_chapter(chapter, llm, max_retries_if_no_narrator):
    print("Start")
    
    # Load the expected JSON schema from file for validation
    with open('../llm_json_schemas/line_identifier_schema.json', 'r') as file:
        schema = json.load(file)
        
    # Instruction/query for the language model
    user_query = (
        "Identify all of the lines in the text that are spoken by a character, and the character who spoke the line.\n"
        "Also include any lines by the narrator.\n"
        "Do not skip any lines. Do not make up any line that does not exist. The line should be the full line, not just part of it.\n"
        "Identify the lines in order. Ensure that each line is written exactly as it is in the text, including punctuation.\n"
        "Ensure you include the narrator's lines as well. Ensure you do not misclassify character and narrator lines.\n"
        "For example, the line '\"Hello!\" John said' should have the 'Hello!' part labeled as a line by John, and the 'John said' part labeled as a narrator line. This is important.\n"
        "DO NOT skip any lines. DO NOT skip a single word. Every word in the text should be in your final output.\n"
        "Do not leave anything out. Do not skip a line. Ensure all characters and narrator lines are correctly assigned.\n"
        "If you are unsure of the speaker of a line, label it as a Narrator line. Do not skip it.\n"
        "NEVER return an empty lines array. Ensure you include the non-speaker (Narrator) lines in your output. Ensure that ALL Narrator lines are included:\n\n"
    )

    max_retries = 200  # How many times to retry a chunk if issues occur
    retry_if_no_narrator = True
    current_no_narrator_retries = 0

    # Break the chapter into smaller text chunks based on model context limit
    chunks = split_text_into_chunks(chapter, int(llm.model_config['context_length']))
    identified_chunks = []

    # Process each chunk individually
    for i, chunk in enumerate(chunks):
        current_no_narrator_retries = 0  # Reset retry count for each chunk
        for attempt in range(max_retries):
            try:
                print("\nCurrent chunk:", (i + 1), "of", len(chunk), "\nChunk text:\n")
                print(chunk)
                print("\nProcessing...")
                
                # Ask the LLM to process this chunk
                response = generate_json_text(user_query + chunk, llm, schema)
                content = response['choices'][0]['message']['content']

                print("\n\n\nOutput:\n", content, "\n\n\n")

                # Attempt to parse the response content as JSON
                parsed_chunk = json.loads(content)
                
                # If model indicates an internal error
                if parsed_chunk.get("was_error"):
                    print(f"MODEL ERROR: {parsed_chunk.get('error_message')}")
                    raise Exception("Error")

                # If no lines returned, retry
                if not parsed_chunk.get("lines"):
                    print(f"Empty 'lines' array for chunk: {chunk[:100]}... (Attempt {attempt + 1}/{max_retries})")
                    continue

                # Check that narrator lines are included
                has_narrator = any(
                    line.get("speaker", "").strip().lower() == "narrator"
                    for line in parsed_chunk["lines"]
                )

                # Retry if no narrator lines are found
                if not has_narrator and retry_if_no_narrator:
                    if current_no_narrator_retries < max_retries_if_no_narrator:
                        current_no_narrator_retries += 1
                        print(f"No 'Narrator' found, retrying chunk... (Narrator retry {current_no_narrator_retries}/{max_retries_if_no_narrator})")
                        continue
                    else:
                        print(f"No 'Narrator' found after {max_retries_if_no_narrator} retries. Accepting chunk.")
                
                # Append successful result
                identified_chunks.append(parsed_chunk)
                break  # Stop retrying on success

            except json.JSONDecodeError as e:
                # JSON parsing failed, retry
                print(f"JSON error for chunk: {chunk[:100]}... (Attempt {attempt + 1}/{max_retries})")
                print(f"Error: {e}")

            except Exception as e:
                # Handle other unexpected errors
                print(f"Unexpected error for chunk: {chunk[:100]}... (Attempt {attempt + 1}/{max_retries})")
                print(f"Error: {e}")

        else:
            # If all retries fail, skip the chunk
            print("Max retries reached for a chunk. Skipping it.")
            continue

        print(i + 1, "of", len(chunks), "chunks completed")

    # Flatten the list of lines from all chunks
    combined_lines = [line for chunk in identified_chunks for line in chunk["lines"]]

    combined_json_dict = {"lines": combined_lines}

    # Merge adjacent lines with the same speaker
    merged_json = merge_consecutive_lines(combined_json_dict)

    print(merged_json)
    return merged_json


# Combines consecutive lines from the same speaker into one
def merge_consecutive_lines(data):
    merged_lines = []
    previous = None

    for entry in data['lines']:
        if previous and entry['speaker'].lower() == previous['speaker'].lower():
            # Append text if speaker is the same
            previous['line'] += " " + entry['line']
        else:
            # Push the previous line to the list
            if previous:
                merged_lines.append(previous)
            previous = entry

    # Add the last entry
    if previous:
        merged_lines.append(previous)

    data['lines'] = merged_lines

    print("Merging complete.")
    return data


# Splits the input text into chunks that fit within the model's context length
def split_text_into_chunks(text, chunk_size):
    text = text.replace("\r", "\n")  # Normalize line endings

    # Step 1: Split text into paragraphs using double newlines
    paragraphs = re.split(r'\n\s*\n', text.strip())

    processed_paragraphs = []
    # Step 2: Ensure no single paragraph exceeds the chunk size
    for para in paragraphs:
        if len(para) <= chunk_size:
            processed_paragraphs.append(para)
        else:
            # Break large paragraphs down further by sentence
            processed_paragraphs.extend(split_large_paragraph(para, chunk_size))

    # Step 3: Combine paragraphs into chunks without exceeding chunk size
    chunks = []
    current_chunk = ""

    for para in processed_paragraphs:
        # If adding this paragraph doesn't exceed limit, append it
        if len(current_chunk) + len(para) + 2 <= chunk_size:
            current_chunk += ("\n\n" if current_chunk else "") + para
        else:
            # Start a new chunk
            chunks.append(current_chunk)
            current_chunk = para

    # Append any remaining content
    if current_chunk:
        chunks.append(current_chunk)

    print(f"Successfully created {len(chunks)} chunks")
    return chunks


# Further splits a large paragraph into sentence-sized pieces that fit in the chunk size
def split_large_paragraph(paragraph, chunk_size):
    # Split paragraph into sentences using punctuation as delimiter
    sentences = re.split(r'(?<=[.!?]) +', paragraph)
    
    parts = []
    current = ""

    for sentence in sentences:
        # If adding this sentence doesn't exceed size, append it to current part
        if len(current) + len(sentence) + 1 <= chunk_size:
            current += (" " if current else "") + sentence
        else:
            # Save current part and start a new one
            if current:
                parts.append(current)
            # If a single sentence is still too long, break it further
            if len(sentence) > chunk_size:
                parts.extend(split_long_sentence(sentence, chunk_size))
                current = ""
            else:
                current = sentence

    # Append any leftover text
    if current:
        parts.append(current)

    return parts


# Breaks a sentence that exceeds the chunk size into smaller parts by word
def split_long_sentence(sentence, chunk_size):
    words = sentence.split()
    parts = []
    current = ""

    for word in words:
        # Try to fit this word into the current chunk
        if len(current) + len(word) + 1 <= chunk_size:
            current += (" " if current else "") + word
        else:
            # Save current part and start a new one with the current word
            parts.append(current)
            current = word

    # Append any final leftover text
    if current:
        parts.append(current)

    return parts


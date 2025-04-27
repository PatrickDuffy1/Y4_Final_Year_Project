import json
import re
import os
from text_generator import generate_json_text

# Main function to identify spoken and narrator lines in a given chapter
def identify_lines_in_chapter(chapter, llm, max_retries_if_no_narrator):
    print("Start")
    
    # Get the absolute path to the schema, relative to this file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    schema_path = os.path.join(script_dir, '../llm_json_schemas/line_identifier_schema.json')
    
    # Load the expected JSON schema from file for validation
    with open(schema_path, 'r') as file:
        schema = json.load(file)
        
    # Instruction/query for the language model
    user_query = (
        "Given the input text, identify and label every line in the exact order it appears. For each line:\n"
        "- Extract the exact text, including all punctuation, without omissions or modifications.\n"
        "- Assign each line a speaker: either the character who spoke it or Narrator.\n"
        "- If a line includes both narration and dialogue (e.g., \"Hello!\" John said.), split and label the parts accordingly:\n"
        "  - \"Hello!\" → Character: John\n"
        "  - John said. → Narrator\n"
        "\n"
        "Important Instructions:\n"
        "- Do NOT skip any lines or words.\n"
        "- Do NOT invent or paraphrase any text.\n"
        "- Include every line in your output — even those by the Narrator.\n"
        "- If the speaker is ambiguous or unknown, default to Narrator.\n"
        "- The final output must include every word from the input text.\n"
        "- The output should NEVER be empty.\n"
        "\n"
        "Your goal is to produce a complete and accurate list of lines with correct speaker attributions.\n"
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
                print("\nCurrent chunk:", (i + 1), "of", len(chunks), "\nChunk text (first 100 characters):\n")
                print(chunk[:100] + "...")

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


import json

def process_repo_file(input_file, output_file, max_chunk_size=500):
    """
    Processes a repository file and chunks it into smaller logical parts for training.
    Args:
        input_file (str): Path to the input file (e.g., repo.txt).
        output_file (str): Path to save the JSON output.
        max_chunk_size (int): Maximum chunk size in terms of token length.
    """
    with open(input_file, 'r',encoding='utf-8') as f:
        lines = f.readlines()

    chunks = []
    current_chunk = {
        "file": None,
        "directory": None,
        "description": None,
        "chunk_id": None,
        "content": ""
    }
    chunk_id = 1
    content_accumulator = ""

    for line in lines:
        # Detect file path headers
        if line.startswith("File:"):
            # Save the current chunk if it exists
            if current_chunk["content"]:
                current_chunk["chunk_id"] = chunk_id
                chunks.append(current_chunk)
                chunk_id += 1
                current_chunk = {
                    "file": None,
                    "directory": None,
                    "description": None,
                    "chunk_id": None,
                    "content": ""
                }
            
            # Process new file metadata
            file_path = line.split("File:")[1].strip()
            current_chunk["file"] = file_path
            current_chunk["directory"] = "/".join(file_path.split("/")[:-1])
            current_chunk["description"] = f"Content from {file_path}"
            content_accumulator = ""
        
        elif line.strip() == "================================================":
            # If a delimiter is found, save the current chunk
            if len(content_accumulator) > max_chunk_size:
                current_chunk["content"] = content_accumulator.strip()
                current_chunk["chunk_id"] = chunk_id
                chunks.append(current_chunk)
                chunk_id += 1
                content_accumulator = ""
                current_chunk = {
                    "file": current_chunk["file"],
                    "directory": current_chunk["directory"],
                    "description": current_chunk["description"],
                    "chunk_id": None,
                    "content": ""
                }
        
        else:
            # Accumulate content
            content_accumulator += line

    # Save the last chunk
    if content_accumulator.strip():
        current_chunk["content"] = content_accumulator.strip()
        current_chunk["chunk_id"] = chunk_id
        chunks.append(current_chunk)

    # Write chunks to the output file
    with open(output_file, 'w') as out_file:
        json.dump(chunks, out_file, indent=4)

    print(f"Processed {len(chunks)} chunks and saved to {output_file}")


# Path to the input file (e.g., repo.txt) and output JSON
input_file = "repo_slice/data.txt"
output_file = "chunks/repo_chunks.json"

# Run the processing function
process_repo_file(input_file, output_file)

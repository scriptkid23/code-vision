import json


def _split_and_store_chunk(
    current_chunk, content_lines, chunks, max_chunk_size, start_chunk_id
):
    """
    Splits content into smaller chunks based on max_chunk_size (number of lines) and stores them.
    """
    chunk_parts = [
        content_lines[i : i + max_chunk_size]
        for i in range(0, len(content_lines), max_chunk_size)
    ]

    for idx, part in enumerate(chunk_parts):
        new_chunk = {
            "file": current_chunk["file"],
            "directory": current_chunk["directory"],
            "description": current_chunk["description"],
            "chunk_id": start_chunk_id + idx,
            "content": "\n".join(part).strip(),  # Kết hợp lại các dòng thành chuỗi
        }
        chunks.append(new_chunk)


def process_repo_file(
    input_file, output_file, max_chunk_size=50
):  # Mặc định 50 dòng mỗi chunk
    """
    Processes a repository file and chunks it into smaller logical parts for training.
    Args:
        input_file (str): Path to the input file (e.g., repo.txt).
        output_file (str): Path to save the JSON output.
        max_chunk_size (int): Maximum number of lines per chunk.
    """
    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    chunks = []
    current_chunk = None
    chunk_id = 1
    content_accumulator = []

    for line in lines:
        # Detect file path headers
        if line.startswith("File:"):
            # Save the current chunk if it exists
            if current_chunk and content_accumulator:
                _split_and_store_chunk(
                    current_chunk, content_accumulator, chunks, max_chunk_size, chunk_id
                )
                chunk_id += len(chunks)  # Cập nhật chunk_id theo số lượng đã thêm

            # Process new file metadata
            file_path = line.split("File:", 1)[1].strip()
            current_chunk = {
                "file": file_path,
                "directory": "/".join(file_path.split("/")[:-1]),
                "description": f"Content from {file_path}",
                "chunk_id": None,
                "content": "",
            }
            content_accumulator = []

        elif line.strip() == "================================================":
            # If a delimiter is found, save the current chunk
            if current_chunk and content_accumulator:
                _split_and_store_chunk(
                    current_chunk, content_accumulator, chunks, max_chunk_size, chunk_id
                )
                chunk_id += len(chunks)  # Cập nhật chunk_id theo số lượng đã thêm
                content_accumulator = []

        else:
            # Accumulate content as list of lines
            content_accumulator.append(line.strip())

    # Save the last chunk if it exists
    if current_chunk and content_accumulator:
        _split_and_store_chunk(
            current_chunk, content_accumulator, chunks, max_chunk_size, chunk_id
        )

    # Write chunks to the output file
    with open(output_file, "w", encoding="utf-8") as out_file:
        json.dump(chunks, out_file, indent=4, ensure_ascii=False)

    print(f"Processed {len(chunks)} chunks and saved to {output_file}")


# Path to the input file (e.g., repo.txt) and output JSON
input_file = "repo_slice/data.txt"
output_file = "chunks/repo_chunks.json"

# Run the processing function with line-based chunking
process_repo_file(
    input_file, output_file, max_chunk_size=500
)  # Giới hạn 50 dòng mỗi chunk

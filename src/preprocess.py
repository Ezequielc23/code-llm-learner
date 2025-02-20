from langchain.text_splitter import RecursiveCharacterTextSplitter

def preprocess_code(codebase, chunk_size=1000, chunk_overlap=200):
    """Split code into manageable chunks."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    chunks = []
    for file_path, content in codebase.items():
        split_content = splitter.split_text(content)
        for i, chunk in enumerate(split_content):
            chunks.append({
                "file": file_path,
                "chunk_id": i,
                "content": chunk
            })
    return chunks

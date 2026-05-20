from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_text(text):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        separators=["\n\n", "\n", ".", " ", ""]
    )

    chunks = text_splitter.split_text(text)

    # Remove very small chunks
    cleaned_chunks = [
        chunk.strip()
        for chunk in chunks
        if len(chunk.strip()) > 50
    ]

    return cleaned_chunks
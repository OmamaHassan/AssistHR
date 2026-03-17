from langchain_text_splitters import RecursiveCharacterTextSplitter

# page +1 because index started at 0.
def chunk_documents(documents):
    for doc in documents:
        doc.metadata["filename"] = doc.metadata.get("source", "unknown")
        if "page" in doc.metadata:         
            doc.metadata["page"] = doc.metadata["page"] + 1

    splitter = RecursiveCharacterTextSplitter(
        chunk_size   = 500,
        chunk_overlap= 100
    )
    return splitter.split_documents(documents)
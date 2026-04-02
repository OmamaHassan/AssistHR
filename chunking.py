from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_documents(documents):

    for doc in documents:
        doc.metadata["filename"] = doc.metadata.get("source", "unknown")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    return splitter.split_documents(documents)
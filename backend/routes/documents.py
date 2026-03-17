import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from auth import get_current_user

router     = APIRouter()
BASE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads", "documents")
ALLOWED    = {".pdf", ".docx", ".txt"}


@router.post("/upload")
async def upload_document(
    file        : UploadFile = File(...),
    current_user: dict       = Depends(get_current_user)
):
    from document_loader import load_document
    from chunking        import chunk_documents
    from embedding       import create_vector_store, get_existing_files

    ext = os.path.splitext(file.filename)[-1].lower()
    if ext not in ALLOWED:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{ext}'. Allowed: {ALLOWED}"
        )

    existing = get_existing_files()
    if file.filename in existing:
        raise HTTPException(
            status_code=409,
            detail=f"'{file.filename}' already exists."
        )

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        docs   = load_document(file_path)
        chunks = chunk_documents(docs)
        create_vector_store(chunks)
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "filename": file.filename,
        "chunks"  : len(chunks),
        "message" : "Uploaded successfully"
    }


@router.get("/list")
def list_documents(
    current_user: dict = Depends(get_current_user)
):
    from embedding import get_existing_files
    existing = get_existing_files()
    return {
        "documents": list(existing),
        "total"    : len(existing)
    }


@router.delete("/{filename}")
def delete_document(
    filename    : str,
    current_user: dict = Depends(get_current_user)
):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail=f"'{filename}' not found."
        )
    os.remove(file_path)
    return {"message": f"'{filename}' deleted."}
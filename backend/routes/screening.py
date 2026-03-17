import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from typing import List
from auth import get_current_user

router     = APIRouter()
BASE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESUME_DIR = os.path.join(BASE_DIR, "uploads", "resumes")
JD_DIR     = os.path.join(BASE_DIR, "uploads", "jd")
ALLOWED    = {".pdf", ".docx", ".jpg", ".jpeg", ".png"}

# =====================================
# AVAILABLE SCREENING MODELS
# =====================================

SCREENING_MODELS = {
    "llama-3.1-70b-versatile": "Llama 3.1 70B",
    "llama-3.1-8b-instant"   : "Llama 3.1 8B",
    "mixtral-8x7b-32768"     : "Mixtral 8x7B",
    "gemma2-9b-it"           : "Gemma 2 9B (Google)",
}

DEFAULT_SCREENING_MODEL = "llama-3.1-70b-versatile"


@router.get("/models")
def get_screening_models():
    return {
        "models" : [
            {"id": k, "name": v}
            for k, v in SCREENING_MODELS.items()
        ],
        "default": DEFAULT_SCREENING_MODEL
    }


@router.post("/screen")
async def screen_resumes(
    jd          : UploadFile       = File(...),
    resumes     : List[UploadFile] = File(...),
    current_user: dict             = Depends(get_current_user),
    model       : str              = DEFAULT_SCREENING_MODEL
):
    from screener import screen_all

    # validate model
    if model not in SCREENING_MODELS:
        model = DEFAULT_SCREENING_MODEL

    jd_ext = os.path.splitext(jd.filename)[-1].lower()
    if jd_ext not in ALLOWED:
        raise HTTPException(
            status_code=400,
            detail="JD must be PDF or DOCX."
        )

    for r in resumes:
        ext = os.path.splitext(r.filename)[-1].lower()
        if ext not in ALLOWED:
            raise HTTPException(
                status_code=400,
                detail=f"'{r.filename}' not supported."
            )

    # save JD
    jd_path = os.path.join(JD_DIR, jd.filename)
    with open(jd_path, "wb") as f:
        shutil.copyfileobj(jd.file, f)

    # save resumes
    resume_paths = []
    for resume in resumes:
        path = os.path.join(RESUME_DIR, resume.filename)
        with open(path, "wb") as f:
            shutil.copyfileobj(resume.file, f)
        resume_paths.append(path)

    try:
        results = screen_all(resume_paths, jd_path, model)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "total"  : len(results),
        "model"  : model,
        "results": results
    }
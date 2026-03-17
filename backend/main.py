import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

for folder in ["uploads/documents", "uploads/resumes", "uploads/jd"]:
    full_path = os.path.join(BASE_DIR, *folder.split("/"))
    if not os.path.exists(full_path):
        os.makedirs(full_path)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import documents, qa, screening

app = FastAPI(
    title      = "AssistHR API",
    description= "AI-powered HR Assistant",
    version    = "1.0.0"
)

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

app.add_middleware(
    CORSMiddleware,
    allow_origins = [FRONTEND_URL, "http://localhost:5173"],
    allow_methods = ["*"],
    allow_headers = ["*"],
)

app.include_router(documents.router, prefix="/documents", tags=["Documents"])
app.include_router(qa.router,        prefix="/qa",        tags=["Q&A"])
app.include_router(screening.router, prefix="/screening", tags=["Screening"])

@app.get("/health")
def health():
    return {
        "status": "AssistHR is running ✅",
        "env"   : os.getenv("ENV", "development")
    }

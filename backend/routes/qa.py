import os
import sqlite3
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from auth import get_current_user

router = APIRouter()

# =====================================
# AVAILABLE MODELS
# =====================================

AVAILABLE_MODELS = {
    "llama-3.1-70b-versatile" : "Llama 3.1 70B",
    "llama-3.1-8b-instant"    : "Llama 3.1 8B",
    "mixtral-8x7b-32768"      : "Mixtral 8x7B",
    "gemma2-9b-it"            : "Gemma 2 9B",
    "llama3-70b-8192"         : "Llama 3 70B",
}

DEFAULT_MODEL = "llama-3.1-70b-versatile"


# =====================================
# REQUEST MODELS
# =====================================

class AskRequest(BaseModel):
    question  : str
    session_id: str   = "default"
    model     : str   = DEFAULT_MODEL


# =====================================
# GET AVAILABLE MODELS
# =====================================

@router.get("/models")
def get_models():
    return {
        "models" : [
            {"id": k, "name": v}
            for k, v in AVAILABLE_MODELS.items()
        ],
        "default": DEFAULT_MODEL
    }


# =====================================
# ASK QUESTION
# =====================================

@router.post("/ask")
def ask_question(
    request     : AskRequest,
    current_user: dict = Depends(get_current_user)
):
    from rag_chain  import ask
    from chat_store import create_session, load_history

    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    # validate model
    model = request.model if request.model in AVAILABLE_MODELS \
            else DEFAULT_MODEL

    # prefix session with user email for isolation
    session_id = f"{current_user['email']}_{request.session_id}"
    create_session(session_id)

    try:
        answer  = ask(request.question, session_id, model)
        history = load_history(session_id)
        return {
            "answer"    : answer,
            "session_id": request.session_id,
            "model"     : model,
            "turns"     : len(history) // 2
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =====================================
# GET CHAT HISTORY
# =====================================

@router.get("/history/{session_id}")
def get_history(
    session_id  : str,
    current_user: dict = Depends(get_current_user)
):
    from chat_store import load_history
    try:
        full_id  = f"{current_user['email']}_{session_id}"
        history  = load_history(full_id)
        messages = []
        for msg in history:
            messages.append({
                "role"   : "human" if msg.type == "human" else "ai",
                "content": msg.content
            })
        return {
            "session_id": session_id,
            "messages"  : messages,
            "turns"     : len(messages) // 2
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =====================================
# LIST SESSIONS
# =====================================

@router.get("/sessions")
def list_sessions(
    current_user: dict = Depends(get_current_user)
):
    from chat_store import DB_PATH
    try:
        conn   = sqlite3.connect(DB_PATH) if DB_PATH \
                 else None

        # use PostgreSQL
        from chat_store import get_conn
        conn   = get_conn()
        cursor = conn.cursor()
        prefix = f"{current_user['email']}_%"
        cursor.execute("""
            SELECT session_id, created_at, last_active
            FROM sessions
            WHERE session_id LIKE %s
            ORDER BY last_active DESC
        """, (prefix,))
        rows = cursor.fetchall()
        conn.close()

        return {
            "sessions": [
                {
                    "session_id" : r[0].split("_", 1)[1],
                    "created_at" : r[1],
                    "last_active": r[2]
                }
                for r in rows
            ],
            "total": len(rows)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =====================================
# DELETE SESSION
# =====================================

@router.delete("/sessions/{session_id}")
def remove_session(
    session_id  : str,
    current_user: dict = Depends(get_current_user)
):
    from chat_store import delete_session
    try:
        full_id = f"{current_user['email']}_{session_id}"
        delete_session(full_id)
        return {"message": f"Session '{session_id}' deleted."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
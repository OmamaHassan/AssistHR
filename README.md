# 🤖 AssistHR - AI-Powered HR Assistant

An intelligent HR assistant combining **Retrieval-Augmented Generation (RAG)** with **Groq LLM** to manage HR documents, answer policy questions, and screen resumes - all in one web app.

---

## 🌐 Live Demo

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://assisthr.streamlit.app)

> **Live URL:** `https://assisthr.streamlit.app`

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔐 **Auth** | Secure login & register via Supabase |
| 📚 **Knowledge Base** | Upload HR docs (PDF, DOCX, TXT) — auto-indexed |
| 💬 **HR Q&A** | RAG-powered answers from your documents |
| 💬 **Chat Sessions** | Multiple named sessions with history |
| 📄 **Resume Screener** | Upload resumes + JD → ranked candidates |
| 📝 **JD Input** | Upload job description file |
| 🤖 **Model Selection** | Choose from multiple llama models from Groq |
| 🌓 **Dark/Light Theme** | Theme-aware UI |

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────┐
│     Streamlit Cloud (Frontend + App)     │
│         assisthr.streamlit.app           │
└─────────────────┬────────────────────────┘
                  │
       ┌──────────▼──────────┐
       │    Supabase Auth    │
       │  Login / Register   │
       └──────────┬──────────┘
                  │ JWT
       ┌──────────▼───────────────────────┐
       │       Python Backend              │
       │  document_loader · chunking       │
       │  embedding · rag_chain · screener │
       └───────┬──────────┬───────────────┘
               │          │
    ┌──────────▼──┐ ┌─────▼───────────────┐
    │  Groq API   │ │  Supabase PostgreSQL │
    │ llama-3.3   │ │  pgvector · sessions │
    │    -70b     │ │  messages · docs     │
    └─────────────┘ └─────────────────────┘
               │
    ┌──────────▼──────────┐
    │    Mistral OCR      │
    │(scanned PDFs/images)│
    └─────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend/App** | Streamlit |
| **LLM** | Groq API (llama models) |
| **Embeddings** | sentence-transformers/all-MiniLM-L12-v2 |
| **Vector DB** | Supabase pgvector |
| **Database** | Supabase PostgreSQL |
| **Auth** | Supabase Auth |
| **OCR** | Mistral OCR API |
| **PDF Processing** | PyMuPDF |
| **RAG Framework** | LangChain |
| **Hosting** | Streamlit Cloud (free) |

---

## 📁 Project Structure

```
AssistHR/
├── streamlit_app.py          ← main app entry point
├── requirements.txt          ← Python dependencies
├── .gitignore
├── README.md
├── document_loader.py        ← PDF/DOCX/TXT/image loading + OCR
├── chunking.py               ← text splitting
├── embedding.py              ← Supabase pgvector operations
├── retriever.py              ← similarity search
├── rag_chain.py              ← RAG pipeline with Groq
├── chat_store.py             ← PostgreSQL chat history
└── screener.py               ← resume screening engine
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Git
- Free accounts: [Supabase](https://supabase.com), [Groq](https://console.groq.com), [Mistral](https://console.mistral.ai)

---

### 1. Clone

```bash
git clone https://github.com/omamahassan/assisthr.git
cd assisthr
```

### 2. Install

```bash
pip install -r requirements.txt
```

### 3. Setup Supabase Database

Go to Supabase → SQL Editor → run:

```sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS documents (
    id         BIGSERIAL PRIMARY KEY,
    filename   TEXT,
    page       INTEGER,
    content    TEXT,
    embedding  vector(384),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS documents_embedding_idx
ON documents USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

CREATE TABLE IF NOT EXISTS sessions (
    session_id  TEXT PRIMARY KEY,
    created_at  TEXT,
    last_active TEXT
);

CREATE TABLE IF NOT EXISTS messages (
    id         BIGSERIAL PRIMARY KEY,
    session_id TEXT,
    role       TEXT,
    content    TEXT,
    timestamp  TEXT
);
```

### 4. Get API Keys

| Key | Where |
|---|---|
| `GROQ_API_KEY` | [console.groq.com](https://console.groq.com) → API Keys |
| `MISTRAL_API_KEY` | [console.mistral.ai](https://console.mistral.ai) → API Keys |
| `SUPABASE_URL` | 
| `SUPABASE_ANON_KEY` |
| `DATABASE_URL` | 

### 5. Run Locally

Create `.streamlit/secrets.toml`:

```toml
GROQ_API_KEY      = "gsk_..."
MISTRAL_API_KEY   = "..."
SUPABASE_URL      = "https://xxxxx.supabase.co"
SUPABASE_ANON_KEY = "eyJhbG..."
DATABASE_URL      = "postgresql://postgres.xxx:pass@aws-0-region.pooler.supabase.com:6543/postgres"
```

```bash
streamlit run streamlit_app.py
# opens at http://localhost:8501
```

---

## ☁️ Deploy to Streamlit Cloud (Free)

```
1. Push to GitHub
2. Go to share.streamlit.io
3. Sign in with GitHub → New App
4. Select repo · branch: main · file: streamlit_app.py
5. Advanced Settings → Secrets → paste your keys
6. Deploy → live at assisthr.streamlit.app
```

---

## 📖 How to Use

**1. Register & Login** — create account with email/password via Supabase

**2. Upload HR Documents** — Knowledge Base → upload PDF/DOCX/TXT → auto-indexed into pgvector

**3. Ask HR Questions** — HR Q&A → type question → RAG retrieves context → Groq answers

**4. Manage Sessions** — create named sessions, switch between them in sidebar, history persists

**5. Screen Resumes** — Resume Screener → upload JD (file or paste text) + resumes → ranked results with scores, skills, strengths, weaknesses

---

## 🤖 Available Models

| Models
|
| `llama-3.3-70b-versatile`
| `llama-4-scout-17b` 
| `llama-3.1-8b-instant`

---


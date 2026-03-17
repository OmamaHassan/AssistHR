import os
import psycopg2
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def get_embedding_model():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L12-v2"
    )


def get_conn():
    return psycopg2.connect(
        DATABASE_URL,
        connect_timeout = 10,
        sslmode         = "require"
    )


def init_vector_table():
    try:
        conn   = get_conn()
        cursor = conn.cursor()
        cursor.execute(
            "CREATE EXTENSION IF NOT EXISTS vector"
        )
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id         BIGSERIAL PRIMARY KEY,
                filename   TEXT,
                page       INTEGER,
                content    TEXT,
                embedding  vector(384),
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS
            documents_embedding_idx
            ON documents
            USING ivfflat (embedding vector_cosine_ops)
            WITH (lists = 100)
        """)
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"⚠️ Vector table init warning: {e}")


def get_existing_files() -> set:
    try:
        conn   = get_conn()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT DISTINCT filename FROM documents"
        )
        rows = cursor.fetchall()
        conn.close()
        return set(r[0] for r in rows if r[0])
    except Exception:
        return set()


def create_vector_store(chunks):
    existing   = get_existing_files()
    new_chunks = [
        c for c in chunks
        if c.metadata.get("filename") not in existing
    ]

    if not new_chunks:
        print("⚠️ Already exists. Skipping.")
        return

    print(f"✅ Adding {len(new_chunks)} chunks.")
    model  = get_embedding_model()
    conn   = get_conn()
    cursor = conn.cursor()

    for chunk in new_chunks:
        try:
            embedding = model.embed_query(
                chunk.page_content
            )
            cursor.execute("""
                INSERT INTO documents
                (filename, page, content, embedding)
                VALUES (%s, %s, %s, %s)
            """, (
                chunk.metadata.get("filename"),
                chunk.metadata.get("page", 1),
                chunk.page_content,
                embedding
            ))
        except Exception as e:
            print(f"⚠️ Chunk insert warning: {e}")

    conn.commit()
    conn.close()
    print("✅ Done.")


def similarity_search(
    query: str,
    k    : int = 4
) -> list:
    try:
        model     = get_embedding_model()
        query_vec = model.embed_query(query)
        conn      = get_conn()
        cursor    = conn.cursor()
        cursor.execute("""
            SELECT filename, page, content,
                   1 - (embedding <=> %s::vector)
                   AS score
            FROM documents
            ORDER BY embedding <=> %s::vector
            LIMIT %s
        """, (query_vec, query_vec, k))
        rows = cursor.fetchall()
        conn.close()

        results = []
        for filename, page, content, score in rows:
            if score >= 0.3:
                results.append(Document(
                    page_content=content,
                    metadata={
                        "filename": filename,
                        "page"    : page,
                        "score"   : score
                    }
                ))
        return results
    except Exception as e:
        print(f"⚠️ Similarity search warning: {e}")
        return []


# initialize on import
init_vector_table()
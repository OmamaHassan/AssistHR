import os
import psycopg2
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
DB_PATH      = None


def get_conn():
    conn = psycopg2.connect(
        DATABASE_URL,
        connect_timeout = 10,
        sslmode         = "require"
    )
    return conn


def init_db():
    try:
        conn   = get_conn()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                session_id  TEXT PRIMARY KEY,
                created_at  TEXT,
                last_active TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id         SERIAL PRIMARY KEY,
                session_id TEXT,
                role       TEXT,
                content    TEXT,
                timestamp  TEXT
            )
        """)
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"⚠️ DB init warning: {e}")


def create_session(session_id: str):
    try:
        conn   = get_conn()
        cursor = conn.cursor()
        now    = datetime.now().isoformat()
        cursor.execute("""
            INSERT INTO sessions
            (session_id, created_at, last_active)
            VALUES (%s, %s, %s)
            ON CONFLICT (session_id) DO NOTHING
        """, (session_id, now, now))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"⚠️ Session create warning: {e}")


def save_message(
    session_id: str,
    role      : str,
    content   : str
):
    try:
        conn   = get_conn()
        cursor = conn.cursor()
        now    = datetime.now().isoformat()
        cursor.execute("""
            INSERT INTO messages
            (session_id, role, content, timestamp)
            VALUES (%s, %s, %s, %s)
        """, (session_id, role, content, now))
        cursor.execute("""
            UPDATE sessions
            SET last_active = %s
            WHERE session_id = %s
        """, (now, session_id))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"⚠️ Save message warning: {e}")


def load_history(session_id: str):
    from langchain_core.messages import (
        HumanMessage,
        AIMessage
    )
    try:
        conn   = get_conn()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT role, content
            FROM messages
            WHERE session_id = %s
            ORDER BY id ASC
        """, (session_id,))
        rows = cursor.fetchall()
        conn.close()
        messages = []
        for role, content in rows:
            if role == "human":
                messages.append(
                    HumanMessage(content=content)
                )
            else:
                messages.append(
                    AIMessage(content=content)
                )
        return messages
    except Exception as e:
        print(f"⚠️ Load history warning: {e}")
        return []


def delete_session(session_id: str):
    try:
        conn   = get_conn()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM messages WHERE session_id = %s",
            (session_id,)
        )
        cursor.execute(
            "DELETE FROM sessions WHERE session_id = %s",
            (session_id,)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"⚠️ Delete session warning: {e}")


def list_sessions():
    try:
        conn   = get_conn()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT session_id, created_at, last_active
            FROM sessions
            ORDER BY last_active DESC
        """)
        rows = cursor.fetchall()
        conn.close()
        for r in rows:
            print(f"{r[0]} | {r[1]} | {r[2]}")
    except Exception as e:
        print(f"⚠️ List sessions warning: {e}")

init_db()
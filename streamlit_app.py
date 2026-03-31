import os
import html
import json
import tempfile
from pathlib import Path
from datetime import datetime
from typing import Dict, List

import streamlit as st
from supabase import create_client


# =========================================================
# Config + Secrets
# =========================================================
def get_secret(key: str) -> str:
    try:
        return st.secrets[key]
    except Exception:
        return os.getenv(key, "")


os.environ["GROQ_API_KEY"] = get_secret("GROQ_API_KEY")
os.environ["MISTRAL_API_KEY"] = get_secret("MISTRAL_API_KEY")
os.environ["SUPABASE_URL"] = get_secret("SUPABASE_URL")
os.environ["SUPABASE_ANON_KEY"] = get_secret("SUPABASE_ANON_KEY")
os.environ["DATABASE_URL"] = get_secret("DATABASE_URL")

st.set_page_config(
    page_title="AssistHR",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

supabase = create_client(
    get_secret("SUPABASE_URL"),
    get_secret("SUPABASE_ANON_KEY"),
)


# =========================================================
# Product UI Theme
# =========================================================
def inject_ui() -> None:
    st.markdown(
        """
        <style>
        :root {
            --bg-1: #090f1f;
            --bg-2: #111b35;
            --card: rgba(255,255,255,0.05);
            --card-2: rgba(255,255,255,0.03);
            --text: #e8ecff;
            --muted: #9aa7d4;
            --accent: #7c9cff;
            --accent-2: #61e6d7;
            --good: #34d399;
            --warn: #fbbf24;
            --danger: #fb7185;
            --border: rgba(255,255,255,0.13);
            --shadow: 0 10px 30px rgba(0,0,0,0.30);
        }

        .stApp {
            background:
                radial-gradient(1200px 650px at 5% -10%, #1f2f66 0%, transparent 56%),
                radial-gradient(1000px 550px at 100% 0%, #104158 0%, transparent 52%),
                linear-gradient(180deg, var(--bg-2), var(--bg-1));
            color: var(--text);
        }

        .block-container {
            max-width: 1260px;
            padding-top: 1rem !important;
            padding-bottom: 1.4rem !important;
        }

        .hero {
            border: 1px solid var(--border);
            background: linear-gradient(120deg, rgba(124,156,255,0.24), rgba(97,230,215,0.12));
            border-radius: 18px;
            padding: 1rem 1.2rem;
            margin-bottom: 0.9rem;
            box-shadow: var(--shadow);
            backdrop-filter: blur(4px);
        }

        .hero h1 {
            margin: 0;
            color: var(--text);
            line-height: 1.15;
            font-size: clamp(1.25rem, 2.7vw, 2.05rem);
        }

        .hero p {
            margin: .35rem 0 0 0;
            color: var(--muted);
            font-size: .95rem;
        }

        .glass-card {
            border: 1px solid var(--border);
            background: linear-gradient(180deg, var(--card), var(--card-2));
            border-radius: 16px;
            padding: .9rem 1rem;
            box-shadow: var(--shadow);
            margin-bottom: .9rem;
        }

        [data-testid="stMetric"] {
            border-radius: 14px !important;
            border: 1px solid var(--border) !important;
            background: linear-gradient(180deg, rgba(124,156,255,.13), rgba(255,255,255,.02)) !important;
            padding: 16px !important;
            box-shadow: var(--shadow) !important;
            min-height: 110px !important;
        }

        [data-testid="stMetricLabel"] p {
            color: var(--muted) !important;
            font-size: .73rem !important;
            letter-spacing: .08em !important;
            text-transform: uppercase !important;
            font-weight: 700 !important;
        }

        [data-testid="stMetricValue"] {
            color: var(--text) !important;
            font-size: 1.48rem !important;
            font-weight: 700 !important;
        }

        .stTextInput input, .stTextArea textarea {
            border-radius: 12px !important;
        }

        .stSelectbox [data-baseweb="select"] > div {
            border-radius: 12px !important;
        }

        .stButton > button {
            border-radius: 12px !important;
            border: 1px solid rgba(124,156,255,.55) !important;
            background: linear-gradient(90deg, #607fff, #7897ff) !important;
            color: #fff !important;
            font-weight: 600 !important;
            transition: transform .12s ease, box-shadow .12s ease;
        }

        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 7px 18px rgba(96,127,255,.35);
        }

        [data-testid="stSidebar"] {
            border-right: 1px solid var(--border);
            background: linear-gradient(180deg, rgba(18,26,48,.95), rgba(10,16,33,.98));
        }

        .doc-item {
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: .65rem .8rem;
            margin-bottom: .5rem;
            color: var(--text);
            background: rgba(255,255,255,0.03);
        }

        .conversation-caption {
            color: var(--muted);
            font-size: .82rem;
            margin-top: -.35rem;
            margin-bottom: .4rem;
        }

        .pill {
            display: inline-block;
            border-radius: 999px;
            border: 1px solid var(--border);
            background: rgba(124,156,255,0.16);
            padding: .16rem .5rem;
            margin-right: .35rem;
            margin-bottom: .35rem;
            font-size: .82rem;
            color: #dbe4ff;
        }

        @media (max-width: 920px) {
            .block-container { padding: .8rem .75rem 1rem .75rem !important; }
            [data-testid="stMetricValue"] { font-size: 1.18rem !important; }
            .hero { border-radius: 14px; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def hero(title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div class="hero">
            <h1>{html.escape(title)}</h1>
            <p>{html.escape(subtitle)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def card_start() -> None:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)


def card_end() -> None:
    st.markdown("</div>", unsafe_allow_html=True)


inject_ui()


# =========================================================
# Session Storage (for real bot-like conversations)
# =========================================================
def session_store_path(email: str) -> Path:
    safe = email.replace("@", "_at_").replace(".", "_")
    return Path(tempfile.gettempdir()) / f"assisthr_sessions_{safe}.json"


def load_session_meta(email: str) -> List[Dict]:
    path = session_store_path(email)
   
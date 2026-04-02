import os
import sys
import streamlit as st
import streamlit.components.v1 as components

# ─── PATH FIX ────────────────────────────────────────────────
# FIX #1: Removed broken BACKEND_DIR path (no backend/ subfolder exists)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# ─── SECRETS ─────────────────────────────────────────────────
def get_secret(key: str) -> str:
    try:
        return st.secrets[key]
    except Exception:
        return os.getenv(key, "")

os.environ["GROQ_API_KEY"]      = get_secret("GROQ_API_KEY")
os.environ["MISTRAL_API_KEY"]   = get_secret("MISTRAL_API_KEY")
os.environ["SUPABASE_URL"]      = get_secret("SUPABASE_URL")
os.environ["SUPABASE_ANON_KEY"] = get_secret("SUPABASE_ANON_KEY")
os.environ["DATABASE_URL"]      = get_secret("DATABASE_URL")

# ─── SUPABASE ────────────────────────────────────────────────
from supabase import create_client

supabase = create_client(
    get_secret("SUPABASE_URL"),
    get_secret("SUPABASE_ANON_KEY")
)

# ─── PAGE CONFIG ─────────────────────────────────────────────
st.set_page_config(
    page_title="AssistHR",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ─── GLOBAL CSS ──────────────────────────────────────────────
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet"/>

<style>
:root {
    --app-bg: #f3f6fb;
    --surface: #ffffff;
    --surface-2: #f8fafc;
    --text-main: #0f172a;
    --text-muted: #64748b;
    --border: #e2e8f0;
}
[data-theme="dark"], [data-user-theme="dark"] {
    --app-bg: #0b1220;
    --surface: #1e293b;
    --surface-2: #0f172a;
    --text-main: #f8fafc;
    --text-muted: #cbd5e1;
    --border: #475569;
}
[data-theme="dark"] [data-testid="stMain"] p,
[data-theme="dark"] [data-testid="stMain"] li,
[data-user-theme="dark"] [data-testid="stMain"] p,
[data-user-theme="dark"] [data-testid="stMain"] li {
    color: var(--text-main) !important;
}
[data-theme="dark"] label,
[data-user-theme="dark"] label,
[data-theme="dark"] [data-testid="stWidgetLabel"] p,
[data-user-theme="dark"] [data-testid="stWidgetLabel"] p {
    color: #e2e8f0 !important;
}
[data-theme="dark"] [data-testid="stCaption"],
[data-user-theme="dark"] [data-testid="stCaption"] {
    color: var(--text-muted) !important;
}
[data-theme="dark"] [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"],
[data-user-theme="dark"] [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] {
    color: #e2e8f0 !important;
}
[data-theme="dark"] .stSelectbox [data-baseweb="select"] span,
[data-user-theme="dark"] .stSelectbox [data-baseweb="select"] span {
    color: var(--text-main) !important;
}
[data-theme="dark"] [data-baseweb="popover"] li,
[data-user-theme="dark"] [data-baseweb="popover"] li {
    color: #0f172a !important;
}

/* ══════════════════════════════════════════════════════════
   RESET & BASE
══════════════════════════════════════════════════════════ */
html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}
[data-testid="stAppViewContainer"] {
    background: var(--app-bg) !important;
}
#MainMenu, footer { visibility: hidden; }

[data-testid="stHeader"]     { background: transparent !important}

/* Style the toggle button only — never override display/visibility/position */
[data-testid="stSidebarCollapsedControl"] button,
[data-testid="collapsedControl"] button {
    background     : linear-gradient(145deg, #1e293b 0%, #0f172a 100%) !important;
    border         : 2px solid rgba(148,163,184,.55) !important;
    border-radius  : 12px !important;
    box-shadow     : 0 4px 14px rgba(0,0,0,.35) !important;
    width          : 44px !important;
    height         : 44px !important;
    cursor         : pointer !important;
}
[data-testid="stSidebarCollapsedControl"] button:hover,
[data-testid="collapsedControl"] button:hover {
    border-color: rgba(96,165,250,.85) !important;
    box-shadow  : 0 6px 20px rgba(37,99,235,.35) !important;
}
[data-testid="stSidebarCollapsedControl"] button svg,
[data-testid="collapsedControl"] button svg {
    fill  : #f1f5f9 !important;
    width : 20px !important;
    height: 20px !important;
}

.block-container {
    padding-top   : 12px !important;
    padding-left  : 32px !important;
    padding-right : 32px !important;
    max-width     : 100% !important;
}
.app-topbar {
    background   : var(--surface);
    border       : 1px solid var(--border);
    border-radius: 12px;
    padding      : 10px 16px;
    margin-bottom: 18px;
    box-shadow   : 0 1px 3px rgba(15, 23, 42, 0.06);
}
.app-topbar-inner {
    display    : flex;
    align-items: center;
    gap        : 8px;
    flex-wrap  : wrap;
    font-family: 'Plus Jakarta Sans', sans-serif;
}
.app-topbar-brand { font-weight: 800; font-size: 15px; color: var(--text-main); }
.app-topbar-sep   { color: var(--text-muted); font-weight: 600; }
.app-topbar-page  { font-size: 13px; font-weight: 600; color: var(--text-muted); }

/* ══════════════════════════════════════════════════════════
   SIDEBAR — only style internals, never override dimensions
   or visibility so Streamlit JS can freely toggle it
══════════════════════════════════════════════════════════ */
[data-testid="stSidebar"] {
    background  : linear-gradient(180deg, #0f172a 0%, #111b34 100%) !important;
    border-right: 1px solid rgba(148,163,184,0.18) !important;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}
[data-testid="stSidebar"] .stRadio > div[role="radiogroup"],
[data-testid="stSidebar"] .stRadio > div {
    display       : flex !important;
    flex-direction: column !important;
    gap           : 4px !important;
    width         : 100% !important;
    align-items   : stretch !important;
}
[data-testid="stSidebar"] .stRadio label {
    color        : #94a3b8 !important;
    font-size    : 13.5px !important;
    font-weight  : 500 !important;
    padding      : 10px 12px !important;
    border-radius: 8px !important;
    transition   : all 0.18s ease !important;
    cursor       : pointer !important;
    width        : 100% !important;
    box-sizing   : border-box !important;
    margin       : 0 !important;
}
[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(255,255,255,0.07) !important;
    color     : #e2e8f0 !important;
}
[data-testid="stSidebar"] .stRadio label:has(input:checked) {
    background: linear-gradient(135deg, rgba(37,99,235,.25), rgba(56,189,248,.18)) !important;
    color     : #dbeafe !important;
    border    : 1px solid rgba(96,165,250,.45) !important;
}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: #94a3b8 !important;
}
/* Toggle button styles already defined above — no duplicate needed */
[data-testid="stSidebar"] kbd,
[data-testid="stSidebar"] [data-testid="stKeyboardShortcut"],
[data-testid="stSidebar"] .st-keyboard-shortcut {
    display: none !important;
}

/* ══════════════════════════════════════════════════════════
   METRIC CARDS
══════════════════════════════════════════════════════════ */
[data-testid="stMetric"] {
    border-radius  : 14px !important;
    padding        : 22px 24px !important;
    min-height     : 115px !important;
    display        : flex !important;
    flex-direction : column !important;
    justify-content: center !important;
    box-shadow     : 0 1px 4px rgba(0,0,0,0.06), 0 4px 16px rgba(0,0,0,0.04) !important;
    border         : 1px solid rgba(0,0,0,0.08) !important;
    transition     : transform 0.18s ease, box-shadow 0.18s ease !important;
    position       : relative !important;
    overflow       : hidden !important;
}
[data-testid="stMetric"]:hover {
    transform : translateY(-3px) !important;
    box-shadow: 0 8px 30px rgba(0,0,0,0.1) !important;
}
[data-testid="stMetricLabel"] p {
    font-size     : 10.5px !important;
    font-weight   : 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    white-space   : normal !important;
    word-break    : break-word !important;
    line-height   : 1.4 !important;
}
[data-testid="stMetricValue"] {
    font-size  : 26px !important;
    font-weight: 800 !important;
    line-height: 1.2 !important;
    white-space: normal !important;
    word-break : break-word !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}
[data-testid="column"] {
    display       : flex !important;
    flex-direction: column !important;
}
[data-testid="column"] [data-testid="stMetric"] {
    flex: 1 !important;
}
[data-theme="light"] [data-testid="stMetric"],
[data-user-theme="light"] [data-testid="stMetric"] {
    background: #ffffff !important;
    border    : 1px solid #e2e8f0 !important;
}
[data-theme="light"] [data-testid="stMetricLabel"] p,
[data-user-theme="light"] [data-testid="stMetricLabel"] p { color: #64748b !important; }
[data-theme="light"] [data-testid="stMetricValue"],
[data-user-theme="light"] [data-testid="stMetricValue"] { color: #0f172a !important; }
[data-theme="dark"] [data-testid="stMetric"],
[data-user-theme="dark"] [data-testid="stMetric"] {
    background: #1e293b !important;
    border    : 1px solid #334155 !important;
}
[data-theme="dark"] [data-testid="stMetricLabel"] p,
[data-user-theme="dark"] [data-testid="stMetricLabel"] p { color: #94a3b8 !important; }
[data-theme="dark"] [data-testid="stMetricValue"],
[data-user-theme="dark"] [data-testid="stMetricValue"] { color: #f1f5f9 !important; }

[data-testid="column"]:nth-child(1) [data-testid="stMetric"]::before {
    content: ''; position: absolute; top:0; left:0; right:0;
    height: 3px; background: linear-gradient(90deg, #2563eb, #3b82f6);
    border-radius: 14px 14px 0 0;
}
[data-testid="column"]:nth-child(2) [data-testid="stMetric"]::before {
    content: ''; position: absolute; top:0; left:0; right:0;
    height: 3px; background: linear-gradient(90deg, #0891b2, #22d3ee);
    border-radius: 14px 14px 0 0;
}
[data-testid="column"]:nth-child(3) [data-testid="stMetric"]::before {
    content: ''; position: absolute; top:0; left:0; right:0;
    height: 3px; background: linear-gradient(90deg, #7c3aed, #a78bfa);
    border-radius: 14px 14px 0 0;
}
[data-testid="column"]:nth-child(4) [data-testid="stMetric"]::before {
    content: ''; position: absolute; top:0; left:0; right:0;
    height: 3px; background: linear-gradient(90deg, #059669, #34d399);
    border-radius: 14px 14px 0 0;
}

/* ══════════════════════════════════════════════════════════
   BUTTONS
══════════════════════════════════════════════════════════ */
.stButton > button {
    font-family   : 'Plus Jakarta Sans', sans-serif !important;
    font-weight   : 600 !important;
    font-size     : 13px !important;
    border-radius : 10px !important;
    border        : none !important;
    transition    : all 0.18s ease !important;
    letter-spacing: 0.01em !important;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
    color     : #ffffff !important;
    box-shadow: 0 2px 8px rgba(37,99,235,0.3) !important;
    padding   : 12px 28px !important;
}
.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #1d4ed8, #1e40af) !important;
    transform : translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(37,99,235,0.4) !important;
}
.stButton > button[kind="secondary"] {
    background  : transparent !important;
    color       : #2563eb !important;
    border      : 1.5px solid #2563eb !important;
}
.stButton > button[kind="secondary"]:hover {
    background: #eff6ff !important;
}
[data-theme="dark"] .stButton > button[kind="secondary"],
[data-user-theme="dark"] .stButton > button[kind="secondary"] {
    color       : #e2e8f0 !important;
    border-color: #475569 !important;
    background  : rgba(30, 41, 59, 0.5) !important;
}
[data-theme="dark"] .stButton > button[kind="secondary"]:hover,
[data-user-theme="dark"] .stButton > button[kind="secondary"]:hover {
    background: rgba(51, 65, 85, 0.65) !important;
}
[data-testid="stSidebar"] .stButton > button[kind="secondary"] {
    color       : #cbd5e1 !important;
    border-color: #475569 !important;
}
[data-testid="stSidebar"] .stButton > button[kind="secondary"]:hover {
    background: rgba(255,255,255,0.06) !important;
}

/* ══════════════════════════════════════════════════════════
   INPUTS & SELECTBOX
══════════════════════════════════════════════════════════ */
.stTextInput input,
.stTextArea textarea {
    font-family  : 'Plus Jakarta Sans', sans-serif !important;
    border       : 1.5px solid var(--border) !important;
    border-radius: 10px !important;
    font-size    : 13.5px !important;
    transition   : all 0.18s ease !important;
    color        : var(--text-main) !important;
    background   : var(--surface) !important;
}
.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: #2563eb !important;
    box-shadow  : 0 0 0 3px rgba(37,99,235,0.12) !important;
}

/* ══════════════════════════════════════════════════════════
   FILE UPLOADER
/* ══════════════════════════════════════════════════════════

/* ══════════════════════════════════════════════════════════
   FILE UPLOADER — FINAL CLEAN VERSION
══════════════════════════════════════════════════════════ */

/* Wrapper cleanup */
[data-testid="stFileUploader"] {
    border: none !important;
    padding: 0 !important;
}

/* MAIN DROP AREA */
[data-testid="stFileUploader"] section {
    border: 2px dashed var(--border) !important;
    border-radius: 14px !important;
    background: var(--surface-2) !important;
    padding: 30px 20px !important;
    text-align: center !important;
    transition: all 0.25s ease !important;
    cursor: pointer !important;
}

/* LIGHT HOVER */
[data-testid="stFileUploader"] section:hover {
    border-color: #3b82f6 !important;
    background: #eff6ff !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.10) !important;
}

/* DARK MODE BASE */
[data-theme="dark"] [data-testid="stFileUploader"] section,
[data-user-theme="dark"] [data-testid="stFileUploader"] section {
    background: #0b1220 !important;
    border: 2px dashed #334155 !important;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.03) !important;
}

/* DARK HOVER */
[data-theme="dark"] [data-testid="stFileUploader"] section:hover,
[data-user-theme="dark"] [data-testid="stFileUploader"] section:hover {
    border-color: #60a5fa !important;
    background: linear-gradient(
        135deg,
        rgba(37,99,235,0.25),
        rgba(14,165,233,0.18)
    ) !important;
    box-shadow: 
        0 0 0 3px rgba(96,165,250,0.18),
        0 10px 30px rgba(0,0,0,0.5) !important;
}

/* ══════════════════════════════════════════════════════════
   REMOVE DEFAULT ELEMENTS
══════════════════════════════════════════════════════════ */

/* Remove upload button */
[data-testid="stFileUploader"] section button {
    display: none !important;
}

/* Remove "200MB limit" text */
[data-testid="stFileUploader"] small,
[data-testid="stFileUploader"] section small {
    display: none !important;
}

/* Hide default text (without breaking layout) */
[data-testid="stFileUploader"] section div {
    font-size: 0 !important;
}

/* ══════════════════════════════════════════════════════════
   CUSTOM LABEL
══════════════════════════════════════════════════════════ */

[data-testid="stFileUploader"] section::before {
    content: "📄 Drag & drop your file or click to upload";
    display: block;
    font-size: 14px;
    font-weight: 600;
    color: var(--text-muted);
    text-align: center;
}

/* ══════════════════════════════════════════════════════════
   ICON STYLING
══════════════════════════════════════════════════════════ */

[data-testid="stFileUploader"] section svg {
    fill: #64748b !important;
    margin-bottom: 8px;
    transition: all 0.2s ease !important;
}

[data-testid="stFileUploader"] section:hover svg {
    fill: #3b82f6 !important;
}

/* DARK ICON */
[data-theme="dark"] [data-testid="stFileUploader"] section svg,
[data-user-theme="dark"] [data-testid="stFileUploader"] section svg {
    fill: #475569 !important;
}

[data-theme="dark"] [data-testid="stFileUploader"] section:hover svg,
[data-user-theme="dark"] [data-testid="stFileUploader"] section:hover svg {
    fill: #93c5fd !important;
}
            
[data-testid="stFileUploader"] section > div:last-child {
    display: none !important;
}
/* ══════════════════════════════════════════════════════════
   EXPANDER
══════════════════════════════════════════════════════════ */
[data-testid="stExpander"] {
    border       : 1.5px solid var(--border) !important;
    border-radius: 14px !important;
    background   : var(--surface) !important;
    box-shadow   : 0 1px 4px rgba(0,0,0,0.05) !important;
    margin-bottom: 14px !important;
    overflow     : hidden !important;
    transition   : all 0.18s ease !important;
}
[data-testid="stExpander"]:hover {
    box-shadow: 0 6px 24px rgba(0,0,0,0.08) !important;
    transform : translateY(-1px) !important;
}
[data-theme="dark"] [data-testid="stExpander"],
[data-user-theme="dark"] [data-testid="stExpander"] {
    background  : #1e293b !important;
    border-color: #334155 !important;
}

/* ══════════════════════════════════════════════════════════
   CHAT MESSAGES
══════════════════════════════════════════════════════════ */
[data-testid="stChatMessage"] {
    border-radius: 14px !important;
    margin-bottom: 10px !important;
    border       : 1px solid var(--border) !important;
    box-shadow   : 0 1px 4px rgba(0,0,0,0.04) !important;
}
[data-theme="dark"] [data-testid="stChatMessage"],
[data-user-theme="dark"] [data-testid="stChatMessage"] { border-color: #334155 !important; }
[data-testid="stChatMessageAvatarUser"]      { background: linear-gradient(135deg, #2563eb, #3b82f6) !important; color: #ffffff !important; }
[data-testid="stChatMessageAvatarAssistant"] { background: linear-gradient(135deg, #0891b2, #14b8a6) !important; color: #ffffff !important; }

  /* ══════════════════════════════════════════════════════════
   CHAT INPUT — IMPROVED (modern bot style, full dark/light support)
/* ══════════════════════════════════════════════════════════
   CHAT INPUT — FULLY FIXED, DARK & LIGHT, AUTO-EXPANDING
══════════════════════════════════════════════════════════ */

/* ============================= */
/* WRAPPER / FOOTER CONSISTENCY */
/* ============================= */
.stBottom {
    background: var(--surface) !important;
    padding: 12px 20px !important;
    display: flex !important;
    justify-content: center !important;
}

[data-theme="dark"] .stBottom,
[data-user-theme="dark"] .stBottom {
    background: #0f172a !important; /* uniform dark footer */
}

/* ============================= */
/* MAIN CHAT INPUT CONTAINER */
/* ============================= */
[data-testid="stChatInput"] {
    display: flex !important;
    flex-direction: row !important;
    align-items: flex-end !important;
    width: 100% !important;
}

/* INPUT BOX WRAPPER */
[data-testid="stChatInput"] > div {
    flex-grow: 1 !important;
    border-radius: 28px !important;
    border: 1.5px solid rgba(59,130,246,0.35) !important;
    background: #ffffff !important;
    box-shadow: 0 6px 20px rgba(0,0,0,0.08) !important;
    transition: all 0.25s ease !important;
    display: flex !important;
    align-items: center !important;
    padding: 6px 14px !important;
    min-height: 44px !important;
}

/* DARK MODE INPUT BOX */
[data-theme="dark"] [data-testid="stChatInput"] > div,
[data-user-theme="dark"] [data-testid="stChatInput"] > div {
    background: #0f172a !important;
    border: 1.5px solid rgba(96,165,250,0.4) !important;
    box-shadow: 0 10px 35px rgba(0,0,0,0.6) !important;
    color: #f1f5f9 !important; /* make user input text visible */
}

/* FOCUS EFFECT */
[data-testid="stChatInput"] > div:focus-within {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 4px rgba(59,130,246,0.2),
                0 10px 30px rgba(37,99,235,0.25) !important;
}

[data-theme="dark"] [data-testid="stChatInput"] > div:focus-within,
[data-user-theme="dark"] [data-testid="stChatInput"] > div:focus-within {
    border-color: #60a5fa !important;
    box-shadow: 0 0 0 4px rgba(96,165,250,0.25),
                0 12px 40px rgba(37,99,235,0.4) !important;
}

/* ============================= */
/* TEXT AREA STYLING (AUTO-EXPAND) */
/* ============================= */
[data-testid="stChatInput"] textarea {
    flex-grow: 1 !important;
    background: transparent !important;
    color: inherit !important;
    border: none !important;
    outline: none !important;
    resize: none !important;
    overflow: hidden !important;
    min-height: 28px !important;
    line-height: 1.4em !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 14px !important;
    padding: 8px 0 !important;
    color: #111827 !important; /* light theme text */
}

[data-theme="dark"] [data-testid="stChatInput"] textarea,
[data-user-theme="dark"] [data-testid="stChatInput"] textarea {
    color: #f1f5f9 !important; /* dark theme text visible */
}

/* ============================= */
/* SEND BUTTON FIXED POSITION */
/* ============================= */
[data-testid="stChatInput"] button {
    border-radius: 50% !important;
    background: #3b82f6 !important;
    color: white !important;
    width: 42px !important;
    height: 42px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    margin-left: 8px !important;
    flex-shrink: 0 !important;
    box-shadow: 0 4px 14px rgba(59,130,246,0.35) !important;
}

/* DARK MODE SEND BUTTON */
[data-theme="dark"] [data-testid="stChatInput"] button,
[data-user-theme="dark"] [data-testid="stChatInput"] button {
    background: #60a5fa !important;
    box-shadow: 0 6px 20px rgba(96,165,250,0.45) !important;
}

/* SEND ICON */
[data-testid="stChatInput"] button svg {
    fill: white !important;
    width: 18px !important;
    height: 18px !important;
}

/* ============================= */
/* HELPER TEXT BELOW INPUT (optional) */
/* ============================= */
.rag-helper-text {
    text-align: center;
    font-size: 13px;
    margin-top: 6px;
    color: var(--text-muted);
    width: 100%;
}

[data-theme="dark"] .rag-helper-text,
[data-user-theme="dark"] .rag-helper-text {
    color: #94a3b8;
}

/* ============================= */
/* FULL FOOTER BACKGROUND DARK MODE */
/* ============================= */
[data-theme="dark"] .stBottom,
[data-user-theme="dark"] .stBottom {
    background-color: #0f172a !important;
}

 /* ============================= */
/* FORCE FOOTER DARK MODE UNIFORMITY */
/* ============================= */
[data-theme="dark"] .stBottom,
[data-user-theme="dark"] .stBottom,
[data-theme="dark"] section > .stBottom,
[data-user-theme="dark"] section > .stBottom,
[data-theme="dark"] .withScreencast .stBottom,
[data-user-theme="dark"] .withScreencast .stBottom {
    background: #0f172a !important;  /* solid dark background */
    color: #f1f5f9 !important;       /* ensure text/icons are visible */
}
/* ============================= */
/* OPTIONAL: smooth hover effect for send button */
[data-testid="stChatInput"] button:hover {
    filter: brightness(1.1) !important;
}
/* ══════════════════════════════════════════════════════════
   MISC
══════════════════════════════════════════════════════════ */
.stSuccess, .stError, .stInfo, .stWarning { border-radius: 10px !important; font-family: 'Plus Jakarta Sans', sans-serif !important; }
hr { border-color: var(--border) !important; margin: 20px 0 !important; }
[data-testid="stProgress"] > div > div { background: linear-gradient(90deg, #2563eb, #0891b2) !important; border-radius: 99px !important; }

.chip-green { display:inline-block; padding:3px 10px; border-radius:99px; font-size:11.5px; font-weight:600; background:#d1fae5; color:#059669; border:1px solid #a7f3d0; margin:2px; }
.chip-red   { display:inline-block; padding:3px 10px; border-radius:99px; font-size:11.5px; font-weight:600; background:#fee2e2; color:#dc2626; border:1px solid #fca5a5; margin:2px; }
.verdict-badge { display:inline-block; padding:4px 12px; border-radius:99px; font-size:11px; font-weight:700; }
.doc-row {
    display: flex; align-items: center; gap: 12px;
    padding: 11px 16px; border-radius: 10px; margin-bottom: 6px;
    border: 1px solid #e2e8f0; background: #ffffff;
    transition: all 0.18s ease; font-size: 13.5px; font-weight: 500; color: #334155;
}
.doc-row:hover { border-color: #2563eb; box-shadow: 0 0 0 3px rgba(37,99,235,0.08); }
[data-theme="dark"] .doc-row,
[data-user-theme="dark"] .doc-row { background: #1e293b; border-color: #334155; color: #cbd5e1; }
.doc-badge { font-size:10px; padding:2px 8px; border-radius:99px; background:#eff6ff; color:#2563eb; font-weight:700; text-transform:uppercase; margin-left:auto; }
[data-theme="dark"] .doc-badge,
[data-user-theme="dark"] .doc-badge { background:#1e3a5f; color:#60a5fa; }
.info-row { display:flex; justify-content:space-between; align-items:center; padding:9px 0; border-bottom:1px solid #f1f5f9; font-size:13px; }
.info-val { font-size:11.5px; font-weight:700; background:#f1f5f9; padding:3px 10px; border-radius:99px; color:#0f172a; }
[data-theme="dark"] .info-val  { background:#334155; color:#f1f5f9; }
[data-theme="dark"] .info-row,
[data-user-theme="dark"] .info-row { border-color:#1e293b; color:#94a3b8; }
.card { background:#ffffff; border:1px solid #e2e8f0; border-radius:14px; overflow:hidden; box-shadow:0 1px 4px rgba(0,0,0,0.06); margin-bottom:20px; }
[data-theme="dark"] .card { background:#1e293b; border-color:#334155; }
.card-head { padding:16px 22px; border-bottom:1px solid #e2e8f0; display:flex; align-items:center; justify-content:space-between; }
[data-theme="dark"] .card-head { border-color:#334155; }
.card-title { font-size:14px; font-weight:700; color:#0f172a; }
[data-theme="dark"] .card-title { color:#f1f5f9; }
.card-body { padding:20px 22px; }
.step-item  { display:flex; gap:12px; align-items:flex-start; margin-bottom:18px; }
.step-num   { min-width:30px; height:30px; border-radius:8px; color:#ffffff; display:flex; align-items:center; justify-content:center; font-weight:800; font-size:13px; flex-shrink:0; }
.step-title { font-size:13.5px; font-weight:700; color:#0f172a; margin-bottom:3px; }
[data-theme="dark"] .step-title,
[data-user-theme="dark"] .step-title { color:#f1f5f9; }
.step-desc { font-size:12.5px; color:#64748b; line-height:1.5; }
.section-title { font-size:22px; font-weight:800; color:#0f172a; margin:0 0 4px 0; font-family:'Plus Jakarta Sans',sans-serif; }
[data-theme="dark"] .section-title,
[data-user-theme="dark"] .section-title { color:#f1f5f9; }
.section-sub { font-size:13.5px; color:var(--text-muted); margin-bottom:22px; }
.card-sub    { font-size:11.5px; color:var(--text-muted); }
.field-label { font-size:12px; font-weight:700; color:var(--text-main); margin-bottom:6px; font-family:'Plus Jakarta Sans',sans-serif; }
.upload-preview { display:flex; align-items:center; gap:10px; padding:10px 14px; background:rgba(37,99,235,0.08); border:1px solid rgba(37,99,235,0.22); border-radius:10px; font-size:12.5px; margin-top:8px; }
.upload-preview-name { flex:1; font-weight:600; color:#2563eb; }
.upload-preview-meta { color:var(--text-muted); }
.callout-info { margin-top:14px; padding:12px 16px; background:rgba(37,99,235,0.08); border:1px solid rgba(37,99,235,0.2); border-radius:10px; font-size:12.5px; color:var(--text-main); line-height:1.55; }
[data-theme="dark"] .callout-info,
[data-user-theme="dark"] .callout-info { background:rgba(30,58,138,0.25); border-color:rgba(96,165,250,0.28); }
.empty-state { text-align:center; padding:36px 24px 20px; }
.empty-state-title { font-size:18px; font-weight:700; color:var(--text-main); margin-bottom:6px; font-family:'Plus Jakarta Sans',sans-serif; }
.empty-state-sub { font-size:13px; color:var(--text-muted); max-width:340px; margin:0 auto; line-height:1.55; }
.body-text { font-size:12.5px; color:var(--text-main); line-height:1.8; }
.body-text a { color:#2563eb; font-weight:600; }
[data-theme="dark"] .body-text a,
[data-user-theme="dark"] .body-text a { color:#60a5fa; }
.insight-box { background:var(--surface-2); border-radius:10px; padding:14px 16px; font-size:12.5px; line-height:1.7; color:var(--text-main); border:1px solid var(--border); }
.score-track { height:6px; background:var(--border); border-radius:99px; overflow:hidden; }
.detailed-results-title { font-size:15px; font-weight:700; color:var(--text-main); margin-bottom:12px; font-family:'Plus Jakarta Sans',sans-serif; }
.skill-section-label { font-size:10.5px; font-weight:700; color:var(--text-muted); text-transform:uppercase; letter-spacing:0.7px; margin-bottom:8px; }
[data-theme="dark"] .step-desc,
[data-user-theme="dark"] .step-desc { color:var(--text-muted); }
[data-theme="dark"] .upload-preview,
[data-user-theme="dark"] .upload-preview { background:rgba(37,99,235,0.14); border-color:rgba(96,165,250,0.35); }
[data-theme="dark"] .upload-preview-name,
[data-user-theme="dark"] .upload-preview-name { color:#93c5fd; }
            

/* FORCE override Streamlit default red */
input:focus, textarea:focus, input:hover, textarea:hover {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 2px rgba(59,130,246,0.15) !important;
    outline: none !important;
}    

/* ============================= */
/* CHAT INPUT CONTAINER — DARK MODE FIX */
/* ============================= */
[data-theme="dark"] [data-testid="stChatInput"],
[data-user-theme="dark"] [data-testid="stChatInput"] {
    background: #0f172a !important;      /* uniform dark background for container */
    border-radius: 28px !important;
    padding: 8px 12px !important;        /* optional, to match real bot style */
    box-shadow: 0 6px 20px rgba(0,0,0,0.5) !important;
}

/* ACTUAL INPUT BOX (textarea wrapper) */
[data-theme="dark"] [data-testid="stChatInput"] > div,
[data-user-theme="dark"] [data-testid="stChatInput"] > div {
    background: #0f172a !important;      /* match container */
    border: 1.5px solid rgba(96,165,250,0.4) !important;
    color: #f1f5f9 !important;           /* text inside input */
}

/* TEXTAREA ITSELF */
[data-theme="dark"] [data-testid="stChatInput"] textarea,
[data-user-theme="dark"] [data-testid="stChatInput"] textarea {
    background: transparent !important;   /* already handled by parent */
    color: #f1f5f9 !important;            /* ensures typing text is visible */
}

/* SEND BUTTON */
[data-theme="dark"] [data-testid="stChatInput"] button,
[data-user-theme="dark"] [data-testid="stChatInput"] button {
    background: #60a5fa !important;
    color: #fff !important;
    box-shadow: 0 6px 20px rgba(96,165,250,0.45) !important;
}    
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# AUTH
# ══════════════════════════════════════════════════════════════

def login_page():
    st.markdown("""
    <div style="max-width:440px; margin:60px auto 0;">
        <div style="background:linear-gradient(135deg,#0f172a 0%,#1e3a5f 100%);
                    border-radius:20px; padding:40px 36px 32px;
                    text-align:center; margin-bottom:24px;
                    position:relative; overflow:hidden;">
            <div style="position:absolute;right:-30px;top:-30px;width:160px;height:160px;
                        border-radius:50%;background:rgba(37,99,235,0.25);"></div>
            <div style="position:absolute;left:-20px;bottom:-40px;width:120px;height:120px;
                        border-radius:50%;background:rgba(8,145,178,0.2);"></div>
            <div style="font-size:52px;margin-bottom:12px;position:relative;z-index:1;">🤖</div>
            <div style="font-size:28px;font-weight:800;color:#ffffff;
                        position:relative;z-index:1;font-family:'Plus Jakarta Sans',sans-serif;">
                AssistHR
            </div>
            <div style="font-size:11px;color:#60a5fa;font-weight:700;letter-spacing:2px;
                        text-transform:uppercase;margin-top:4px;position:relative;z-index:1;">
                AI · HR · Intelligence
            </div>
            <div style="display:flex;gap:8px;justify-content:center;flex-wrap:wrap;
                        margin-top:16px;position:relative;z-index:1;">
                <span style="padding:4px 10px;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.15);border-radius:99px;font-size:11px;color:#cbd5e1;">🧠 RAG</span>
                <span style="padding:4px 10px;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.15);border-radius:99px;font-size:11px;color:#cbd5e1;">⚡ Groq</span>
                <span style="padding:4px 10px;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.15);border-radius:99px;font-size:11px;color:#cbd5e1;">🗄️ pgvector</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    _, col, _ = st.columns([1, 2, 1])
    with col:
        tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])
        with tab1:
            email    = st.text_input("Email", key="login_email", placeholder="you@company.com")
            password = st.text_input("Password", type="password", key="login_pass", placeholder="••••••••")
            if st.button("Login →", use_container_width=True, type="primary", key="login_btn"):
                if not email or not password:
                    st.error("Please fill in all fields.")
                else:
                    try:
                        r = supabase.auth.sign_in_with_password({"email": email, "password": password})
                        st.session_state.user  = r.user
                        st.session_state.token = r.session.access_token
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Login failed: {e}")
        with tab2:
            name     = st.text_input("Full Name", key="reg_name", placeholder="John Smith")
            email    = st.text_input("Email", key="reg_email", placeholder="you@company.com")
            password = st.text_input("Password", type="password", key="reg_pass", placeholder="Min 6 characters")
            confirm  = st.text_input("Confirm Password", type="password", key="reg_confirm", placeholder="Repeat password")
            if st.button("Create Account →", use_container_width=True, type="primary", key="reg_btn"):
                if not all([name, email, password, confirm]):
                    st.error("Please fill in all fields.")
                elif len(password) < 6:
                    st.error("Password must be at least 6 characters.")
                elif password != confirm:
                    st.error("Passwords do not match.")
                else:
                    try:
                        supabase.auth.sign_up({"email": email, "password": password, "options": {"data": {"name": name}}})
                        st.success("✅ Account created! Please login.")
                    except Exception as e:
                        st.error(f"❌ {e}")


def logout():
    try:
        supabase.auth.sign_out()
    except Exception:
        pass
    st.session_state.user  = None
    st.session_state.token = None
    st.rerun()


# ── CHECK AUTH ────────────────────────────────────────────────
if "user" not in st.session_state:
    st.session_state.user  = None
    st.session_state.token = None

if not st.session_state.user:
    login_page()
    st.stop()

current_user  = st.session_state.user
current_email = current_user.email


# ══════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════

st.sidebar.markdown(f"""
<div style="padding:20px 16px 16px;">
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;">
        <div style="width:38px;height:38px;background:#2563eb;border-radius:10px;
                    display:flex;align-items:center;justify-content:center;font-size:18px;">🤖</div>
        <div>
            <div style="color:#ffffff;font-size:17px;font-weight:800;line-height:1;font-family:'Plus Jakarta Sans',sans-serif;">AssistHR</div>
            <div style="color:#475569;font-size:9.5px;letter-spacing:1.2px;text-transform:uppercase;margin-top:1px;">AI HR Assistant</div>
        </div>
    </div>
</div>
<div style="padding:2px 16px 6px;">
    <div style="color:#475569;font-size:9px;letter-spacing:1.5px;text-transform:uppercase;font-weight:700;margin-bottom:4px;">Main Menu</div>
</div>
""", unsafe_allow_html=True)

if "ui_theme" not in st.session_state:
    st.session_state.ui_theme = "System"

theme_choice = st.sidebar.selectbox(
    "Theme",
    ["System", "Light", "Dark"],
    index=["System", "Light", "Dark"].index(st.session_state.ui_theme),
    key="ui_theme",
)

components.html(f"""
<script>
(function() {{
  const root = window.parent.document.documentElement;
  const app  = window.parent.document.querySelector('[data-testid="stAppViewContainer"]');
  const main = window.parent.document.querySelector('[data-testid="stMain"]');
  const choice = "{theme_choice}";
  let mode = "light";
  if (choice === "Dark") mode = "dark";
  else if (choice === "System") {{
    mode = window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }}
  root.setAttribute("data-user-theme", mode);
  root.setAttribute("data-theme", mode);
  if (app)  app.setAttribute("data-theme", mode);
  if (main) main.setAttribute("data-theme", mode);
  const body = window.parent.document.body;
  if (body) body.setAttribute("data-user-theme", mode);

  function stripHints() {{
    const doc = window.parent.document;
    doc.querySelectorAll('[data-testid="stSidebar"] button[title],[data-testid="stSidebar"] [title]').forEach(function(el) {{
      const t = (el.getAttribute("title") || "") + (el.getAttribute("aria-label") || "");
      if (/keyboard|shortcut|Press |⌘|Ctrl|\\[/i.test(t)) {{
        el.removeAttribute("title");
        el.removeAttribute("aria-label");
      }}
    }});
  }}
  stripHints();
  [200, 600, 1200].forEach(function(ms) {{ setTimeout(stripHints, ms); }});
  try {{
    const obs = new MutationObserver(stripHints);
    const sb  = window.parent.document.querySelector('[data-testid="stSidebar"]');
    if (sb) obs.observe(sb, {{ childList: true, subtree: true, attributes: true }});
  }} catch(e) {{}}
}})();
</script>
""", height=0)

page = st.sidebar.radio(
    "nav",
    ["📊  Dashboard", "📚  Knowledge Base", "💬  HR Q&A", "📄  Resume Screener"],
    label_visibility="collapsed"
)

st.sidebar.markdown("<div style='margin-top:12px'></div>", unsafe_allow_html=True)

if page == "💬  HR Q&A":
    st.sidebar.markdown("""
    <div style="padding:0 16px 6px;">
        <div style="color:#64748b;font-size:9px;letter-spacing:1.4px;text-transform:uppercase;font-weight:700;">
            Chat Sessions
        </div>
    </div>
    """, unsafe_allow_html=True)

    if "active_session" not in st.session_state:
        st.session_state.active_session = "default"

    if st.sidebar.button("＋ New Session", use_container_width=True, key="new_session_btn"):
        import time
        st.session_state.active_session = f"chat-{int(time.time())}"
        st.session_state.messages       = []
        st.session_state.last_session   = ""
        st.rerun()

    try:
        from chat_store import get_conn as _gc
        _conn = _gc()
        _cur  = _conn.cursor()
        _cur.execute(
            "SELECT session_id FROM sessions WHERE session_id LIKE %s ORDER BY last_active DESC LIMIT 8",
            (f"{current_email}_%",)
        )
        _rows = _cur.fetchall()
        _conn.close()
        for row in _rows:
            raw      = row[0]
            disp     = raw.split("_", 1)[1] if "_" in raw else raw
            is_active = disp == st.session_state.active_session
            icon = "🤖" if is_active else "💬"
            if st.sidebar.button(f"{icon}  {disp}", key=f"chat_session_{raw}",
                                  use_container_width=True,
                                  type="primary" if is_active else "secondary"):
                st.session_state.active_session = disp
                st.session_state.messages       = []
                st.session_state.last_session   = ""
                st.rerun()
    except Exception:
        pass

st.sidebar.divider()

st.sidebar.markdown(f"""
<div style="padding:0 4px;">
    <div style="display:flex;align-items:center;gap:8px;background:rgba(255,255,255,0.05);
                border-radius:8px;padding:10px 12px;margin-bottom:10px;">
        <div style="width:7px;height:7px;background:#22c55e;border-radius:50%;flex-shrink:0;"></div>
        <div>
            <div style="color:#e2e8f0;font-size:11px;font-weight:700;">System Ready</div>
            <div style="color:#64748b;font-size:10px;margin-top:1px;">RAG · Supabase pgvector · Groq</div>
        </div>
    </div>
    <div style="color:#64748b;font-size:11px;padding:2px 2px 8px;">👤 {current_email}</div>
</div>
""", unsafe_allow_html=True)

if st.sidebar.button("Logout", use_container_width=True, key="logout_btn"):
    logout()

st.sidebar.markdown("""
<div style="padding:12px 4px 4px;text-align:center;">
    <div style="color:#334155;font-size:10px;font-family:'JetBrains Mono',monospace;">
        AssistHR v1.0 · MIT License
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="app-topbar">
    <div class="app-topbar-inner">
        <span class="app-topbar-brand">AssistHR</span>
        <span class="app-topbar-sep">·</span>
        <span class="app-topbar-page">{page}</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════════════

if page == "📊  Dashboard":
    st.markdown("""
    <div style="background:linear-gradient(135deg,#0f172a 0%,#1e3a5f 100%);
                border-radius:18px; padding:32px 36px; margin-bottom:24px;
                position:relative; overflow:hidden;">
        <div style="position:absolute;right:-50px;top:-50px;width:220px;height:220px;
                    border-radius:50%;background:rgba(37,99,235,0.25);"></div>
        <div style="position:absolute;right:100px;bottom:-70px;width:170px;height:170px;
                    border-radius:50%;background:rgba(8,145,178,0.18);"></div>
        <div style="position:relative;z-index:1;">
            <h2 style="color:#ffffff;margin:0;font-size:24px;font-weight:800;font-family:'Plus Jakarta Sans',sans-serif;">
                Welcome to <span style="color:#60a5fa;">AssistHR</span> 🤖
            </h2>
            <p style="color:#94a3b8;margin:8px 0 16px;font-size:13.5px;line-height:1.6;max-width:520px;">
                AI-powered HR assistant built with RAG, Groq LLM and Supabase pgvector.
                Upload HR policies, ask questions, screen resumes — all in one place.
            </p>
            <div style="display:flex;gap:8px;flex-wrap:wrap;">
                <span style="padding:5px 13px;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.15);border-radius:99px;font-size:11.5px;color:#cbd5e1;">🧠 RAG Pipeline</span>
                <span style="padding:5px 13px;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.15);border-radius:99px;font-size:11.5px;color:#cbd5e1;">🔍 Semantic Search</span>
                <span style="padding:5px 13px;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.15);border-radius:99px;font-size:11.5px;color:#cbd5e1;">📊 Resume Ranking</span>
                <span style="padding:5px 13px;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.15);border-radius:99px;font-size:11.5px;color:#cbd5e1;">⚡ Supabase pgvector</span>
                <span style="padding:5px 13px;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.15);border-radius:99px;font-size:11.5px;color:#cbd5e1;">🤖 Groq llama-3.3-70b</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    from embedding import get_existing_files
    try:
        all_docs   = get_existing_files()
        docs_count = len(all_docs)
    except Exception:
        all_docs   = set()
        docs_count = 0

    try:
        from chat_store import get_conn as _gc_dash
        _cd    = _gc_dash()
        _cur_d = _cd.cursor()
        _cur_d.execute("SELECT COUNT(*) FROM sessions WHERE session_id LIKE %s", (f"{current_email}_%",))
        sessions_count = _cur_d.fetchone()[0]
        _cur_d.execute(
            "SELECT session_id FROM sessions WHERE session_id LIKE %s ORDER BY last_active DESC LIMIT 6",
            (f"{current_email}_%",)
        )
        dash_session_rows = _cur_d.fetchall()
        _cd.close()
    except Exception:
        sessions_count    = 0
        dash_session_rows = []

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("📄  Documents",    docs_count,      help="HR documents in knowledge base")
    with c2: st.metric("💬  Chat Sessions", sessions_count,  help="Your saved HR Q&A sessions")
    with c3: st.metric("🤖  LLM",          "Groq",          help="llama-3.3-70b-versatile")
    with c4: st.metric("✅  Status",        "Online",        help="All systems operational")

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    col_left, col_right = st.columns([1.6, 1], gap="medium")
    with col_left:
        st.markdown("""
        <div class="card"><div class="card-head"><div class="card-title">📖 How to Use AssistHR</div></div>
        <div class="card-body">
            <div class="step-item">
                <div class="step-num" style="background:#2563eb;">1</div>
                <div><div class="step-title">Upload HR Documents</div>
                <div class="step-desc">Go to <b>Knowledge Base</b> → Upload HR policy files (PDF, DOCX, TXT). They get indexed automatically.</div></div>
            </div>
            <div class="step-item">
                <div class="step-num" style="background:#0891b2;">2</div>
                <div><div class="step-title">Ask Questions (RAG)</div>
                <div class="step-desc">Go to <b>HR Q&A</b> → Type any question. AssistHR searches your documents and answers using Groq LLM.</div></div>
            </div>
            <div class="step-item" style="margin-bottom:0">
                <div class="step-num" style="background:#d97706;">3</div>
                <div><div class="step-title">Screen Resumes</div>
                <div class="step-desc">Go to <b>Resume Screener</b> → Upload JD + resumes → get ranked candidates with scores and skill analysis.</div></div>
            </div>
        </div></div>
        """, unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="card"><div class="card-head"><div class="card-title">⚙️ System Info</div></div><div class="card-body">', unsafe_allow_html=True)
        for label, value in [
            ("🤖 LLM",        "Groq llama-3.3-70b"),
            ("⚡ Vector DB",  "Supabase pgvector"),
            ("📐 Embeddings", "MiniLM-L12-v2"),
            ("🔍 Search",     "Cosine Similarity"),
            ("🗄️ Database",   "Supabase PostgreSQL"),
            ("🔐 Auth",       "Supabase Auth"),
        ]:
            st.markdown(f'<div class="info-row"><span style="color:#64748b;font-size:12.5px;">{label}</span><span class="info-val">{value}</span></div>', unsafe_allow_html=True)
        st.markdown("</div></div>", unsafe_allow_html=True)

    dc, sc = st.columns([1.55, 1], gap="medium")
    with dc:
        st.markdown(f'<div class="card"><div class="card-head"><div class="card-title">📁 Recent Documents</div><span class="card-sub">{docs_count} file{"s" if docs_count!=1 else ""}</span></div><div class="card-body">', unsafe_allow_html=True)
        if not all_docs:
            st.info("No documents yet. Upload from Knowledge Base.")
        else:
            icons = {"pdf": "📕", "docx": "📘", "txt": "📄"}
            for doc in list(all_docs)[:6]:
                ext  = doc.split(".")[-1].lower() if "." in doc else "file"
                icon = icons.get(ext, "📄")
                st.markdown(f'<div class="doc-row"><span style="font-size:18px;">{icon}</span><span style="flex:1;font-size:13px;font-weight:600;">{doc}</span><span class="doc-badge">{ext}</span></div>', unsafe_allow_html=True)
        st.markdown("</div></div>", unsafe_allow_html=True)

    with sc:
        st.markdown(f'<div class="card"><div class="card-head"><div class="card-title">💬 Chat Sessions</div><span class="card-sub">{sessions_count} saved</span></div><div class="card-body">', unsafe_allow_html=True)
        if not dash_session_rows:
            st.info("No sessions yet. Open **HR Q&A** to start chatting.")
        else:
            for row in dash_session_rows:
                raw  = row[0]
                disp = raw.split("_", 1)[1] if "_" in raw else raw
                st.markdown(f'<div class="doc-row"><span style="font-size:18px;">💬</span><span style="flex:1;font-size:13px;font-weight:600;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{disp}</span><span class="doc-badge">chat</span></div>', unsafe_allow_html=True)
        st.markdown("</div></div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# KNOWLEDGE BASE
# ══════════════════════════════════════════════════════════════

elif page == "📚  Knowledge Base":
    st.markdown('<p class="section-title">📚 Knowledge Base</p><p class="section-sub">Upload and manage HR documents</p>', unsafe_allow_html=True)

    from document_loader import load_document
    from chunking        import chunk_documents
    from embedding       import create_vector_store, get_existing_files

    st.markdown('<div class="card"><div class="card-head"><div class="card-title">📁 Upload HR Document</div><span class="card-sub">PDF · DOCX · TXT</span></div><div class="card-body">', unsafe_allow_html=True)

    uploaded = st.file_uploader("Drop file here or click to browse", type=["pdf", "docx", "txt"], label_visibility="visible")
    if uploaded:
        c1, c2 = st.columns([3, 1])
        with c1:
            st.markdown(f'<div class="upload-preview"><span>📄</span><span class="upload-preview-name">{uploaded.name}</span><span class="upload-preview-meta">{uploaded.size/1024:.1f} KB</span></div>', unsafe_allow_html=True)
        with c2:
            if st.button("⬆️ Process", use_container_width=True, type="primary"):
                with st.spinner(f"Processing '{uploaded.name}'..."):
                    tmp = f"/tmp/{uploaded.name}"
                    with open(tmp, "wb") as f:
                        f.write(uploaded.getbuffer())
                    try:
                        docs   = load_document(tmp)
                        chunks = chunk_documents(docs)
                        create_vector_store(chunks)
                        st.success(f"✅ '{uploaded.name}' — {len(chunks)} chunks indexed")
                    except Exception as e:
                        st.error(f"❌ {e}")
                    finally:
                        if os.path.exists(tmp):
                            os.remove(tmp)
    st.markdown("</div></div>", unsafe_allow_html=True)

    st.markdown('<div class="card"><div class="card-head"><div class="card-title">📚 Indexed Documents</div></div><div class="card-body">', unsafe_allow_html=True)
    try:
        existing = get_existing_files()
        if not existing:
            st.info("No documents yet. Upload above.")
        else:
            icons = {"pdf": "📕", "docx": "📘", "txt": "📄"}
            for doc in existing:
                ext  = doc.split(".")[-1].lower() if "." in doc else "file"
                icon = icons.get(ext, "📄")
                st.markdown(f'<div class="doc-row"><span style="font-size:18px;">{icon}</span><span style="flex:1;font-size:13px;font-weight:600;">{doc}</span><span class="doc-badge">{ext}</span></div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Could not load: {e}")
    st.markdown("</div></div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# HR Q&A
# ══════════════════════════════════════════════════════════════

elif page == "💬  HR Q&A":
    st.markdown('<p class="section-title">💬 HR Q&amp;A</p><p class="section-sub">Ask questions answered from your documents via RAG</p>', unsafe_allow_html=True)

    from rag_chain  import ask
    from chat_store import create_session, load_history

    c1, c2 = st.columns([2, 1])
    with c1:
        default_session = st.session_state.get("active_session", "default")
        session_id      = st.text_input("Session Name", value=default_session, placeholder="e.g. hr-queries")
        st.session_state.active_session = session_id
    with c2:
        model = st.selectbox("Model", [
            "llama-3.3-70b-versatile",
            "meta-llama/llama-4-scout-17b-16e-instruct",
            "llama-3.1-8b-instant",
        ])

    full_session = f"{current_email}_{session_id}"

    if ("messages"     not in st.session_state or
        "last_session" not in st.session_state or
         st.session_state.last_session != full_session):
        st.session_state.last_session = full_session
        try:
            create_session(full_session)
            history = load_history(full_session)
            st.session_state.messages = [
                {"role": "user" if m.type == "human" else "assistant", "content": m.content}
                for m in history
            ]
        except Exception:
            st.session_state.messages = []

    if not st.session_state.messages:
        st.markdown("""
        <div class="empty-state">
            <div style="font-size:48px;margin-bottom:12px;">💬</div>
            <div class="empty-state-title">Ask AssistHR Anything</div>
            <div class="empty-state-sub">Questions are answered using your uploaded HR documents via RAG</div>
        </div>
        """, unsafe_allow_html=True)
        sugs  = ["What is the leave policy?", "What are the working hours?", "How to apply for remote work?", "What is the probation period?"]
        cols  = st.columns(len(sugs))
        for col, sug in zip(cols, sugs):
            with col:
                if st.button(sug, use_container_width=True, key=f"sug_{sug}"):
                    st.session_state.messages.append({"role": "user", "content": sug})
                    with st.spinner("AssistHR is thinking..."):
                        try:
                            ans = ask(sug, full_session, model)
                            st.session_state.messages.append({"role": "assistant", "content": ans})
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ {e}")

    for msg in st.session_state.messages:
        avatar = "🧑‍💼" if msg["role"] == "user" else "🤖"
        with st.chat_message(msg["role"], avatar=avatar):
            st.write(msg["content"])

    if prompt := st.chat_input("Ask about HR policies, leave, dress code..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="🧑‍💼"):
            st.write(prompt)
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("AssistHR is thinking..."):
                try:
                    ans = ask(prompt, full_session, model)
                    st.write(ans)
                    st.session_state.messages.append({"role": "assistant", "content": ans})
                except Exception as e:
                    st.error(f"❌ {e}")


    st.markdown(
    '<div class="rag-helper-text">💡 Answers sourced from uploaded documents using Retrieval-Augmented Generation (RAG).</div>',
    unsafe_allow_html=True
)

# ══════════════════════════════════════════════════════════════
# RESUME SCREENER
# ══════════════════════════════════════════════════════════════

elif page == "📄  Resume Screener":
    st.markdown('<p class="section-title">📄 Resume Screener</p><p class="section-sub">Semantic AI-based candidate evaluation</p>', unsafe_allow_html=True)

    from screener import screen_all

    st.markdown('<div class="card"><div class="card-head"><div class="card-title">🔍 Screening Engine</div><span class="card-sub">Semantic AI evaluation</span></div><div class="card-body">', unsafe_allow_html=True)

    model = st.selectbox("AI Model", [
        "llama-3.3-70b-versatile",
        "meta-llama/llama-4-scout-17b-16e-instruct",
        "llama-3.1-8b-instant",
    ], help="llama-3.3-70b recommended for best accuracy")

    c1, c2 = st.columns(2, gap="medium")
    with c1:
        st.markdown('<div class="field-label">📄 Upload Resumes</div>', unsafe_allow_html=True)
        resumes = st.file_uploader("Resumes", type=["pdf","docx","jpg","jpeg","png"], accept_multiple_files=True, key="resumes", label_visibility="collapsed")
    with c2:
        st.markdown('<div class="field-label">💼 Upload Job Description</div>', unsafe_allow_html=True)
        jd = st.file_uploader("JD", type=["pdf","docx"], key="jd", label_visibility="collapsed")

    st.markdown('<div class="callout-info">💡 <b>Scoring:</b> Skills match · Experience level · Education · Role alignment. Score ≥ 65 = Recommended.</div>', unsafe_allow_html=True)
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    screen_clicked = st.button("🔍 Screen Resumes", type="primary", use_container_width=True)
    st.markdown("</div></div>", unsafe_allow_html=True)

    if screen_clicked:
        if not jd:
            st.error("Please upload a Job Description.")
        elif not resumes:
            st.error("Please upload at least one resume.")
        else:
            jd_path = f"/tmp/{jd.name}"
            with open(jd_path, "wb") as f:
                f.write(jd.getbuffer())
            resume_paths = []
            for r in resumes:
                p = f"/tmp/{r.name}"
                with open(p, "wb") as f:
                    f.write(r.getbuffer())
                resume_paths.append(p)

            with st.spinner("Screening candidates..."):
                try:
                    results = screen_all(resume_paths, jd_path, model)
                except Exception as e:
                    st.error(f"❌ {e}")
                    results = []

            if os.path.exists(jd_path): os.remove(jd_path)
            for p in resume_paths:
                if os.path.exists(p): os.remove(p)

            if results:
                st.success(f"✅ Screened {len(results)} candidate(s)")
                st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

                for i, r in enumerate(results, 1):
                    score   = r.get("score",   0)
                    verdict = r.get("verdict", "")
                    name    = r.get("name", "Unknown")

                    if "Strongly" in verdict: v_bg, v_col = "#d1fae5", "#059669"
                    elif "Recommended" in verdict: v_bg, v_col = "#dbeafe", "#2563eb"
                    elif "Maybe" in verdict: v_bg, v_col = "#fef3c7", "#d97706"
                    else: v_bg, v_col = "#fee2e2", "#dc2626"

                    s_col  = "#059669" if score >= 65 else "#d97706" if score >= 40 else "#dc2626"
                    medals = {1:"🥇", 2:"🥈", 3:"🥉"}
                    medal  = medals.get(i, f"#{i}")

                    with st.expander(f"{medal}  {name}  |  {score}%  |  {verdict}", expanded=(i == 1)):
                        st.markdown(f"""
                        <div style="margin-bottom:14px;">
                            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                                <div style="font-size:22px;font-weight:800;color:{s_col};">{score}/100</div>
                                <span class="verdict-badge" style="background:{v_bg};color:{v_col};">{verdict}</span>
                            </div>
                            <div class="score-track">
                                <div style="height:100%;width:{score}%;background:linear-gradient(90deg,{s_col},{s_col}99);border-radius:99px;"></div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                        c1, c2 = st.columns(2)
                        with c1:
                            st.markdown(f'<div class="body-text">📧 {r.get("email","N/A")}<br/>📞 {r.get("phone","N/A")}<br/>🎓 {r.get("education","N/A")}</div>', unsafe_allow_html=True)
                        with c2:
                            links = ""
                            if r.get("linkedin"): links += f'🔗 <a href="{r["linkedin"]}" target="_blank">LinkedIn</a> '
                            if r.get("github"):   links += f'💻 <a href="{r["github"]}" target="_blank">GitHub</a>'
                            st.markdown(f'<div class="body-text">💼 {r.get("experience","N/A")}<br/>{links}</div>', unsafe_allow_html=True)

                        st.divider()
                        c1, c2 = st.columns(2)
                        with c1:
                            if r.get("matched_skills"):
                                st.markdown('<div class="skill-section-label">✅ Matched Skills</div>', unsafe_allow_html=True)
                                st.markdown("".join([f'<span class="chip-green">✓ {s}</span>' for s in r["matched_skills"][:8]]), unsafe_allow_html=True)
                        with c2:
                            if r.get("missing_skills"):
                                st.markdown('<div class="skill-section-label">❌ Missing Skills</div>', unsafe_allow_html=True)
                                st.markdown("".join([f'<span class="chip-red">✗ {s}</span>' for s in r["missing_skills"][:6]]), unsafe_allow_html=True)

                        st.divider()
                        st.markdown(f"""
                        <div class="insight-box">
                            <div style="margin-bottom:8px;">💪 <b>Strengths:</b> {r.get("strengths","")}</div>
                            <div>⚠️ <b>Weaknesses:</b> {r.get("weaknesses","")}</div>
                        </div>
                        <div style="font-size:10.5px;color:var(--text-muted);margin-top:8px;text-align:right;">Model: {r.get("model", model)}</div>
                        """, unsafe_allow_html=True)
            else:
                st.warning("No results returned.")
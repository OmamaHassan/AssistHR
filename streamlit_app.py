import os
import sys
import streamlit as st
import streamlit.components.v1 as components
from supabase import create_client

# ─── PATH FIX ────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(BASE_DIR, "backend")
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

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

supabase = create_client(
    get_secret("SUPABASE_URL"),
    get_secret("SUPABASE_ANON_KEY")
)

# ─── PAGE CONFIG ─────────────────────────────────────────────

st.set_page_config(
    page_title = "AssistHR",
    page_icon  = "🤖",
    layout     = "wide",
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
    --surface-2: #111827;
    --text-main: #f1f5f9;
    --text-muted: #94a3b8;
    --border: #334155;
}
/* ══════════════════════════════════════════════════════════
   RESET & BASE
══════════════════════════════════════════════════════════ */
html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    font-family : 'Plus Jakarta Sans', sans-serif !important;
}
[data-testid="stAppViewContainer"] {
    background  : var(--app-bg) !important;
}
#MainMenu, footer { visibility: hidden; }
.block-container {
    padding-top   : 24px !important;
    padding-left  : 32px !important;
    padding-right : 32px !important;
    max-width     : 100% !important;
}

/* ══════════════════════════════════════════════════════════
   SIDEBAR
══════════════════════════════════════════════════════════ */
[data-testid="stSidebar"] {
    background    : linear-gradient(180deg, #0f172a 0%, #111b34 100%) !important;
    border-right  : 1px solid rgba(148,163,184,0.18) !important;
    width         : 248px !important;
}
[data-testid="stSidebar"] * {
    font-family   : 'Plus Jakarta Sans', sans-serif !important;
}
[data-testid="stSidebar"] .stRadio label {
    color         : #94a3b8 !important;
    font-size     : 13.5px !important;
    font-weight   : 500 !important;
    padding       : 10px 12px !important;
    border-radius : 8px !important;
    transition    : all 0.18s ease !important;
    cursor        : pointer !important;
}
[data-testid="stSidebar"] .stRadio label:hover {
    background    : rgba(255,255,255,0.07) !important;
    color         : #e2e8f0 !important;
}
[data-testid="stSidebar"] .stRadio label:has(input:checked) {
    background    : linear-gradient(135deg, rgba(37,99,235,.25), rgba(56,189,248,.18)) !important;
    color         : #dbeafe !important;
    border        : 1px solid rgba(96,165,250,.45) !important;
}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color         : #94a3b8 !important;
}
[data-testid="collapsedControl"]{
    background:rgba(15,23,42,.9)!important;
    border:1px solid rgba(148,163,184,.28)!important;
    border-radius:10px!important;
}
[data-testid="collapsedControl"] svg{
    fill:#e2e8f0!important;
}

/* ══════════════════════════════════════════════════════════
   METRIC CARDS — theme aware
══════════════════════════════════════════════════════════ */
[data-testid="stMetric"] {
    border-radius  : 14px !important;
    padding        : 22px 24px !important;
    min-height     : 115px !important;
    display        : flex !important;
    flex-direction : column !important;
    justify-content: center !important;
    box-shadow     : 0 1px 4px rgba(0,0,0,0.06),
                     0 4px 16px rgba(0,0,0,0.04) !important;
    border         : 1px solid rgba(0,0,0,0.08) !important;
    transition     : transform 0.18s ease,
                     box-shadow 0.18s ease !important;
    position       : relative !important;
    overflow       : hidden !important;
}
[data-testid="stMetric"]:hover {
    transform      : translateY(-3px) !important;
    box-shadow     : 0 8px 30px rgba(0,0,0,0.1) !important;
}
[data-testid="stMetricLabel"] p {
    font-size      : 10.5px !important;
    font-weight    : 700 !important;
    text-transform : uppercase !important;
    letter-spacing : 0.08em !important;
    white-space    : normal !important;
    word-break     : break-word !important;
    line-height    : 1.4 !important;
}
[data-testid="stMetricValue"] {
    font-size      : 26px !important;
    font-weight    : 800 !important;
    line-height    : 1.2 !important;
    white-space    : normal !important;
    word-break     : break-word !important;
    font-family    : 'Plus Jakarta Sans', sans-serif !important;
}
[data-testid="column"] {
    display        : flex !important;
    flex-direction : column !important;
}
[data-testid="column"] [data-testid="stMetric"] {
    flex           : 1 !important;
}

/* Light theme cards */
[data-theme="light"] [data-testid="stMetric"] {
    background : #ffffff !important;
    border     : 1px solid #e2e8f0 !important;
}
[data-theme="light"] [data-testid="stMetricLabel"] p {
    color : #64748b !important;
}
[data-theme="light"] [data-testid="stMetricValue"] {
    color : #0f172a !important;
}

/* Dark theme cards */
[data-theme="dark"] [data-testid="stMetric"] {
    background : #1e293b !important;
    border     : 1px solid #334155 !important;
}
[data-theme="dark"] [data-testid="stMetricLabel"] p {
    color : #94a3b8 !important;
}
[data-theme="dark"] [data-testid="stMetricValue"] {
    color : #f1f5f9 !important;
}

/* Colored accent top border per column */
[data-testid="column"]:nth-child(1) [data-testid="stMetric"]::before {
    content    : '';
    position   : absolute;
    top:0; left:0; right:0;
    height     : 3px;
    background : linear-gradient(90deg, #2563eb, #3b82f6);
    border-radius: 14px 14px 0 0;
}
[data-testid="column"]:nth-child(2) [data-testid="stMetric"]::before {
    content    : '';
    position   : absolute;
    top:0; left:0; right:0;
    height     : 3px;
    background : linear-gradient(90deg, #0891b2, #22d3ee);
    border-radius: 14px 14px 0 0;
}
[data-testid="column"]:nth-child(3) [data-testid="stMetric"]::before {
    content    : '';
    position   : absolute;
    top:0; left:0; right:0;
    height     : 3px;
    background : linear-gradient(90deg, #7c3aed, #a78bfa);
    border-radius: 14px 14px 0 0;
}
[data-testid="column"]:nth-child(4) [data-testid="stMetric"]::before {
    content    : '';
    position   : absolute;
    top:0; left:0; right:0;
    height     : 3px;
    background : linear-gradient(90deg, #059669, #34d399);
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
    background    : linear-gradient(135deg, #2563eb, #1d4ed8) !important;
    color         : #ffffff !important;
    box-shadow    : 0 2px 8px rgba(37,99,235,0.3) !important;
    padding       : 12px 28px !important;
}
.stButton > button[kind="primary"]:hover {
    background    : linear-gradient(135deg, #1d4ed8, #1e40af) !important;
    transform     : translateY(-1px) !important;
    box-shadow    : 0 6px 20px rgba(37,99,235,0.4) !important;
}
.stButton > button[kind="secondary"] {
    background    : transparent !important;
    color         : #2563eb !important;
    border        : 1.5px solid #2563eb !important;
}
.stButton > button[kind="secondary"]:hover {
    background    : #eff6ff !important;
}

/* ══════════════════════════════════════════════════════════
   INPUTS & SELECTBOX
══════════════════════════════════════════════════════════ */
.stTextInput input,
.stTextArea textarea {
    font-family   : 'Plus Jakarta Sans', sans-serif !important;
    border        : 1.5px solid var(--border) !important;
    border-radius : 10px !important;
    font-size     : 13.5px !important;
    transition    : all 0.18s ease !important;
    color         : var(--text-main) !important;
    background    : var(--surface) !important;
}
.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color  : #2563eb !important;
    box-shadow    : 0 0 0 3px rgba(37,99,235,0.12) !important;
}

/* ══════════════════════════════════════════════════════════
   FILE UPLOADER
══════════════════════════════════════════════════════════ */
[data-testid="stFileUploader"] {
    border        : 2px dashed var(--border) !important;
    border-radius : 12px !important;
    background    : var(--surface-2) !important;
    transition    : all 0.18s ease !important;
}
[data-testid="stFileUploader"]:hover {
    border-color  : #2563eb !important;
    background    : #eff6ff !important;
}

/* ══════════════════════════════════════════════════════════
   EXPANDER (screening results)
══════════════════════════════════════════════════════════ */
[data-testid="stExpander"] {
    border        : 1.5px solid var(--border) !important;
    border-radius : 14px !important;
    background    : var(--surface) !important;
    box-shadow    : 0 1px 4px rgba(0,0,0,0.05) !important;
    margin-bottom : 14px !important;
    overflow      : hidden !important;
    transition    : all 0.18s ease !important;
}
[data-testid="stExpander"]:hover {
    box-shadow    : 0 6px 24px rgba(0,0,0,0.08) !important;
    transform     : translateY(-1px) !important;
}
[data-theme="dark"] [data-testid="stExpander"] {
    background    : #1e293b !important;
    border-color  : #334155 !important;
}

/* ══════════════════════════════════════════════════════════
   CHAT MESSAGES
══════════════════════════════════════════════════════════ */
[data-testid="stChatMessage"] {
    border-radius : 14px !important;
    margin-bottom : 10px !important;
    border        : 1px solid var(--border) !important;
    box-shadow    : 0 1px 4px rgba(0,0,0,0.04) !important;
}
[data-theme="dark"] [data-testid="stChatMessage"] {
    border-color  : #334155 !important;
}
[data-testid="stChatMessageAvatarUser"] {
    background: linear-gradient(135deg, #2563eb, #3b82f6) !important;
    color: #ffffff !important;
}
[data-testid="stChatMessageAvatarAssistant"] {
    background: linear-gradient(135deg, #0891b2, #14b8a6) !important;
    color: #ffffff !important;
}

/* ══════════════════════════════════════════════════════════
   ALERTS
══════════════════════════════════════════════════════════ */
.stSuccess, .stError, .stInfo, .stWarning {
    border-radius : 10px !important;
    font-family   : 'Plus Jakarta Sans', sans-serif !important;
}

/* ══════════════════════════════════════════════════════════
   DIVIDER
══════════════════════════════════════════════════════════ */
hr {
    border-color  : #e2e8f0 !important;
    margin        : 20px 0 !important;
}

/* ══════════════════════════════════════════════════════════
   PROGRESS BAR
══════════════════════════════════════════════════════════ */
[data-testid="stProgress"] > div > div {
    background    : linear-gradient(90deg, #2563eb, #0891b2) !important;
    border-radius : 99px !important;
}

/* ══════════════════════════════════════════════════════════
   SKILL CHIPS
══════════════════════════════════════════════════════════ */
.chip-green {
    display       : inline-block;
    padding       : 3px 10px;
    border-radius : 99px;
    font-size     : 11.5px;
    font-weight   : 600;
    background    : #d1fae5;
    color         : #059669;
    border        : 1px solid #a7f3d0;
    margin        : 2px;
}
.chip-red {
    display       : inline-block;
    padding       : 3px 10px;
    border-radius : 99px;
    font-size     : 11.5px;
    font-weight   : 600;
    background    : #fee2e2;
    color         : #dc2626;
    border        : 1px solid #fca5a5;
    margin        : 2px;
}
.verdict-badge {
    display       : inline-block;
    padding       : 4px 12px;
    border-radius : 99px;
    font-size     : 11px;
    font-weight   : 700;
}
.doc-row {
    display        : flex;
    align-items    : center;
    gap            : 12px;
    padding        : 11px 16px;
    border-radius  : 10px;
    margin-bottom  : 6px;
    border         : 1px solid #e2e8f0;
    background     : #ffffff;
    transition     : all 0.18s ease;
    font-size      : 13.5px;
    font-weight    : 500;
    color          : #334155;
}
.doc-row:hover {
    border-color   : #2563eb;
    box-shadow     : 0 0 0 3px rgba(37,99,235,0.08);
}
[data-theme="dark"] .doc-row {
    background     : #1e293b;
    border-color   : #334155;
    color          : #cbd5e1;
}
.doc-badge {
    font-size      : 10px;
    padding        : 2px 8px;
    border-radius  : 99px;
    background     : #eff6ff;
    color          : #2563eb;
    font-weight    : 700;
    text-transform : uppercase;
    margin-left    : auto;
}
.info-row {
    display        : flex;
    justify-content: space-between;
    align-items    : center;
    padding        : 9px 0;
    border-bottom  : 1px solid #f1f5f9;
    font-size      : 13px;
}
.info-val {
    font-size      : 11.5px;
    font-weight    : 700;
    background     : #f1f5f9;
    padding        : 3px 10px;
    border-radius  : 99px;
    color          : #0f172a;
}
[data-theme="dark"] .info-val {
    background     : #334155;
    color          : #f1f5f9;
}
[data-theme="dark"] .info-row {
    border-color   : #1e293b;
    color          : #94a3b8;
}
.card {
    background     : #ffffff;
    border         : 1px solid #e2e8f0;
    border-radius  : 14px;
    overflow       : hidden;
    box-shadow     : 0 1px 4px rgba(0,0,0,0.06);
    margin-bottom  : 20px;
}
[data-theme="dark"] .card {
    background     : #1e293b;
    border-color   : #334155;
}
.card-head {
    padding        : 16px 22px;
    border-bottom  : 1px solid #e2e8f0;
    display        : flex;
    align-items    : center;
    justify-content: space-between;
}
[data-theme="dark"] .card-head {
    border-color   : #334155;
}
.card-title {
    font-size      : 14px;
    font-weight    : 700;
    color          : #0f172a;
}
[data-theme="dark"] .card-title {
    color          : #f1f5f9;
}
.card-body {
    padding        : 20px 22px;
}
.step-item {
    display        : flex;
    gap            : 12px;
    align-items    : flex-start;
    margin-bottom  : 18px;
}
.step-num {
    min-width      : 30px;
    height         : 30px;
    border-radius  : 8px;
    color          : #ffffff;
    display        : flex;
    align-items    : center;
    justify-content: center;
    font-weight    : 800;
    font-size      : 13px;
    flex-shrink    : 0;
}
.step-title {
    font-size      : 13.5px;
    font-weight    : 700;
    color          : #0f172a;
    margin-bottom  : 3px;
}
[data-theme="dark"] .step-title {
    color          : #f1f5f9;
}
.step-desc {
    font-size      : 12.5px;
    color          : #64748b;
    line-height    : 1.5;
}
.section-title {
    font-size      : 22px;
    font-weight    : 800;
    color          : #0f172a;
    margin         : 0 0 4px 0;
    font-family    : 'Plus Jakarta Sans', sans-serif;
}
[data-theme="dark"] .section-title {
    color          : #f1f5f9;
}
.section-sub {
    font-size      : 13.5px;
    color          : var(--text-muted);
    margin-bottom  : 22px;
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# AUTH
# ══════════════════════════════════════════════════════════════

def login_page():
    # centered hero
    st.markdown("""
    <div style="max-width:440px; margin:60px auto 0;">
        <div style="
            background   : linear-gradient(135deg,#0f172a 0%,#1e3a5f 100%);
            border-radius: 20px;
            padding      : 40px 36px 32px;
            text-align   : center;
            margin-bottom: 24px;
            position     : relative;
            overflow     : hidden;
        ">
            <div style="position:absolute;right:-30px;top:-30px;
                        width:160px;height:160px;border-radius:50%;
                        background:rgba(37,99,235,0.25);"></div>
            <div style="position:absolute;left:-20px;bottom:-40px;
                        width:120px;height:120px;border-radius:50%;
                        background:rgba(8,145,178,0.2);"></div>
            <div style="font-size:52px;margin-bottom:12px;
                        position:relative;z-index:1;">🤖</div>
            <div style="font-size:28px;font-weight:800;color:#ffffff;
                        position:relative;z-index:1;
                        font-family:'Plus Jakarta Sans',sans-serif;">
                AssistHR
            </div>
            <div style="font-size:11px;color:#60a5fa;font-weight:700;
                        letter-spacing:2px;text-transform:uppercase;
                        margin-top:4px;position:relative;z-index:1;">
                AI · HR · Intelligence
            </div>
            <div style="display:flex;gap:8px;justify-content:center;
                        flex-wrap:wrap;margin-top:16px;
                        position:relative;z-index:1;">
                <span style="padding:4px 10px;background:rgba(255,255,255,.1);
                      border:1px solid rgba(255,255,255,.15);border-radius:99px;
                      font-size:11px;color:#cbd5e1;">🧠 RAG</span>
                <span style="padding:4px 10px;background:rgba(255,255,255,.1);
                      border:1px solid rgba(255,255,255,.15);border-radius:99px;
                      font-size:11px;color:#cbd5e1;">⚡ Groq</span>
                <span style="padding:4px 10px;background:rgba(255,255,255,.1);
                      border:1px solid rgba(255,255,255,.15);border-radius:99px;
                      font-size:11px;color:#cbd5e1;">🗄️ pgvector</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    _, col, _ = st.columns([1, 2, 1])
    with col:
        tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])

        with tab1:
            email    = st.text_input("Email", key="login_email",
                                     placeholder="you@company.com")
            password = st.text_input("Password", type="password",
                                     key="login_pass",
                                     placeholder="••••••••")
            if st.button("Login →", use_container_width=True,
                         type="primary", key="login_btn"):
                if not email or not password:
                    st.error("Please fill in all fields.")
                else:
                    try:
                        r = supabase.auth.sign_in_with_password(
                            {"email": email, "password": password}
                        )
                        st.session_state.user  = r.user
                        st.session_state.token = r.session.access_token
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Login failed: {e}")

        with tab2:
            name     = st.text_input("Full Name", key="reg_name",
                                     placeholder="John Smith")
            email    = st.text_input("Email", key="reg_email",
                                     placeholder="you@company.com")
            password = st.text_input("Password", type="password",
                                     key="reg_pass",
                                     placeholder="Min 6 characters")
            confirm  = st.text_input("Confirm Password",
                                     type="password",
                                     key="reg_confirm",
                                     placeholder="Repeat password")
            if st.button("Create Account →",
                         use_container_width=True,
                         type="primary", key="reg_btn"):
                if not all([name, email, password, confirm]):
                    st.error("Please fill in all fields.")
                elif len(password) < 6:
                    st.error("Password must be at least 6 characters.")
                elif password != confirm:
                    st.error("Passwords do not match.")
                else:
                    try:
                        supabase.auth.sign_up({
                            "email": email, "password": password,
                            "options": {"data": {"name": name}}
                        })
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
    <div style="display:flex;align-items:center;gap:10px;
                margin-bottom:10px;">
        <div style="width:38px;height:38px;background:#2563eb;
                    border-radius:10px;display:flex;
                    align-items:center;justify-content:center;
                    font-size:18px;">🤖</div>
        <div>
            <div style="color:#ffffff;font-size:17px;
                        font-weight:800;line-height:1;
                        font-family:'Plus Jakarta Sans',sans-serif;">
                AssistHR
            </div>
            <div style="color:#475569;font-size:9.5px;
                        letter-spacing:1.2px;
                        text-transform:uppercase;margin-top:1px;">
                AI HR Assistant
            </div>
        </div>
    </div>
    <div style="background:rgba(255,255,255,0.05);
                border-radius:8px;padding:8px 10px;margin-top:4px;">
        <div style="color:#e2e8f0;font-size:11px;font-weight:700;">
            Saylani Mass IT Training
        </div>
        <div style="color:#64748b;font-size:10.5px;
                    margin-top:2px;line-height:1.5;">
            AI &amp; Data Science · Batch 9
        </div>
    </div>
</div>
<div style="padding:2px 16px 6px;">
    <div style="color:#475569;font-size:9px;letter-spacing:1.5px;
                text-transform:uppercase;font-weight:700;
                margin-bottom:4px;">Main Menu</div>
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

components.html(
    f"""
    <script>
    (function() {{
      const root = window.parent.document.documentElement;
      const app = window.parent.document.querySelector('[data-testid="stAppViewContainer"]');
      const main = window.parent.document.querySelector('[data-testid="stMain"]');
      const choice = "{theme_choice}";
      let mode = "light";
      if (choice === "Dark") mode = "dark";
      else if (choice === "System") {{
        mode = window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
      }}
      root.setAttribute("data-user-theme", mode);
      root.setAttribute("data-theme", mode);
      if (app) app.setAttribute("data-theme", mode);
      if (main) main.setAttribute("data-theme", mode);
    }})();
    </script>
    """,
    height=0,
)

st.sidebar.markdown("""
<div style="padding:0 16px 10px;">
    <div style="display:flex;gap:8px;">
        <div style="flex:1;background:rgba(255,255,255,.05);border:1px solid rgba(148,163,184,.2);
                    border-radius:8px;padding:8px 10px;">
            <div style="color:#e2e8f0;font-size:11px;font-weight:700;">Mode</div>
            <div style="color:#94a3b8;font-size:10px;">Production</div>
        </div>
        <div style="flex:1;background:rgba(255,255,255,.05);border:1px solid rgba(148,163,184,.2);
                    border-radius:8px;padding:8px 10px;">
            <div style="color:#e2e8f0;font-size:11px;font-weight:700;">Stack</div>
            <div style="color:#94a3b8;font-size:10px;">RAG + Groq</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

page = st.sidebar.radio(
    "nav",
    ["📊  Dashboard",
     "📚  Knowledge Base",
     "💬  HR Q&A",
     "📄  Resume Screener"],
    label_visibility="collapsed"
)

st.sidebar.markdown("<div style='margin-top:12px'></div>",
                    unsafe_allow_html=True)

if page == "💬  HR Q&A":
    st.sidebar.markdown("""
    <div style="padding:0 16px 6px;">
        <div style="color:#64748b;font-size:9px;letter-spacing:1.4px;
                    text-transform:uppercase;font-weight:700;">
            Chat Sessions
        </div>
    </div>
    """, unsafe_allow_html=True)

    if "active_session" not in st.session_state:
        st.session_state.active_session = "default"

    if st.sidebar.button("＋ New Session", use_container_width=True, key="new_session_btn"):
        import time
        st.session_state.active_session = f"chat-{int(time.time())}"
        st.session_state.messages = []
        st.session_state.last_session = ""
        st.rerun()

    try:
        from chat_store import get_conn as _gc
        _conn = _gc()
        _cur = _conn.cursor()
        _cur.execute(
            """
            SELECT session_id FROM sessions
            WHERE session_id LIKE %s
            ORDER BY last_active DESC LIMIT 8
            """,
            (f"{current_email}_%",)
        )
        _rows = _cur.fetchall()
        _conn.close()

        for row in _rows:
            raw = row[0]
            disp = raw.split("_", 1)[1] if "_" in raw else raw
            is_active = disp == st.session_state.active_session
            icon = "🤖" if is_active else "💬"
            if st.sidebar.button(
                f"{icon}  {disp}",
                key=f"chat_session_{raw}",
                use_container_width=True,
                type="primary" if is_active else "secondary",
            ):
                st.session_state.active_session = disp
                st.session_state.messages = []
                st.session_state.last_session = ""
                st.rerun()
    except Exception:
        pass

st.sidebar.divider()

st.sidebar.markdown(f"""
<div style="padding:0 4px;">
    <div style="display:flex;align-items:center;gap:8px;
                background:rgba(255,255,255,0.05);
                border-radius:8px;padding:10px 12px;
                margin-bottom:10px;">
        <div style="width:7px;height:7px;background:#22c55e;
                    border-radius:50%;flex-shrink:0;"></div>
        <div>
            <div style="color:#e2e8f0;font-size:11px;
                        font-weight:700;">System Ready</div>
            <div style="color:#64748b;font-size:10px;margin-top:1px;">
                RAG · Supabase pgvector · Groq
            </div>
        </div>
    </div>
    <div style="color:#64748b;font-size:11px;padding:2px 2px 8px;">
        👤 {current_email}
    </div>
</div>
""", unsafe_allow_html=True)

if st.sidebar.button("Logout", use_container_width=True,
                     key="logout_btn"):
    logout()

st.sidebar.markdown("""
<div style="padding:12px 4px 4px;text-align:center;">
    <div style="color:#334155;font-size:10px;
                font-family:'JetBrains Mono',monospace;">
        AssistHR v1.0 · MIT License
    </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════════════

if page == "📊  Dashboard":

    # hero
    st.markdown("""
    <div style="
        background   : linear-gradient(135deg,#0f172a 0%,#1e3a5f 100%);
        border-radius: 18px;
        padding      : 32px 36px;
        margin-bottom: 24px;
        position     : relative;
        overflow     : hidden;
    ">
        <div style="position:absolute;right:-50px;top:-50px;
                    width:220px;height:220px;border-radius:50%;
                    background:rgba(37,99,235,0.25);"></div>
        <div style="position:absolute;right:100px;bottom:-70px;
                    width:170px;height:170px;border-radius:50%;
                    background:rgba(8,145,178,0.18);"></div>
        <div style="position:relative;z-index:1;">
            <h2 style="color:#ffffff;margin:0;font-size:24px;
                       font-weight:800;
                       font-family:'Plus Jakarta Sans',sans-serif;">
                Welcome to <span style="color:#60a5fa;">AssistHR</span> 🤖
            </h2>
            <p style="color:#94a3b8;margin:8px 0 16px;
                      font-size:13.5px;line-height:1.6;max-width:520px;">
                AI-powered HR assistant built with RAG, Groq LLM
                and Supabase pgvector. Upload HR policies,
                ask questions, screen resumes — all in one place.
            </p>
            <div style="display:flex;gap:8px;flex-wrap:wrap;">
                <span style="padding:5px 13px;background:rgba(255,255,255,.1);
                      border:1px solid rgba(255,255,255,.15);border-radius:99px;
                      font-size:11.5px;color:#cbd5e1;">🧠 RAG Pipeline</span>
                <span style="padding:5px 13px;background:rgba(255,255,255,.1);
                      border:1px solid rgba(255,255,255,.15);border-radius:99px;
                      font-size:11.5px;color:#cbd5e1;">🔍 Semantic Search</span>
                <span style="padding:5px 13px;background:rgba(255,255,255,.1);
                      border:1px solid rgba(255,255,255,.15);border-radius:99px;
                      font-size:11.5px;color:#cbd5e1;">📊 Resume Ranking</span>
                <span style="padding:5px 13px;background:rgba(255,255,255,.1);
                      border:1px solid rgba(255,255,255,.15);border-radius:99px;
                      font-size:11.5px;color:#cbd5e1;">⚡ Supabase pgvector</span>
                <span style="padding:5px 13px;background:rgba(255,255,255,.1);
                      border:1px solid rgba(255,255,255,.15);border-radius:99px;
                      font-size:11.5px;color:#cbd5e1;">🤖 Groq llama-3.3-70b</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # metrics
    from embedding import get_existing_files
    try:
        all_docs   = get_existing_files()
        docs_count = len(all_docs)
    except Exception:
        all_docs   = set()
        docs_count = 0

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("📄  Documents",  docs_count,
                  help="HR documents in knowledge base")
    with c2:
        st.metric("⚡  Vector DB",  "pgvector",
                  help="Supabase pgvector extension")
    with c3:
        st.metric("🤖  LLM",        "Groq",
                  help="llama-3.3-70b-versatile")
    with c4:
        st.metric("✅  Status",      "Online",
                  help="All systems operational")

    st.markdown("<div style='height:8px'></div>",
                unsafe_allow_html=True)

    # two column layout
    col_left, col_right = st.columns([1.6, 1], gap="medium")

    with col_left:
        st.markdown("""
        <div class="card">
            <div class="card-head">
                <div class="card-title">📖 How to Use AssistHR</div>
            </div>
            <div class="card-body">
                <div class="step-item">
                    <div class="step-num" style="background:#2563eb;">1</div>
                    <div>
                        <div class="step-title">Upload HR Documents</div>
                        <div class="step-desc">
                            Go to <b>Knowledge Base</b> → Upload HR
                            policy files (PDF, DOCX, TXT).
                            They get indexed automatically.
                        </div>
                    </div>
                </div>
                <div class="step-item">
                    <div class="step-num" style="background:#0891b2;">2</div>
                    <div>
                        <div class="step-title">Ask Questions (RAG)</div>
                        <div class="step-desc">
                            Go to <b>HR Q&A</b> → Type any question.
                            AssistHR searches your documents and
                            answers using Groq LLM.
                        </div>
                    </div>
                </div>
                <div class="step-item" style="margin-bottom:0">
                    <div class="step-num" style="background:#d97706;">3</div>
                    <div>
                        <div class="step-title">Screen Resumes</div>
                        <div class="step-desc">
                            Go to <b>Resume Screener</b> → Upload JD
                            + resumes → get ranked candidates
                            with scores and skill analysis.
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="card"><div class="card-head">'
                    '<div class="card-title">⚙️ System Info</div>'
                    '</div><div class="card-body">',
                    unsafe_allow_html=True)

        items = [
            ("🤖 LLM",         "Groq llama-3.3-70b"),
            ("⚡ Vector DB",   "Supabase pgvector"),
            ("📐 Embeddings",  "MiniLM-L12-v2"),
            ("🔍 Search",      "Cosine Similarity"),
            ("🗄️ Database",    "Supabase PostgreSQL"),
            ("🔐 Auth",        "Supabase Auth"),
        ]
        for label, value in items:
            st.markdown(f"""
            <div class="info-row">
                <span style="color:#64748b;font-size:12.5px;">
                    {label}
                </span>
                <span class="info-val">{value}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div></div>", unsafe_allow_html=True)

    # recent documents
    st.markdown('<div class="card"><div class="card-head">'
                '<div class="card-title">📁 Recent Documents</div>'
                f'<div style="font-size:11.5px;color:#64748b;">'
                f'{docs_count} file{"s" if docs_count!=1 else ""}</div>'
                '</div><div class="card-body">',
                unsafe_allow_html=True)

    if not all_docs:
        st.info("No documents yet. Upload from Knowledge Base.")
    else:
        icons = {"pdf":"📕","docx":"📘","txt":"📄"}
        for doc in list(all_docs)[:6]:
            ext  = doc.split(".")[-1].lower() if "." in doc else "file"
            icon = icons.get(ext, "📄")
            st.markdown(f"""
            <div class="doc-row">
                <span style="font-size:18px;">{icon}</span>
                <span style="flex:1;font-size:13px;
                             font-weight:600;">{doc}</span>
                <span class="doc-badge">{ext}</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div></div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# KNOWLEDGE BASE
# ══════════════════════════════════════════════════════════════

elif page == "📚  Knowledge Base":

    st.markdown('<p class="section-title">📚 Knowledge Base</p>'
                '<p class="section-sub">'
                'Upload and manage HR documents</p>',
                unsafe_allow_html=True)

    from document_loader import load_document
    from chunking        import chunk_documents
    from embedding       import create_vector_store, get_existing_files

    # upload card
    st.markdown('<div class="card"><div class="card-head">'
                '<div class="card-title">📁 Upload HR Document</div>'
                '<span style="font-size:11.5px;color:#64748b;">'
                'PDF · DOCX · TXT</span>'
                '</div><div class="card-body">',
                unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Drop file here or click to browse",
        type=["pdf", "docx", "txt"],
        label_visibility="visible"
    )

    if uploaded:
        c1, c2 = st.columns([3, 1])
        with c1:
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:10px;
                        padding:10px 14px;background:#eff6ff;
                        border:1px solid #dbeafe;border-radius:10px;
                        font-size:12.5px;margin-top:8px;">
                <span>📄</span>
                <span style="flex:1;font-weight:600;color:#1d4ed8;">
                    {uploaded.name}
                </span>
                <span style="color:#64748b;">
                    {uploaded.size/1024:.1f} KB
                </span>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            if st.button("⬆️ Process", use_container_width=True,
                         type="primary"):
                with st.spinner(f"Processing '{uploaded.name}'..."):
                    tmp = f"/tmp/{uploaded.name}"
                    with open(tmp, "wb") as f:
                        f.write(uploaded.getbuffer())
                    try:
                        docs   = load_document(tmp)
                        chunks = chunk_documents(docs)
                        create_vector_store(chunks)
                        st.success(
                            f"✅ '{uploaded.name}' — "
                            f"{len(chunks)} chunks indexed"
                        )
                    except Exception as e:
                        st.error(f"❌ {e}")
                    finally:
                        if os.path.exists(tmp):
                            os.remove(tmp)

    st.markdown("</div></div>", unsafe_allow_html=True)

    # documents list
    st.markdown('<div class="card"><div class="card-head">'
                '<div class="card-title">'
                '📚 Indexed Documents</div>'
                '</div><div class="card-body">',
                unsafe_allow_html=True)

    try:
        existing = get_existing_files()
        if not existing:
            st.info("No documents yet. Upload above.")
        else:
            icons = {"pdf":"📕","docx":"📘","txt":"📄"}
            for doc in existing:
                ext  = doc.split(".")[-1].lower() \
                       if "." in doc else "file"
                icon = icons.get(ext, "📄")
                st.markdown(f"""
                <div class="doc-row">
                    <span style="font-size:18px;">{icon}</span>
                    <span style="flex:1;font-size:13px;
                                 font-weight:600;">{doc}</span>
                    <span class="doc-badge">{ext}</span>
                </div>
                """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Could not load: {e}")

    st.markdown("</div></div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# HR Q&A
# ══════════════════════════════════════════════════════════════

elif page == "💬  HR Q&A":

    st.markdown('<p class="section-title">💬 HR Q&amp;A</p>'
                '<p class="section-sub">'
                'Ask questions answered from your documents via RAG</p>',
                unsafe_allow_html=True)

    from rag_chain  import ask
    from chat_store import create_session, load_history

    c1, c2 = st.columns([2, 1])
    with c1:
        default_session = st.session_state.get("active_session", "default")
        session_id = st.text_input(
            "Session Name", value=default_session,
            placeholder="e.g. hr-queries"
        )
        st.session_state.active_session = session_id
    with c2:
        model = st.selectbox("Model", [
            "llama-3.3-70b-versatile",
            "meta-llama/llama-4-scout-17b-16e-instruct",
            "llama-3.1-8b-instant",
        ])

    full_session = f"{current_email}_{session_id}"

    # load history on session change
    if ("messages"     not in st.session_state or
        "last_session" not in st.session_state or
         st.session_state.last_session != full_session):

        st.session_state.last_session = full_session
        try:
            create_session(full_session)
            history = load_history(full_session)
            st.session_state.messages = [
                {"role": "user" if m.type == "human"
                         else "assistant",
                 "content": m.content}
                for m in history
            ]
        except Exception:
            st.session_state.messages = []

    # empty state with suggestions
    if not st.session_state.messages:
        st.markdown("""
        <div style="text-align:center;padding:36px 24px 20px;">
            <div style="font-size:48px;margin-bottom:12px;">💬</div>
            <div style="font-size:18px;font-weight:700;
                        color:#0f172a;margin-bottom:6px;
                        font-family:'Plus Jakarta Sans',sans-serif;">
                Ask AssistHR Anything
            </div>
            <div style="font-size:13px;color:#64748b;max-width:320px;
                        margin:0 auto;">
                Questions are answered using your uploaded
                HR documents via RAG
            </div>
        </div>
        """, unsafe_allow_html=True)

        sugs = [
            "What is the leave policy?",
            "What are the working hours?",
            "How to apply for remote work?",
            "What is the probation period?",
        ]
        cols = st.columns(len(sugs))
        for col, sug in zip(cols, sugs):
            with col:
                if st.button(sug, use_container_width=True,
                             key=f"sug_{sug}"):
                    st.session_state.messages.append(
                        {"role": "user", "content": sug}
                    )
                    with st.spinner("AssistHR is thinking..."):
                        try:
                            ans = ask(sug, full_session, model)
                            st.session_state.messages.append(
                                {"role": "assistant", "content": ans}
                            )
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ {e}")

    # show messages
    for msg in st.session_state.messages:
        avatar = "🧑‍💼" if msg["role"] == "user" else "🤖"
        with st.chat_message(msg["role"], avatar=avatar):
            st.write(msg["content"])

    # input
    if prompt := st.chat_input(
        "Ask about HR policies, leave, dress code..."
    ):
        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )
        with st.chat_message("user", avatar="🧑‍💼"):
            st.write(prompt)
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("AssistHR is thinking..."):
                try:
                    ans = ask(prompt, full_session, model)
                    st.write(ans)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": ans}
                    )
                except Exception as e:
                    st.error(f"❌ {e}")

    st.caption(
        "💡 Answers sourced from uploaded documents "
        "using Retrieval-Augmented Generation (RAG)"
    )


# ══════════════════════════════════════════════════════════════
# RESUME SCREENER
# ══════════════════════════════════════════════════════════════

elif page == "📄  Resume Screener":

    st.markdown('<p class="section-title">📄 Resume Screener</p>'
                '<p class="section-sub">'
                'Semantic AI-based candidate evaluation</p>',
                unsafe_allow_html=True)

    from screener import screen_all

    # settings card
    st.markdown('<div class="card"><div class="card-head">'
                '<div class="card-title">'
                '🔍 Screening Engine</div>'
                '<span style="font-size:11.5px;color:#64748b;">'
                'Semantic AI evaluation</span>'
                '</div><div class="card-body">',
                unsafe_allow_html=True)

    model = st.selectbox("AI Model", [
        "llama-3.3-70b-versatile",
        "meta-llama/llama-4-scout-17b-16e-instruct",
        "llama-3.1-8b-instant",
    ], help="llama-3.3-70b recommended for best accuracy")

    c1, c2 = st.columns(2, gap="medium")
    with c1:
        st.markdown("""
        <div style="font-size:12px;font-weight:700;
                    color:#334155;margin-bottom:6px;">
            📄 Upload Resumes
        </div>
        """, unsafe_allow_html=True)
        resumes = st.file_uploader(
            "Resumes",
            type=["pdf","docx","jpg","jpeg","png"],
            accept_multiple_files=True,
            key="resumes",
            label_visibility="collapsed"
        )
    with c2:
        st.markdown("""
        <div style="font-size:12px;font-weight:700;
                    color:#334155;margin-bottom:6px;">
            💼 Upload Job Description
        </div>
        """, unsafe_allow_html=True)
        jd = st.file_uploader(
            "JD",
            type=["pdf","docx"],
            key="jd",
            label_visibility="collapsed"
        )

    st.markdown("""
    <div style="margin-top:14px;padding:12px 16px;
                background:#eff6ff;border:1px solid #dbeafe;
                border-radius:10px;font-size:12.5px;color:#334155;">
        💡 <b>Scoring:</b> Skills match · Experience level ·
        Education · Role alignment.
        Score ≥ 65 = Recommended.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>",
                unsafe_allow_html=True)

    screen_clicked = st.button(
        "🔍 Screen Resumes",
        type="primary",
        use_container_width=True
    )

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
                    results = screen_all(
                        resume_paths, jd_path, model
                    )
                except Exception as e:
                    st.error(f"❌ {e}")
                    results = []

            if os.path.exists(jd_path):
                os.remove(jd_path)
            for p in resume_paths:
                if os.path.exists(p):
                    os.remove(p)

            if results:
                st.success(
                    f"✅ Screened {len(results)} candidate(s)"
                )
                st.markdown(
                    "<div style='height:8px'></div>",
                    unsafe_allow_html=True
                )

                for i, r in enumerate(results, 1):
                    score   = r.get("score",   0)
                    verdict = r.get("verdict", "")
                    name    = r.get("name", "Unknown")

                    # verdict styling
                    if "Strongly" in verdict:
                        v_bg, v_col = "#d1fae5", "#059669"
                    elif "Recommended" in verdict:
                        v_bg, v_col = "#dbeafe", "#2563eb"
                    elif "Maybe" in verdict:
                        v_bg, v_col = "#fef3c7", "#d97706"
                    else:
                        v_bg, v_col = "#fee2e2", "#dc2626"

                    # score color
                    s_col = ("#059669" if score >= 65
                             else "#d97706" if score >= 40
                             else "#dc2626")

                    medals = {1:"🥇",2:"🥈",3:"🥉"}
                    medal  = medals.get(i, f"#{i}")

                    with st.expander(
                        f"{medal}  {name}  |  "
                        f"{score}%  |  {verdict}",
                        expanded=(i == 1)
                    ):
                        # score bar
                        st.markdown(f"""
                        <div style="margin-bottom:14px;">
                            <div style="display:flex;
                                        justify-content:space-between;
                                        align-items:center;
                                        margin-bottom:6px;">
                                <div style="font-size:22px;
                                            font-weight:800;
                                            color:{s_col};">
                                    {score}/100
                                </div>
                                <span class="verdict-badge"
                                      style="background:{v_bg};
                                             color:{v_col};">
                                    {verdict}
                                </span>
                            </div>
                            <div style="height:6px;
                                        background:#e2e8f0;
                                        border-radius:99px;
                                        overflow:hidden;">
                                <div style="height:100%;
                                            width:{score}%;
                                            background:linear-gradient(
                                                90deg,{s_col},{s_col}99);
                                            border-radius:99px;">
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                        # contact
                        c1, c2 = st.columns(2)
                        with c1:
                            st.markdown(f"""
                            <div style="font-size:12.5px;
                                        color:#334155;
                                        line-height:1.8;">
                                📧 {r.get('email','N/A')}<br/>
                                📞 {r.get('phone','N/A')}<br/>
                                🎓 {r.get('education','N/A')}
                            </div>
                            """, unsafe_allow_html=True)
                        with c2:
                            st.markdown(f"""
                            <div style="font-size:12.5px;
                                        color:#334155;
                                        line-height:1.8;">
                                💼 {r.get('experience','N/A')}<br/>
                                {'🔗 <a href="' + r.get("linkedin","") + '" target="_blank" style="color:#2563eb;">LinkedIn</a>' if r.get("linkedin") else ''}
                                {'💻 <a href="' + r.get("github","") + '" target="_blank" style="color:#2563eb;">GitHub</a>' if r.get("github") else ''}
                            </div>
                            """, unsafe_allow_html=True)

                        st.divider()

                        # skills
                        c1, c2 = st.columns(2)
                        with c1:
                            if r.get("matched_skills"):
                                st.markdown("""
                                <div style="font-size:10.5px;
                                    font-weight:700;color:#64748b;
                                    text-transform:uppercase;
                                    letter-spacing:.7px;
                                    margin-bottom:8px;">
                                    ✅ Matched Skills
                                </div>
                                """, unsafe_allow_html=True)
                                chips = "".join([
                                    f'<span class="chip-green">'
                                    f'✓ {s}</span>'
                                    for s in
                                    r["matched_skills"][:8]
                                ])
                                st.markdown(chips,
                                            unsafe_allow_html=True)
                        with c2:
                            if r.get("missing_skills"):
                                st.markdown("""
                                <div style="font-size:10.5px;
                                    font-weight:700;color:#64748b;
                                    text-transform:uppercase;
                                    letter-spacing:.7px;
                                    margin-bottom:8px;">
                                    ❌ Missing Skills
                                </div>
                                """, unsafe_allow_html=True)
                                chips = "".join([
                                    f'<span class="chip-red">'
                                    f'✗ {s}</span>'
                                    for s in
                                    r["missing_skills"][:6]
                                ])
                                st.markdown(chips,
                                            unsafe_allow_html=True)

                        st.divider()

                        # strengths/weaknesses
                        st.markdown(f"""
                        <div style="background:#f8fafc;
                                    border-radius:10px;
                                    padding:14px 16px;
                                    font-size:12.5px;
                                    line-height:1.7;
                                    color:#334155;
                                    border:1px solid #e2e8f0;">
                            <div style="margin-bottom:8px;">
                                💪 <b>Strengths:</b>
                                {r.get('strengths','')}
                            </div>
                            <div>
                                ⚠️ <b>Weaknesses:</b>
                                {r.get('weaknesses','')}
                            </div>
                        </div>
                        <div style="font-size:10.5px;color:#94a3b8;
                                    margin-top:8px;text-align:right;">
                            Model: {r.get('model', model)}
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.warning("No results returned.")

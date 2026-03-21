import os
import sys
import streamlit as st
from supabase import create_client

# =====================================
# ADD BACKEND FOLDER TO PATH
# =====================================

BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(BASE_DIR, "backend")

if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

# =====================================
# GET SECRETS
# =====================================

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

# =====================================
# SUPABASE CLIENT
# =====================================

supabase = create_client(
    get_secret("SUPABASE_URL"),
    get_secret("SUPABASE_ANON_KEY")
)

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title = "AssistHR",
    page_icon  = "🤖",
    layout     = "wide"
)

# =====================================
# GLOBAL CSS — inspired by HTML design
# =====================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

/* ── BASE ─────────────────────────── */
html, body, [data-testid="stAppViewContainer"] {
    font-family : 'Plus Jakarta Sans', sans-serif !important;
    background  : #f0f4f8 !important;
}

/* ── HIDE STREAMLIT DEFAULTS ──────── */
#MainMenu        {visibility: hidden;}
footer           {visibility: hidden;}
header           {visibility: hidden;}
.block-container {
    padding-top   : 20px !important;
    padding-left  : 28px !important;
    padding-right : 28px !important;
    max-width     : 100% !important;
}

/* ── SIDEBAR ──────────────────────── */
[data-testid="stSidebar"] {
    background   : #0f172a !important;
    border-right : none !important;
    min-width    : 240px !important;
    max-width    : 240px !important;
}
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] .stMarkdown span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stRadio label {
    color       : #94a3b8 !important;
    font-family : 'Plus Jakarta Sans', sans-serif !important;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color : #ffffff !important;
}
/* radio selected item */
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
    color : #e2e8f0 !important;
}

/* ── METRIC CARDS ─────────────────── */
[data-testid="stMetric"] {
    background     : #ffffff;
    border         : 1px solid #e2e8f0;
    border-radius  : 12px;
    padding        : 20px 20px !important;
    box-shadow     : 0 1px 3px rgba(0,0,0,.08);
    min-height     : 110px !important;
    position       : relative;
    overflow       : hidden;
    transition     : all 0.18s ease;
}
[data-testid="stMetric"]:hover {
    box-shadow     : 0 4px 16px rgba(0,0,0,.08);
    transform      : translateY(-2px);
}
/* colored top border */
[data-testid="column"]:nth-child(1) [data-testid="stMetric"]::after {
    content    : '';
    position   : absolute;
    top:0; left:0; right:0;
    height     : 3px;
    background : #2563eb;
}
[data-testid="column"]:nth-child(2) [data-testid="stMetric"]::after {
    content    : '';
    position   : absolute;
    top:0; left:0; right:0;
    height     : 3px;
    background : #0891b2;
}
[data-testid="column"]:nth-child(3) [data-testid="stMetric"]::after {
    content    : '';
    position   : absolute;
    top:0; left:0; right:0;
    height     : 3px;
    background : #7c3aed;
}
[data-testid="column"]:nth-child(4) [data-testid="stMetric"]::after {
    content    : '';
    position   : absolute;
    top:0; left:0; right:0;
    height     : 3px;
    background : #059669;
}
[data-testid="stMetricLabel"] p {
    font-size      : 10.5px !important;
    font-weight    : 700 !important;
    text-transform : uppercase !important;
    letter-spacing : .8px !important;
    color          : #64748b !important;
    white-space    : normal !important;
    word-break     : break-word !important;
}
[data-testid="stMetricValue"] {
    font-size   : 28px !important;
    font-weight : 800 !important;
    color       : #0f172a !important;
    line-height : 1 !important;
}

/* dark theme metric cards */
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

/* ── BUTTONS ──────────────────────── */
.stButton > button {
    background    : #2563eb !important;
    color         : #ffffff !important;
    border        : none !important;
    border-radius : 8px !important;
    font-family   : 'Plus Jakarta Sans', sans-serif !important;
    font-weight   : 600 !important;
    font-size     : 13px !important;
    padding       : 10px 20px !important;
    transition    : all 0.18s ease !important;
}
.stButton > button:hover {
    background    : #1d4ed8 !important;
    transform     : translateY(-1px) !important;
    box-shadow    : 0 4px 12px rgba(37,99,235,.3) !important;
}
.stButton > button:disabled {
    background    : #cbd5e1 !important;
    cursor        : not-allowed !important;
    transform     : none !important;
}

/* ── FILE UPLOADER ────────────────── */
[data-testid="stFileUploader"] {
    border        : 2px dashed #cbd5e1 !important;
    border-radius : 12px !important;
    padding       : 20px !important;
    background    : #f8fafc !important;
    transition    : all 0.18s ease !important;
}
[data-testid="stFileUploader"]:hover {
    border-color  : #2563eb !important;
    background    : #eff6ff !important;
}

/* ── INPUTS ───────────────────────── */
.stTextInput input,
.stTextArea textarea,
.stSelectbox select {
    border        : 1.5px solid #e2e8f0 !important;
    border-radius : 8px !important;
    font-family   : 'Plus Jakarta Sans', sans-serif !important;
    font-size     : 13.5px !important;
    background    : #f8fafc !important;
    transition    : all 0.18s ease !important;
}
.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color  : #2563eb !important;
    background    : #ffffff !important;
    box-shadow    : 0 0 0 3px rgba(37,99,235,.1) !important;
}

/* ── EXPANDER ─────────────────────── */
[data-testid="stExpander"] {
    border        : 1.5px solid #e2e8f0 !important;
    border-radius : 12px !important;
    background    : #ffffff !important;
    box-shadow    : 0 1px 3px rgba(0,0,0,.06) !important;
    margin-bottom : 12px !important;
    overflow      : hidden !important;
    transition    : all 0.18s ease !important;
}
[data-testid="stExpander"]:hover {
    box-shadow    : 0 4px 16px rgba(0,0,0,.08) !important;
}

/* ── DIVIDER ──────────────────────── */
hr {
    border-color : #e2e8f0 !important;
    margin       : 20px 0 !important;
}

/* ── CHAT MESSAGES ────────────────── */
[data-testid="stChatMessage"] {
    border-radius : 12px !important;
    margin-bottom : 8px !important;
    border        : 1px solid #e2e8f0 !important;
}

/* ── SPINNER ──────────────────────── */
.stSpinner {
    color : #2563eb !important;
}

/* ── SUCCESS / ERROR / INFO ───────── */
.stSuccess {
    border-radius : 8px !important;
    border-left   : 3px solid #059669 !important;
}
.stError {
    border-radius : 8px !important;
    border-left   : 3px solid #dc2626 !important;
}
.stInfo {
    border-radius : 8px !important;
    border-left   : 3px solid #2563eb !important;
}
</style>
""", unsafe_allow_html=True)


# =====================================
# AUTH FUNCTIONS
# =====================================

def login_page():
    # hero section
    st.markdown("""
    <div style="
        background   : linear-gradient(135deg, #0f172a 0%, #1e3a5f 100%);
        border-radius: 16px;
        padding      : 40px;
        text-align   : center;
        margin-bottom: 32px;
    ">
        <div style="font-size:48px; margin-bottom:12px;">🤖</div>
        <h1 style="color:white; margin:0; font-size:28px; font-weight:800;">
            AssistHR
        </h1>
        <p style="color:#60a5fa; margin:4px 0 0; font-size:14px;
                  font-weight:600; letter-spacing:1px; text-transform:uppercase;">
            AI-Powered HR Assistant
        </p>
        <p style="color:#94a3b8; margin-top:12px; font-size:13.5px; line-height:1.6;">
            Upload HR documents · Ask questions · Screen resumes
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])

        with tab1:
            email    = st.text_input(
                "Email",
                key        = "login_email",
                placeholder= "you@company.com"
            )
            password = st.text_input(
                "Password",
                type       = "password",
                key        = "login_pass",
                placeholder= "••••••••"
            )
            if st.button(
                "Login →",
                use_container_width=True,
                key="login_btn"
            ):
                if not email or not password:
                    st.error("Please fill in all fields.")
                else:
                    try:
                        response = supabase.auth\
                            .sign_in_with_password({
                                "email"   : email,
                                "password": password
                            })
                        st.session_state.user  = response.user
                        st.session_state.token = \
                            response.session.access_token
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Login failed: {e}")

        with tab2:
            name = st.text_input(
                "Full Name",
                key        = "reg_name",
                placeholder= "John Smith"
            )
            email = st.text_input(
                "Email",
                key        = "reg_email",
                placeholder= "you@company.com"
            )
            password = st.text_input(
                "Password",
                type       = "password",
                key        = "reg_pass",
                placeholder= "Min 6 characters"
            )
            confirm = st.text_input(
                "Confirm Password",
                type       = "password",
                key        = "reg_confirm",
                placeholder= "Repeat password"
            )
            if st.button(
                "Create Account →",
                use_container_width=True,
                key="register_btn"
            ):
                if not name or not email \
                   or not password or not confirm:
                    st.error("Please fill in all fields.")
                elif len(password) < 6:
                    st.error(
                        "Password must be "
                        "at least 6 characters."
                    )
                elif password != confirm:
                    st.error("Passwords do not match.")
                else:
                    try:
                        supabase.auth.sign_up({
                            "email"   : email,
                            "password": password,
                            "options" : {
                                "data": {"name": name}
                            }
                        })
                        st.success(
                            "✅ Account created! "
                            "Please login."
                        )
                    except Exception as e:
                        st.error(
                            f"❌ Registration failed: {e}"
                        )


def logout():
    try:
        supabase.auth.sign_out()
    except Exception:
        pass
    st.session_state.user  = None
    st.session_state.token = None
    st.rerun()


# =====================================
# CHECK AUTH
# =====================================

if "user" not in st.session_state:
    st.session_state.user  = None
    st.session_state.token = None

if not st.session_state.user:
    login_page()
    st.stop()

current_user  = st.session_state.user
current_email = current_user.email


# =====================================
# SIDEBAR
# =====================================

st.sidebar.markdown("""
<div style="padding: 8px 4px 16px;">
    <div style="display:flex; align-items:center; gap:10px; margin-bottom:8px;">
        <div style="width:36px; height:36px; background:#2563eb;
                    border-radius:10px; display:flex; align-items:center;
                    justify-content:center; font-size:18px;">🤖</div>
        <div>
            <div style="color:#ffffff; font-size:17px;
                        font-weight:800; line-height:1;">AssistHR</div>
            <div style="color:#64748b; font-size:10px;
                        letter-spacing:1px; text-transform:uppercase;">
                AI HR Assistant
            </div>
        </div>
    </div>
    <div style="background:rgba(255,255,255,.05); border-radius:8px;
                padding:8px 10px; margin-top:8px;">
        <div style="color:#e2e8f0; font-size:11px;
                    font-weight:700;">Saylani Mass IT Training</div>
        <div style="color:#64748b; font-size:10.5px;
                    margin-top:2px; line-height:1.5;">
            AI & Data Science · Batch 9
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown(
    "<div style='color:#475569; font-size:9.5px; "
    "letter-spacing:1.5px; text-transform:uppercase; "
    "padding:8px 4px 4px; font-weight:700;'>Main Menu</div>",
    unsafe_allow_html=True
)

page = st.sidebar.radio(
    "Navigation",
    [
        "📊  Dashboard",
        "📚  Knowledge Base",
        "💬  HR Q&A",
        "📄  Resume Screener",
    ],
    label_visibility="collapsed"
)

st.sidebar.markdown("<div style='margin-top:16px'></div>",
                    unsafe_allow_html=True)
st.sidebar.divider()

# status pill
st.sidebar.markdown(f"""
<div style="background:rgba(255,255,255,.05); border-radius:8px;
            padding:10px 12px; margin-bottom:12px;">
    <div style="display:flex; align-items:center; gap:8px;">
        <div style="width:7px; height:7px; background:#22c55e;
                    border-radius:50%;"></div>
        <div>
            <div style="color:#e2e8f0; font-size:11px;
                        font-weight:700;">System Ready</div>
            <div style="color:#64748b; font-size:10.5px;
                        margin-top:1px;">RAG + Supabase pgvector</div>
        </div>
    </div>
</div>
<div style="color:#64748b; font-size:10.5px; padding:4px;">
    👤 {current_email}
</div>
""", unsafe_allow_html=True)

if st.sidebar.button(
    "Logout",
    use_container_width=True,
    key="logout_btn"
):
    logout()

st.sidebar.caption("AssistHR v1.0")


# =====================================
# DASHBOARD
# =====================================

if page == "📊  Dashboard":

    # hero banner
    st.markdown("""
    <div style="
        background   : linear-gradient(135deg, #0f172a 0%, #1e3a5f 100%);
        border-radius: 16px;
        padding      : 30px 34px;
        margin-bottom: 24px;
        position     : relative;
        overflow     : hidden;
    ">
        <div style="position:absolute; right:-40px; top:-40px;
                    width:200px; height:200px; border-radius:50%;
                    background:rgba(37,99,235,.3);"></div>
        <div style="position:absolute; right:80px; bottom:-60px;
                    width:150px; height:150px; border-radius:50%;
                    background:rgba(8,145,178,.2);"></div>
        <h2 style="color:white; margin:0; font-size:24px;
                   font-weight:800; position:relative; z-index:1;">
            Welcome to <span style="color:#60a5fa">AssistHR</span> 🤖
        </h2>
        <p style="color:#94a3b8; margin-top:8px; font-size:13.5px;
                  line-height:1.6; position:relative; z-index:1;
                  max-width:500px;">
            AI-powered HR assistant built with RAG,
            Groq LLM and Supabase pgvector.
            Upload HR policies, ask questions,
            screen resumes automatically.
        </p>
        <div style="display:flex; gap:8px; margin-top:16px;
                    flex-wrap:wrap; position:relative; z-index:1;">
            <span style="padding:5px 12px;
                  background:rgba(255,255,255,.1);
                  border:1px solid rgba(255,255,255,.15);
                  border-radius:99px; font-size:11.5px;
                  color:#cbd5e1;">🧠 RAG Pipeline</span>
            <span style="padding:5px 12px;
                  background:rgba(255,255,255,.1);
                  border:1px solid rgba(255,255,255,.15);
                  border-radius:99px; font-size:11.5px;
                  color:#cbd5e1;">🔍 Semantic Search</span>
            <span style="padding:5px 12px;
                  background:rgba(255,255,255,.1);
                  border:1px solid rgba(255,255,255,.15);
                  border-radius:99px; font-size:11.5px;
                  color:#cbd5e1;">📊 Resume Ranking</span>
            <span style="padding:5px 12px;
                  background:rgba(255,255,255,.1);
                  border:1px solid rgba(255,255,255,.15);
                  border-radius:99px; font-size:11.5px;
                  color:#cbd5e1;">⚡ Supabase pgvector</span>
            <span style="padding:5px 12px;
                  background:rgba(255,255,255,.1);
                  border:1px solid rgba(255,255,255,.15);
                  border-radius:99px; font-size:11.5px;
                  color:#cbd5e1;">🤖 Groq llama-3.3-70b</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # metric cards
    from embedding import get_existing_files

    try:
        all_docs   = get_existing_files()
        docs_count = len(all_docs)
    except Exception:
        all_docs   = set()
        docs_count = 0

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📄  Documents", docs_count,
                  help="Total HR documents in knowledge base")
    with col2:
        st.metric("⚡  Vector DB", "pgvector",
                  help="Supabase pgvector for semantic search")
    with col3:
        st.metric("🤖  AI Model", "Groq",
                  help="llama-3.3-70b-versatile")
    with col4:
        st.metric("✅  Status", "Online",
                  help="All systems operational")

    st.markdown("<div style='margin-top:24px'></div>",
                unsafe_allow_html=True)

    # two column layout
    col1, col2 = st.columns([1.6, 1])

    with col1:
        st.markdown("""
        <div style="background:#ffffff; border:1px solid #e2e8f0;
                    border-radius:12px; overflow:hidden;
                    box-shadow:0 1px 3px rgba(0,0,0,.08);">
            <div style="padding:18px 22px 14px;
                        border-bottom:1px solid #e2e8f0;">
                <div style="font-size:14px; font-weight:700;
                            color:#0f172a;">📖 How to Use AssistHR</div>
            </div>
            <div style="padding:18px 22px; display:flex;
                        flex-direction:column; gap:18px;">
                <div style="display:flex; gap:12px; align-items:flex-start;">
                    <div style="min-width:30px; height:30px;
                                background:#2563eb; border-radius:8px;
                                color:#fff; display:flex;
                                align-items:center; justify-content:center;
                                font-weight:800; font-size:13px;">1</div>
                    <div>
                        <div style="font-weight:700; font-size:13.5px;
                                    color:#0f172a;">
                            Upload HR Documents
                        </div>
                        <div style="font-size:12.5px; color:#64748b;
                                    margin-top:3px;">
                            Go to <b>Knowledge Base</b> → Upload HR
                            policy files (PDF, DOCX, TXT).
                        </div>
                    </div>
                </div>
                <div style="display:flex; gap:12px; align-items:flex-start;">
                    <div style="min-width:30px; height:30px;
                                background:#0891b2; border-radius:8px;
                                color:#fff; display:flex;
                                align-items:center; justify-content:center;
                                font-weight:800; font-size:13px;">2</div>
                    <div>
                        <div style="font-weight:700; font-size:13.5px;
                                    color:#0f172a;">
                            Ask Questions (RAG)
                        </div>
                        <div style="font-size:12.5px; color:#64748b;
                                    margin-top:3px;">
                            Go to <b>HR Q&A</b> → Type any question
                            about your uploaded documents.
                        </div>
                    </div>
                </div>
                <div style="display:flex; gap:12px; align-items:flex-start;">
                    <div style="min-width:30px; height:30px;
                                background:#d97706; border-radius:8px;
                                color:#fff; display:flex;
                                align-items:center; justify-content:center;
                                font-weight:800; font-size:13px;">3</div>
                    <div>
                        <div style="font-weight:700; font-size:13.5px;
                                    color:#0f172a;">
                            Screen Resumes
                        </div>
                        <div style="font-size:12.5px; color:#64748b;
                                    margin-top:3px;">
                            Go to <b>Resume Screener</b> → Upload JD
                            + resumes → get ranked results.
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background:#ffffff; border:1px solid #e2e8f0;
                    border-radius:12px; overflow:hidden;
                    box-shadow:0 1px 3px rgba(0,0,0,.08);">
            <div style="padding:18px 22px 14px;
                        border-bottom:1px solid #e2e8f0;">
                <div style="font-size:14px; font-weight:700;
                            color:#0f172a;">📊 System Info</div>
            </div>
            <div style="padding:18px 22px;">
        """, unsafe_allow_html=True)

        info_items = [
            ("🤖", "LLM",        "Groq llama-3.3-70b"),
            ("⚡", "Vector DB",  "Supabase pgvector"),
            ("📐", "Embeddings", "all-MiniLM-L12-v2"),
            ("🔍", "Search",     "Cosine Similarity"),
            ("🗄️", "Database",   "Supabase PostgreSQL"),
            ("🔐", "Auth",       "Supabase Auth"),
        ]

        for icon, label, value in info_items:
            st.markdown(f"""
            <div style="display:flex; justify-content:space-between;
                        align-items:center; padding:8px 0;
                        border-bottom:1px solid #f1f5f9;">
                <div style="font-size:12.5px; color:#64748b;">
                    {icon} {label}
                </div>
                <div style="font-size:12px; font-weight:700;
                            color:#0f172a; background:#f1f5f9;
                            padding:2px 8px; border-radius:99px;">
                    {value}
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div></div>", unsafe_allow_html=True)

    # recent documents
    st.markdown("<div style='margin-top:20px'></div>",
                unsafe_allow_html=True)
    st.markdown("""
    <div style="background:#ffffff; border:1px solid #e2e8f0;
                border-radius:12px; overflow:hidden;
                box-shadow:0 1px 3px rgba(0,0,0,.08);">
        <div style="padding:18px 22px 14px;
                    border-bottom:1px solid #e2e8f0;">
            <div style="font-size:14px; font-weight:700;
                        color:#0f172a;">📁 Recent Documents</div>
        </div>
        <div style="padding:18px 22px;">
    """, unsafe_allow_html=True)

    if not all_docs:
        st.info(
            "No documents yet. "
            "Go to Knowledge Base to upload."
        )
    else:
        for doc in list(all_docs)[:5]:
            ext  = doc.split(".")[-1].lower() \
                   if "." in doc else "file"
            icons = {
                "pdf" : ("📕", "#fee2e2"),
                "docx": ("📘", "#dbeafe"),
                "txt" : ("📄", "#fef9c3")
            }
            icon, bg = icons.get(ext, ("📄", "#f1f5f9"))
            st.markdown(f"""
            <div style="display:flex; align-items:center;
                        gap:12px; padding:10px 0;
                        border-bottom:1px solid #f8fafc;">
                <div style="width:36px; height:36px;
                            background:{bg}; border-radius:8px;
                            display:flex; align-items:center;
                            justify-content:center; font-size:16px;">
                    {icon}
                </div>
                <div style="flex:1; min-width:0;">
                    <div style="font-size:13px; font-weight:600;
                                color:#0f172a; white-space:nowrap;
                                overflow:hidden;
                                text-overflow:ellipsis;">
                        {doc}
                    </div>
                    <div style="font-size:11px; color:#94a3b8;
                                margin-top:2px;">
                        {ext.upper()} document
                    </div>
                </div>
                <div style="font-size:10px; padding:3px 8px;
                            border-radius:99px;
                            background:#eff6ff; color:#2563eb;
                            font-weight:700;">
                    {ext.upper()}
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div></div>", unsafe_allow_html=True)


# =====================================
# KNOWLEDGE BASE
# =====================================

elif page == "📚  Knowledge Base":

    st.markdown("""
    <div style="margin-bottom:24px;">
        <h2 style="font-size:22px; font-weight:800;
                   color:#0f172a; margin:0;">
            📚 Knowledge Base
        </h2>
        <p style="color:#64748b; font-size:13.5px;
                  margin-top:4px;">
            Upload and manage HR documents
        </p>
    </div>
    """, unsafe_allow_html=True)

    from document_loader import load_document
    from chunking        import chunk_documents
    from embedding       import (
        create_vector_store,
        get_existing_files
    )

    # upload card
    st.markdown("""
    <div style="background:#ffffff; border:1px solid #e2e8f0;
                border-radius:12px; overflow:hidden;
                box-shadow:0 1px 3px rgba(0,0,0,.08);
                margin-bottom:20px;">
        <div style="padding:18px 22px 14px;
                    border-bottom:1px solid #e2e8f0;
                    display:flex; justify-content:space-between;
                    align-items:center;">
            <div style="font-size:14px; font-weight:700;
                        color:#0f172a;">📁 Upload HR Document</div>
            <div style="font-size:11.5px; color:#64748b;">
                PDF · DOCX · TXT
            </div>
        </div>
        <div style="padding:18px 22px;">
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Drop file here or click to browse",
        type=["pdf", "docx", "txt"]
    )

    if uploaded:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"""
            <div style="display:flex; align-items:center; gap:10px;
                        padding:10px 14px; background:#eff6ff;
                        border:1px solid #dbeafe; border-radius:8px;
                        font-size:12.5px;">
                <span>📄</span>
                <span style="flex:1; font-weight:600;
                             color:#1d4ed8;">{uploaded.name}</span>
                <span style="color:#64748b;">
                    {uploaded.size/1024:.1f} KB
                </span>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            if st.button(
                "⬆️ Upload & Process",
                use_container_width=True
            ):
                with st.spinner("Processing..."):
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

    # documents list card
    st.markdown("""
    <div style="background:#ffffff; border:1px solid #e2e8f0;
                border-radius:12px; overflow:hidden;
                box-shadow:0 1px 3px rgba(0,0,0,.08);">
        <div style="padding:18px 22px 14px;
                    border-bottom:1px solid #e2e8f0;">
            <div style="font-size:14px; font-weight:700;
                        color:#0f172a;">
                📚 Knowledge Base Documents
            </div>
        </div>
        <div style="padding:18px 22px;">
    """, unsafe_allow_html=True)

    try:
        existing = get_existing_files()
        if not existing:
            st.info(
                "No documents yet. "
                "Upload your first HR document above."
            )
        else:
            for doc in existing:
                ext   = doc.split(".")[-1].lower() \
                        if "." in doc else "file"
                icons = {
                    "pdf" : ("📕", "#fee2e2"),
                    "docx": ("📘", "#dbeafe"),
                    "txt" : ("📄", "#fef9c3")
                }
                icon, bg = icons.get(ext, ("📄", "#f1f5f9"))
                st.markdown(f"""
                <div style="display:flex; align-items:center;
                            gap:12px; padding:12px 0;
                            border-bottom:1px solid #f8fafc;">
                    <div style="width:38px; height:38px;
                                background:{bg}; border-radius:8px;
                                display:flex; align-items:center;
                                justify-content:center;
                                font-size:16px;">{icon}</div>
                    <div style="flex:1; min-width:0;">
                        <div style="font-size:13px; font-weight:600;
                                    color:#0f172a;">{doc}</div>
                        <div style="font-size:11px;
                                    color:#94a3b8; margin-top:2px;">
                            {ext.upper()} · HR Document
                        </div>
                    </div>
                    <div style="font-size:10px; padding:3px 8px;
                                border-radius:99px;
                                background:#eff6ff; color:#2563eb;
                                font-weight:700;">{ext.upper()}</div>
                </div>
                """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Could not load documents: {e}")

    st.markdown("</div></div>", unsafe_allow_html=True)


# =====================================
# HR Q&A
# =====================================

elif page == "💬  HR Q&A":

    st.markdown("""
    <div style="margin-bottom:20px;">
        <h2 style="font-size:22px; font-weight:800;
                   color:#0f172a; margin:0;">
            💬 HR Q&A
        </h2>
        <p style="color:#64748b; font-size:13.5px; margin-top:4px;">
            Ask questions answered from your documents (RAG)
        </p>
    </div>
    """, unsafe_allow_html=True)

    from rag_chain  import ask
    from chat_store import create_session, load_history

    col1, col2 = st.columns([2, 1])
    with col1:
        session_id = st.text_input(
            "Session Name",
            value      = "default",
            placeholder= "e.g. hr-queries"
        )
    with col2:
        model = st.selectbox(
            "Model",
            [
                "llama-3.3-70b-versatile",
                "meta-llama/llama-4-scout-17b-16e-instruct",
                "llama-3.1-8b-instant",
            ]
        )

    full_session = f"{current_email}_{session_id}"

    if "messages"     not in st.session_state or \
       "last_session" not in st.session_state or \
        st.session_state.last_session != full_session:

        st.session_state.last_session = full_session
        try:
            create_session(full_session)
            history = load_history(full_session)
            st.session_state.messages = [
                {
                    "role"   : "user"
                               if msg.type == "human"
                               else "assistant",
                    "content": msg.content
                }
                for msg in history
            ]
        except Exception:
            st.session_state.messages = []

    # suggestion pills
    if not st.session_state.messages:
        st.markdown("""
        <div style="text-align:center; padding:32px 24px 16px;">
            <div style="font-size:40px; margin-bottom:12px;">💬</div>
            <div style="font-size:17px; font-weight:700;
                        color:#0f172a; margin-bottom:6px;">
                Ask AssistHR Anything
            </div>
            <div style="font-size:13px; color:#64748b;">
                Questions answered using your uploaded
                HR documents via RAG
            </div>
        </div>
        """, unsafe_allow_html=True)

        suggestions = [
            "What is the leave policy?",
            "What are the working hours?",
            "How to apply for remote work?",
            "What is the probation period?",
        ]

        cols = st.columns(len(suggestions))
        for col, sug in zip(cols, suggestions):
            with col:
                if st.button(
                    sug,
                    use_container_width=True,
                    key=f"sug_{sug}"
                ):
                    st.session_state.messages.append({
                        "role"   : "user",
                        "content": sug
                    })
                    with st.spinner(
                        "AssistHR is thinking..."
                    ):
                        try:
                            answer = ask(
                                sug,
                                full_session,
                                model
                            )
                            st.session_state\
                                .messages.append({
                                "role"   : "assistant",
                                "content": answer
                            })
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ {e}")

    # show messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # chat input
    if prompt := st.chat_input(
        "Type your HR question here..."
    ):
        st.session_state.messages.append({
            "role"   : "user",
            "content": prompt
        })
        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            with st.spinner(
                "AssistHR is thinking..."
            ):
                try:
                    answer = ask(
                        prompt,
                        full_session,
                        model
                    )
                    st.write(answer)
                    st.session_state.messages.append({
                        "role"   : "assistant",
                        "content": answer
                    })
                except Exception as e:
                    st.error(f"❌ {e}")

    st.caption(
        "Answers sourced from uploaded documents "
        "using Retrieval-Augmented Generation (RAG)"
    )


# =====================================
# RESUME SCREENER
# =====================================

elif page == "📄  Resume Screener":

    st.markdown("""
    <div style="margin-bottom:24px;">
        <h2 style="font-size:22px; font-weight:800;
                   color:#0f172a; margin:0;">
            📄 Resume Screener
        </h2>
        <p style="color:#64748b; font-size:13.5px;
                  margin-top:4px;">
            Semantic AI-based candidate evaluation
        </p>
    </div>
    """, unsafe_allow_html=True)

    from screener import screen_all

    # screening card
    st.markdown("""
    <div style="background:#ffffff; border:1px solid #e2e8f0;
                border-radius:12px; overflow:hidden;
                box-shadow:0 1px 3px rgba(0,0,0,.08);
                margin-bottom:20px;">
        <div style="padding:18px 22px 14px;
                    border-bottom:1px solid #e2e8f0;
                    display:flex; justify-content:space-between;
                    align-items:center;">
            <div style="font-size:14px; font-weight:700;
                        color:#0f172a;">
                🔍 Resume Screening Engine
            </div>
            <div style="font-size:11.5px; color:#64748b;">
                Semantic AI-based evaluation
            </div>
        </div>
        <div style="padding:18px 22px;">
    """, unsafe_allow_html=True)

    model = st.selectbox(
        "Select AI Model",
        [
            "llama-3.3-70b-versatile",
            "meta-llama/llama-4-scout-17b-16e-instruct",
            "llama-3.1-8b-instant",
        ],
        help="llama-3.3-70b recommended for best accuracy"
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div style="font-size:12px; font-weight:700;
                    color:#334155; margin-bottom:7px;">
            📄 Upload Resumes
        </div>
        """, unsafe_allow_html=True)
        resumes = st.file_uploader(
            "Upload Resumes",
            type                 = [
                "pdf", "docx", "jpg", "jpeg", "png"
            ],
            accept_multiple_files= True,
            key                  = "resumes",
            label_visibility     = "collapsed"
        )

    with col2:
        st.markdown("""
        <div style="font-size:12px; font-weight:700;
                    color:#334155; margin-bottom:7px;">
            💼 Upload Job Description
        </div>
        """, unsafe_allow_html=True)
        jd = st.file_uploader(
            "Upload JD",
            type             = ["pdf", "docx"],
            key              = "jd",
            label_visibility = "collapsed"
        )

    # info box
    st.markdown("""
    <div style="margin-top:14px; padding:12px 14px;
                background:#eff6ff; border:1px solid #dbeafe;
                border-radius:8px; font-size:12.5px;
                color:#334155;">
        💡 <b>How scoring works:</b>
        Skills match · Experience level ·
        Education · Role alignment.
        Score ≥ 65 = Recommended.
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        "<div style='margin-top:16px'></div>",
        unsafe_allow_html=True
    )

    if st.button(
        "🔍 Screen Resumes",
        type               = "primary",
        use_container_width= True
    ):
        if not jd:
            st.error("Please upload a Job Description.")
        elif not resumes:
            st.error(
                "Please upload at least one resume."
            )
        else:
            jd_path = f"/tmp/{jd.name}"
            with open(jd_path, "wb") as f:
                f.write(jd.getbuffer())

            resume_paths = []
            for r in resumes:
                path = f"/tmp/{r.name}"
                with open(path, "wb") as f:
                    f.write(r.getbuffer())
                resume_paths.append(path)

            with st.spinner(
                "Screening candidates... "
                "this may take a moment."
            ):
                try:
                    results = screen_all(
                        resume_paths, jd_path, model
                    )
                except Exception as e:
                    st.error(f"❌ {e}")
                    results = []

            if os.path.exists(jd_path):
                os.remove(jd_path)
            for path in resume_paths:
                if os.path.exists(path):
                    os.remove(path)

            if results:
                st.markdown("</div></div>",
                            unsafe_allow_html=True)
                st.success(
                    f"✅ Screened "
                    f"{len(results)} candidate(s)"
                )

                for i, r in enumerate(results, 1):
                    score   = r.get("score",   0)
                    verdict = r.get("verdict", "")
                    name    = r.get("name", "Unknown")

                    # verdict color
                    if "Strongly" in verdict:
                        v_bg  = "#d1fae5"
                        v_col = "#059669"
                    elif "Recommended" in verdict:
                        v_bg  = "#dbeafe"
                        v_col = "#2563eb"
                    elif "Maybe" in verdict:
                        v_bg  = "#fef3c7"
                        v_col = "#d97706"
                    else:
                        v_bg  = "#fee2e2"
                        v_col = "#dc2626"

                    # rank medal
                    medals = {1: "🥇", 2: "🥈", 3: "🥉"}
                    medal  = medals.get(i, f"#{i}")

                    # score color
                    s_col = "#059669" if score >= 65 \
                            else "#d97706" if score >= 40 \
                            else "#dc2626"

                    with st.expander(
                        f"{medal}  {name}  "
                        f"|  {score}%  |  {verdict}",
                        expanded = (i == 1)
                    ):
                        # top section
                        col1, col2 = st.columns([2, 1])
                        with col1:
                            st.markdown(f"""
                            <div style="margin-bottom:12px;">
                                <div style="font-size:20px;
                                            font-weight:800;
                                            color:{s_col};">
                                    {score}/100
                                </div>
                                <div style="height:6px;
                                            background:#e2e8f0;
                                            border-radius:99px;
                                            overflow:hidden;
                                            margin-top:6px;">
                                    <div style="height:100%;
                                                width:{score}%;
                                                background:linear-gradient(90deg,
                                                {s_col},{s_col}99);
                                                border-radius:99px;">
                                    </div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                        with col2:
                            st.markdown(f"""
                            <div style="text-align:right;">
                                <span style="padding:4px 12px;
                                    background:{v_bg};
                                    color:{v_col};
                                    border-radius:99px;
                                    font-size:11px;
                                    font-weight:700;">
                                    {verdict}
                                </span>
                            </div>
                            """, unsafe_allow_html=True)

                        # contact info
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"""
                            <div style="font-size:12.5px;
                                        color:#334155;">
                                📧 {r.get('email','N/A')}<br/>
                                📞 {r.get('phone','N/A')}<br/>
                                🎓 {r.get('education','N/A')}
                            </div>
                            """, unsafe_allow_html=True)
                        with col2:
                            st.markdown(f"""
                            <div style="font-size:12.5px;
                                        color:#334155;">
                                💼 {r.get('experience',
                                          'N/A')}<br/>
                                {'🔗 <a href="' +
                                r.get("linkedin","") +
                                '" target="_blank"'
                                '>LinkedIn</a>'
                                if r.get("linkedin") else ''}
                                {'💻 <a href="' +
                                r.get("github","") +
                                '" target="_blank"'
                                '>GitHub</a>'
                                if r.get("github") else ''}
                            </div>
                            """, unsafe_allow_html=True)

                        st.divider()

                        # skills
                        col1, col2 = st.columns(2)
                        with col1:
                            if r.get("matched_skills"):
                                st.markdown("""
                                <div style="font-size:10.5px;
                                    font-weight:700;
                                    color:#64748b;
                                    text-transform:uppercase;
                                    letter-spacing:.7px;
                                    margin-bottom:7px;">
                                    ✅ Matched Skills
                                </div>
                                """, unsafe_allow_html=True)
                                chips = " ".join([
                                    f'<span style="padding:3px 9px;'
                                    f'border-radius:99px;'
                                    f'font-size:11px;'
                                    f'font-weight:600;'
                                    f'background:#d1fae5;'
                                    f'color:#059669;'
                                    f'border:1px solid #a7f3d0;'
                                    f'margin:2px;'
                                    f'display:inline-block;">'
                                    f'✓ {s}</span>'
                                    for s in
                                    r["matched_skills"][:8]
                                ])
                                st.markdown(
                                    chips,
                                    unsafe_allow_html=True
                                )

                        with col2:
                            if r.get("missing_skills"):
                                st.markdown("""
                                <div style="font-size:10.5px;
                                    font-weight:700;
                                    color:#64748b;
                                    text-transform:uppercase;
                                    letter-spacing:.7px;
                                    margin-bottom:7px;">
                                    ❌ Missing Skills
                                </div>
                                """, unsafe_allow_html=True)
                                chips = " ".join([
                                    f'<span style="padding:3px 9px;'
                                    f'border-radius:99px;'
                                    f'font-size:11px;'
                                    f'font-weight:600;'
                                    f'background:#fee2e2;'
                                    f'color:#dc2626;'
                                    f'border:1px solid #fca5a5;'
                                    f'margin:2px;'
                                    f'display:inline-block;">'
                                    f'✗ {s}</span>'
                                    for s in
                                    r["missing_skills"][:6]
                                ])
                                st.markdown(
                                    chips,
                                    unsafe_allow_html=True
                                )

                        st.divider()

                        # strengths weaknesses
                        st.markdown(f"""
                        <div style="background:#f8fafc;
                                    border-radius:8px;
                                    padding:12px 14px;
                                    font-size:12.5px;
                                    line-height:1.7;
                                    color:#334155;
                                    border:1px solid #e2e8f0;">
                            <div style="margin-bottom:8px;">
                                💪 <b>Strengths:</b>
                                {r.get('strengths', '')}
                            </div>
                            <div>
                                ⚠️ <b>Weaknesses:</b>
                                {r.get('weaknesses', '')}
                            </div>
                        </div>
                        <div style="font-size:10.5px;
                                    color:#94a3b8;
                                    margin-top:8px;
                                    text-align:right;">
                            Model: {r.get('model', model)}
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.warning("No results returned.")
                st.markdown("</div></div>",
                            unsafe_allow_html=True)
                

st.markdown("</div></div>", unsafe_allow_html=True)
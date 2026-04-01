import os
import sys
import streamlit as st
from supabase import create_client

# ── PATH FIX ──────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(BASE_DIR, "backend")
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

# ── SECRETS ───────────────────────────────────────────────────
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

supabase = create_client(
    get_secret("SUPABASE_URL"),
    get_secret("SUPABASE_ANON_KEY")
)

st.set_page_config(
    page_title            = "AssistHR",
    page_icon             = "🤖",
    layout                = "wide",
    initial_sidebar_state = "expanded"
)

# ── GLOBAL CSS ────────────────────────────────────────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet"/>
<style>
html,body,[data-testid="stAppViewContainer"],[data-testid="stMain"]{
    font-family:'Plus Jakarta Sans',sans-serif!important;
}
[data-testid="stAppViewContainer"]{background:#f0f4f8!important;}
[data-theme="dark"] [data-testid="stAppViewContainer"],
[data-theme="dark"] [data-testid="stMain"]{background:#0d1117!important;}
#MainMenu,footer,header{visibility:hidden;}
.block-container{
    padding-top:20px!important;
    padding-left:28px!important;
    padding-right:28px!important;
    max-width:100%!important;
}
/* SIDEBAR */
[data-testid="stSidebar"]{
    background:#0f172a!important;
    min-width:256px!important;
    max-width:256px!important;
}
[data-testid="stSidebar"] *{font-family:'Plus Jakarta Sans',sans-serif!important;}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label{color:#94a3b8!important;}
[data-testid="stSidebarNav"]{display:none!important;}
[data-testid="stSidebar"] .stRadio>div{gap:2px!important;}
[data-testid="stSidebar"] .stRadio label{
    display:flex!important;align-items:center!important;
    gap:8px!important;padding:10px 14px!important;
    border-radius:10px!important;color:#94a3b8!important;
    font-size:13.5px!important;font-weight:500!important;
    transition:all .15s!important;cursor:pointer!important;
    border:none!important;
}
[data-testid="stSidebar"] .stRadio label:hover{
    background:rgba(255,255,255,.08)!important;color:#e2e8f0!important;
}
/* METRIC CARDS */
div[data-testid="metric-container"]{
    background:#ffffff;border:1px solid #e2e8f0;
    border-radius:14px;padding:20px 22px!important;
    box-shadow:0 1px 3px rgba(0,0,0,.06),0 4px 16px rgba(0,0,0,.04);
    min-height:108px;position:relative;overflow:hidden;
    transition:transform .2s,box-shadow .2s;
}
div[data-testid="metric-container"]:hover{
    transform:translateY(-2px);box-shadow:0 8px 24px rgba(0,0,0,.09);
}
[data-theme="dark"] div[data-testid="metric-container"]{
    background:#1e293b!important;border:1px solid #334155!important;
}
div[data-testid="metric-container"] label{
    font-size:10.5px!important;font-weight:700!important;
    text-transform:uppercase!important;letter-spacing:.07em!important;
    color:#64748b!important;
}
[data-theme="dark"] div[data-testid="metric-container"] label{color:#94a3b8!important;}
div[data-testid="metric-container"] [data-testid="stMetricValue"]{
    font-size:26px!important;font-weight:800!important;
    color:#0f172a!important;line-height:1.2!important;
}
[data-theme="dark"] div[data-testid="metric-container"] [data-testid="stMetricValue"]{
    color:#f1f5f9!important;
}
[data-testid="column"]:nth-child(1) div[data-testid="metric-container"]::before,
[data-testid="column"]:nth-child(2) div[data-testid="metric-container"]::before,
[data-testid="column"]:nth-child(3) div[data-testid="metric-container"]::before,
[data-testid="column"]:nth-child(4) div[data-testid="metric-container"]::before{
    content:'';position:absolute;top:0;left:0;right:0;
    height:3px;border-radius:14px 14px 0 0;
}
[data-testid="column"]:nth-child(1) div[data-testid="metric-container"]::before{
    background:linear-gradient(90deg,#2563eb,#60a5fa);}
[data-testid="column"]:nth-child(2) div[data-testid="metric-container"]::before{
    background:linear-gradient(90deg,#0891b2,#22d3ee);}
[data-testid="column"]:nth-child(3) div[data-testid="metric-container"]::before{
    background:linear-gradient(90deg,#7c3aed,#a78bfa);}
[data-testid="column"]:nth-child(4) div[data-testid="metric-container"]::before{
    background:linear-gradient(90deg,#059669,#34d399);}
/* BUTTONS */
.stButton>button{
    font-family:'Plus Jakarta Sans',sans-serif!important;
    font-weight:600!important;border-radius:10px!important;
    transition:all .18s!important;border:none!important;
}
.stButton>button[kind="primary"]{
    background:linear-gradient(135deg,#2563eb,#1d4ed8)!important;
    color:#fff!important;box-shadow:0 2px 8px rgba(37,99,235,.3)!important;
}
.stButton>button[kind="primary"]:hover{
    background:linear-gradient(135deg,#1d4ed8,#1e40af)!important;
    transform:translateY(-1px)!important;
    box-shadow:0 6px 20px rgba(37,99,235,.4)!important;
}
.stButton>button[kind="secondary"]{
    background:transparent!important;
    border:1.5px solid #e2e8f0!important;color:#334155!important;
}
[data-theme="dark"] .stButton>button[kind="secondary"]{
    border-color:#334155!important;color:#cbd5e1!important;
}
/* INPUTS */
.stTextInput input,.stTextArea textarea,.stSelectbox>div>div{
    font-family:'Plus Jakarta Sans',sans-serif!important;
    border-radius:10px!important;border:1.5px solid #e2e8f0!important;
    transition:all .18s!important;font-size:13.5px!important;
}
.stTextInput input:focus,.stTextArea textarea:focus{
    border-color:#2563eb!important;
    box-shadow:0 0 0 3px rgba(37,99,235,.12)!important;
}
[data-theme="dark"] .stTextInput input,
[data-theme="dark"] .stTextArea textarea{
    border-color:#334155!important;background:#1e293b!important;color:#f1f5f9!important;
}
/* FILE UPLOADER */
[data-testid="stFileUploader"]{
    border:2px dashed #cbd5e1!important;border-radius:12px!important;
    background:#f8fafc!important;transition:all .18s!important;
}
[data-testid="stFileUploader"]:hover{
    border-color:#2563eb!important;background:#eff6ff!important;
}
[data-theme="dark"] [data-testid="stFileUploader"]{
    border-color:#334155!important;background:#1e293b!important;
}
/* EXPANDER */
[data-testid="stExpander"]{
    border:1.5px solid #e2e8f0!important;border-radius:14px!important;
    background:#ffffff!important;box-shadow:0 1px 4px rgba(0,0,0,.05)!important;
    margin-bottom:12px!important;overflow:hidden!important;transition:all .18s!important;
}
[data-testid="stExpander"]:hover{box-shadow:0 6px 20px rgba(0,0,0,.08)!important;}
[data-theme="dark"] [data-testid="stExpander"]{
    background:#1e293b!important;border-color:#334155!important;
}
/* CHAT */
[data-testid="stChatMessage"]{
    border-radius:14px!important;border:1px solid #e2e8f0!important;
    margin-bottom:10px!important;box-shadow:0 1px 4px rgba(0,0,0,.04)!important;
}
[data-theme="dark"] [data-testid="stChatMessage"]{
    border-color:#334155!important;background:#1e293b!important;
}
/* MISC */
hr{border-color:#e2e8f0!important;margin:18px 0!important;}
[data-theme="dark"] hr{border-color:#334155!important;}
[data-testid="stProgress"]>div>div{
    background:linear-gradient(90deg,#2563eb,#0891b2)!important;
    border-radius:99px!important;
}
.stSuccess,.stError,.stInfo,.stWarning{
    border-radius:10px!important;
    font-family:'Plus Jakarta Sans',sans-serif!important;
}
/* CUSTOM */
.card{background:#ffffff;border:1px solid #e2e8f0;border-radius:14px;
      overflow:hidden;box-shadow:0 1px 4px rgba(0,0,0,.06);margin-bottom:18px;}
[data-theme="dark"] .card{background:#1e293b;border-color:#334155;}
.card-head{padding:16px 22px;border-bottom:1px solid #e2e8f0;
           display:flex;align-items:center;justify-content:space-between;}
[data-theme="dark"] .card-head{border-color:#334155;}
.card-title{font-size:14px;font-weight:700;color:#0f172a;
            font-family:'Plus Jakarta Sans',sans-serif;}
[data-theme="dark"] .card-title{color:#f1f5f9;}
.card-body{padding:18px 22px;}
.doc-row{display:flex;align-items:center;gap:12px;padding:10px 14px;
         border-radius:10px;margin-bottom:6px;border:1px solid #e2e8f0;
         background:#ffffff;transition:all .18s;font-size:13px;
         font-weight:500;color:#334155;font-family:'Plus Jakarta Sans',sans-serif;}
.doc-row:hover{border-color:#2563eb;box-shadow:0 0 0 3px rgba(37,99,235,.08);}
[data-theme="dark"] .doc-row{background:#1e293b;border-color:#334155;color:#cbd5e1;}
.doc-badge{font-size:10px;padding:2px 8px;border-radius:99px;
           background:#eff6ff;color:#2563eb;font-weight:700;
           text-transform:uppercase;margin-left:auto;flex-shrink:0;}
[data-theme="dark"] .doc-badge{background:#1e3a5f;color:#60a5fa;}
.chip-green{display:inline-block;padding:3px 10px;border-radius:99px;
            font-size:11.5px;font-weight:600;background:#d1fae5;
            color:#059669;border:1px solid #a7f3d0;margin:2px;}
.chip-red{display:inline-block;padding:3px 10px;border-radius:99px;
          font-size:11.5px;font-weight:600;background:#fee2e2;
          color:#dc2626;border:1px solid #fca5a5;margin:2px;}
.verdict-pill{display:inline-block;padding:4px 13px;border-radius:99px;
              font-size:11px;font-weight:700;}
.info-row{display:flex;justify-content:space-between;align-items:center;
          padding:9px 0;border-bottom:1px solid #f1f5f9;
          font-size:12.5px;color:#64748b;}
[data-theme="dark"] .info-row{border-color:#1e293b;color:#94a3b8;}
.info-badge{font-size:11.5px;font-weight:700;background:#f1f5f9;
            padding:3px 10px;border-radius:99px;color:#0f172a;}
[data-theme="dark"] .info-badge{background:#334155;color:#f1f5f9;}
.step-row{display:flex;gap:12px;align-items:flex-start;margin-bottom:18px;}
.step-num{min-width:30px;height:30px;border-radius:8px;color:#fff;
          display:flex;align-items:center;justify-content:center;
          font-weight:800;font-size:13px;flex-shrink:0;}
.step-title{font-size:13.5px;font-weight:700;color:#0f172a;margin-bottom:3px;}
[data-theme="dark"] .step-title{color:#f1f5f9;}
.step-desc{font-size:12.5px;color:#64748b;line-height:1.5;}
.session-pill{display:inline-flex;align-items:center;gap:6px;
              padding:6px 12px;border-radius:8px;font-size:12px;
              font-weight:500;color:#94a3b8;cursor:pointer;
              transition:all .15s;border:1px solid transparent;
              width:100%;margin-bottom:2px;background:transparent;}
.session-pill:hover{background:rgba(255,255,255,.08);color:#e2e8f0;}
.session-pill.active{background:rgba(37,99,235,.25);
                     border-color:rgba(37,99,235,.4);color:#93c5fd;}
.score-bar-wrap{height:6px;background:#e2e8f0;border-radius:99px;
                overflow:hidden;margin-top:6px;}
[data-theme="dark"] .score-bar-wrap{background:#334155;}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# AUTH
# ══════════════════════════════════════════════════════════════
def login_page():
    _, col, _ = st.columns([1, 1.4, 1])
    with col:
        st.markdown("""
        <div style="background:linear-gradient(135deg,#0f172a 0%,#1e3a5f 100%);
            border-radius:20px;padding:36px 32px 28px;text-align:center;
            margin-bottom:24px;position:relative;overflow:hidden;">
            <div style="position:absolute;right:-30px;top:-30px;width:150px;
                height:150px;border-radius:50%;background:rgba(37,99,235,.25);"></div>
            <div style="position:absolute;left:-20px;bottom:-40px;width:120px;
                height:120px;border-radius:50%;background:rgba(8,145,178,.2);"></div>
            <div style="font-size:48px;margin-bottom:10px;position:relative;z-index:1;">🤖</div>
            <div style="font-size:26px;font-weight:800;color:#fff;
                font-family:'Plus Jakarta Sans',sans-serif;position:relative;z-index:1;">
                AssistHR</div>
            <div style="font-size:11px;color:#60a5fa;font-weight:700;letter-spacing:2px;
                text-transform:uppercase;margin-top:4px;position:relative;z-index:1;">
                AI · HR · Intelligence</div>
            <div style="display:flex;gap:7px;justify-content:center;flex-wrap:wrap;
                margin-top:14px;position:relative;z-index:1;">
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
        """, unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])
        with tab1:
            email    = st.text_input("Email", key="le", placeholder="you@company.com")
            password = st.text_input("Password", type="password", key="lp", placeholder="••••••••")
            if st.button("Login →", use_container_width=True, type="primary", key="lb"):
                if not email or not password:
                    st.error("Please fill in all fields.")
                else:
                    try:
                        r = supabase.auth.sign_in_with_password({"email": email, "password": password})
                        st.session_state.user  = r.user
                        st.session_state.token = r.session.access_token
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ {e}")

        with tab2:
            name     = st.text_input("Full Name", key="rn", placeholder="John Smith")
            email    = st.text_input("Email", key="re", placeholder="you@company.com")
            password = st.text_input("Password", type="password", key="rp", placeholder="Min 6 chars")
            confirm  = st.text_input("Confirm Password", type="password", key="rc", placeholder="Repeat")
            if st.button("Create Account →", use_container_width=True, type="primary", key="rb"):
                if not all([name, email, password, confirm]):
                    st.error("Please fill in all fields.")
                elif len(password) < 6:
                    st.error("Password must be at least 6 characters.")
                elif password != confirm:
                    st.error("Passwords do not match.")
                else:
                    try:
                        supabase.auth.sign_up({"email": email, "password": password,
                                               "options": {"data": {"name": name}}})
                        st.success("✅ Account created! Please login.")
                    except Exception as e:
                        st.error(f"❌ {e}")


def logout():
    try:
        supabase.auth.sign_out()
    except Exception:
        pass
    for k in ["user","token","messages","last_session","active_session"]:
        st.session_state.pop(k, None)
    st.rerun()


if "user" not in st.session_state:
    st.session_state.user  = None
    st.session_state.token = None

if not st.session_state.user:
    login_page()
    st.stop()

current_email = st.session_state.user.email


# ══════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════
st.sidebar.markdown(f"""
<div style="padding:18px 14px 10px;">
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;">
        <div style="width:36px;height:36px;background:#2563eb;border-radius:10px;
            display:flex;align-items:center;justify-content:center;font-size:17px;flex-shrink:0;">🤖</div>
        <div>
            <div style="color:#fff;font-size:16px;font-weight:800;
                font-family:'Plus Jakarta Sans',sans-serif;line-height:1;">AssistHR</div>
            <div style="color:#475569;font-size:9px;letter-spacing:1.2px;
                text-transform:uppercase;margin-top:1px;">AI HR Assistant</div>
        </div>
    </div>
    <div style="background:rgba(255,255,255,.05);border-radius:8px;padding:8px 10px;margin-bottom:6px;">
        <div style="color:#e2e8f0;font-size:11px;font-weight:700;">Saylani Mass IT Training</div>
        <div style="color:#64748b;font-size:10px;margin-top:1px;line-height:1.5;">AI & Data Science · Batch 9</div>
    </div>
</div>
<div style="padding:2px 14px 4px;">
    <div style="color:#475569;font-size:9px;letter-spacing:1.5px;text-transform:uppercase;font-weight:700;">
        Main Menu</div>
</div>
""", unsafe_allow_html=True)

page = st.sidebar.radio(
    "nav",
    ["📊  Dashboard","📚  Knowledge Base","💬  HR Q&A","📄  Resume Screener"],
    label_visibility="collapsed"
)

st.sidebar.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

# Chat sessions panel (only on Q&A page)
if page == "💬  HR Q&A":
    st.sidebar.markdown("""
    <div style="padding:0 14px 4px;">
        <div style="color:#475569;font-size:9px;letter-spacing:1.5px;
            text-transform:uppercase;font-weight:700;margin-bottom:6px;">
            Chat Sessions</div>
    </div>
    """, unsafe_allow_html=True)

    if st.sidebar.button("＋ New Session", use_container_width=True, key="new_sess"):
        import time
        st.session_state.active_session = f"session_{int(time.time())}"
        st.session_state.messages       = []
        st.session_state.last_session   = ""
        st.rerun()

    try:
        from chat_store import get_conn as _gc
        _conn = _gc()
        _cur  = _conn.cursor()
        _cur.execute("""
            SELECT session_id FROM sessions
            WHERE session_id LIKE %s
            ORDER BY last_active DESC LIMIT 10
        """, (f"{current_email}_%",))
        _rows = _cur.fetchall()
        _conn.close()
        active = st.session_state.get("active_session", "default")
        for row in _rows:
            raw   = row[0]
            disp  = raw.split("_", 1)[1] if "_" in raw else raw
            is_on = (disp == active)
            cls   = "active" if is_on else ""
            if st.sidebar.button(
                f"{'🔵' if is_on else '💬'} {disp}",
                key=f"s_{raw}",
                use_container_width=True
            ):
                st.session_state.active_session = disp
                st.session_state.messages       = []
                st.session_state.last_session   = ""
                st.rerun()
    except Exception:
        pass

st.sidebar.divider()

st.sidebar.markdown(f"""
<div style="padding:0 6px;">
    <div style="display:flex;align-items:center;gap:8px;background:rgba(255,255,255,.05);
        border-radius:8px;padding:9px 11px;margin-bottom:10px;">
        <div style="width:7px;height:7px;background:#22c55e;border-radius:50%;
            flex-shrink:0;box-shadow:0 0 6px #22c55e;"></div>
        <div>
            <div style="color:#e2e8f0;font-size:11px;font-weight:700;">System Ready</div>
            <div style="color:#64748b;font-size:10px;margin-top:1px;">RAG · pgvector · Groq</div>
        </div>
    </div>
    <div style="color:#64748b;font-size:11px;padding:0 2px 8px;overflow:hidden;
        text-overflow:ellipsis;white-space:nowrap;" title="{current_email}">
        👤 {current_email}</div>
</div>
""", unsafe_allow_html=True)

if st.sidebar.button("Logout", use_container_width=True, key="logout_btn"):
    logout()

st.sidebar.markdown("""
<div style="padding:10px 6px 4px;text-align:center;">
    <div style="color:#334155;font-size:9.5px;font-family:'JetBrains Mono',monospace;">
        AssistHR v1.0 · MIT</div>
</div>
""", unsafe_allow_html=True)


# ── HELPERS ──────────────────────────────────────────────────
def card_start(title, subtitle=""):
    sub = (f'<span style="font-size:11.5px;color:#64748b;">{subtitle}</span>'
           if subtitle else "")
    st.markdown(
        f'<div class="card"><div class="card-head">'
        f'<div class="card-title">{title}</div>{sub}'
        f'</div><div class="card-body">',
        unsafe_allow_html=True
    )

def card_end():
    st.markdown("</div></div>", unsafe_allow_html=True)

def doc_row(name):
    ext  = name.split(".")[-1].lower() if "." in name else "file"
    icon = {"pdf":"📕","docx":"📘","txt":"📄"}.get(ext,"📄")
    st.markdown(f"""
    <div class="doc-row">
        <span style="font-size:18px;">{icon}</span>
        <span style="flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{name}</span>
        <span class="doc-badge">{ext}</span>
    </div>
    """, unsafe_allow_html=True)

def section_header(title, sub=""):
    st.markdown(f"""
    <h2 style="font-size:22px;font-weight:800;color:#0f172a;margin:0 0 4px;
               font-family:'Plus Jakarta Sans',sans-serif;">{title}</h2>
    {'<p style="color:#64748b;font-size:13.5px;margin-bottom:18px;">'+sub+'</p>' if sub else ''}
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════════════
if page == "📊  Dashboard":

    st.markdown("""
    <div style="background:linear-gradient(135deg,#0f172a 0%,#1e3a5f 100%);
        border-radius:18px;padding:30px 34px;margin-bottom:22px;
        position:relative;overflow:hidden;">
        <div style="position:absolute;right:-40px;top:-40px;width:200px;height:200px;
            border-radius:50%;background:rgba(37,99,235,.22);"></div>
        <div style="position:absolute;right:90px;bottom:-60px;width:160px;height:160px;
            border-radius:50%;background:rgba(8,145,178,.18);"></div>
        <div style="position:relative;z-index:1;">
            <h2 style="color:#fff;margin:0;font-size:23px;font-weight:800;
                font-family:'Plus Jakarta Sans',sans-serif;">
                Welcome to <span style="color:#60a5fa;">AssistHR</span> 🤖</h2>
            <p style="color:#94a3b8;margin:8px 0 14px;font-size:13.5px;
                line-height:1.6;max-width:520px;">
                AI-powered HR assistant with RAG, Groq LLM and Supabase pgvector.
                Upload HR policies, ask questions, screen resumes.</p>
            <div style="display:flex;gap:7px;flex-wrap:wrap;">
                <span style="padding:4px 12px;background:rgba(255,255,255,.1);
                    border:1px solid rgba(255,255,255,.14);border-radius:99px;
                    font-size:11.5px;color:#cbd5e1;">🧠 RAG Pipeline</span>
                <span style="padding:4px 12px;background:rgba(255,255,255,.1);
                    border:1px solid rgba(255,255,255,.14);border-radius:99px;
                    font-size:11.5px;color:#cbd5e1;">🔍 Semantic Search</span>
                <span style="padding:4px 12px;background:rgba(255,255,255,.1);
                    border:1px solid rgba(255,255,255,.14);border-radius:99px;
                    font-size:11.5px;color:#cbd5e1;">📊 Resume Ranking</span>
                <span style="padding:4px 12px;background:rgba(255,255,255,.1);
                    border:1px solid rgba(255,255,255,.14);border-radius:99px;
                    font-size:11.5px;color:#cbd5e1;">⚡ Supabase pgvector</span>
                <span style="padding:4px 12px;background:rgba(255,255,255,.1);
                    border:1px solid rgba(255,255,255,.14);border-radius:99px;
                    font-size:11.5px;color:#cbd5e1;">🤖 Groq llama-3.3-70b</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # load data
    try:
        from embedding import get_existing_files
        all_docs   = get_existing_files()
        docs_count = len(all_docs)
    except Exception:
        all_docs   = set()
        docs_count = 0

    try:
        from chat_store import get_conn as _gc
        _c = _gc(); _cur = _c.cursor()
        _cur.execute(
            "SELECT COUNT(*) FROM sessions WHERE session_id LIKE %s",
            (f"{current_email}_%",)
        )
        sessions_count = _cur.fetchone()[0]; _c.close()
    except Exception:
        sessions_count = 0

    # metrics
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("📄  Documents",     docs_count,   help="HR documents indexed")
    with c2: st.metric("💬  Chat Sessions", sessions_count, help="Your chat sessions")
    with c3: st.metric("🤖  LLM",           "Groq",       help="llama-3.3-70b-versatile")
    with c4: st.metric("✅  Status",         "Online",     help="All systems operational")

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    left, right = st.columns([1.55, 1], gap="medium")

    with left:
        card_start("📖 How to Use AssistHR")
        for color, num, title, desc in [
            ("#2563eb","1","Upload HR Documents",
             "Go to <b>Knowledge Base</b> → Upload PDF, DOCX or TXT. Files are chunked and indexed automatically."),
            ("#0891b2","2","Ask Questions (RAG)",
             "Go to <b>HR Q&A</b> → Type your question. AssistHR retrieves relevant context and answers using Groq LLM."),
            ("#d97706","3","Screen Resumes",
             "Go to <b>Resume Screener</b> → Upload JD + resumes → get ranked candidates with scores and analysis."),
        ]:
            st.markdown(f"""
            <div class="step-row">
                <div class="step-num" style="background:{color};">{num}</div>
                <div>
                    <div class="step-title">{title}</div>
                    <div class="step-desc">{desc}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        card_end()

    with right:
        card_start("⚙️ System Info")
        for label, value in [
            ("🤖 LLM","Groq llama-3.3-70b"),("⚡ Vector DB","Supabase pgvector"),
            ("📐 Embeddings","MiniLM-L12-v2"),("🔍 Search","Cosine Similarity"),
            ("🗄️ Database","Supabase PostgreSQL"),("🔐 Auth","Supabase Auth"),
        ]:
            st.markdown(f"""
            <div class="info-row">
                <span>{label}</span>
                <span class="info-badge">{value}</span>
            </div>
            """, unsafe_allow_html=True)
        card_end()

    card_start("📁 Recent Documents",
               f'{docs_count} file{"s" if docs_count!=1 else ""}')
    if not all_docs:
        st.info("No documents yet. Go to Knowledge Base to upload.")
    else:
        for name in list(all_docs)[:6]:
            doc_row(name)
    card_end()


# ══════════════════════════════════════════════════════════════
# KNOWLEDGE BASE
# ══════════════════════════════════════════════════════════════
elif page == "📚  Knowledge Base":
    section_header("📚 Knowledge Base", "Upload and manage HR documents")

    from document_loader import load_document
    from chunking        import chunk_documents
    from embedding       import create_vector_store, get_existing_files

    card_start("📁 Upload HR Document", "PDF · DOCX · TXT")
    uploaded = st.file_uploader("Drop file here or click to browse",
                                type=["pdf","docx","txt"])
    if uploaded:
        c1, c2 = st.columns([3,1])
        with c1:
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:10px;padding:10px 14px;
                background:#eff6ff;border:1px solid #dbeafe;border-radius:10px;
                font-size:12.5px;margin-top:8px;">
                <span>📄</span>
                <span style="flex:1;font-weight:600;color:#1d4ed8;">{uploaded.name}</span>
                <span style="color:#64748b;">{uploaded.size/1024:.1f} KB</span>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            if st.button("⬆️ Process", use_container_width=True, type="primary"):
                with st.spinner(f"Processing '{uploaded.name}'..."):
                    tmp = f"/tmp/{uploaded.name}"
                    with open(tmp,"wb") as f: f.write(uploaded.getbuffer())
                    try:
                        docs   = load_document(tmp)
                        chunks = chunk_documents(docs)
                        create_vector_store(chunks)
                        st.success(f"✅ '{uploaded.name}' — {len(chunks)} chunks indexed")
                    except Exception as e:
                        st.error(f"❌ {e}")
                    finally:
                        if os.path.exists(tmp): os.remove(tmp)
    card_end()

    card_start("📚 Indexed Documents")
    try:
        existing = get_existing_files()
        if not existing:
            st.info("No documents yet. Upload above.")
        else:
            for name in existing:
                doc_row(name)
    except Exception as e:
        st.error(f"Could not load: {e}")
    card_end()


# ══════════════════════════════════════════════════════════════
# HR Q&A
# ══════════════════════════════════════════════════════════════
elif page == "💬  HR Q&A":
    section_header("💬 HR Q&A", "Ask questions answered from your documents via RAG")

    from rag_chain  import ask
    from chat_store import create_session, load_history

    c1, c2 = st.columns([2,1])
    with c1:
        default_sess = st.session_state.get("active_session","default")
        session_id   = st.text_input("Session Name", value=default_sess,
                                     placeholder="e.g. hr-queries",
                                     key="qa_sess_input")
        st.session_state.active_session = session_id
    with c2:
        model = st.selectbox("Model",[
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
                {"role":"user" if m.type=="human" else "assistant",
                 "content":m.content} for m in history
            ]
        except Exception:
            st.session_state.messages = []

    if not st.session_state.messages:
        st.markdown("""
        <div style="text-align:center;padding:32px 24px 18px;">
            <div style="font-size:44px;margin-bottom:12px;">💬</div>
            <div style="font-size:18px;font-weight:700;color:#0f172a;margin-bottom:6px;
                font-family:'Plus Jakarta Sans',sans-serif;">Ask AssistHR Anything</div>
            <div style="font-size:13px;color:#64748b;max-width:340px;
                margin:0 auto;line-height:1.6;">
                Questions answered from your uploaded HR documents using RAG</div>
        </div>
        """, unsafe_allow_html=True)
        sugs = ["What is the leave policy?","What are working hours?",
                "How to apply for remote work?","What is the probation period?"]
        cols = st.columns(len(sugs))
        for col, sug in zip(cols, sugs):
            with col:
                if st.button(sug, use_container_width=True, key=f"sug_{sug}"):
                    st.session_state.messages.append({"role":"user","content":sug})
                    with st.spinner("Thinking..."):
                        try:
                            ans = ask(sug, full_session, model)
                            st.session_state.messages.append({"role":"assistant","content":ans})
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ {e}")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt := st.chat_input("Ask about HR policies, leave, dress code..."):
        st.session_state.messages.append({"role":"user","content":prompt})
        with st.chat_message("user"): st.write(prompt)
        with st.chat_message("assistant"):
            with st.spinner("AssistHR is thinking..."):
                try:
                    ans = ask(prompt, full_session, model)
                    st.write(ans)
                    st.session_state.messages.append({"role":"assistant","content":ans})
                except Exception as e:
                    st.error(f"❌ {e}")

    st.caption("💡 Answers sourced from uploaded documents via RAG")


# ══════════════════════════════════════════════════════════════
# RESUME SCREENER
# ══════════════════════════════════════════════════════════════
elif page == "📄  Resume Screener":
    section_header("📄 Resume Screener","Semantic AI-based candidate evaluation")

    from screener import screen_all

    card_start("🔍 Screening Engine","Semantic AI evaluation")

    model = st.selectbox("AI Model",[
        "llama-3.3-70b-versatile",
        "meta-llama/llama-4-scout-17b-16e-instruct",
        "llama-3.1-8b-instant",
    ], help="llama-3.3-70b recommended")

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2, gap="medium")
    with c1:
        st.markdown("""<div style="font-size:12px;font-weight:700;color:#334155;margin-bottom:6px;">
            📄 Upload Resumes <span style="color:#94a3b8;font-weight:400;">(PDF · DOCX · JPG · PNG)</span></div>
        """, unsafe_allow_html=True)
        resumes = st.file_uploader("Resumes", type=["pdf","docx","jpg","jpeg","png"],
                                   accept_multiple_files=True, key="resumes",
                                   label_visibility="collapsed")
    with c2:
        st.markdown("""<div style="font-size:12px;font-weight:700;color:#334155;margin-bottom:6px;">
            💼 Job Description <span style="color:#94a3b8;font-weight:400;">(file or text)</span></div>
        """, unsafe_allow_html=True)
        jd_t1, jd_t2 = st.tabs(["📁 Upload File","📝 Paste Text"])
        with jd_t1:
            jd_file = st.file_uploader("JD File", type=["pdf","docx"],
                                       key="jd_file", label_visibility="collapsed")
        with jd_t2:
            jd_text = st.text_area("JD Text",
                                   placeholder="Paste job description here...\n\nRole, required skills, experience...",
                                   height=150, key="jd_text", label_visibility="collapsed")

    st.markdown("""
    <div style="margin-top:12px;padding:11px 15px;background:#eff6ff;
        border:1px solid #dbeafe;border-radius:10px;font-size:12.5px;color:#334155;">
        💡 <b>Scoring:</b> Skills match · Experience level · Education · Role alignment.
        Score ≥ 65 = Recommended.
    </div>
    <div style="height:14px;"></div>
    """, unsafe_allow_html=True)

    screen_btn = st.button("🔍 Screen Resumes", type="primary", use_container_width=True)
    card_end()

    if screen_btn:
        has_jd_file = jd_file is not None
        has_jd_text = bool(jd_text and jd_text.strip())

        if not resumes:
            st.error("Please upload at least one resume.")
        elif not has_jd_file and not has_jd_text:
            st.error("Please upload a JD file or paste JD text.")
        else:
            if has_jd_file:
                jd_path = f"/tmp/{jd_file.name}"
                with open(jd_path,"wb") as f: f.write(jd_file.getbuffer())
            else:
                jd_path = "/tmp/job_description.txt"
                with open(jd_path,"w",encoding="utf-8") as f: f.write(jd_text)

            resume_paths = []
            for r in resumes:
                p = f"/tmp/{r.name}"
                with open(p,"wb") as f: f.write(r.getbuffer())
                resume_paths.append(p)

            with st.spinner(f"Screening {len(resumes)} candidate(s)..."):
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

                # ranking summary table
                card_start("🏆 Ranking Summary")
                medals = {1:"🥇",2:"🥈",3:"🥉"}

                hc = st.columns([.4,2.2,1,1.6,1.4])
                for h, t in zip(hc,["#","Candidate","Score","Verdict","Experience"]):
                    h.markdown(f"**{t}**")
                st.divider()

                for i, r in enumerate(results, 1):
                    score   = r.get("score",0)
                    verdict = r.get("verdict","")
                    if "Strongly" in verdict: v_bg,v_col="#d1fae5","#059669"
                    elif "Recommended" in verdict: v_bg,v_col="#dbeafe","#2563eb"
                    elif "Maybe" in verdict: v_bg,v_col="#fef3c7","#d97706"
                    else: v_bg,v_col="#fee2e2","#dc2626"
                    s_col = "#059669" if score>=65 else "#d97706" if score>=40 else "#dc2626"

                    rc = st.columns([.4,2.2,1,1.6,1.4])
                    rc[0].write(medals.get(i,f"#{i}"))
                    rc[1].write(f"**{r.get('name','Unknown')}**")
                    rc[2].markdown(f'<span style="font-weight:800;color:{s_col};">{score}%</span>',
                                   unsafe_allow_html=True)
                    rc[3].markdown(f'<span class="verdict-pill" style="background:{v_bg};color:{v_col};">{verdict}</span>',
                                   unsafe_allow_html=True)
                    rc[4].write(r.get("experience","N/A"))
                card_end()

                st.markdown("""<div style="font-size:15px;font-weight:700;color:#0f172a;
                    margin-bottom:12px;font-family:'Plus Jakarta Sans',sans-serif;">
                    📋 Detailed Results</div>""", unsafe_allow_html=True)

                for i, r in enumerate(results, 1):
                    score   = r.get("score",0)
                    verdict = r.get("verdict","")
                    name    = r.get("name","Unknown")
                    if "Strongly" in verdict: v_bg,v_col="#d1fae5","#059669"
                    elif "Recommended" in verdict: v_bg,v_col="#dbeafe","#2563eb"
                    elif "Maybe" in verdict: v_bg,v_col="#fef3c7","#d97706"
                    else: v_bg,v_col="#fee2e2","#dc2626"
                    s_col = "#059669" if score>=65 else "#d97706" if score>=40 else "#dc2626"

                    with st.expander(
                        f"{medals.get(i,f'#{i}')}  {name}  |  {score}%  |  {verdict}",
                        expanded=(i==1)
                    ):
                        st.markdown(f"""
                        <div style="display:flex;justify-content:space-between;
                            align-items:center;margin-bottom:8px;">
                            <div style="font-size:24px;font-weight:800;color:{s_col};">{score}/100</div>
                            <span class="verdict-pill" style="background:{v_bg};color:{v_col};">{verdict}</span>
                        </div>
                        <div class="score-bar-wrap">
                            <div style="height:100%;width:{score}%;
                                background:linear-gradient(90deg,{s_col},{s_col}bb);
                                border-radius:99px;transition:width .6s ease;"></div>
                        </div>
                        """, unsafe_allow_html=True)

                        st.divider()

                        c1, c2 = st.columns(2)
                        with c1:
                            st.markdown(f"""<div style="font-size:12.5px;color:#334155;line-height:1.9;">
                                📧 {r.get('email','N/A')}<br/>
                                📞 {r.get('phone','N/A')}<br/>
                                🎓 {r.get('education','N/A')}</div>""",
                                unsafe_allow_html=True)
                        with c2:
                            ln = r.get("linkedin",""); gh = r.get("github","")
                            st.markdown(f"""<div style="font-size:12.5px;color:#334155;line-height:1.9;">
                                💼 {r.get('experience','N/A')}<br/>
                                {'🔗 <a href="'+ln+'" target="_blank" style="color:#2563eb;">LinkedIn</a><br/>' if ln else ''}
                                {'💻 <a href="'+gh+'" target="_blank" style="color:#2563eb;">GitHub</a>' if gh else ''}
                                </div>""", unsafe_allow_html=True)

                        st.divider()

                        c1, c2 = st.columns(2)
                        with c1:
                            if r.get("matched_skills"):
                                st.markdown("""<div style="font-size:10px;font-weight:700;color:#64748b;
                                    text-transform:uppercase;letter-spacing:.7px;margin-bottom:7px;">
                                    ✅ Matched Skills</div>""", unsafe_allow_html=True)
                                st.markdown("".join(
                                    f'<span class="chip-green">✓ {s}</span>'
                                    for s in r["matched_skills"][:8]
                                ), unsafe_allow_html=True)
                        with c2:
                            if r.get("missing_skills"):
                                st.markdown("""<div style="font-size:10px;font-weight:700;color:#64748b;
                                    text-transform:uppercase;letter-spacing:.7px;margin-bottom:7px;">
                                    ❌ Missing Skills</div>""", unsafe_allow_html=True)
                                st.markdown("".join(
                                    f'<span class="chip-red">✗ {s}</span>'
                                    for s in r["missing_skills"][:6]
                                ), unsafe_allow_html=True)

                        st.divider()
                        st.markdown(f"""
                        <div style="background:#f8fafc;border-radius:10px;padding:13px 16px;
                            font-size:12.5px;line-height:1.8;color:#334155;border:1px solid #e2e8f0;">
                            <div style="margin-bottom:8px;">💪 <b>Strengths:</b> {r.get('strengths','')}</div>
                            <div>⚠️ <b>Weaknesses:</b> {r.get('weaknesses','')}</div>
                        </div>
                        <div style="font-size:10px;color:#94a3b8;margin-top:8px;text-align:right;">
                            Model: {r.get('model',model)}</div>
                        """, unsafe_allow_html=True)
            else:
                st.warning("No results returned.")
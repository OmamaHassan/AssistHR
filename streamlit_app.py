import os
import sys
import streamlit as st
from supabase import create_client

# ── PATH FIX ──────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(BASE_DIR, "backend")
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

# ── SECRETS ───────────────────────────────────────────────────
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

supabase = create_client(
    get_secret("SUPABASE_URL"),
    get_secret("SUPABASE_ANON_KEY")
)

st.set_page_config(
    page_title="AssistHR",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CLEAN & THEME-FRIENDLY CSS (Keeps your blue style) ────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet"/>
<style>
    html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    [data-testid="stAppViewContainer"] {
        background-color: var(--background-color) !important;
    }

    /* Sidebar - Your original blue/dark feel */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a, #1e2937) !important;
    }

    /* Better Chat Bubbles */
    [data-testid="stChatMessage"] {
        border-radius: 18px !important;
        padding: 14px 18px !important;
        margin-bottom: 16px !important;
    }

    /* User message - Your blue brand color */
    [data-testid="stChatMessage"] [data-testid="stChatMessageContent"] {
        background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
        color: white !important;
        border-radius: 18px !important;
        padding: 12px 16px !important;
        margin-left: auto !important;
        max-width: 80%;
    }

    /* Assistant message */
    [data-testid="stChatMessage"] [data-testid="stChatMessageContent"]:not(:has(~ *)) {
        background-color: var(--secondary-background-color) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 18px !important;
        padding: 12px 16px !important;
    }

    .stButton>button[kind="primary"] {
        background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
    }
    .stButton>button[kind="primary"]:hover {
        background: linear-gradient(135deg, #1d4ed8, #1e40af) !important;
    }
</style>
""", unsafe_allow_html=True)

# AUTH (kept almost same as your original)
def login_page():
    _, col, _ = st.columns([1, 1.4, 1])
    with col:
        st.markdown("""
        <div style="background:linear-gradient(135deg,#0f172a 0%,#1e3a5f 100%);
            border-radius:20px;padding:40px 32px;text-align:center;margin-bottom:24px;">
            <div style="font-size:52px;margin-bottom:12px;">🤖</div>
            <div style="font-size:28px;font-weight:800;color:#fff;">AssistHR</div>
            <div style="color:#60a5fa;font-weight:700;letter-spacing:2px;font-size:12px;">
                AI HR INTELLIGENCE
            </div>
        </div>
        """, unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])
        with tab1:
            email = st.text_input("Email", key="le", placeholder="you@company.com")
            password = st.text_input("Password", type="password", key="lp", placeholder="••••••••")
            if st.button("Login →", use_container_width=True, type="primary"):
                if not email or not password:
                    st.error("Please fill in all fields.")
                else:
                    try:
                        r = supabase.auth.sign_in_with_password({"email": email, "password": password})
                        st.session_state.user = r.user
                        st.session_state.token = r.session.access_token
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ {e}")

        with tab2:
            name = st.text_input("Full Name", key="rn", placeholder="John Smith")
            email = st.text_input("Email", key="re", placeholder="you@company.com")
            password = st.text_input("Password", type="password", key="rp", placeholder="Min 6 chars")
            confirm = st.text_input("Confirm Password", type="password", key="rc", placeholder="Repeat")
            if st.button("Create Account →", use_container_width=True, type="primary"):
                if not all([name, email, password, confirm]):
                    st.error("Please fill in all fields.")
                elif password != confirm:
                    st.error("Passwords do not match.")
                elif len(password) < 6:
                    st.error("Password must be at least 6 characters.")
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
    st.session_state.user = None
    st.session_state.token = None

if not st.session_state.user:
    login_page()
    st.stop()

current_email = st.session_state.user.email

# ── IMPROVED SIDEBAR ──────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="padding:20px 12px 12px;">
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:16px;">
            <div style="width:42px;height:42px;background:#2563eb;border-radius:12px;
                display:flex;align-items:center;justify-content:center;font-size:22px;color:white;">
                🤖
            </div>
            <div>
                <div style="color:white;font-size:19px;font-weight:800;">AssistHR</div>
                <div style="color:#94a3b8;font-size:11px;">AI HR Assistant</div>
            </div>
        </div>
        
        <div style="background:rgba(255,255,255,0.08);border-radius:10px;padding:10px 12px;margin-bottom:20px;">
            <div style="color:#e2e8f0;font-size:12px;font-weight:600;">Saylani Mass IT Training</div>
            <div style="color:#64748b;font-size:10.5px;">AI & Data Science · Batch 9</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        ["📊  Dashboard", "📚  Knowledge Base", "💬  HR Q&A", "📄  Resume Screener"],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown(f"""
    <div style="padding:0 12px 20px;">
        <div style="color:#94a3b8;font-size:12px;">👤 Logged in as</div>
        <div style="color:#e2e8f0;font-size:13.5px;font-weight:500;">{current_email}</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚪 Logout", use_container_width=True):
        logout()

# ── HR Q&A - REAL CHATBOT LOOK ────────────────────────────────
    elif page == "💬  HR Q&A":
        st.markdown("<h2 style='margin-bottom:8px;'>💬 HR Q&A</h2>", unsafe_allow_html=True)
        st.caption("Ask questions about HR policies • Answers powered by RAG + Groq")

        from rag_chain import ask
        from chat_store import create_session, load_history

        default_sess = st.session_state.get("active_session", "default")
        session_id = st.text_input("Session Name", value=default_sess, key="qa_sess_input")
        st.session_state.active_session = session_id
        full_session = f"{current_email}_{session_id}"

        model = st.selectbox("Model", [
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant"
        ], label_visibility="collapsed")

        # Initialize messages
        if "messages" not in st.session_state or st.session_state.get("last_session") != full_session:
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

        # Display chat with nice avatars
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                with st.chat_message("user", avatar="👤"):
                    st.write(msg["content"])
            else:
                with st.chat_message("assistant", avatar="🧠"):
                    st.write(msg["content"])

        # Chat input
        if prompt := st.chat_input("Ask about leave policy, working hours, benefits..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user", avatar="👤"):
                st.write(prompt)

            with st.chat_message("assistant", avatar="🧠"):
                with st.spinner("AssistHR is thinking..."):
                    try:
                        ans = ask(prompt, full_session, model)
                        st.write(ans)
                        st.session_state.messages.append({"role": "assistant", "content": ans})
                    except Exception as e:
                        st.error(f"❌ {e}")

    # Add your other pages (Dashboard, Knowledge Base, Resume Screener) below as they were in your original code.

    st.caption("AssistHR • Powered by Groq + Supabase")
import os
import html
import tempfile
from pathlib import Path

import streamlit as st
from supabase import create_client


# ======================================================
# ENV / Secrets (same backend behavior)
# ======================================================
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


# ======================================================
# UI System (light + dark adaptive)
# ======================================================
def inject_ui() -> None:
    st.markdown(
        """
        <style>
        /* ---- Base semantic tokens ---- */
        :root {
            --radius-lg: 18px;
            --radius-md: 12px;
            --shadow-lg: 0 18px 40px rgba(15, 23, 42, 0.14);
            --shadow-md: 0 8px 20px rgba(15, 23, 42, 0.10);
        }

        /* ---- Light theme ---- */
        [data-theme="light"] {
            --bg: #f6f8ff;
            --bg-grad-1: #eef2ff;
            --bg-grad-2: #ecfeff;
            --text: #0f172a;
            --muted: #475569;
            --card: #ffffff;
            --card-soft: #f8fafc;
            --border: #e2e8f0;
            --accent: #4f46e5;
            --accent-2: #06b6d4;
            --ok: #059669;
            --warn: #d97706;
        }

        /* ---- Dark theme ---- */
        [data-theme="dark"] {
            --bg: #0b1120;
            --bg-grad-1: #172554;
            --bg-grad-2: #083344;
            --text: #e2e8f0;
            --muted: #94a3b8;
            --card: #0f172a;
            --card-soft: #111827;
            --border: #243244;
            --accent: #818cf8;
            --accent-2: #22d3ee;
            --ok: #34d399;
            --warn: #fbbf24;
        }

        .stApp {
            background:
                radial-gradient(900px 420px at 8% -10%, color-mix(in srgb, var(--bg-grad-1) 70%, transparent), transparent 60%),
                radial-gradient(760px 380px at 95% -12%, color-mix(in srgb, var(--bg-grad-2) 65%, transparent), transparent 62%),
                var(--bg);
            color: var(--text);
        }

        .block-container {
            max-width: 1220px;
            padding-top: 1rem !important;
            padding-bottom: 1.4rem !important;
        }

        [data-testid="stSidebar"] {
            border-right: 1px solid var(--border);
            background: linear-gradient(180deg, color-mix(in srgb, var(--card) 92%, transparent), color-mix(in srgb, var(--card-soft) 88%, transparent));
        }

        .hero {
            border: 1px solid var(--border);
            background: linear-gradient(120deg, color-mix(in srgb, var(--accent) 14%, var(--card)), color-mix(in srgb, var(--accent-2) 12%, var(--card)));
            border-radius: var(--radius-lg);
            padding: 1rem 1.1rem;
            margin-bottom: 0.9rem;
            box-shadow: var(--shadow-md);
        }
        .hero h1 {
            margin: 0;
            color: var(--text);
            font-size: clamp(1.3rem, 2.6vw, 2rem);
            line-height: 1.2;
            letter-spacing: -0.01em;
        }
        .hero p {
            margin: .35rem 0 0 0;
            color: var(--muted);
            font-size: .94rem;
        }

        .card {
            border: 1px solid var(--border);
            background: color-mix(in srgb, var(--card) 96%, transparent);
            border-radius: var(--radius-lg);
            padding: .95rem 1rem;
            box-shadow: var(--shadow-md);
            margin-bottom: .85rem;
        }

        .auth-wrap {
            max-width: 560px;
            margin: 1.4rem auto 0 auto;
        }

        .brand-chip {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            border: 1px solid var(--border);
            border-radius: 999px;
            padding: .35rem .7rem;
            font-size: .82rem;
            color: var(--muted);
            background: color-mix(in srgb, var(--card-soft) 88%, transparent);
            margin-bottom: .65rem;
        }

        [data-testid="stMetric"] {
            border-radius: 14px !important;
            border: 1px solid var(--border) !important;
            background: linear-gradient(180deg, var(--card), var(--card-soft)) !important;
            box-shadow: var(--shadow-md) !important;
            padding: 15px !important;
        }
        [data-testid="stMetricLabel"] p {
            color: var(--muted) !important;
            font-size: .72rem !important;
            letter-spacing: .06em !important;
            text-transform: uppercase !important;
            font-weight: 700 !important;
        }
        [data-testid="stMetricValue"] {
            color: var(--text) !important;
            font-size: 1.45rem !important;
        }

        .stButton > button {
            border-radius: 12px !important;
            border: 1px solid color-mix(in srgb, var(--accent) 55%, var(--border)) !important;
            background: linear-gradient(90deg, var(--accent), color-mix(in srgb, var(--accent) 70%, #7dd3fc)) !important;
            color: white !important;
            font-weight: 600 !important;
            transition: .15s ease;
        }
        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 10px 22px color-mix(in srgb, var(--accent) 35%, transparent);
        }

        .stTextInput input, .stTextArea textarea {
            border-radius: 10px !important;
        }
        .stSelectbox [data-baseweb="select"] > div {
            border-radius: 10px !important;
        }

        .doc-item {
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: .62rem .78rem;
            margin-bottom: .45rem;
            background: color-mix(in srgb, var(--card-soft) 90%, transparent);
            color: var(--text);
        }

        .chat-shell {
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            background: color-mix(in srgb, var(--card) 95%, transparent);
            box-shadow: var(--shadow-md);
            padding: .75rem;
        }

        .chat-session-active {
            border-radius: 10px;
            border: 1px solid color-mix(in srgb, var(--accent) 45%, var(--border));
            background: color-mix(in srgb, var(--accent) 12%, var(--card));
            padding: .42rem .55rem;
            color: var(--text);
            margin-bottom: .4rem;
        }

        .chat-session {
            border-radius: 10px;
            border: 1px solid var(--border);
            background: color-mix(in srgb, var(--card-soft) 85%, transparent);
            padding: .42rem .55rem;
            color: var(--text);
            margin-bottom: .4rem;
        }

        @media (max-width: 900px) {
            .block-container { padding: .7rem .75rem 1rem .75rem !important; }
            [data-testid="stMetricValue"] { font-size: 1.15rem !important; }
            .auth-wrap { margin-top: .8rem; }
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
    st.markdown('<div class="card">', unsafe_allow_html=True)


def card_end() -> None:
    st.markdown("</div>", unsafe_allow_html=True)


def save_uploaded_file(uploaded_file, target_dir: Path) -> Path:
    target_dir.mkdir(parents=True, exist_ok=True)
    fp = target_dir / uploaded_file.name
    with open(fp, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return fp


# ======================================================
# Auth
# ======================================================
def login_page() -> None:
    st.markdown('<div class="auth-wrap">', unsafe_allow_html=True)

    st.markdown(
        '<div class="brand-chip">🤖 AssistHR • Product Suite</div>',
        unsafe_allow_html=True,
    )
    hero("Welcome to AssistHR", "Secure HR workspace for docs, copilots, and candidate screening")

    card_start()
    tab1, tab2 = st.tabs(["Sign In", "Create Account"])

    with tab1:
        st.subheader("Sign in")
        email = st.text_input("Work Email", key="login_email", placeholder="you@company.com")
        password = st.text_input("Password", key="login_pass", type="password", placeholder="••••••••")
        if st.button("Sign In", use_container_width=True):
            if not email or not password:
                st.error("Please fill in all fields.")
            else:
                try:
                    response = supabase.auth.sign_in_with_password({"email": email, "password": password})
                    st.session_state.user = response.user
                    st.session_state.token = response.session.access_token
                    st.toast("Signed in successfully")
                    st.rerun()
                except Exception as e:
                    st.error(f"Sign in failed: {e}")

    with tab2:
        st.subheader("Create your account")
        name = st.text_input("Full Name", key="reg_name", placeholder="John Smith")
        email = st.text_input("Work Email", key="reg_email", placeholder="you@company.com")
        password = st.text_input("Password", key="reg_pass", type="password", placeholder="Minimum 6 characters")
        confirm = st.text_input("Confirm Password", key="reg_confirm", type="password", placeholder="Repeat password")

        if st.button("Create Account", use_container_width=True):
            if not name or not email or not password or not confirm:
                st.error("Please fill in all fields.")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters.")
            elif password != confirm:
                st.error("Passwords do not match.")
            else:
                try:
                    supabase.auth.sign_up(
                        {
                            "email": email,
                            "password": password,
                            "options": {"data": {"name": name}},
                        }
                    )
                    st.success("Account created. Please sign in.")
                except Exception as e:
                    st.error(f"Registration failed: {e}")

    card_end()
    st.markdown("</div>", unsafe_allow_html=True)


def logout() -> None:
    try:
        supabase.auth.sign_out()
    except Exception:
        pass
    st.session_state.user = None
    st.session_state.token = None
    st.rerun()


# ======================================================
# App bootstrap
# ======================================================
inject_ui()

if "user" not in st.session_state:
    st.session_state.user = None
    st.session_state.token = None

if not st.session_state.user:
    login_page()
    st.stop()

current_user = st.session_state.user
current_email = current_user.email if current_user else "unknown@user"


# ======================================================
# Sidebar
# ======================================================
st.sidebar.title("🤖 AssistHR")
st.sidebar.caption("HR Intelligence Platform")
st.sidebar.divider()

page = st.sidebar.radio("Navigation", ["📊 Dashboard", "📄 Documents", "💬 Chat", "👥 Screening"])

st.sidebar.divider()
st.sidebar.write(f"👤 {current_email}")

if st.sidebar.button("Logout", use_container_width=True):
    logout()

st.sidebar.divider()
st.sidebar.caption("v3.0 • Product UI")


# ======================================================
# Dashboard
# ======================================================
if page == "📊 Dashboard":
    hero("Dashboard", "A single place to monitor your HR knowledge workspace")

    from embedding import get_existing_files

    try:
        docs = get_existing_files()
    except Exception:
        docs = []

    temp_resumes = Path(tempfile.gettempdir()) / "resumes"
    try:
        resume_count = (
            len([f for f in os.listdir(temp_resumes) if f.lower().endswith((".pdf", ".docx", ".jpg", ".jpeg", ".png"))])
            if temp_resumes.exists()
            else 0
        )
    except Exception:
        resume_count = 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Documents", len(docs))
    c2.metric("Resumes Cached", resume_count)
    c3.metric("AI Provider", "Groq")
    c4.metric("Vector DB", "Supabase")

    st.divider()
    s1, s2, s3 = st.columns(3)
    s1.success("System Online")
    s2.info("Embeddings Synced")
    s3.warning("Screening Queue Idle")

    st.divider()
    st.subheader("Uploaded Documents")
    if not docs:
        st.info("No documents uploaded yet. Go to Documents page to upload.")
    else:
        for d in docs:
            st.markdown(f'<div class="doc-item">📄 {html.escape(str(d))}</div>', unsafe_allow_html=True)


# ======================================================
# Documents
# ======================================================
elif page == "📄 Documents":
    hero("Documents", "Upload and process policy files for better assistant responses")

    from document_loader import load_document
    from chunking import chunk_documents
    from embedding import create_vector_store, get_existing_files

    card_start()
    st.subheader("Upload Document")
    st.caption("Accepted formats: PDF, DOCX, TXT")
    uploaded = st.file_uploader("Choose file", type=["pdf", "docx", "txt"])

    if uploaded and st.button("Upload & Process", use_container_width=True):
        with st.spinner(f"Processing '{uploaded.name}'..."):
            temp_dir = Path(tempfile.gettempdir()) / "assisthr_docs"
            fp = save_uploaded_file(uploaded, temp_dir)
            try:
                loaded_docs = load_document(str(fp))
                chunks = chunk_documents(loaded_docs)
                create_vector_store(chunks)
                st.success(f"Uploaded '{uploaded.name}' ({len(chunks)} chunks)")
                st.toast("Document processed successfully")
            except Exception as e:
                st.error(f"Error: {e}")
            finally:
                fp.unlink(missing_ok=True)

    card_end()

    st.subheader("Uploaded Documents")
    try:
        existing = get_existing_files()
        if not existing:
            st.info("No documents uploaded yet.")
        else:
            for doc in existing:
                st.markdown(f'<div class="doc-item">📄 {html.escape(str(doc))}</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Could not load documents: {e}")


# ======================================================
# Chat (real bot side sessions)
# ======================================================
elif page == "💬 Chat":
    hero("AssistHR Copilot", "Chat with your HR knowledge base like a production bot")

    from rag_chain import ask
    from chat_store import create_session, load_history

    if "chat_sessions" not in st.session_state:
        st.session_state.chat_sessions = ["default"]
    if "active_chat_session" not in st.session_state:
        st.session_state.active_chat_session = "default"
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "last_loaded_session" not in st.session_state:
        st.session_state.last_loaded_session = None

    left, right = st.columns([1.05, 2.95])

    with left:
        st.markdown('<div class="chat-shell">', unsafe_allow_html=True)
        st.subheader("Sessions")
        new_name = st.text_input("New session name", placeholder="e.g. leave-policy")
        if st.button("＋ New Chat", use_container_width=True):
            name = (new_name or "").strip()
            if not name:
                name = f"chat-{len(st.session_state.chat_sessions)+1}"
            if name not in st.session_state.chat_sessions:
                st.session_state.chat_sessions.append(name)
            st.session_state.active_chat_session = name
            st.session_state.last_loaded_session = None
            st.rerun()

        st.caption("Your conversations")
        for s in st.session_state.chat_sessions:
            is_active = s == st.session_state.active_chat_session
            css = "chat-session-active" if is_active else "chat-session"
            st.markdown(f'<div class="{css}">{"●" if is_active else "○"} {html.escape(s)}</div>', unsafe_allow_html=True)
            if st.button(f"Open {s}", key=f"open_{s}", use_container_width=True):
                st.session_state.active_chat_session = s
                st.session_state.last_loaded_session = None
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        card_start()
        c1, c2 = st.columns([2, 1])
        with c1:
            st.markdown(f"**Active Session:** `{st.session_state.active_chat_session}`")
        with c2:
            model = st.selectbox(
                "Model",
                [
                    "llama-3.1-8b-instant",
                    "llama-3.3-70b-versatile",
                    "meta-llama/llama-4-scout-17b-16e-instruct",
                ],
            )
        card_end()

        full_session = f"{current_email}_{st.session_state.active_chat_session}"

        if st.session_state.last_loaded_session != full_session:
            try:
                create_session(full_session)
                history = load_history(full_session)
                st.session_state.messages = [
                    {"role": "user" if msg.type == "human" else "assistant", "content": msg.content}
                    for msg in history
                ]
            except Exception:
                st.session_state.messages = []
            st.session_state.last_loaded_session = full_session

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        prompt = st.chat_input("Ask about policies, leave, dress code, hiring SOPs...")
        if prompt:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)

            with st.chat_message("assistant"):
                with st.spinner("AssistHR is thinking..."):
                    try:
                        answer = ask(prompt, full_session, model)
                        st.write(answer)
                        st.session_state.messages.append({"role": "assistant", "content": answer})
                    except Exception as e:
                        st.error(f"Error: {e}")


# ======================================================
# Screening
# ======================================================
elif page == "👥 Screening":
    hero("Resume Screening", "Evaluate candidates against role requirements faster")

    from screener import screen_all

    card_start()
    model = st.selectbox(
        "Select Model",
        [
            "llama-3.1-8b-instant",
            "llama-3.3-70b-versatile",
            "meta-llama/llama-4-scout-17b-16e-instruct",
        ],
    )
    st.caption("Upload one Job Description + multiple resumes")
    card_end()

    col1, col2 = st.columns(2)

    with col1:
        card_start()
        st.subheader("Job Description")
        jd = st.file_uploader("Upload JD (PDF/DOCX)", type=["pdf", "docx"], key="jd")
        card_end()

    with col2:
        card_start()
        st.subheader("Resumes")
        resumes = st.file_uploader(
            "Upload resumes",
            type=["pdf", "docx", "jpg", "jpeg", "png"],
            accept_multiple_files=True,
            key="resumes",
        )
        card_end()

    if st.button("Start Screening", type="primary", use_container_width=True):
        if not jd:
            st.error("Please upload a Job Description.")
        elif not resumes:
            st.error("Please upload at least one resume.")
        else:
            tmp = Path(tempfile.gettempdir()) / "assisthr_screening"
            tmp.mkdir(parents=True, exist_ok=True)

            jd_path = save_uploaded_file(jd, tmp)
            resume_paths = [save_uploaded_file(r, tmp) for r in resumes]

            with st.spinner("Screening candidates..."):
                try:
                    results = screen_all([str(p) for p in resume_paths], str(jd_path), model)
                except Exception as e:
                    st.error(f"Screening failed: {e}")
                    results = []

            jd_path.unlink(missing_ok=True)
            for p in resume_paths:
                p.unlink(missing_ok=True)

            if results:
                st.success(f"Screened {len(results)} candidate(s)")
                for i, r in enumerate(results, 1):
                    with st.expander(f"#{i} {r.get('name', 'Unknown')} | {r.get('score', 0)}% | {r.get('verdict', 'N/A')}"):
                        m1, m2 = st.columns(2)
                        m1.metric("Score", f"{r.get('score', 0)}%")
                        m2.metric("Experience", r.get("experience", "Not specified"))
                        st.progress(max(0, min(int(r.get("score", 0)), 100)) / 100.0)

                        st.divider()
                        a, b = st.columns(2)
                        a.write(f"📧 {r.get('email', 'N/A')}")
                        a.write(f"📞 {r.get('phone', 'N/A')}")
                        b.write(f"🎓 {r.get('education', 'N/A')}")
                        if r.get("linkedin"):
                            b.write(f"🔗 [LinkedIn]({r.get('linkedin')})")
                        if r.get("github"):
                            b.write(f"💻 [GitHub]({r.get('github')})")

                        st.divider()
                        c, d = st.columns(2)
                        c.write("✅ **Matched Skills**")
                        c.write(" • ".join(r.get("matched_skills", [])) or "N/A")
                        d.write("❌ **Missing Skills**")
                        d.write(" • ".join(r.get("missing_skills", [])) or "N/A")

                        st.divider()
                        st.write(f"💪 **Strengths:** {r.get('strengths', '')}")
                        st.write(f"⚠️ **Weaknesses:** {r.get('weaknesses', '')}")
                        st.caption(f"Model used: {r.get('model', model)}")
            else:
                st.warning("No results returned.")
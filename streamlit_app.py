import os
import html
import tempfile
from pathlib import Path

import streamlit as st
from supabase import create_client


# ======================================================
# Secrets / env
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

supabase = create_client(get_secret("SUPABASE_URL"), get_secret("SUPABASE_ANON_KEY"))


# ======================================================
# UI styling
# ======================================================
def inject_ui() -> None:
    st.markdown(
        """
        <style>
        :root {
            --radius-lg: 16px;
            --radius-md: 12px;
        }

        /* Light */
        [data-theme="light"] {
            --bg: #f5f7ff;
            --text: #0f172a;
            --muted: #475569;
            --card: #ffffff;
            --card-soft: #f8fafc;
            --border: #e2e8f0;
            --accent: #4f46e5;
            --accent2: #0891b2;

            --sidebar-bg: #0f172a;
            --sidebar-bg-2: #1e293b;
            --sidebar-text: #e2e8f0;
            --sidebar-muted: #94a3b8;
            --sidebar-border: #334155;
        }

        /* Dark */
        [data-theme="dark"] {
            --bg: #0b1120;
            --text: #e2e8f0;
            --muted: #94a3b8;
            --card: #0f172a;
            --card-soft: #111827;
            --border: #243244;
            --accent: #818cf8;
            --accent2: #22d3ee;

            --sidebar-bg: #020617;
            --sidebar-bg-2: #0f172a;
            --sidebar-text: #e2e8f0;
            --sidebar-muted: #94a3b8;
            --sidebar-border: #1f2937;
        }

        .stApp {
            background:
                radial-gradient(900px 420px at 8% -10%, color-mix(in srgb, var(--accent) 12%, transparent), transparent 60%),
                radial-gradient(760px 380px at 95% -12%, color-mix(in srgb, var(--accent2) 12%, transparent), transparent 62%),
                var(--bg);
            color: var(--text);
        }

        .block-container {
            max-width: 1260px;
            padding-top: 1rem !important;
            padding-bottom: 1.4rem !important;
        }

        /* Sidebar differentiation */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, var(--sidebar-bg), var(--sidebar-bg-2));
            border-right: 1px solid var(--sidebar-border);
        }
        [data-testid="stSidebar"] * {
            color: var(--sidebar-text);
        }
        [data-testid="stSidebar"] .stCaption {
            color: var(--sidebar-muted) !important;
        }

        .hero {
            border: 1px solid var(--border);
            background: linear-gradient(
                115deg,
                color-mix(in srgb, var(--accent) 12%, var(--card)),
                color-mix(in srgb, var(--accent2) 10%, var(--card))
            );
            border-radius: var(--radius-lg);
            padding: 1rem 1.1rem;
            margin-bottom: .9rem;
            box-shadow: 0 10px 26px rgba(15, 23, 42, 0.12);
        }
        .hero h1 {
            margin: 0;
            font-size: clamp(1.25rem, 2.6vw, 2rem);
            line-height: 1.2;
            color: var(--text);
        }
        .hero p {
            margin: .35rem 0 0 0;
            color: var(--muted);
            font-size: .94rem;
        }

        .card {
            border: 1px solid var(--border);
            background: var(--card);
            border-radius: var(--radius-lg);
            padding: .95rem 1rem;
            margin-bottom: .85rem;
            box-shadow: 0 8px 20px rgba(15, 23, 42, 0.08);
        }

        .auth-wrap {
            max-width: 580px;
            margin: 1.4rem auto 0 auto;
        }

        .brand-chip {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            border: 1px solid var(--border);
            border-radius: 999px;
            padding: .36rem .72rem;
            font-size: .82rem;
            color: var(--muted);
            background: var(--card-soft);
            margin-bottom: .65rem;
        }

        [data-testid="stMetric"] {
            border-radius: 14px !important;
            border: 1px solid var(--border) !important;
            background: linear-gradient(180deg, var(--card), var(--card-soft)) !important;
            box-shadow: 0 8px 20px rgba(15, 23, 42, 0.08) !important;
            padding: 15px !important;
        }
        [data-testid="stMetricLabel"] p {
            color: var(--muted) !important;
            text-transform: uppercase !important;
            letter-spacing: .06em !important;
            font-size: .72rem !important;
            font-weight: 700 !important;
        }
        [data-testid="stMetricValue"] {
            color: var(--text) !important;
            font-size: 1.45rem !important;
        }

        .stTextInput input, .stSelectbox [data-baseweb="select"] > div {
            border-radius: 10px !important;
        }

        .stButton > button {
            border-radius: 12px !important;
            border: 1px solid color-mix(in srgb, var(--accent) 50%, var(--border)) !important;
            background: linear-gradient(90deg, var(--accent), color-mix(in srgb, var(--accent) 70%, #7dd3fc)) !important;
            color: white !important;
            font-weight: 600 !important;
        }

        .doc-item {
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: .62rem .78rem;
            margin-bottom: .45rem;
            background: var(--card-soft);
            color: var(--text);
        }

        .chat-shell {
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            background: var(--card);
            padding: .75rem;
            box-shadow: 0 8px 20px rgba(15, 23, 42, 0.08);
        }

        @media (max-width: 900px) {
            .block-container { padding: .7rem .75rem 1rem .75rem !important; }
            [data-testid="stMetricValue"] { font-size: 1.2rem !important; }
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
    st.markdown('<div class="brand-chip">🤖 AssistHR • HR Intelligence Platform</div>', unsafe_allow_html=True)
    hero("Welcome back", "Sign in to access dashboard, documents, chat, and screening")

    card_start()
    t1, t2 = st.tabs(["Sign In", "Create Account"])

    with t1:
        st.subheader("Sign In")
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

    with t2:
        st.subheader("Create Account")
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
                        {"email": email, "password": password, "options": {"data": {"name": name}}}
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

if "page" not in st.session_state:
    st.session_state.page = "📊 Dashboard"


# ======================================================
# Sidebar nav (no radio buttons)
# ======================================================
st.sidebar.title("🤖 AssistHR")
st.sidebar.caption("HR Intelligence Platform")
st.sidebar.divider()

if st.sidebar.button(
    "📊 Dashboard",
    use_container_width=True,
    type="primary" if st.session_state.page == "📊 Dashboard" else "secondary",
):
    st.session_state.page = "📊 Dashboard"
    st.rerun()

if st.sidebar.button(
    "📄 Documents",
    use_container_width=True,
    type="primary" if st.session_state.page == "📄 Documents" else "secondary",
):
    st.session_state.page = "📄 Documents"
    st.rerun()

if st.sidebar.button(
    "💬 Chat",
    use_container_width=True,
    type="primary" if st.session_state.page == "💬 Chat" else "secondary",
):
    st.session_state.page = "💬 Chat"
    st.rerun()

if st.sidebar.button(
    "👥 Screening",
    use_container_width=True,
    type="primary" if st.session_state.page == "👥 Screening" else "secondary",
):
    st.session_state.page = "👥 Screening"
    st.rerun()

st.sidebar.divider()
st.sidebar.write(f"👤 {current_email}")

if st.sidebar.button("Logout", use_container_width=True):
    logout()

st.sidebar.divider()
st.sidebar.caption("v4.0")


page = st.session_state.page


# ======================================================
# Dashboard
# ======================================================
if page == "📊 Dashboard":
    hero("Dashboard", "Track your HR knowledge and AI stack health")

    from embedding import get_existing_files

    try:
        all_docs = get_existing_files()
        docs_count = len(all_docs)
    except Exception:
        all_docs = []
        docs_count = 0

    # Keep metric info as before
    c1, c2, c3 = st.columns(3)
    c1.metric("📄 Documents", docs_count)
    c2.metric("🤖 AI Model", "Groq")
    c3.metric("🗄️ Vector DB", "Supabase")

    st.divider()
    st.subheader("📁 Uploaded Documents")

    if not all_docs:
        st.info("No documents uploaded yet. Go to Documents page to upload.")
    else:
        for d in all_docs:
            st.markdown(f'<div class="doc-item">📄 {html.escape(str(d))}</div>', unsafe_allow_html=True)


# ======================================================
# Documents
# ======================================================
elif page == "📄 Documents":
    hero("Documents", "Upload and process HR policy files")

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
                docs = load_document(str(fp))
                chunks = chunk_documents(docs)
                create_vector_store(chunks)
                st.success(f"Uploaded '{uploaded.name}' ({len(chunks)} chunks)")
                st.toast("Document processed")
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
# Chat (improved side-session bot layout)
# ======================================================
elif page == "💬 Chat":
    hero("AssistHR Copilot", "Persistent chat sessions like a real assistant app")

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
        new_name = st.text_input("New session", placeholder="e.g. leave-policy")

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("＋ New", use_container_width=True):
                name = (new_name or "").strip()
                if not name:
                    name = f"chat-{len(st.session_state.chat_sessions) + 1}"
                if name not in st.session_state.chat_sessions:
                    st.session_state.chat_sessions.append(name)
                st.session_state.active_chat_session = name
                st.session_state.last_loaded_session = None
                st.rerun()
        with col_b:
            if st.button("Clear View", use_container_width=True):
                st.session_state.messages = []
                st.rerun()

        st.caption("Open a chat")
        for s in st.session_state.chat_sessions:
            is_active = s == st.session_state.active_chat_session
            if st.button(
                f"{'●' if is_active else '○'} {s}",
                key=f"session_{s}",
                use_container_width=True,
                type="primary" if is_active else "secondary",
            ):
                st.session_state.active_chat_session = s
                st.session_state.last_loaded_session = None
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        card_start()
        top1, top2 = st.columns([2, 1])
        with top1:
            st.markdown(f"**Active Session:** `{st.session_state.active_chat_session}`")
        with top2:
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
                    {
                        "role": "user" if msg.type == "human" else "assistant",
                        "content": msg.content,
                    }
                    for msg in history
                ]
            except Exception:
                st.session_state.messages = []
            st.session_state.last_loaded_session = full_session

        # Chat thread
        thread = st.container(border=True)
        with thread:
            if not st.session_state.messages:
                st.info("Start the conversation. Ask any HR policy or process question.")
            for msg in st.session_state.messages:
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])

        prompt = st.chat_input("Ask about HR policies, leave, dress code, recruitment SOP...")
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
    hero("Resume Screening", "Evaluate candidate fit against the job description")

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
    st.caption("Upload one JD and multiple resumes")
    card_end()

    col1, col2 = st.columns(2)
    with col1:
        card_start()
        st.subheader("📋 Job Description")
        jd = st.file_uploader("Upload JD (PDF/DOCX)", type=["pdf", "docx"], key="jd")
        card_end()

    with col2:
        card_start()
        st.subheader("📄 Resumes")
        resumes = st.file_uploader(
            "Upload resumes",
            type=["pdf", "docx", "jpg", "jpeg", "png"],
            accept_multiple_files=True,
            key="resumes",
        )
        card_end()

    if st.button("Start Screening", use_container_width=True, type="primary"):
        if not jd:
            st.error("Please upload a Job Description.")
        elif not resumes:
            st.error("Please upload at least one resume.")
        else:
            temp_dir = Path(tempfile.gettempdir()) / "assisthr_screening"
            temp_dir.mkdir(parents=True, exist_ok=True)

            jd_path = save_uploaded_file(jd, temp_dir)
            resume_paths = [save_uploaded_file(r, temp_dir) for r in resumes]

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
                        s1, s2 = st.columns(2)
                        s1.write("✅ **Matched Skills**")
                        s1.write(" • ".join(r.get("matched_skills", [])) or "N/A")
                        s2.write("❌ **Missing Skills**")
                        s2.write(" • ".join(r.get("missing_skills", [])) or "N/A")

                        st.divider()
                        st.write(f"💪 **Strengths:** {r.get('strengths', '')}")
                        st.write(f"⚠️ **Weaknesses:** {r.get('weaknesses', '')}")
                        st.caption(f"Model used: {r.get('model', model)}")
            else:
                st.warning("No results returned.")
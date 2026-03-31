import os
import html
import tempfile
from pathlib import Path

import streamlit as st
from supabase import create_client


# ======================================================
# Secrets / env (unchanged backend behavior)
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
# UI Styling
# ======================================================
def inject_ui() -> None:
    st.markdown(
        """
        <style>
        :root {
            --bg: #0a0f1f;
            --bg-soft: #111a33;
            --card: #111a30;
            --card-2: #192745;
            --text: #eaf0ff;
            --muted: #aeb9d9;
            --accent: #7b9cff;
            --accent-2: #4ce3c2;
            --border: rgba(255,255,255,0.13);
            --shadow: 0 14px 34px rgba(0,0,0,0.28);
        }

        .stApp {
            background:
                radial-gradient(1200px 600px at 10% -10%, #1b2d66 0%, transparent 55%),
                radial-gradient(900px 500px at 100% -10%, #11415a 0%, transparent 50%),
                linear-gradient(180deg, var(--bg-soft), var(--bg));
        }

        .block-container {
            max-width: 1280px;
            padding-top: 1rem !important;
            padding-bottom: 1.6rem !important;
        }

        [data-testid="stSidebar"] {
            border-right: 1px solid var(--border);
            background: linear-gradient(180deg, rgba(16,24,46,.96), rgba(10,16,32,.98));
        }

        .hero {
            border: 1px solid var(--border);
            background: linear-gradient(120deg, rgba(123,156,255,.20), rgba(76,227,194,.12));
            border-radius: 18px;
            padding: 1.05rem 1.2rem;
            margin-bottom: .9rem;
            box-shadow: var(--shadow);
        }
        .hero h1 {
            margin: 0;
            color: var(--text);
            font-size: clamp(1.25rem, 2.6vw, 2rem);
            line-height: 1.2;
        }
        .hero p {
            margin: .35rem 0 0 0;
            color: var(--muted);
        }

        .glass-card {
            border: 1px solid var(--border);
            background: linear-gradient(180deg, rgba(255,255,255,.05), rgba(255,255,255,.02));
            border-radius: 16px;
            padding: .9rem 1rem;
            box-shadow: var(--shadow);
            margin-bottom: .85rem;
        }

        [data-testid="stMetric"] {
            border-radius: 14px !important;
            border: 1px solid var(--border) !important;
            background: linear-gradient(180deg, var(--card), var(--card-2)) !important;
            padding: 16px !important;
            box-shadow: var(--shadow) !important;
        }
        [data-testid="stMetricLabel"] p {
            color: var(--muted) !important;
            text-transform: uppercase !important;
            letter-spacing: .07em !important;
            font-size: .72rem !important;
            font-weight: 700 !important;
        }
        [data-testid="stMetricValue"] {
            color: var(--text) !important;
            font-size: 1.45rem !important;
        }

        .stButton > button {
            border-radius: 12px !important;
            border: 1px solid rgba(123,156,255,.55) !important;
            background: linear-gradient(90deg, #5f80ff, #7594ff) !important;
            color: #fff !important;
            font-weight: 600 !important;
        }

        .stTextInput input, .stSelectbox [data-baseweb="select"] > div {
            border-radius: 12px !important;
        }

        .doc-item {
            border: 1px solid var(--border);
            border-radius: 12px;
            background: rgba(255,255,255,.03);
            color: var(--text);
            padding: .68rem .82rem;
            margin-bottom: .48rem;
        }

        .chat-shell {
            border: 1px solid var(--border);
            border-radius: 16px;
            background: linear-gradient(180deg, rgba(17,26,48,.78), rgba(10,15,31,.85));
            box-shadow: var(--shadow);
            padding: .7rem;
        }

        .session-chip {
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: .42rem .55rem;
            margin-bottom: .4rem;
            background: rgba(255,255,255,.03);
            color: var(--text);
            font-size: .85rem;
        }

        @media (max-width: 900px) {
            .block-container { padding: .7rem .75rem 1rem .75rem !important; }
            [data-testid="stMetricValue"] { font-size: 1.18rem !important; }
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


# ======================================================
# Auth
# ======================================================
def login_page() -> None:
    hero("🤖 AssistHR", "AI-powered HR command center for modern teams")

    card_start()
    tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])

    with tab1:
        st.subheader("Welcome back")
        email = st.text_input("Email", key="login_email", placeholder="you@company.com")
        password = st.text_input("Password", type="password", key="login_pass", placeholder="••••••••")

        if st.button("Login", use_container_width=True):
            if not email or not password:
                st.error("Please fill in all fields.")
            else:
                try:
                    response = supabase.auth.sign_in_with_password({"email": email, "password": password})
                    st.session_state.user = response.user
                    st.session_state.token = response.session.access_token
                    st.toast("Logged in")
                    st.rerun()
                except Exception as e:
                    st.error(f"Login failed: {e}")

    with tab2:
        st.subheader("Create account")
        name = st.text_input("Full Name", key="reg_name", placeholder="John Smith")
        email = st.text_input("Email", key="reg_email", placeholder="you@company.com")
        password = st.text_input("Password", type="password", key="reg_pass", placeholder="Min 6 characters")
        confirm = st.text_input("Confirm Password", type="password", key="reg_confirm", placeholder="Repeat password")

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
                    st.success("Account created. Please login.")
                except Exception as e:
                    st.error(f"Registration failed: {e}")
    card_end()


def logout() -> None:
    try:
        supabase.auth.sign_out()
    except Exception:
        pass
    st.session_state.user = None
    st.session_state.token = None
    st.rerun()


def save_uploaded_file(uploaded_file, target_dir: Path) -> Path:
    target_dir.mkdir(parents=True, exist_ok=True)
    out_path = target_dir / uploaded_file.name
    with open(out_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return out_path


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
# Sidebar nav
# ======================================================
st.sidebar.title("🤖 AssistHR")
st.sidebar.caption("Product Suite")
st.sidebar.divider()

page = st.sidebar.radio(
    "Navigation",
    ["📊 Dashboard", "📄 Documents", "💬 Chat", "👥 Screening"],
)

st.sidebar.divider()
st.sidebar.write(f"👤 {current_email}")

if st.sidebar.button("Logout", use_container_width=True):
    logout()

st.sidebar.divider()
st.sidebar.caption("AssistHR • Product UI")


# ======================================================
# Dashboard
# ======================================================
if page == "📊 Dashboard":
    hero("📊 Dashboard", "Unified view of HR intelligence and system readiness")

    from embedding import get_existing_files

    try:
        all_docs = get_existing_files()
        docs_count = len(all_docs)
    except Exception:
        all_docs = []
        docs_count = 0

    temp_resumes = Path(tempfile.gettempdir()) / "resumes"
    try:
        resume_count = (
            len([f for f in os.listdir(temp_resumes) if f.lower().endswith((".pdf", ".docx", ".jpg", ".jpeg", ".png"))])
            if temp_resumes.exists()
            else 0
        )
    except Exception:
        resume_count = 0

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("📄 Documents", docs_count)
    m2.metric("👥 Cached Resumes", resume_count)
    m3.metric("🤖 LLM Provider", "Groq")
    m4.metric("🗄️ Vector DB", "Supabase")

    st.divider()
    a, b, c = st.columns(3)
    a.success("System: Online")
    b.info("Embeddings: Synced")
    c.warning("Screening Queue: Idle")

    st.divider()
    st.subheader("📁 Uploaded Documents")
    if not all_docs:
        st.info("No documents uploaded yet. Go to Documents page to upload.")
    else:
        for doc in all_docs:
            st.markdown(f'<div class="doc-item">📄 {html.escape(str(doc))}</div>', unsafe_allow_html=True)


# ======================================================
# Documents
# ======================================================
elif page == "📄 Documents":
    hero("📄 Documents", "Upload policy files and build your HR knowledge base")

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
# Chat (product-style with side sessions)
# ======================================================
elif page == "💬 Chat":
    hero("💬 AssistHR Copilot", "Conversational HR assistant with persistent sessions")

    from rag_chain import ask
    from chat_store import create_session, load_history

    # Session manager state
    if "chat_sessions" not in st.session_state:
        st.session_state.chat_sessions = ["default"]
    if "active_chat_session" not in st.session_state:
        st.session_state.active_chat_session = "default"
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "last_loaded_session" not in st.session_state:
        st.session_state.last_loaded_session = None

    left, right = st.columns([1, 3])

    # -------- Left: Session list (real bot style) --------
    with left:
        st.markdown('<div class="chat-shell">', unsafe_allow_html=True)
        st.subheader("🧠 Sessions")

        new_session_name = st.text_input("New Session", placeholder="e.g. leave-policy")
        if st.button("＋ New Chat", use_container_width=True):
            clean = (new_session_name or "").strip()
            if not clean:
                clean = f"chat-{len(st.session_state.chat_sessions) + 1}"
            if clean not in st.session_state.chat_sessions:
                st.session_state.chat_sessions.append(clean)
            st.session_state.active_chat_session = clean
            st.session_state.last_loaded_session = None
            st.rerun()

        st.caption("Select a chat")
        for s in st.session_state.chat_sessions:
            active = s == st.session_state.active_chat_session
            label = f"● {s}" if active else f"○ {s}"
            if st.button(label, key=f"session_btn_{s}", use_container_width=True):
                st.session_state.active_chat_session = s
                st.session_state.last_loaded_session = None
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # -------- Right: Chat thread --------
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

        # Load only when session changes
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

        # Render conversation
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        prompt = st.chat_input("Ask about leave, policies, hiring SOPs, dress code...")
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
    hero("👥 Resume Screening", "Smart candidate evaluation against your job description")

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
    st.caption("Upload one JD and multiple resumes for ranking.")
    card_end()

    c1, c2 = st.columns(2)
    with c1:
        card_start()
        st.subheader("📋 Job Description")
        jd = st.file_uploader("Upload JD (PDF or DOCX)", type=["pdf", "docx"], key="jd")
        card_end()

    with c2:
        card_start()
        st.subheader("📄 Resumes")
        resumes = st.file_uploader(
            "Upload Resumes (multiple allowed)",
            type=["pdf", "docx", "jpg", "jpeg", "png"],
            accept_multiple_files=True,
            key="resumes",
        )
        card_end()

    if st.button("🔍 Start Screening", type="primary", use_container_width=True):
        if not jd:
            st.error("Please upload a Job Description.")
        elif not resumes:
            st.error("Please upload at least one resume.")
        else:
            temp_dir = Path(tempfile.gettempdir()) / "assisthr_screening"
            temp_dir.mkdir(parents=True, exist_ok=True)

            jd_path = save_uploaded_file(jd, temp_dir)
            resume_paths = [save_uploaded_file(r, temp_dir) for r in resumes]

            with st.spinner("Screening candidates... this may take a moment."):
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
                    verdict = r.get("verdict", "N/A")
                    score = r.get("score", 0)
                    name = r.get("name", "Unknown")

                    with st.expander(f"#{i}  {name}  |  {score}%  |  {verdict}"):
                        m1, m2 = st.columns(2)
                        m1.metric("Score", f"{score}%")
                        m2.metric("Experience", r.get("experience", "Not specified"))
                        st.progress(max(0, min(int(score), 100)) / 100)

                        st.divider()
                        d1, d2 = st.columns(2)
                        d1.write(f"📧 {r.get('email', 'N/A')}")
                        d1.write(f"📞 {r.get('phone', 'N/A')}")
                        d2.write(f"🎓 {r.get('education', 'N/A')}")
                        if r.get("linkedin"):
                            d2.write(f"🔗 [LinkedIn]({r.get('linkedin')})")
                        if r.get("github"):
                            d2.write(f"💻 [GitHub]({r.get('github')})")

                        st.divider()
                        s1, s2 = st.columns(2)
                        with s1:
                            st.write("✅ **Matched Skills**")
                            matched = r.get("matched_skills", [])
                            st.write(" • ".join(matched) if matched else "N/A")
                        with s2:
                            st.write("❌ **Missing Skills**")
                            missing = r.get("missing_skills", [])
                            st.write(" • ".join(missing) if missing else "N/A")

                        st.divider()
                        st.write(f"💪 **Strengths:** {r.get('strengths', '')}")
                        st.write(f"⚠️ **Weaknesses:** {r.get('weaknesses', '')}")
                        st.caption(f"Model used: {r.get('model', model)}")
            else:
                st.warning("No results returned.")
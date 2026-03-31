import os
import html
import tempfile
from pathlib import Path

import streamlit as st
from supabase import create_client


# =========================
# Config + Secrets
# =========================
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


# =========================
# UI Styling
# =========================
def inject_ui() -> None:
    st.markdown(
        """
        <style>
        :root {
            --bg-1: #0b1020;
            --bg-2: #111a33;
            --card-1: #121a30;
            --card-2: #18223f;
            --text: #e8ecf8;
            --muted: #a8b2d1;
            --accent: #7c9cff;
            --accent-2: #5eead4;
            --border: rgba(255,255,255,0.12);
            --shadow: 0 10px 28px rgba(0,0,0,0.28);
        }

        .stApp {
            background:
                radial-gradient(1200px 620px at 8% -12%, #1d2a59 0%, transparent 55%),
                radial-gradient(900px 520px at 95% -8%, #13354f 0%, transparent 50%),
                linear-gradient(180deg, var(--bg-2) 0%, var(--bg-1) 70%);
            color: var(--text);
        }

        .block-container {
            max-width: 1250px;
            padding-top: 1.0rem !important;
            padding-bottom: 1.5rem !important;
        }

        .hero {
            border: 1px solid var(--border);
            background: linear-gradient(120deg, rgba(124,156,255,0.20), rgba(94,234,212,0.10));
            border-radius: 18px;
            padding: 1rem 1.1rem;
            margin-bottom: 0.9rem;
            box-shadow: var(--shadow);
            backdrop-filter: blur(4px);
        }
        .hero h1 {
            margin: 0;
            color: var(--text);
            font-size: clamp(1.25rem, 2.6vw, 2rem);
            line-height: 1.2;
        }
        .hero p {
            margin: 0.35rem 0 0 0;
            color: var(--muted);
            font-size: 0.95rem;
        }

        .glass-card {
            border: 1px solid var(--border);
            background: linear-gradient(180deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
            border-radius: 16px;
            padding: 0.9rem 1rem;
            box-shadow: var(--shadow);
            margin-bottom: 0.9rem;
        }

        [data-testid="stMetric"] {
            border-radius: 14px !important;
            border: 1px solid var(--border) !important;
            background: linear-gradient(180deg, var(--card-1), var(--card-2)) !important;
            padding: 16px !important;
            box-shadow: var(--shadow) !important;
            min-height: 108px !important;
        }
        [data-testid="stMetricLabel"] p {
            color: var(--muted) !important;
            font-size: 0.74rem !important;
            letter-spacing: 0.07em !important;
            text-transform: uppercase !important;
            font-weight: 700 !important;
        }
        [data-testid="stMetricValue"] {
            color: var(--text) !important;
            font-size: 1.5rem !important;
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
            border: 1px solid rgba(124,156,255,0.55) !important;
            background: linear-gradient(90deg, #5f7fff, #7493ff) !important;
            color: white !important;
            font-weight: 600 !important;
            transition: transform .12s ease, box-shadow .12s ease;
        }
        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 8px 18px rgba(95,127,255,.34);
        }

        [data-testid="stSidebar"] {
            border-right: 1px solid var(--border);
            background: linear-gradient(180deg, rgba(18,26,48,.93), rgba(10,16,33,.98));
        }

        .doc-item {
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 0.65rem 0.8rem;
            margin-bottom: 0.5rem;
            color: var(--text);
            background: rgba(255,255,255,0.03);
        }

        .candidate-pill {
            display: inline-block;
            border: 1px solid var(--border);
            border-radius: 999px;
            padding: 0.2rem 0.55rem;
            margin-right: 0.35rem;
            margin-bottom: 0.35rem;
            font-size: 0.85rem;
            background: rgba(124,156,255,0.18);
            color: #dbe5ff;
        }

        @media (max-width: 900px) {
            .block-container { padding: .8rem .8rem 1rem .8rem !important; }
            [data-testid="stMetricValue"] { font-size: 1.2rem !important; }
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


# =========================
# Auth Pages
# =========================
def login_page():
    hero("🤖 AssistHR", "AI-powered HR workspace for modern teams")

    card_start()
    tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])

    with tab1:
        st.subheader("Welcome back")
        email = st.text_input(
            "Email",
            key="login_email",
            placeholder="you@company.com",
        )
        password = st.text_input(
            "Password",
            type="password",
            key="login_pass",
            placeholder="••••••••",
        )

        if st.button("Login", use_container_width=True):
            if not email or not password:
                st.error("Please fill in all fields.")
            else:
                try:
                    response = supabase.auth.sign_in_with_password(
                        {"email": email, "password": password}
                    )
                    st.session_state.user = response.user
                    st.session_state.token = response.session.access_token
                    st.toast("Logged in successfully")
                    st.rerun()
                except Exception as e:
                    st.error(f"Login failed: {e}")

    with tab2:
        st.subheader("Create account")
        name = st.text_input(
            "Full Name",
            key="reg_name",
            placeholder="John Smith",
        )
        email = st.text_input(
            "Email",
            key="reg_email",
            placeholder="you@company.com",
        )
        password = st.text_input(
            "Password",
            type="password",
            key="reg_pass",
            placeholder="Min 6 characters",
        )
        confirm = st.text_input(
            "Confirm Password",
            type="password",
            key="reg_confirm",
            placeholder="Repeat password",
        )

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
                    st.success("Account created. Please login.")
                except Exception as e:
                    st.error(f"Registration failed: {e}")

    card_end()


def logout():
    try:
        supabase.auth.sign_out()
    except Exception:
        pass
    st.session_state.user = None
    st.session_state.token = None
    st.rerun()


# =========================
# Helpers
# =========================
def save_uploaded_file(uploaded_file, target_dir: Path) -> Path:
    target_dir.mkdir(parents=True, exist_ok=True)
    file_path = target_dir / uploaded_file.name
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path


# =========================
# App Entry
# =========================
inject_ui()

if "user" not in st.session_state:
    st.session_state.user = None
    st.session_state.token = None

if not st.session_state.user:
    login_page()
    st.stop()

current_user = st.session_state.user
current_email = current_user.email if current_user else "unknown@user"

# Sidebar
st.sidebar.title("🤖 AssistHR")
st.sidebar.caption("AI HR Assistant")
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
st.sidebar.caption("AssistHR v2.0")


# =========================
# Dashboard
# =========================
if page == "📊 Dashboard":
    hero(
        "📊 HR Dashboard",
        "Monitor documents, AI readiness, and screening pipeline health",
    )

    from embedding import get_existing_files

    try:
        all_docs = get_existing_files()
        docs_count = len(all_docs)
    except Exception:
        all_docs = []
        docs_count = 0

    # Optional local resumes count
    resumes_dir = Path(tempfile.gettempdir()) / "resumes"
    try:
        resume_count = (
            len(
                [
                    f
                    for f in os.listdir(resumes_dir)
                    if f.lower().endswith((".pdf", ".docx", ".jpg", ".jpeg", ".png"))
                ]
            )
            if resumes_dir.exists()
            else 0
        )
    except Exception:
        resume_count = 0

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("📄 Documents", docs_count)
    with c2:
        st.metric("👥 Resumes Cached", resume_count)
    with c3:
        st.metric("🤖 AI Model", "Groq")
    with c4:
        st.metric("🗄️ Vector DB", "Supabase")

    st.divider()

    col_a, col_b, col_c = st.columns(3)
    col_a.success("System: Online")
    col_b.info("Embeddings: Synced")
    col_c.warning("Screening queue: Idle")

    st.divider()
    st.subheader("📁 Uploaded Documents")

    if not all_docs:
        st.info("No documents uploaded yet. Go to Documents page to upload.")
    else:
        for doc in all_docs:
            safe_doc = html.escape(str(doc))
            st.markdown(f'<div class="doc-item">📄 {safe_doc}</div>', unsafe_allow_html=True)


# =========================
# Documents
# =========================
elif page == "📄 Documents":
    hero("📄 HR Documents", "Upload, process, and track your knowledge base")

    from document_loader import load_document
    from chunking import chunk_documents
    from embedding import create_vector_store, get_existing_files

    card_start()
    st.subheader("Upload Document")
    st.caption("Accepted: PDF, DOCX, TXT")
    uploaded = st.file_uploader("Choose file", type=["pdf", "docx", "txt"])

    if uploaded and st.button("Upload & Process", use_container_width=True):
        with st.spinner(f"Processing '{uploaded.name}'..."):
            temp_dir = Path(tempfile.gettempdir()) / "assisthr_docs"
            file_path = save_uploaded_file(uploaded, temp_dir)

            try:
                docs = load_document(str(file_path))
                chunks = chunk_documents(docs)
                create_vector_store(chunks)
                st.success(f"'{uploaded.name}' uploaded ({len(chunks)} chunks)")
                st.toast("Document processed successfully")
            except Exception as e:
                st.error(f"Error: {e}")
            finally:
                if file_path.exists():
                    file_path.unlink(missing_ok=True)
    card_end()

    st.divider()
    st.subheader("Uploaded Documents")
    try:
        existing = get_existing_files()
        if not existing:
            st.info("No documents uploaded yet.")
        else:
            for doc in existing:
                st.markdown(
                    f'<div class="doc-item">📄 {html.escape(str(doc))}</div>',
                    unsafe_allow_html=True,
                )
    except Exception as e:
        st.error(f"Could not load documents: {e}")


# =========================
# Chat
# =========================
elif page == "💬 Chat":
    hero("💬 HR Assistant", "Ask policy, process, and HR operations questions")

    from rag_chain import ask
    from chat_store import create_session, load_history

    card_start()
    col1, col2 = st.columns([2, 1])

    with col1:
        session_id = st.text_input(
            "Session Name",
            value="default",
            placeholder="e.g. hr-queries",
        )
    with col2:
        model = st.selectbox(
            "Select Model",
            [
                "llama-3.1-8b-instant",
                "llama-3.3-70b-versatile",
                "meta-llama/llama-4-scout-17b-16e-instruct",
            ],
        )
    card_end()

    full_session = f"{current_email}_{session_id}"

    if (
        "messages" not in st.session_state
        or "last_session" not in st.session_state
        or st.session_state.last_session != full_session
    ):
        st.session_state.last_session = full_session
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

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    prompt = st.chat_input("Ask about HR policies, leave, dress code...")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            with st.spinner("AssistHR is thinking..."):
                try:
                    answer = ask(prompt, full_session, model)
                    st.write(answer)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": answer}
                    )
                except Exception as e:
                    st.error(f"Error: {e}")


# =========================
# Screening
# =========================
elif page == "👥 Screening":
    hero("👥 Resume Screening", "Score candidates against role requirements in minutes")

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
    st.caption("Upload one JD and multiple resumes. PDF, DOCX, and image resumes are supported.")
    card_end()

    col1, col2 = st.columns(2)
    with col1:
        card_start()
        st.subheader("📋 Job Description")
        jd = st.file_uploader("Upload JD (PDF or DOCX)", type=["pdf", "docx"], key="jd")
        card_end()

    with col2:
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
                    results = screen_all(
                        [str(p) for p in resume_paths],
                        str(jd_path),
                        model,
                    )
                except Exception as e:
                    st.error(f"Screening failed: {e}")
                    results = []

            # cleanup temp files
            jd_path.unlink(missing_ok=True)
            for p in resume_paths:
                p.unlink(missing_ok=True)

            if results:
                st.success(f"Screened {len(results)} candidate(s)")
                st.toast("Screening complete")

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
                        c1, c2 = st.columns(2)
                        c1.write(f"📧 {r.get('email', 'N/A')}")
                        c1.write(f"📞 {r.get('phone', 'N/A')}")
                        c2.write(f"🎓 {r.get('education', 'N/A')}")

                        if r.get("linkedin"):
                            c2.write(f"🔗 [LinkedIn]({r.get('linkedin')})")
                        if r.get("github"):
                            c2.write(f"💻 [GitHub]({r.get('github')})")

                        st.divider()
                        col_l, col_r = st.columns(2)
                        with col_l:
                            st.write("✅ **Matched Skills**")
                            for s in r.get("matched_skills", []):
                                st.markdown(
                                    f'<span class="candidate-pill">{html.escape(str(s))}</span>',
                                    unsafe_allow_html=True,
                                )
                        with col_r:
                            st.write("❌ **Missing Skills**")
                            for s in r.get("missing_skills", []):
                                st.markdown(
                                    f'<span class="candidate-pill" style="background:rgba(251,113,133,.15);color:#ffd5de;">{html.escape(str(s))}</span>',
                                    unsafe_allow_html=True,
                                )

                        st.divider()
                        st.write(f"💪 **Strengths:** {r.get('strengths', '')}")
                        st.write(f"⚠️ **Weaknesses:** {r.get('weaknesses', '')}")
                        st.caption(f"Model used: {r.get('model', model)}")
            else:
                st.warning("No results returned.")
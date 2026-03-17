import os
import streamlit as st
from supabase import create_client


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
    page_title = "AssistHR",
    page_icon  = "🤖",
    layout     = "centered"
)


def login_page():
    st.title("🤖 AssistHR")
    st.caption("AI-powered HR Assistant")
    st.divider()

    tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])

    # ── LOGIN ─────────────────────────────────
    with tab1:
        st.subheader("Welcome back")
        email = st.text_input(
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
            "Login",
            use_container_width=True
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
                    st.success("✅ Logged in!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Login failed: {e}")

    # ── REGISTER ──────────────────────────────
    with tab2:
        st.subheader("Create account")
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
            "Create Account",
            use_container_width=True
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


if "user" not in st.session_state:
    st.session_state.user  = None
    st.session_state.token = None

if not st.session_state.user:
    login_page()
    st.stop()

# get current user info
current_user  = st.session_state.user
current_email = current_user.email

st.sidebar.title("🤖 AssistHR")
st.sidebar.caption("AI HR Assistant")
st.sidebar.divider()

page = st.sidebar.radio(
    "Navigation",
    [
        "📊 Dashboard",
        "📄 Documents",
        "💬 Chat",
        "👥 Screening"
    ]
)

st.sidebar.divider()
st.sidebar.write(f"👤 {current_email}")
if st.sidebar.button(
    "Logout",
    use_container_width=True
):
    logout()

st.sidebar.divider()
st.sidebar.caption("AssistHR v1.0")

if page == "📊 Dashboard":
    st.title("📊 Dashboard")

    st.markdown("""
        <style>
                
        [data-testid="stMetric"] {
            border-radius  : 12px !important;
            padding        : 20px 20px !important;
            min-height     : 110px !important;
            display        : flex !important;
            flex-direction : column !important;
            justify-content: center !important;
            box-shadow     : 0 1px 4px rgba(0,0,0,0.08) !important;
            border         : 1px solid rgba(0,0,0,0.1) !important;
            background     : var(--card-bg) !important;
        }

        
        [data-testid="stMetricLabel"] p {
            font-size     : 11px !important;
            font-weight   : 600 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.06em !important;
            white-space   : normal !important;
            word-break    : break-word !important;
            line-height   : 1.4 !important;
            color         : var(--card-label) !important;
        }

        
        [data-testid="stMetricValue"] {
            font-size  : 24px !important;
            font-weight: 700 !important;
            line-height: 1.2 !important;
            white-space: normal !important;
            word-break : break-word !important;
            color      : var(--card-value) !important;
        }

        
        [data-testid="column"] {
            display       : flex !important;
            flex-direction: column !important;
        }

        [data-testid="column"] [data-testid="stMetric"] {
            flex      : 1 !important;
            height    : 100% !important;
        }

        
        [data-theme="light"],
        [data-theme="light"] * {
            --card-bg    : #ffffff;
            --card-label : #64748b;
            --card-value : #1e293b;
            --doc-bg     : #ffffff;
            --doc-border : #e2e8f0;
            --doc-text   : #334155;
        }

        [data-theme="light"] [data-testid="stMetric"] {
            background: #ffffff !important;
            border    : 1px solid #e2e8f0 !important;
        }

        [data-theme="light"] [data-testid="stMetricLabel"] p {
            color: #64748b !important;
        }

        [data-theme="light"] [data-testid="stMetricValue"] {
            color: #1e293b !important;
        }

        
        [data-theme="dark"],
        [data-theme="dark"] * {
            --card-bg    : #1e293b;
            --card-label : #94a3b8;
            --card-value : #f1f5f9;
            --doc-bg     : #1e293b;
            --doc-border : #334155;
            --doc-text   : #cbd5e1;
        }

        [data-theme="dark"] [data-testid="stMetric"] {
            background: #1e293b !important;
            border    : 1px solid #334155 !important;
        }

        [data-theme="dark"] [data-testid="stMetricLabel"] p {
            color: #94a3b8 !important;
        }

        [data-theme="dark"] [data-testid="stMetricValue"] {
            color: #f1f5f9 !important;
        }

        
        .doc-item {
            border-radius : 8px;
            padding       : 10px 16px;
            margin-bottom : 6px;
            font-size     : 14px;
            display       : flex;
            align-items   : center;
            gap           : 8px;
            transition    : all 0.2s ease;
        }

        [data-theme="light"] .doc-item {
            background: #ffffff;
            border    : 1px solid #e2e8f0;
            color     : #334155;
        }

        [data-theme="dark"] .doc-item {
            background: #1e293b;
            border    : 1px solid #334155;
            color     : #cbd5e1;
        }

        </style>
        """, unsafe_allow_html=True)

    # get counts
    from embedding import get_existing_files

    try:
        all_docs     = get_existing_files()
        docs_count   = len(all_docs)
    except Exception:
        all_docs     = []
        docs_count   = 0

    # count resumes from uploads folder
    try:
        resume_dir   = "/tmp/resumes"
        resume_count = len([
            f for f in os.listdir(resume_dir)
            if f.endswith((
                ".pdf", ".docx",
                ".jpg", ".jpeg", ".png"
            ))
        ]) if os.path.exists(resume_dir) else 0
    except Exception:
        resume_count = 0

    # ── METRIC CARDS ──────────────────────────
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label = "📄  Documents",
            value = docs_count
        )
    with col2:
        st.metric(
            label = "👥  Resumes Screened",
            value = resume_count
        )
    with col3:
        st.metric(
            label = "🤖  AI Model",
            value = "Groq"
        )
    with col4:
        st.metric(
            label = "🗄️  Vector DB",
            value = "Supabase"
        )

    st.divider()

    # ── RECENT DOCUMENTS ──────────────────────
    st.subheader("📁 Uploaded Documents")

    if not all_docs:
        st.info(
            "No documents uploaded yet. "
            "Go to Documents page to upload."
        )
    else:
        for doc in all_docs:
            st.markdown(
                f"""<div class="doc-item">
                    📄 {doc}
                </div>""",
                unsafe_allow_html=True
            )


# if page == "📊 Dashboard":
#     st.title("📊 Dashboard")

#     from embedding import get_existing_files

#     try:
#         docs_count = len(get_existing_files())
#     except Exception:
#         docs_count = 0

#     col1, col2, col3, col4 = st.columns(4)
#     col1.metric("Documents Uploaded", docs_count)
#     col2.metric("AI Model",           "Groq llama-3.3-70b")
#     col3.metric("Vector DB",          "Supabase pgvector")
#     col4.metric("Status",             "Running ✅")

#     st.divider()
#     st.subheader("Uploaded Documents")

#     try:
#         docs = get_existing_files()
#         if not docs:
#             st.info("No documents uploaded yet.")
#         else:
#             for doc in docs:
#                 st.write(f"📄 {doc}")
#     except Exception as e:
#         st.error(f"Could not load documents: {e}")

# elif page == "📄 Documents":
#     st.title("📄 HR Documents")

#     from document_loader import load_document
#     from chunking        import chunk_documents
#     from embedding       import (
#         create_vector_store,
#         get_existing_files
#     )

#     # ── UPLOAD ────────────────────────────────
#     st.subheader("Upload Document")
#     uploaded = st.file_uploader(
#         "Choose file",
#         type=["pdf", "docx", "txt"]
#     )

#     if uploaded:
#         if st.button(
#             "Upload & Process",
#             use_container_width=True
#         ):
#             with st.spinner(
#                 f"Processing '{uploaded.name}'..."
#             ):
#                 tmp_path = f"/tmp/{uploaded.name}"
#                 with open(tmp_path, "wb") as f:
#                     f.write(uploaded.getbuffer())
#                 try:
#                     docs   = load_document(tmp_path)
#                     chunks = chunk_documents(docs)
#                     create_vector_store(chunks)
#                     st.success(
#                         f"✅ '{uploaded.name}' uploaded "
#                         f"({len(chunks)} chunks)"
#                     )
#                 except Exception as e:
#                     st.error(f"❌ Error: {e}")
#                 finally:
#                     if os.path.exists(tmp_path):
#                         os.remove(tmp_path)

#     # ── LIST ──────────────────────────────────
#     st.divider()
#     st.subheader("Uploaded Documents")

#     try:
#         existing = get_existing_files()
#         if not existing:
#             st.info("No documents uploaded yet.")
#         else:
#             for doc in existing:
#                 col1, col2 = st.columns([4, 1])
#                 col1.write(f"📄 {doc}")
#     except Exception as e:
#         st.error(f"Could not load documents: {e}")



elif page == "💬 Chat":
    st.title("💬 HR Assistant")

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
            "Select Model",
            [
                "llama-3.1-70b-versatile",
                "llama-3.1-8b-instant",
                "mixtral-8x7b-32768",
                "gemma2-9b-it"
            ]
        )

    full_session = f"{current_email}_{session_id}"

    # ── LOAD HISTORY ──────────────────────────
    if "messages"     not in st.session_state or \
       "last_session" not in st.session_state or \
        st.session_state.last_session != full_session:

        st.session_state.last_session = full_session
        try:
            create_session(full_session)
            history  = load_history(full_session)
            st.session_state.messages = [
                {
                    "role"   : "user" if msg.type == "human"
                               else "assistant",
                    "content": msg.content
                }
                for msg in history
            ]
        except Exception:
            st.session_state.messages = []

    # ── SHOW MESSAGES ─────────────────────────
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # ── INPUT ─────────────────────────────────
    if prompt := st.chat_input(
        "Ask about HR policies, leave, dress code..."
    ):
        st.session_state.messages.append({
            "role"   : "user",
            "content": prompt
        })
        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            with st.spinner("AssistHR is thinking..."):
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
                    st.error(f"❌ Error: {e}")

elif page == "👥 Screening":
    st.title("👥 Resume Screening")

    from screener import screen_all

    # ── MODEL SELECTION ───────────────────────
    model = st.selectbox(
        "Select Model",
        [
            "llama-3.3-70b-versatile",  
            "llama-3.1-8b-instant",    
            "llama-3.3-70b-specdec",    
            "meta-llama/llama-4-scout-17b-16e-instruct",
        ]
    )

    st.divider()

    # ── FILE UPLOAD ───────────────────────────
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📋 Job Description")
        jd = st.file_uploader(
            "Upload JD (PDF or DOCX)",
            type=["pdf", "docx"],
            key="jd"
        )

    with col2:
        st.subheader("📄 Resumes")
        resumes = st.file_uploader(
            "Upload Resumes (multiple allowed)",
            type             = ["pdf", "docx",
                                "jpg", "jpeg", "png"],
            accept_multiple_files= True,
            key="resumes"
        )

    st.divider()

    # ── SCREEN BUTTON ─────────────────────────
    if st.button(
        "🔍 Screen Resumes",
        type               = "primary",
        use_container_width= True
    ):
        if not jd:
            st.error("Please upload a Job Description.")
        elif not resumes:
            st.error("Please upload at least one resume.")
        else:
            # save files to /tmp
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
                        resume_paths,
                        jd_path,
                        model
                    )
                except Exception as e:
                    st.error(f"❌ Screening failed: {e}")
                    results = []

            # cleanup tmp files
            if os.path.exists(jd_path):
                os.remove(jd_path)
            for path in resume_paths:
                if os.path.exists(path):
                    os.remove(path)

            # ── RESULTS ───────────────────────
            if results:
                st.success(
                    f"✅ Screened "
                    f"{len(results)} candidate(s)"
                )
                st.divider()

                for i, r in enumerate(results, 1):
                    verdict = r.get("verdict", "")
                    score   = r.get("score",   0)
                    name    = r.get("name", "Unknown")

                    with st.expander(
                        f"#{i}  {name}  "
                        f"|  {score}%  "
                        f"|  {verdict}"
                    ):
                        # score + progress
                        col1, col2 = st.columns(2)
                        col1.metric("Score", f"{score}%")
                        col2.metric(
                            "Experience",
                            r.get("experience",
                                  "Not specified")
                        )
                        st.progress(score / 100)
                        st.divider()

                        # contact info
                        col1, col2 = st.columns(2)
                        col1.write(
                            f"📧 {r.get('email', 'N/A')}"
                        )
                        col1.write(
                            f"📞 {r.get('phone', 'N/A')}"
                        )
                        col2.write(
                            f"🎓 {r.get('education', 'N/A')}"
                        )
                        if r.get("linkedin"):
                            col2.write(
                                f"🔗 [LinkedIn]"
                                f"({r.get('linkedin')})"
                            )
                        if r.get("github"):
                            col2.write(
                                f"💻 [GitHub]"
                                f"({r.get('github')})"
                            )

                        st.divider()

                        # skills
                        col1, col2 = st.columns(2)
                        with col1:
                            if r.get("matched_skills"):
                                st.write(
                                    "✅ **Matched Skills:**"
                                )
                                st.write(
                                    " • ".join(
                                        r["matched_skills"]
                                    )
                                )
                        with col2:
                            if r.get("missing_skills"):
                                st.write(
                                    "❌ **Missing Skills:**"
                                )
                                st.write(
                                    " • ".join(
                                        r["missing_skills"]
                                    )
                                )

                        st.divider()

                        # strengths + weaknesses
                        st.write(
                            f"💪 **Strengths:** "
                            f"{r.get('strengths', '')}"
                        )
                        st.write(
                            f"⚠️ **Weaknesses:** "
                            f"{r.get('weaknesses', '')}"
                        )

                        st.caption(
                            f"Model used: {r.get('model')}"
                        )
            else:
                st.warning("No results returned.")
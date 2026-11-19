import streamlit as st
from pdf_service import extract_pdf_text
from gemini_service import ask_gemini, summarize_pdf

st.set_page_config(
    page_title="NEXUS AI | PDF Intelligence",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Session state ----------
DEFAULTS = {
    "pdf_text": "",
    "page_count": 0,
    "summary": "",
    "file_name": "",
    "chat_history": [],
    "project_name": "My AI Project",
}
for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ---------- Styling ----------
st.markdown("""
<style>
.stApp { background: #080b14; color: #f1f5f9; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.7rem; padding-bottom: 3rem; max-width: 1450px; }
section[data-testid="stSidebar"] { background: #0d1220; border-right: 1px solid #222b40; }
section[data-testid="stSidebar"] > div { padding-top: 1.8rem; }
h1, h2, h3 { color: #f8fafc !important; letter-spacing: -0.4px; }
p, label { color: #a9b4c7; }
.brand { font-size: 27px; font-weight: 800; letter-spacing: 2px; color: #fff; }
.brand span { color: #9b8cff; }
.brand-sub { color: #7c8aa5; font-size: 10px; letter-spacing: 2.5px; }
.hero {
  padding: 34px; border-radius: 22px;
  background: radial-gradient(circle at 90% 10%, #44348b 0%, transparent 40%),
              linear-gradient(120deg, #171b36, #111a2e 65%, #15213a);
  border: 1px solid #34365f; margin-bottom: 24px;
}
.hero-tag { display:inline-block; padding:7px 13px; border-radius:30px;
  background:#30275b; color:#c8baff; font-size:11px; margin-bottom:14px; }
.hero h1 { font-size: clamp(28px, 4vw, 42px); font-weight:800; line-height:1.2; margin:0 0 12px 0; }
.hero p { color:#b4bfd4; font-size:14px; max-width:700px; line-height:1.7; }
.metric-card { background:linear-gradient(145deg,#151d30,#101626);
  border:1px solid #27334c; padding:19px; border-radius:16px; min-height:120px; }
.metric-label { color:#8f9cb5; font-size:12px; }
.metric-value { color:white; font-size:27px; font-weight:800; margin-top:8px; }
.metric-icon { font-size:20px; margin-bottom:7px; }
.info-card { background:#111a2b; border:1px solid #293650; border-radius:16px;
  padding:20px; margin-bottom:12px; }
.info-card h3 { font-size:16px; margin:0 0 8px 0; }
.info-card p { color:#98a6bd; font-size:13px; line-height:1.6; }
.section-heading { font-size:19px; font-weight:700; color:#f1f5f9; margin:22px 0 13px 0; }
div[data-testid="stFileUploader"] { background:#111a2b; border:1px dashed #6558b8; border-radius:16px; padding:14px; }
.stButton > button, .stDownloadButton > button {
  background:linear-gradient(100deg,#7665ed,#a16bf3); color:white !important;
  border:0; border-radius:10px; min-height:43px; font-weight:700; width:100%;
}
.stButton > button:hover, .stDownloadButton > button:hover {
  background:linear-gradient(100deg,#6554db,#8755dc); border:0;
}
.stTextInput input, .stTextArea textarea {
  background:#111a2b !important; color:white !important;
  border:1px solid #303c56 !important; border-radius:10px !important;
}
.stTabs [data-baseweb="tab-list"] { gap:8px; background:#101626; border-radius:11px; padding:7px; }
.stTabs [aria-selected="true"] { background:#40347c !important; color:white !important; }
hr { border-color:#28334b; }
.footer { text-align:center; color:#68758c; font-size:11px; padding:25px 0 8px; }
@media(max-width:768px) {
  .hero { padding:22px; }
  .block-container { padding-left:1rem; padding-right:1rem; }
}
</style>
""", unsafe_allow_html=True)

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown('<div class="brand">NEXUS<span> AI.</span></div><div class="brand-sub">DOCUMENT INTELLIGENCE</div>', unsafe_allow_html=True)
    st.write("")
    st.divider()
    st.markdown("### Navigation")
    page = st.radio(
        "Navigation",
        ["🏠 Dashboard", "📄 PDF Reader", "✨ AI Summary", "💬 Ask AI"],
        label_visibility="collapsed",
        key="navigation",
    )
    st.divider()
    st.markdown("### Project Settings")
    st.session_state.project_name = st.text_input(
        "Project name", value=st.session_state.project_name
    )
    st.divider()
    st.markdown("**System status**")
    st.caption("● PDF engine ready")
    st.caption("● Gemini connects when an AI action is requested")
    st.caption("NEXUS AI · Version 1.0")

# ---------- Hero ----------
st.markdown("""
<div class="hero">
  <div class="hero-tag">✦ YOUR AI DOCUMENT WORKSPACE</div>
  <h1>Understand documents.<br>Think smarter with AI.</h1>
  <p>Upload a PDF, extract its text, generate a clear summary, and ask questions
  about the document using Google Gemini.</p>
</div>
""", unsafe_allow_html=True)

# ---------- Upload ----------
st.markdown('<div class="section-heading">📂 Upload your document</div>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("Choose a PDF document", type=["pdf"])

if uploaded_file is not None:
    if uploaded_file.name != st.session_state.file_name:
        st.session_state.pdf_text = ""
        st.session_state.page_count = 0
        st.session_state.summary = ""
        st.session_state.chat_history = []
        st.session_state.file_name = uploaded_file.name

    st.success(f"Selected: {uploaded_file.name}")
    if st.button("✦ Extract PDF and prepare workspace", key="extract_pdf"):
        with st.spinner("Reading your PDF..."):
            try:
                extracted_text, page_count = extract_pdf_text(uploaded_file)
                st.session_state.pdf_text = extracted_text
                st.session_state.page_count = page_count
                st.session_state.summary = ""
                st.session_state.chat_history = []
                st.success("PDF extracted successfully. Your workspace is ready.")
            except Exception as exc:
                st.error(str(exc))

pdf_text = st.session_state.pdf_text

# ---------- Metrics ----------
st.markdown('<div class="section-heading">📊 Workspace overview</div>', unsafe_allow_html=True)
metrics = [
    ("📄", "TOTAL PAGES", st.session_state.page_count),
    ("📝", "TOTAL WORDS", len(pdf_text.split()) if pdf_text else 0),
    ("🔤", "CHARACTERS", len(pdf_text) if pdf_text else 0),
    ("🤖", "AI STATUS", "READY" if pdf_text else "WAITING"),
]
cols = st.columns(4)
for col, (icon, label, value) in zip(cols, metrics):
    with col:
        st.markdown(
            f'<div class="metric-card"><div class="metric-icon">{icon}</div>'
            f'<div class="metric-label">{label}</div>'
            f'<div class="metric-value">{value}</div></div>',
            unsafe_allow_html=True,
        )

# ---------- Pages ----------
if page == "🏠 Dashboard":
    st.markdown('<div class="section-heading">🚀 Explore your workspace</div>', unsafe_allow_html=True)
    left, right = st.columns(2)
    with left:
        st.markdown('<div class="info-card"><h3>📄 Smart PDF Reader</h3><p>Extract and review the text inside your PDF documents.</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="info-card"><h3>💬 Ask your PDF</h3><p>Ask questions and receive answers grounded in your uploaded document.</p></div>', unsafe_allow_html=True)
    with right:
        st.markdown('<div class="info-card"><h3>✨ AI Document Summary</h3><p>Turn lengthy documents into clear summaries and key points.</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="info-card"><h3>📊 Document Analytics</h3><p>View page, word, and character counts at a glance.</p></div>', unsafe_allow_html=True)
    if pdf_text:
        st.info(f"Active document: {st.session_state.file_name}")
    else:
        st.info("Upload a PDF above and extract its text to activate the workspace.")

elif page == "📄 PDF Reader":
    st.subheader("📄 Document explorer")
    if pdf_text:
        st.caption(f"File: {st.session_state.file_name}")
        st.text_area("Extracted document content", pdf_text, height=420)
        st.download_button("⬇ Download extracted text", pdf_text, "extracted_text.txt", "text/plain")
    else:
        st.warning("Upload and extract a PDF first.")

elif page == "✨ AI Summary":
    st.subheader("✨ Intelligent AI summary")
    st.write("Generate a structured summary of your uploaded document.")
    if pdf_text:
        if st.button("✦ Generate AI summary"):
            with st.spinner("Gemini is analyzing your document..."):
                try:
                    st.session_state.summary = summarize_pdf(pdf_text)
                except Exception as exc:
                    st.error(f"Summary generation failed: {exc}")
        if st.session_state.summary:
            st.markdown("### Your summary")
            st.markdown(st.session_state.summary)
            st.download_button("⬇ Download summary", st.session_state.summary, "ai_summary.txt", "text/plain")
    else:
        st.warning("Upload and extract a PDF first.")

elif page == "💬 Ask AI":
    st.subheader("💬 Chat with your document")
    st.write("Ask a question about the information in your PDF.")
    if pdf_text:
        with st.form("ask_pdf_form"):
            question = st.text_area(
                "Your question",
                placeholder="Example: What are the main objectives of this document?",
                height=100,
            )
            submitted = st.form_submit_button("✦ Ask Gemini AI")
        if submitted:
            if not question.strip():
                st.warning("Please enter a question.")
            else:
                with st.spinner("Gemini is preparing an answer..."):
                    try:
                        answer = ask_gemini(pdf_text, question)
                        st.session_state.chat_history.append({"question": question, "answer": answer})
                    except Exception as exc:
                        st.error(f"AI response failed: {exc}")
        if st.session_state.chat_history:
            st.markdown("### Conversation")
            for item in reversed(st.session_state.chat_history):
                with st.expander(item["question"], expanded=(item == st.session_state.chat_history[-1])):
                    st.markdown(item["answer"])
    else:
        st.warning("Upload and extract a PDF first.")

st.divider()
st.markdown(
    '<div class="footer"><b>NEXUS AI</b> · Intelligent Document Analysis Platform<br>'
    'Built with Python · Streamlit · PyMuPDF · Google Gemini</div>',
    unsafe_allow_html=True,
)

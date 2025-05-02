
import os
import uuid
import streamlit as st
from dotenv import load_dotenv
from camel_agents import MedicalReportAssistant

# --------------------------- Initialization ---------------------------
load_dotenv("api.env")

# --------------------------- Page Config ---------------------------
st.set_page_config(
    page_title="⚡ MedAI Pro",
    page_icon="⚕️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------- UI Setup ---------------------------
def set_theme():
    st.markdown("""
        <style>
            [data-testid=stAppViewContainer] {background-color: #121212;}
            .stTextArea textarea {color: white !important;}
            .result-box {
                padding: 15px; 
                border-radius: 10px; 
                background: #2d2d2d;
                margin-bottom: 20px;
            }
            .stMarkdown h3 {
                color: #4fc3f7;
            }
        </style>
    """, unsafe_allow_html=True)

set_theme()

# --------------------------- Main App ---------------------------
st.title("⚡ MedAI Pro")
st.markdown("**World's Most Advanced Medical Report Analyzer**")


def get_assistant():
    return MedicalReportAssistant()


if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None

if "clear_file" not in st.session_state:
    st.session_state.clear_file = lambda: st.session_state.update(uploaded_file=None)

# File Upload
with st.sidebar:
    st.subheader("📁 Upload Medical Report")
    uploaded_file = st.file_uploader("", type=["pdf"], label_visibility="collapsed")

    # Clear (Dustbin) Option
    if uploaded_file is not None:
        st.sidebar.button("🗑️ Clear Uploaded File", on_click=st.session_state.clear_file)

# Analysis Section
tab1, tab2 = st.tabs(["🧪 Analyze Report", "ℹ️ About"])

with tab1:
    query = st.text_area("🩺 Enter your query (or leave blank to auto-analyze):", 
                        height=120,
                        placeholder="e.g. Explain my blood test results")

    if st.button("🚀 Start Analysis", type="primary", use_container_width=True):
        if not uploaded_file:
            st.error("❌ Please upload a PDF medical report first.")
        else:
            with st.spinner("🧠 Analyzing report with AI..."):
                try:
                    temp_path = f"temp_{uuid.uuid4().hex}.pdf"
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    assistant = MedicalReportAssistant()
                    prompt = query.strip() or "Please analyze this medical report and explain the findings in simple terms."
                    result = assistant.analyze_query(prompt, temp_path)
                    
                    st.markdown("### 🩺 Doctor’s AI Opinion")
                    st.markdown(f'<div class="result-box">{result}</div>', unsafe_allow_html=True)

                    st.success("✅ Analysis completed successfully!")
                
                except Exception as e:
                    st.error(f"⚠️ Error: {str(e)}")
                    st.error("Please try again with a different PDF file")
                
                finally:
                    if os.path.exists(temp_path):
                        os.remove(temp_path)

with tab2:
    st.markdown("""
    ## ℹ️ About MedAI Pro
    Advanced medical report analysis powered by:
    - 🧠 CAMEL AI Framework
    - ⚡ Groq Cloud + Llama 4
    - 🔒 Secure local processing
    
    **Key Features:**
    - Instant PDF report understanding
    - Doctor-level analysis
    - Privacy-focused (no data stored)
    
    **How it works:**
    1. Upload your medical report (PDF)
    2. Ask specific questions or get automatic analysis
    3. Receive easy-to-understand explanations
    """)

st.markdown("---")
st.caption("© 2025 MedAI Pro | For educational and research use only")


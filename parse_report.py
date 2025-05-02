import fitz  # PyMuPDF

def extract_text_from_pdf(file_stream):
    """Streamlit ke file uploader se direct text extract kare"""
    try:
        doc = fitz.open(stream=file_stream.read(), filetype="pdf")
        return "\n".join([page.get_text() for page in doc])
    except Exception as e:
        return f"⚠️ Error: {str(e)}"
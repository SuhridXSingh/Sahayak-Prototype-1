import google.generativeai as genai
import PyPDF2
import os
from dotenv import load_dotenv

# 1. SETUP & CONFIGURATION
def configure_genai():
    api_key = None
    
    # 1. Try fetching from Streamlit Cloud Secrets (The dictionary lookup)
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
    except:
        pass

    # 2. If not found, try local .env file
    if not api_key:
        load_dotenv()
        api_key = os.getenv("GOOGLE_API_KEY")

    # 3. If still nothing, STOP and warn the user
    if not api_key:
        st.error("❌ API Key Missing! Go to 'Manage App' -> 'Secrets' on Streamlit Cloud and add it.")
        st.stop()

    genai.configure(api_key=api_key)
    
    # Using the latest Gemini 3.0 Flash Preview for speed + multimodal
    model = genai.GenerativeModel('gemini-3-flash-preview')
    return model

# Initialize model once
model = configure_genai()

# 2. PDF PROCESSING
def get_pdf_text(uploaded_file):
    """
    Extracts raw text from a PDF file object.
    """
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        return f"Error reading PDF: {e}"

# 3. THE "ELECTRIC FENCE" LOGIC
def ask_sahayak(user_question, document_context):
    """
    Sends the user query + document content to Gemini.
    Enforces strict grounding (no outside knowledge).
    """
    if not document_context:
        return "Please upload a document first."

    # The System Instruction (The "Electric Fence")
    prompt = f"""
    You are Sahayak, an expert government scheme assistant.
    
    STRICT INSTRUCTIONS:
    1. Answer the user's question using ONLY the content provided in the 'Official Document' section below.
    2. If the answer is NOT in the document, you MUST strictly say: "I cannot find this information in the provided document."
    3. Do not make up facts. Do not use outside knowledge.
    4. Format your answer nicely with bullet points if needed.
    5. Be polite and concise.

    --- OFFICIAL DOCUMENT START ---
    {document_context}
    --- OFFICIAL DOCUMENT END ---

    User Question: {user_question}
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI Error: {e}"

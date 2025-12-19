import streamlit as st
import google.generativeai as genai
import PyPDF2
import os
from dotenv import load_dotenv

# 1. SETUP & CONFIGURATION
def configure_genai():
    # 1. Try getting key from Streamlit Cloud Secrets (Production)
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
    except:
        # 2. If that fails, try local .env (Development)
        load_dotenv()
        api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise ValueError("No API Key found! Check Secrets or .env")

    genai.configure(api_key=api_key)
    # Use the Preview model
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

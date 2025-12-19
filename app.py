import streamlit as st
import requests
from streamlit_lottie import st_lottie
import backend  # <--- IMPORTING YOUR BRAIN

# --- CONFIGURATION ---
st.set_page_config(page_title="Sahayak AI", page_icon="🇮🇳", layout="wide")

# --- ANIMATION LOADER ---
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# --- CUSTOM CSS (THE STYLE) ---
# You can swap this block entirely to change the "Theme"
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
    html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }

    /* 1. PULSING AVATAR ANIMATION */
    @keyframes pulse-dot {
        0% { transform: scale(0.9); box-shadow: 0 0 0 0 rgba(255, 75, 75, 0.7); }
        70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(255, 75, 75, 0); }
        100% { transform: scale(0.9); box-shadow: 0 0 0 0 rgba(255, 75, 75, 0); }
    }
    .bot-avatar {
        width: 100px; height: 100px;
        background-color: #ff4b4b;
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        margin: 0 auto;
        animation: pulse-dot 2s infinite;
        color: white; font-size: 40px;
    }

    /* 2. GLASSMORPHISM CARDS */
    .scheme-card {
        background: rgba(255, 255, 255, 0.8);
        border: 1px solid #ddd;
        border-radius: 12px;
        padding: 20px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        margin-bottom: 10px;
    }
    .scheme-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        border-color: #ff4b4b;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR (INPUTS) ---
with st.sidebar:
    # Render HTML for Pulsing Bot
    st.markdown('<div class="bot-avatar">🤖</div>', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>Sahayak AI</h2>", unsafe_allow_html=True)
    
    st.write("---")
    uploaded_file = st.file_uploader("📂 Upload Scheme PDF", type=["pdf"])
    
    if uploaded_file:
        if 'doc_text' not in st.session_state:
            with st.spinner("🧠 Reading Document..."):
                # CALL BACKEND FUNCTION
                st.session_state.doc_text = backend.get_pdf_text(uploaded_file)
            st.success("Document Indexed!")

# --- MAIN PAGE (OUTPUTS) ---
col1, col2 = st.columns([2, 1])

with col1:
    st.title("Simplifying Welfare.")
    st.write("Ask questions about any government scheme document.")
    
    # HTML Cards
    st.markdown("""
    <div style="display: flex; gap: 20px;">
        <div class="scheme-card" style="flex: 1;">
            <h4>📄 Upload PDF</h4>
            <small>Drag & drop official notifications</small>
        </div>
        <div class="scheme-card" style="flex: 1;">
            <h4>⚡ Ask Gemini</h4>
            <small>Powered by Gemini 3.0 Flash</small>
        </div>
    </div>
    <br>
    """, unsafe_allow_html=True)

# --- CHAT LOGIC ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Handle User Input
if user_query := st.chat_input("Ex: What is the age limit for this scheme?"):
    
    # 1. Show User Message
    st.chat_message("user").markdown(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})

    # 2. Process with Backend
    if 'doc_text' in st.session_state:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # CALL BACKEND FUNCTION
                response = backend.ask_sahayak(user_query, st.session_state.doc_text)
                
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
    else:
        st.error("⚠️ Please upload a document first!")

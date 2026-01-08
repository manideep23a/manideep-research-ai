import streamlit as st
from google import genai
import PyPDF2

# --- 1. CONFIGURATION ---
all_keys = [st.secrets.get("KEY1"), st.secrets.get("KEY2"), st.secrets.get("KEY3")]
valid_keys = [k for k in all_keys if k]

# --- 2. PAGE SETUP ---
st.set_page_config(page_title="Research AI", layout="wide")

# --- 3. SIDEBAR (Status Check) ---
with st.sidebar:
    st.header("System Status")
    if valid_keys:
        st.success(f"✅ {len(valid_keys)} Keys Active")
    else:
        st.error("❌ No Keys Found")
    
    st.header("Upload Document")
    uploaded_file = st.file_uploader("Choose a PDF", type="pdf")
    pdf_text = ""
    if uploaded_file:
        reader = PyPDF2.PdfReader(uploaded_file)
        for page in reader.pages:
            pdf_text += page.extract_text()
        st.success("✅ PDF Loaded!")

# --- 4. MAIN AREA (The fix for the blank screen) ---
st.title("Manideep's Research Assistant 🚀")

# Show this if no PDF is uploaded yet
if not uploaded_file:
    st.info("👋 Welcome! Please upload a PDF in the sidebar to start researching.")
else:
    st.write("---")
    st.subheader("Chatting with your Document")

# --- 5. CHAT LOGIC ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask a question about your PDF..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Logic for AI response goes here...
    with st.chat_message("assistant"):
        st.write("I am ready to answer based on your uploaded PDF!")

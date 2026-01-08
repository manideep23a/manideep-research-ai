import streamlit as st
from google import genai
import PyPDF2
import time

# --- 1. CONFIGURATION ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    st.error("⚠️ API Key missing in Secrets!")
    st.stop()

client = genai.Client(api_key=API_KEY)

# --- 2. PAGE SETUP ---
st.set_page_config(page_title="My Research AI", page_icon="📚")
st.title("Manideep's Research Assistant 🚀")

# --- 3. SIDEBAR & UPLOAD ---
with st.sidebar:
    st.header("Upload Document")
    uploaded_file = st.file_uploader("Choose a PDF", type="pdf")
    pdf_text = ""
    if uploaded_file:
        reader = PyPDF2.PdfReader(uploaded_file)
        for page in reader.pages:
            pdf_text += page.extract_text()
        st.success(f"✅ Loaded {len(reader.pages)} pages!")

# --- 4. CHAT LOGIC ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask about your PDF..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...")
        context = f"Context: {pdf_text}\n\nQuestion: {prompt}" if pdf_text else prompt
        
        # --- SMART RETRY LOGIC ---
        success = False
        retries = 0
        while not success and retries < 3:
            try:
                # Switching to 2.5-flash-lite for stable free tier access
                response = client.models.generate_content(
                    model="gemini-2.5-flash-lite", 
                    contents=context
                )
                message_placeholder.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                success = True
            except Exception as e:
                if "429" in str(e):
                    retries += 1
                    message_placeholder.warning(f"⚠️ System busy. Retrying in {retries*5}s...")
                    time.sleep(retries * 5)
                else:
                    message_placeholder.error(f"❌ Error: {e}")
                    break

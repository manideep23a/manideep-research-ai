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

# --- 2. USAGE TRACKER (Session-based) ---
if "message_count" not in st.session_state:
    st.session_state.message_count = 0

# --- 3. PAGE SETUP ---
st.set_page_config(page_title="My Research AI", page_icon="📚")
st.title("Manideep's Research Assistant 🚀")

# --- 4. SIDEBAR & METRICS ---
with st.sidebar:
    st.header("Upload Document")
    uploaded_file = st.file_uploader("Choose a PDF", type="pdf")
    
    # Display the usage counter
    st.markdown("---")
    st.subheader("📊 Your Daily Usage")
    # 1000 is the standard daily limit for Flash-lite in 2026
    remaining = 1000 - st.session_state.message_count
    st.metric(label="Messages Sent", value=st.session_state.message_count, delta=f"{remaining} left")
    
    pdf_text = ""
    if uploaded_file:
        reader = PyPDF2.PdfReader(uploaded_file)
        for page in reader.pages:
            pdf_text += page.extract_text()
        st.success(f"✅ Loaded {len(reader.pages)} pages!")

# --- 5. CHAT LOGIC ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask about your PDF..."):
    # Increment the counter immediately
    st.session_state.message_count += 1
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...")
        context = f"Context: {pdf_text}\n\nQuestion: {prompt}" if pdf_text else prompt
        
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash-lite", 
                contents=context
            )
            message_placeholder.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            message_placeholder.error(f"❌ Error: {e}")

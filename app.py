import streamlit as st
import google.generativeai as genai
import PyPDF2
import time

# --- 1. MULTI-KEY SETUP ---
# In your Streamlit Secrets, save keys as: KEY1="...", KEY2="...", KEY3="..."
KEYS = [st.secrets.get("KEY1"), st.secrets.get("KEY2"), st.secrets.get("KEY3")]
# Filter out any keys you haven't added yet
VALID_KEYS = [k for k in KEYS if k]

if not VALID_KEYS:
    st.error("⚠️ No API keys found! Add KEY1, KEY2, etc. to Secrets.")
    st.stop()

# --- 2. THE ROTATION ENGINE ---
def get_ai_response(full_context):
    """Try each key until one works."""
    for i, key in enumerate(VALID_KEYS):
        try:
            genai.configure(api_key=key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(full_context)
            return response.text, i + 1  # Returns text and which key worked
        except Exception as e:
            if "429" in str(e):
                continue # Try the next key
            else:
                return f"❌ Error: {e}", None
    return "🛑 ALL KEYS EXHAUSTED. Please wait 1 hour.", None

# --- 3. PAGE SETUP ---
st.set_page_config(page_title="Permanent Research AI", page_icon="🚀")
st.title("Manideep's Pro Assistant 🚀")

with st.sidebar:
    st.header("Settings")
    uploaded_file = st.file_uploader("Upload PDF", type="pdf")
    st.write(f"Connected Keys: {len(VALID_KEYS)}")
    
    pdf_text = ""
    if uploaded_file:
        reader = PyPDF2.PdfReader(uploaded_file)
        # Limit to 30 pages to keep requests "light"
        for page in reader.pages[:30]:
            pdf_text += page.extract_text()
        st.success(f"✅ Document Ready")

# --- 4. CHAT INTERFACE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🔄 Searching for an active API key..."):
            context = f"Context: {pdf_text}\n\nQuestion: {prompt}" if pdf_text else prompt
            answer, key_num = get_ai_response(context)
            
            st.markdown(answer)
            if key_num:
                st.caption(f"Used Key #{key_num}")
            st.session_state.messages.append({"role": "assistant", "content": answer})

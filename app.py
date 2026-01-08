import streamlit as st  # <--- THIS MUST BE LINE 1
from google import genai
import PyPDF2

# --- 1. KEY ROTATION ENGINE ---
def get_ai_response(full_context):
    # This checks for KEY1, KEY2, and KEY3 in your Streamlit Secrets
    all_keys = [st.secrets.get("KEY1"), st.secrets.get("KEY2"), st.secrets.get("KEY3")]
    valid_keys = [k for k in all_keys if k]

    for i, key in enumerate(valid_keys):
        try:
            # Using the 2026 'google-genai' library
            client = genai.Client(api_key=key)
            response = client.models.generate_content(
                model="gemini-2.0-flash", 
                contents=full_context
            )
            return response.text, i + 1
        except Exception as e:
            if "429" in str(e):
                continue # Try next key if this one is blocked
            else:
                return f"❌ API Error: {e}", None
    return "🛑 All keys exhausted. Please wait 1 hour.", None

# --- 2. UI SETUP ---
st.set_page_config(page_title="Research AI", layout="wide")
st.title("Manideep's Research Assistant 🚀")

# --- 3. SIDEBAR ---
with st.sidebar:
    st.header("📊 System Status")
    # Show how many keys are working
    keys_found = [k for k in [st.secrets.get("KEY1"), st.secrets.get("KEY2"), st.secrets.get("KEY3")] if k]
    st.success(f"{len(keys_found)} Keys Active")
    
    st.markdown("---")
    st.header("📂 Upload Document")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    pdf_text = ""
    if uploaded_file:
        reader = PyPDF2.PdfReader(uploaded_file)
        for page in reader.pages[:50]: # Optimized for speed
            pdf_text += page.extract_text()
        st.success("✅ PDF Loaded!")

# --- 4. CHAT INTERFACE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show welcome message if empty
if not uploaded_file and not st.session_state.messages:
    st.info("👋 Upload a PDF in the sidebar to start!")

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Ask about your PDF..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🔄 AI is analyzing..."):
            context = f"PDF Text: {pdf_text}\n\nQuestion: {prompt}" if pdf_text else prompt
            answer, key_num = get_ai_response(context)
            st.markdown(answer)
            if key_num:
                st.caption(f"Answered using Key #{key_num}")
            st.session_state.messages.append({"role": "assistant", "content": answer})

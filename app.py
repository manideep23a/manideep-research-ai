import streamlit as st
from google import genai
import time

st.set_page_config(page_title="Manideep AI", layout="centered")
st.title("🤖 Manideep AI Assistant")
st.caption("Gemini – Auto Model Detection (Permanent Fix)")

# -------- LOAD KEY --------
API_KEY = st.secrets.get("GEMINI_KEY_1")

if not API_KEY:
    st.error("❌ Gemini API key missing in Streamlit secrets.")
    st.stop()

client = genai.Client(api_key=API_KEY)

# -------- FIND A WORKING MODEL --------
@st.cache_resource
def get_working_model():
    models = client.models.list()
    for m in models:
        if "generateContent" in (m.supported_generation_methods or []):
            return m.name
    return None

MODEL_NAME = get_working_model()

if not MODEL_NAME:
    st.error("❌ No text-generation models enabled for this API key.")
    st.caption("Create a NEW API key from Google AI Studio.")
    st.stop()

st.success(f"✅ Using model: {MODEL_NAME}")

# -------- RATE LIMIT --------
if "last_time" not in st.session_state:
    st.session_state.last_time = 0

COOLDOWN = 15

prompt = st.text_area("Enter your prompt", height=150)
generate = st.button("🚀 Generate")

if generate:
    now = time.time()
    if now - st.session_state.last_time < COOLDOWN:
        st.warning("⏳ Please wait before next request.")
        st.stop()

    if not prompt.strip():
        st.warning("⚠️ Enter a prompt.")
        st.stop()

    st.session_state.last_time = now

    try:
        with st.spinner("Thinking..."):
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt
            )
        st.write(response.text)

    except Exception as e:
        st.error("🚫 Gemini request failed.")
        st.code(str(e))

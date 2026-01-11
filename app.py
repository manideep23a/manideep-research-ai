import streamlit as st
from google import genai
import time

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Manideep AI",
    layout="centered"
)

st.title("🤖 Manideep AI Assistant")
st.caption("Powered by Google Gemini (Stable & Supported)")

# ------------------ LOAD API KEY ------------------
API_KEY = st.secrets.get("GEMINI_KEY_1")

if not API_KEY:
    st.error("❌ Gemini API key not found in Streamlit secrets.")
    st.stop()

# ------------------ INIT CLIENT ------------------
client = genai.Client(api_key=API_KEY)

# ------------------ MODEL (PERMANENT) ------------------
MODEL_NAME = "models/gemini-1.0-pro"

# ------------------ RATE LIMIT ------------------
if "last_request_time" not in st.session_state:
    st.session_state.last_request_time = 0

COOLDOWN_SECONDS = 15

# ------------------ UI ------------------
prompt = st.text_area(
    "Enter your prompt",
    placeholder="Ask anything...",
    height=150
)

generate = st.button("🚀 Generate")

# ------------------ LOGIC ------------------
if generate:
    now = time.time()

    if now - st.session_state.last_request_time < COOLDOWN_SECONDS:
        st.warning("⏳ Please wait a few seconds before trying again.")
        st.stop()

    if not prompt.strip():
        st.warning("⚠️ Please enter a prompt.")
        st.stop()

    st.session_state.last_request_time = now

    try:
        with st.spinner("Thinking..."):
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt
            )

        if response and response.text:
            st.success("✅ Response generated")
            st.write(response.text)
        else:
            st.error("❌ Empty response from Gemini.")

    except Exception as e:
        st.error("🚫 Gemini request failed.")
        st.caption("This usually means the API key is not enabled for Gemini.")
        st.code(str(e))

# ------------------ FOOTER ------------------
st.divider()
st.caption("⚠️ Cooldown enabled to protect free-tier quota")

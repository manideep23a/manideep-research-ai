import streamlit as st
from google import genai
import itertools
import time

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Manideep AI (Gemini)",
    layout="centered",
)

st.title("🤖 Manideep AI Assistant")
st.caption("Powered by Google Gemini • Stable SDK")

# ------------------ API KEYS ------------------
API_KEYS = [
    st.secrets.get("GEMINI_KEY_1"),
    st.secrets.get("GEMINI_KEY_2"),
    st.secrets.get("GEMINI_KEY_3"),
]

API_KEYS = [k for k in API_KEYS if k]

if not API_KEYS:
    st.error("❌ No Gemini API keys found in Streamlit secrets.")
    st.stop()

key_cycle = itertools.cycle(API_KEYS)

def get_client():
    return genai.Client(api_key=next(key_cycle))

# ------------------ RATE LIMIT ------------------
if "last_request_time" not in st.session_state:
    st.session_state.last_request_time = 0

COOLDOWN_SECONDS = 10

# ------------------ UI ------------------
prompt = st.text_area(
    "Enter your prompt",
    placeholder="Ask anything...",
    height=150
)

generate = st.button("🚀 Generate Response")

# ------------------ LOGIC ------------------
if generate:
    now = time.time()
    elapsed = now - st.session_state.last_request_time

    if elapsed < COOLDOWN_SECONDS:
        st.warning(f"⏳ Please wait {int(COOLDOWN_SECONDS - elapsed)} seconds.")
        st.stop()

    if not prompt.strip():
        st.warning("⚠️ Please enter a prompt.")
        st.stop()

    st.session_state.last_request_time = now

    try:
        with st.spinner("Thinking..."):
            client = get_client()
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt
            )

        if response and response.text:
            st.success("✅ Response generated")
            st.write(response.text)
        else:
            st.error("❌ Empty response from Gemini.")

    except Exception as e:
        st.error("🚫 Quota exceeded or keys exhausted.")
        st.caption("Try again later or replace API keys.")
        st.code(str(e))

# ------------------ FOOTER ------------------
st.divider()
st.caption("⚠️ Cooldown enabled to protect API quota")

import streamlit as st
import google.generativeai as genai
import itertools
import time

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Manideep AI (Gemini)",
    layout="centered",
)

st.title("🤖 Manideep AI Assistant")
st.caption("Powered by Google Gemini • Safe Mode Enabled")

# ------------------ API KEY ROTATION ------------------
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

def get_model():
    genai.configure(api_key=next(key_cycle))
    return genai.GenerativeModel("gemini-1.5-flash")

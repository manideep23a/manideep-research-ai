import streamlit as st
import google.generativeai as genai
import PyPDF2

# --- NEW SAFETY CHECK ---
if "KEY1" not in st.secrets:
    st.error("❌ KEY1 is missing from Secrets! Check your spelling.")
    st.stop()

# Load all available keys into a list
VALID_KEYS = []
for k in ["KEY1", "KEY2", "KEY3"]:
    if k in st.secrets:
        VALID_KEYS.append(st.secrets[k])

st.sidebar.write(f"✅ Active Keys Found: {len(VALID_KEYS)}")

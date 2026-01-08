import streamlit as st

# Check secrets before anything else
if "KEY1" not in st.secrets:
    st.error("⚠️ KEY1 not found in the dashboard Secrets box!")
    st.stop()

# --- 4. MAIN AREA (FORCE RENDER) ---
st.title("Manideep's Research Assistant 🚀")

# This creates a 'Welcome' container that always shows up
with st.container():
    if not uploaded_file:
        st.info("👋 System is Online! Please upload a PDF in the sidebar to begin.")
        # Visual spacer to push the chat input to the bottom
        st.write("##") 
    else:
        st.success(f"📂 Document Active. Ask me anything below!")

# --- 5. CHAT INTERFACE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# The Chat Input - This should always be visible at the bottom
if prompt := st.chat_input("Ask about your document..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🔄 Searching document..."):
            # Use our Key Rotation Engine
            context = f"Context: {pdf_text}\n\nQuestion: {prompt}" if pdf_text else prompt
            answer, key_num = get_ai_response(context)
            
            st.markdown(answer)
            if key_num:
                st.caption(f"Success! Answered using Key #{key_num}")
            st.session_state.messages.append({"role": "assistant", "content": answer})

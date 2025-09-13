import streamlit as st
from ..utils.api_client import send_upload

USER = "user"
ASSISTANT = "assistant"

def upload_form(messages):
    """
    Show upload form and handle sending code/files to backend.
    Returns True if new submission happened.
    """
    submitted = False
    with st.form("upload_form", clear_on_submit=False):
        col1, col2 = st.columns([1, 1])
        with col1:
            text_input = st.text_area(
                "Enter code or text",
                placeholder="Paste code or type any notes here…",
                height=220,
            )

        with col2:
            uploaded = st.file_uploader(
                "Select a file to upload (any type)", 
                type=None
            )

        submitted_btn = st.form_submit_button("⬆️ Upload", use_container_width=True)
    
    if submitted_btn:
        if not text_input and not uploaded:
            st.warning("⚠️ Please provide code/text or a file before uploading.")
            return False

        # Send to backend (or save locally if needed)
        response = send_upload(text_input, uploaded)

        # Append messages
        if text_input:
            messages.append((USER, text_input))

        if response:
            messages.append((ASSISTANT, str(response)))

        st.toast("Upload successful!", icon="✅")
        submitted = True

    return submitted

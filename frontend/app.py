import streamlit as st
from frontend.components.upload_form import upload_form
from frontend.components.chat_display import display_chat

USER = "user"
ASSISTANT = "assistant"

st.caption("💬 Chat-style uploader for saving text/code and files.")

# --- Initialize messages ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Display chat history ---
display_chat(st.session_state.messages)

# --- Show upload form ---
submitted = upload_form(st.session_state.messages)

# --- Rerun to refresh chat if new submission ---
if submitted:
    st.experimental_rerun()

import streamlit as st
from components.chat_ui import chat_box
from components.sidebar_ui import render_sidebar
from components.input_ui import render_input

st.set_page_config(page_title="Chat Upload", page_icon="💬", layout="centered")

render_sidebar(chat_box)

chat_box.init_session()
chat_box.output_messages()

render_input(chat_box)

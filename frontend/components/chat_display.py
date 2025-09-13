import streamlit as st

USER = "user"
ASSISTANT = "assistant"

def display_chat(messages, height=350):
    """
    Display chat messages in a scrollable container.
    User messages are preformatted to preserve spaces.
    """
    st.markdown(
        f"""
        <style>
        .chat-container {{
            max-height: {height}px;
            overflow-y: auto;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 12px;
            background: #fafafa;
            margin-bottom: 1rem;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    with st.container():
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for role, content in messages:
            if role == USER:
                st.chat_message(role).markdown(f"```\n{content}\n```")
            else:
                st.chat_message(role).write(content)
        st.markdown('</div>', unsafe_allow_html=True)

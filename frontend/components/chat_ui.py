from streamlit_chatbox import ChatBox

chat_box = ChatBox(
    use_rich_markdown=True,
    user_theme="gray",
    assistant_theme="blue",
)
chat_box.use_chat_name("chat1")


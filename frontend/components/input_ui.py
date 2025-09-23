import streamlit as st
from services.api_client import save_correct_feedback_response, save_text
from utils.formatting import format_query

def render_input(chat_box):
    try:
        resp = None
        #Handle new chat input
        if query := st.chat_input("Type your code or Upload File"):
            resp = save_text(query)
            formatted_query = format_query(query)
            chat_box.user_say(formatted_query)

            # Show AI answer
            ai_response = f"🤖 {resp['ai_response']}"
            chat_box.ai_say(ai_response)

            # Save latest response in session state
            st.session_state["last_ai_response"] = ai_response 
            st.session_state["last_file_path"] = resp.get("file_path", "")

        #Always render feedback section
        if "last_ai_response" in st.session_state:
            print("Rendering feedback section")
            with st.expander("✏️ Provide Correct Response"):
                corrected = st.text_area(
                    "Enter the correct Response:",
                    key="correct_response_text"
                )
                if st.button("Submit Correction", key="submit_correction"):
                    print("Submitting correction...")
                    if corrected.strip():
                        save_correct_feedback_response(corrected.strip(), 
                            st.session_state.get("last_file_path", ""), 
                            st.session_state["last_ai_response"]
                        )
                        chat_box.ai_say(f"✅ Feedback saved: {corrected}")
                        st.success("Your correction has been saved!") 
                        print("File Path:", st.session_state.get("last_file_path", "N/A"))
                        print("Corrected Response:", corrected) 
                        print("AI Response:", st.session_state["last_ai_response"])
    except Exception as e:
        raise Exception("Failed to process input") from e

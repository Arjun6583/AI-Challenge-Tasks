import streamlit as st
from services.api_client import upload_file, get_analysis 
from services.api_client import save_correct_feedback_response

def render_sidebar(chat_box):
    try:
        with st.sidebar:
            st.subheader("📂 File Upload & Controls")
            uploaded_file = st.file_uploader("Choose any file", key="file_upload")

            # --- Upload File ---
            if st.button("⬆️ Upload File"):
                if not uploaded_file:
                    st.rerun()
                    return
                print("File Uploaded: ", uploaded_file.name)
                if uploaded_file:
                    print("Uploading file:", uploaded_file.name)
                    st.session_state["chat1"] = []
                    resp = upload_file(uploaded_file.name, uploaded_file.getvalue())
                    chat_box.user_say(f"📄 Uploaded file: {uploaded_file.name}")
                    chat_box.ai_say(f"✅ {resp['ai_response']}")

                    # Save last response + file path for feedback
                    st.session_state["last_ai_response"] = resp.get("ai_response", "")
                    st.session_state["last_file_path"] = resp.get("file_path", "")
                    st.rerun()
                else:
                    st.warning("⚠️ Please select a file to upload.")

            # --- Feedback Section (always visible if we have AI response) ---
            if "last_ai_response" in st.session_state:
                print("Rendering feedback section")
                with st.expander("✏️ Provide Correct Response"):
                    corrected = st.text_area(
                        "Enter the correct Response:",
                        key="correct_response_file"
                    )
                    if st.button("Submit Correction", key="submit_correction_btn"):
                        print("Submitting correction...")
                        if corrected.strip():
                            save_correct_feedback_response(
                                corrected.strip(),
                                st.session_state.get("last_file_path", ""),
                                st.session_state["last_ai_response"]
                            )
                            chat_box.ai_say(f"✅ Feedback saved: {corrected}")
                            st.success("Your correction has been saved!") 
                            print("File Path:", st.session_state.get("last_file_path", "N/A"))
                            print("Corrected Response:", corrected) 
                            print("AI Response:", st.session_state["last_ai_response"])

            # --- Analysis Button ---
            if st.button("📊 Analysis"):
                st.session_state["chat1"] = []
                print("Getting analysis...")
                resp = get_analysis()
                if resp is not None:
                    chat_box.ai_say(f"{resp}")
                st.rerun()

            # --- Clear History Button ---
            if st.button("🧹 Clear History"):
                st.session_state["chat1"] = []
                st.rerun()

    except Exception as e:
        st.error(f"⚠️ Error: {str(e)}")

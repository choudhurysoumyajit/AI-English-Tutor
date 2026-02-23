import streamlit as st
from rag_utils import ask_question, audio_transcript, text_to_speech, text_to_speech2
from audio_recorder_streamlit import audio_recorder
from streamlit_float import *
import base64
import os
import sys

# Initialize floating features for the interface
float_init()

def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio controls autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(
            md,
            unsafe_allow_html=True,
        )

# Initialize session state for managing chat messages
def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hi! How may I assist you today?"}]
        audio_bytes = None
        
initialize_session_state()

st.set_page_config(page_title="Advance Rag", layout="wide")
st.title(":material/robot_2: THE BOT ENGLISH TUTOR ")
st.markdown(":green[Click Record button from sidebar to start the chat. Click again to stop.]")

st.sidebar.image("Logo.png")

colspace,col1, col2 = st.sidebar.columns([1,1,1])

with colspace:
    # This column is intentionally left blank
    pass 

with col2:
    if st.sidebar.button("Clear Chat",key="clear_chat_btn",width="stretch"):
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi! How may I assist you today?"}
        ]
        st.rerun()

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

with col1:
    #footer_container = st.sidebar.container()
#with footer_container:
    audio_bytes = audio_recorder(text="",recording_color="#e74c3c",
    neutral_color="#3498db",    
    icon_size="3x", pause_threshold=10.0, sample_rate=41_000)
    

if audio_bytes:
    with st.spinner("Transcribing..."):
        # Write the audio bytes to a temporary file
        webm_file_path = "temp_audio.mp3"
        with open(webm_file_path, "wb") as f:
            f.write(audio_bytes)

        # Convert the audio to text using the speech_to_text function
        transcript = audio_transcript(webm_file_path)

        if transcript:
            st.session_state.messages.append({"role": "user", "content": transcript})
            with st.chat_message("user"):
                st.markdown(transcript)
            os.remove(webm_file_path)

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
            response = ask_question(st.session_state.messages)
            with st.spinner("Generating audio response..."):    
                text_to_speech2(response)
                autoplay_audio('t2s.mp3')

            placeholder = st.empty()
            full_response = response  # Directly use the response
            placeholder.markdown(full_response)
# message = {"role": "assistant", "content": full_response}
    # Append ONE assistant message
    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
        "audio": "t2s.mp3"
    })

    os.remove('t2s.mp3')




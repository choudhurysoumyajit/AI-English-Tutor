import streamlit as st
from rag_utils import ask_question, audio_transcript, text_to_speech, text_to_speech2
from audio_recorder_streamlit import audio_recorder
from streamlit_float import *
import base64
import os
import sys



# Initialize floating features for the interface
float_init()

##############

page_element="""
<style>
[data-testid="stAppViewContainer"]{
  background-image: url("https://cdn.wallpapersafari.com/88/75/cLUQqJ.jpg");
  background-size: cover;
}
[data-testid="stHeader"]{
  background-color: rgba(0,0,0,0);
}
</style>
"""
st.markdown(page_element, unsafe_allow_html=True)

#Styling the Delete Chat Button
st.markdown( """ <style> div.stButton > button:first-child { background-color: #e74c3c; color: white; border-radius: 8px; height: 50px; width: 100%; font-size: 18px; } div.stButton > button:hover { background-color: #c0392b; color: white; } </style> """, unsafe_allow_html=True )

#############

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
#st.title(":material/robot_2: THE BOT ENGLISH TUTOR ")
st.markdown("<h1 style='text-align: center; color: white';>🤖 THE BOT ENGLISH TUTOR</h1>", unsafe_allow_html=True)
st.markdown("<h6 style='text-align: center; color: lime';>Click on Record Button to start. Click again to stop.</h6>", unsafe_allow_html=True)

button_container = st.container()
with button_container:
    if st.button("Clear Chat",key="clear_chat_btn",width="stretch"):
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi! How may I assist you today?"}
        ]
        st.rerun()

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

    #footer_container = st.sidebar.container()
#with footer_container:
with button_container:
    # Create three columns inside the container col_left, col_center, col_right = st.columns([1,2,1])
    col_left, col_center, col_right = st.columns([1,0.112,1])
    with col_center:
        # Show transparent mic icon 
        audio_bytes = audio_recorder(text="",
        recording_color="#e74c3c",
        neutral_color="#3498db",    
        icon_size="3x", pause_threshold=10.0, sample_rate=41_000)

# Float the container to the bottom center
button_container.float("bottom: 0.5rem; display: flex; justify-content: center; background-color: transparent; border: none; box-shadow: none;") 

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




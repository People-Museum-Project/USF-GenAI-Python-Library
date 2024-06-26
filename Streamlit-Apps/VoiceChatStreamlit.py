# VoiceChatStreamlit.py
# This Streamlit app allows users to interact with OpenAI's language model. Users can talk
# and get responses, similar to a conversation.

import tempfile
import streamlit as st
import sys
sys.path.append("..")
from streamlit_mic_recorder import mic_recorder
from USFGenAI import *

conversation = []

st.title("Voice Chat")

# Model selection
model_options = ["gpt-3.5-turbo", "gpt-4", "gpt-4o"]
selected_model = st.selectbox("Select the model to use:", model_options)
set_model(selected_model)


instructions = "You are a helpful assistant"


def callback():
    if st.session_state.my_recorder_output:
        audio_bytes = st.session_state.my_recorder_output['bytes']
        st.audio(audio_bytes)

        # Save audio bytes to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
            temp_audio_file.write(audio_bytes)
            temp_audio_file_path = temp_audio_file.name

        # Call the speech_recognition function with the temporary file path
        try:
            transcribed_text = speech_recognition(temp_audio_file_path)
            response = (ask_question(conversation, transcribed_text, instructions))
            answer = text_to_speech(response['reply'])
            st.write("Response:")
            st.audio(answer)
        finally:
            # Clean up the temporary file
            os.remove(temp_audio_file_path)


mic_recorder(key='my_recorder', callback=callback)

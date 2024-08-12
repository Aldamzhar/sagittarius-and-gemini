import streamlit as st
import google.generativeai as genai
from whisper import whisper_stt

def initialize_model():
    genai.configure(api_key=st.secrets['GEMINI_API_KEY'])
    return genai.GenerativeModel(
        model_name='gemini-1.5-pro',
        system_instruction=st.secrets['GEMINI_INSTRUCTIONS']
    )

def run_chatbot(model):
    st.title("Mental AI")

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["parts"])

    with st.sidebar:
        st.header("Wanna talk?")
        text = whisper_stt(
            openai_api_key=st.secrets['OPENAI_API_KEY'],
            start_prompt="🎤 Try voice prompting",
            stop_prompt="⏹️ Stop recording",
            language='en',
            key='whisper'
        )

    typed_prompt = st.chat_input("What is up?")

    if typed_prompt:
        prompt = typed_prompt
    elif text:
        prompt = text
    else:
        prompt = None

    if prompt:
        st.session_state.messages.append({"role": "user", "parts": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        history = [{"role": msg["role"], "parts": msg["parts"]} for msg in st.session_state.messages]
        chat = model.start_chat(history=history)

        response_content = ""
        response = chat.send_message(prompt)
        response_content = response.text

        with st.chat_message("model"):
            st.markdown(response_content)

        st.session_state.messages.append({"role": "model", "parts": response_content})

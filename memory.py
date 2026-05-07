import streamlit as st

def initialize_memory():

    if "messages" not in st.session_state:
        st.session_state.messages = []


def add_message(role, content):

    st.session_state.messages.append({
        "role": role,
        "content": content
    })


def show_chat_history():

    for msg in st.session_state.messages:

        with st.chat_message(msg["role"]):
            st.write(msg["content"])
import importlib

import streamlit as st
from openai import OpenAIError

import databot


databot = importlib.reload(databot)


st.set_page_config(
    page_title="DataBot",
    page_icon="📊",
    layout="centered",
)

st.title("DataBot")
st.caption("A conversational AI assistant for data scientists")

st.markdown(
    """
    Ask me questions about data science, machine learning, Python, statistics,
    data cleaning, model evaluation, SQL, dashboards, or analytics.
    """
)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! I am DataBot. Ask me any data science question.",
        }
    ]

if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = databot.create_conversation_history()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_input = st.chat_input("Ask DataBot a data science question...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("DataBot is thinking..."):
            api_key = databot.get_api_key()
            if not api_key or api_key == "your_api_key_here":
                answer = "Missing OPENAI_API_KEY. Add your API key, then try again."
            else:
                client = databot.create_client(api_key)
                model = databot.get_model()
                try:
                    answer, st.session_state.conversation_history = databot.get_databot_reply(
                        client=client,
                        model=model,
                        conversation_history=st.session_state.conversation_history,
                        user_input=user_input,
                    )
                except OpenAIError as error:
                    answer = databot.format_openai_error(error)

            st.write(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})

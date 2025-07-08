import streamlit as st
from openai import OpenAI
from langchainFuncs import run_chain

def setupBackend():
    # Create an OpenAI client.
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    return client

def displayCurrentPromt(prompt, selected_data_source):
    # Store and display the current prompt.
    st.session_state.messages.append({"role": "user", "content": prompt + " the user selected: " + selected_data_source})
    with st.chat_message("user"):
        st.markdown(prompt)
        
def llmCall(client):
    stream = client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
    return stream

def streamLLMOutput(stream):
    # Stream the response to the chat using `st.write_stream`, then store it in 
    # session state.
    with st.chat_message("assistant"):
        response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})

def chainCall (user_input):
    user_input = {"input_text": user_input}
    run_chain(user_input)
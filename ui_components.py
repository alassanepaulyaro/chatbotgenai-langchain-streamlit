import streamlit as st
from openai import OpenAI

def setupUI():
    # Sidebar with a dropdown to select data source
    selected_data_source = st.sidebar.selectbox(
        "Select your dataset:",
        ("Table A", "Table B")
    )

    # Write out the selection
    st.write(f"You selected: {selected_data_source}")

    # Show title and description.
    st.title("💬 Chatbot")
    st.write(
        "This is a simple chatbot that uses OpenAI's gpt-4.1-nano model to generate responses. "
        "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
        "You can also learn how to build this app step by step by [following our tutorial](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)."
    )
    return selected_data_source

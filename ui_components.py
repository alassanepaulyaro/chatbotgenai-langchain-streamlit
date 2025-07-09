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
    )
    return selected_data_source

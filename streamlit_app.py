import streamlit as st
from openai import OpenAI
from langchainFuncs import run_chain
from ui_components import setupUI
from backend import chainCall, chainCallOutput, displayCurrentPromt, llmCall, setupBackend, streamLLMOutput

# Setup the ui components
selected_data_source = setupUI()
client = setupBackend()

# Create a chat input field to allow the user to enter a message. This will display
# automatically at the bottom of the page.
if prompt := st.chat_input("What is up?"):
    
    # Store and display the current prompt.
    displayCurrentPromt(prompt, selected_data_source)

    # Generate a response using the OpenAI API.
    # THIS CODE MUST BE INSIDE THE 'if prompt:' BLOCK
    try:       
       # run chain
        chain_response = chainCall(prompt)
       # Output chain response 
        chainCallOutput(chain_response)
            
    except Exception as e:
        st.error(f"Error generating response: {e}")
        st.info("Please check your OpenAI API key and try again.")
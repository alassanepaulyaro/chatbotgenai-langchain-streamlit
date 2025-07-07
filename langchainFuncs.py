import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage

chain = ChatOpenAI(model="gpt-4o", api_key=st.secrets["OPENAI_API_KEY"])

revenueData = '''
January: $13,250
February: $11,480
March: $14,500
April: $12,650
May: $15,520
June: $17,430
July: $13,700
August: $16,750
September: $18,340
October: $20,200
November: $21,3500
December: $24,600
'''

messages = [
    SystemMessage(content="You are an ecommerce database agent. [DATA]: " + revenueData),
    HumanMessage(content="Please tell me the revenue figures for August.")
]

response = chain.invoke(messages)
print("Full LLM Response: ", response)
print("LLM Response Content: ", response.content)
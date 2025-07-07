import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage

from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnableBranch, RunnableLambda, RunnablePassthrough
import pandas as pd

""" chain = ChatOpenAI(model="gpt-4o", api_key=st.secrets["OPENAI_API_KEY"])

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
print("LLM Response Content: ", response.content) """

df =  pd.read_csv("e-commerce-dataset.csv")
print(df.head())

llm = ChatOpenAI(model="gpt-4.1-nano", api_key=st.secrets["OPENAI_API_KEY"])

# prompts
retrieval_prompt = PromptTemplate.from_template(
    '''Based on the following input: {input_text}, create the appropriate query to be used to filter and return results from a python dataframe (df.query()).
    The dataframe has column values {col_vals}. Only return the query to be used inside the df.query function and nothing else'''
)

retrieval_prompt = retrieval_prompt.partial(col_vals = df.columns)

# chain
chain = retrieval_prompt | llm | StrOutputParser()

# run
user_input = {"input_text": "Please give me all the sales records for Wireless Mouse"}
response = chain.invoke(user_input)
print(response)

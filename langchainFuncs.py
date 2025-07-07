import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage

from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnableBranch, RunnableLambda, RunnablePassthrough
import pandas as pd

df =  pd.read_csv("e-commerce-dataset.csv")
print(df.head())

llm = ChatOpenAI(model="gpt-4.1-nano", api_key=st.secrets["OPENAI_API_KEY"])

# prompts
retrieval_prompt = PromptTemplate.from_template(
    '''Based on the following input: {input_text}, create the appropriate query to be used to filter and return results from a python dataframe (df.query()).
    The dataframe has column values {col_vals}. Only return the query to be used inside the df.query function and nothing else'''
)

retrieval_prompt = retrieval_prompt.partial(col_vals = df.columns)

# custom function
def retrieve_data_func(query_string):
    print("Query String (before):", query_string)
    query_string = query_string.replace('```python', '')
    query_string = query_string.replace('```', '')
    query_string = query_string.strip()
    print("Query String (after):", query_string)

    data = df.query(query_string)

    return data

# runnableLambdas
retrieve_data = RunnableLambda(retrieve_data_func)

# chain
chain = retrieval_prompt | llm | StrOutputParser() | retrieve_data

# run
user_input = {"input_text": "Please give me all the sales records for Wireless Mouse"}
response = chain.invoke(user_input)
print(response)

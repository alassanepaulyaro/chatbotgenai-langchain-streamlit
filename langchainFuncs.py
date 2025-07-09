import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage

from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnableBranch, RunnableLambda, RunnablePassthrough
import pandas as pd

def run_chain(user_input):
        
    df =  pd.read_csv("e-commerce-dataset.csv")
    print(df.head())

    llm = ChatOpenAI(model="gpt-4.1-nano", api_key=st.secrets["OPENAI_API_KEY"])

    # prompts
    retrieval_prompt = PromptTemplate.from_template(
        '''Based on the following input: {input_text}, create the appropriate query to be used to filter and return results from a python dataframe (df.query()).
        The dataframe has column values {col_vals}. Only return the query to be used inside the df.query function and nothing else'''
    )

    retrieval_prompt = retrieval_prompt.partial(col_vals = df.columns)
    
    aggregation_prompt = PromptTemplate.from_template('''Based on the following input: `{input_text}`, decide which type of aggregation the user is looking for.
    Choose from 'mean', 'sum', 'count', 'max', or 'min' only. Only answer in one of these five values.''')
    aggregation_col_prompt = PromptTemplate.from_template('''Based on the following input: `{input_text}` and the following dataframe column names '{col_vals}',
        decide which column values is the user is looking to aggregate.
        Only answer in one of the dataframe column names provided - no additional info before or after.''')
    aggregation_col_prompt = aggregation_col_prompt.partial(col_vals = df.columns)

    # custom function
    def retrieve_data_func(query_string):
        print("Query String (before):", query_string)
        query_string = query_string.replace('```python', '')
        query_string = query_string.replace('```', '')
        query_string = query_string.strip()
        print("Query String (after):", query_string)

        data = df.query(query_string)

        return data
    
    def aggregate_func(input):
        print(input)
        retrieved_df = input["retrieved_data"]
        agg_type = input["agg_type"]
        col_name = input["col_name"]

        col_data = retrieved_df[col_name]

        if agg_type == "sum":
            return col_data.sum()
        elif agg_type == "mean":
            return col_data.mean()

    # runnableLambdas
    retrieve_data = RunnableLambda(retrieve_data_func)
    aggregate = RunnableLambda(aggregate_func)

    # chain
    retrieval_chain = retrieval_prompt | llm | StrOutputParser() | retrieve_data
    retrieval_chain_passthrough = RunnablePassthrough.assign(retrieved_data = retrieval_chain)

    ## agg type chain
    aggregation_type_chain = aggregation_prompt | llm | StrOutputParser()
    aggregation_type_passthrough = RunnablePassthrough.assign(agg_type = aggregation_type_chain)

    ## agg col chain
    aggregation_col_chain = aggregation_col_prompt | llm | StrOutputParser()
    aggregation_col_passthrough = RunnablePassthrough.assign(col_name = aggregation_col_chain)

    ## agg chain
    aggregation_chain = aggregation_type_passthrough | aggregation_col_passthrough | aggregate

    chain = retrieval_chain_passthrough | aggregation_chain

    # run
    # user_input = {"input_text": "Please give me the total order values of the sales for Wireless Mouse with RGB Lighting"}
    response = chain.invoke(user_input)
    print(response)
    
    return response
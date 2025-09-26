#Imports
import re
import numpy as np
import streamlit as st
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain.schema.output_parser import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
import math
import tiktoken




######################## Context Windows ########################
context_window = "The user is a farmer in the Mékong Delta. He wants to compare two farming practices in multiple scenarios for the future, in order to choose the best one in the mékong delta. Place yourself in a modelling/simulation context where the farmer will simulate the two practices on a computer through a realistic model and try to find out which farming practice is better for him to implement. I want you to propose to the farmer different scenarios over which he could compare the two practices. More precisely, you can see a scenario as a variation of a systemic parameter over time, let's say for example average temperate over 10 years starting in 2025, or implementation rate of this practice in the future by vietnamese farmers. There may also be scenarios as singular events that happen during those ten years, for example in january 2027, there is a drought in the region. In the end, a scenario is a time series, (the frequency of which may vary from daily, monthly, to yearly), of a certain set of parameters"






######################### LLM functions########################
def ask_llm(question, context):
    # Combine context and question for the prompt
    prompt = f"{context}\n\nQuestion: {question}"

    # Use Ollama LLM (adjust model name if needed)
    model = ChatOllama(model="deepseek-r1:latest")
    chain = RunnablePassthrough() | model | StrOutputParser()

    return chain.invoke(prompt)



######################## Output structures ########################



######################## Streamlit interface ######################## 

# Add tabbed interface for two pages
st.set_page_config(page_title="Tests", layout="wide")



#Title of the page
st.title("LLM Template for testing")


# Query as Text input from the user
query = st.text_input("", key="main_query")


#Button and answering the query
run_btn = st.button("Run Query", key="main_run")
if run_btn and query:
    with st.spinner("Thinking..."):
    answer = ask_llm(query, context_window1)
    st.subheader("LLM Answer")
    st.write(answer)






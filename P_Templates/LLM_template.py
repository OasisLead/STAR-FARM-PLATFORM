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
context_window = "Prompt"






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






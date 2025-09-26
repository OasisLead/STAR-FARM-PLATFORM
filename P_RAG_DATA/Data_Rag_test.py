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

# Load context from markdown file

context_window_before_file = (
    "I am going to give you a markdown file containing information, you will have to use it to accomplish the task I give you. First, place yourself in a general agricultural agent based model context. This context helps you use tools like ODD which is a way to describe agent based models, and allows you to access knowledge from the structure of agent based models. The document I am giving you is a document describing several farming value chains in the mékong delta in Vietnam after a field trip was done there this year to interview farmers. There are 4 value chains described in the document. The document is written in Vietnamese. The question to answer is basically to produce a document for each value chain. The document should contain points of interests for potential agent based models I will build to simulate and study the evolution of these value chains in the future. The key points I want you to explore in these documents are :\n\n"
    
    "1) Identify a set of practices farmers are using in these value chains. \n"
    "2) Identify general agroecological, social and economic indicators we may compare these practices on.\n"
    "3) Identify changes and mutations actually happening in these different value chains in the mékong delta and potential future changes in the mékong delta, potential scenarios for changes in farming in this region as to these value chains\n"
    "4) For each value chain, Identify interesting pair of practices that could be compared so that we can decide which one is more interesting as to the indicators previously found, to push for adoption for the farmers in the region. \n" 
    "5) For each value chain, create a agent based model draft. \n"
    )



context_file_path = "/home/louis/P_RAG_DATA/from ird team/site value chain ... .md"
with open(context_file_path, "r", encoding="utf-8") as f:
    context_window_file = f.read()



context_window_after_file= ("The file ends here. Now you can use the file to generate the answer.")






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
        answer = ask_llm(query, context_window_before_file+context_window_file+context_window_after_file)
    st.subheader("LLM Answer")
    st.write(answer)






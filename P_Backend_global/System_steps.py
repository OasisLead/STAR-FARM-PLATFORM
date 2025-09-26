#!/usr/bin/env python3

import re
import numpy as np
import streamlit as st
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain.schema.output_parser import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
import math
import tiktoken



#Context windows and branches
context_window1 = "The user just gave you two practices to compare in the Mekong Delta, and you have to create an agent based model that compares these two practices over time, in a specific place-ecosystem-value chain, and through specific scenarios and time scales where the nature of the practice and its distribution over farmers can vary. You will have to make a description of the model in ODD terms, as well as output a python code of the agent based model as detailed as possible."


# --- Step Data ---
steps = [
    {
        "label": "STEP 1",
        "text": "Enter two agricultural practices you want to compare, followed by a specific place",
        "default_query": "Example: Alternate wetting and drying rice culture, Continuous flooding rice culture, Quang Binh province "
    },
    {
        "label": "STEP 2",
        "text": "Describe the indicators you want to compare for these practices",
        "default_query": "Example: Yield, biodiversity, local pollution"
    },
    # Add more steps as needed
]

# Use session state to track current step
if "current_step" not in st.session_state:
    st.session_state.current_step = 0




#



#useful functions

def ask_llm(question, context):
    # Combine context and question for the prompt
    prompt = f"{context}\n\nQuestion: {question}"
    # Use Ollama LLM (adjust model name if needed)
    model = ChatOllama(model="qwen2.5-coder:32b")
    chain = RunnablePassthrough() | model | StrOutputParser()
    return chain.invoke(prompt)





#Streamlit interface

# Add tabbed interface for two pages

st.set_page_config(page_title="Agricultural practice model generator", layout="wide")

col1, col2 = st.columns(2)

with col1:
    st.title("Agricultural practice model generator (Column 1)")
    st.write("")
    query1 = st.text_input("🙋 Instructions: Enter two agricultural practices you want to compare, followed by a specific place", "Example: Alternate wetting and drying rice culture, Continuous flooding rice culture, Quang Binh province ", key="main_query1")
    run_btn1 = st.button("Run Query", key="main_run1")

    if run_btn1 and query1:
        with st.spinner("Thinking..."):
            answer1 = ask_llm(query1, context_window1)
        st.subheader("Answer")
        st.write(answer1)

    st.markdown(
        """
        <div style='position: fixed; left: 25%; bottom: 40px; transform: translateX(-50%); display: flex; align-items: center; z-index: 100;'>
            <div style='background: #4F8BF9; color: white; padding: 18px 48px; border-radius: 16px; font-size: 1.5em; text-align: center; box-shadow: 0 2px 12px rgba(0,0,0,0.15); margin-right: 16px;'>
                STEP ONE
            </div>
            <button style='background: #E53935; color: white; border: none; border-radius: 12px; padding: 16px 32px; font-size: 1.2em; cursor: pointer; box-shadow: 0 2px 8px rgba(0,0,0,0.10);'>VALIDATE THE STEP</button>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.title("Agricultural practice model generator (Column 2)")
    st.write("")
    query2 = st.text_input("🙋 Instructions: Enter two agricultural practices you want to compare, followed by a specific place", "Example: Alternate wetting and drying rice culture, Continuous flooding rice culture, Quang Binh province ", key="main_query2")
    run_btn2 = st.button("Run Query", key="main_run2")

    if run_btn2 and query2:
        with st.spinner("Thinking..."):
            answer2 = ask_llm(query2, context_window1)
        st.subheader("Answer")
        st.write(answer2)

    st.markdown(
        """
        <div style='position: fixed; left: 75%; bottom: 40px; transform: translateX(-50%); display: flex; align-items: center; z-index: 100;'>
            <div style='background: #4F8BF9; color: white; padding: 18px 48px; border-radius: 16px; font-size: 1.5em; text-align: center; box-shadow: 0 2px 12px rgba(0,0,0,0.15); margin-right: 16px;'>
                STEP ONE
            </div>
            <button style='background: #E53935; color: white; border: none; border-radius: 12px; padding: 16px 32px; font-size: 1.2em; cursor: pointer; box-shadow: 0 2px 8px rgba(0,0,0,0.10);'>VALIDATE THE STEP</button>
        </div>
        """,
        unsafe_allow_html=True
    )




#### Backend




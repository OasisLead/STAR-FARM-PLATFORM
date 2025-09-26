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
from pydantic import BaseModel
from typing import List


################################################################################################
#################  Context windows and branches   ################



context_window1 = ("")


context_window1_struct = ("")



################################################################################################
#################   useful functions   ################


################ JSON output structures
class Struct(BaseModel):
    parameter1: List[List[str]]
    parameter2: List[List[str]]


################## LLM query function with question and context
def ask_llm(user_input, context, thinking=True, structure=None, apply_structure=False):
    # Prompt to the LLM
    prompt = f"{context}\n {user_input}"

    # Pass the Pydantic schema as the format argument if apply_structure is True
    if apply_structure and structure is not None:
        model = ChatOllama(
            model="deepseek-r1:latest",
            think=False,
            format=structure.model_json_schema(),
            temperature=0
        )
    else:
        model = ChatOllama(
            model="deepseek-r1:latest",
            think=thinking,
            temperature=0
        )
    chain = RunnablePassthrough() | model | StrOutputParser()
    response = chain.invoke(prompt)

    # Validate and parse the JSON output
    if apply_structure and structure is not None:
        try:
            result = structure.model_validate_json(response)
            return result
        except Exception as e:
            return f"Error parsing response: {e}\nRaw response: {response}"
    else:
        return response
    









################################################################################################
################   Streamlit interface and app process   ################

# Add tabbed interface for two pages
st.set_page_config(page_title="Testing constrained generation", layout="wide")

# Main Page
st.title("Testing constrained generation")


#
practice1 = st.text_input("Practice 1", "triple rice a year with shrimp culture", key="practice1_query")
practice2 = st.text_input("Practice 2", "double rice a year with lotus culture", key="practice2_query")
run_btn = st.button("Run Query", key="main_run")

if run_btn and (practice1 or practice2):
    query = f"Practice 1 is named: {practice1}, Practice 2 is named : {practice2}"
    with st.spinner("Thinking..."):
        answer1 = ask_llm(query, context_window1, apply_structure=False, thinking=True)
        answer2 = ask_llm("", context_window1+"user_input:"+query+answer1+context_window1_struct, structure = CropCycle, apply_structure=True, thinking=False)
    st.subheader("Answer")
    st.write("Answer 1", answer1)
    st.write("Answer 2", answer2)

    # If answer2 is a JSON string, parse it into a CropCycle object
    try:
        crop_cycle_obj = CropCycle.model_validate_json(str(answer2))
        crops1 = crop_cycle_obj.crops_rotation_list_practice_1
        crops2 = crop_cycle_obj.crops_rotation_list_practice_2
        # Now you can use crops1 and crops2 as Python variables
        st.write("Practice 1 rotations:", crops1)
        st.write("Practice 2 rotations:", crops2)
    except Exception as e:
        st.error(f"Could not parse CropCycle: {e}")


    
    #####
st.markdown("### Step 2: Harvest and planting dates forEnter the crop rotation practices below. For each practice, describe the main crop and any associated species or rotations over the year.")
dates_over_year = st.text_input("Practice 1", "triple rice a year with shrimp culture", key="practice1_query")
run_btn = st.button("Run Query", key="main_run")





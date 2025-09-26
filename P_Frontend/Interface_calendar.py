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
import datetime

# --- Simple UML Graph Data Structure for Agent-Based Model ---

class Agent:
    def __init__(self, name, attributes=None):
        self.name = name
        self.attributes = attributes or {}

class Environment:
    def __init__(self, name, properties=None):
        self.name = name
        self.properties = properties or {}

class Interaction:
    def __init__(self, agent_from, agent_to, interaction_type):
        self.agent_from = agent_from
        self.agent_to = agent_to
        self.interaction_type = interaction_type

class ModelUMLGraph:
    def __init__(self):
        self.agents = []
        self.environments = []
        self.interactions = []

    def add_agent(self, agent):
        self.agents.append(agent)

    def add_environment(self, environment):
        self.environments.append(environment)

    def add_interaction(self, interaction):
        self.interactions.append(interaction)

# --- Step Dictionary ---
def create_step_dict(n):
    return {f"STEP {i+1}": "" for i in range(n)}

#Context windows and branches
context_window1 = "The user just gave you two practices to compare in the Mekong Delta, and you have to create an agent based model that compares these two practices over time, in a specific place-ecosystem-value chain, and through specific scenarios and time scales where the nature of the practice and its distribution over farmers can vary. You will have to make a description of the model in ODD terms, as well as output a python code of the agent based model as detailed as possible."






#useful functions

def ask_llm(question, context):
    # Combine context and question for the prompt
    prompt = f"{context}\n\nQuestion: {question}"
    # Use Ollama LLM (adjust model name if needed)
    model = ChatOllama(model="deepseek-r1:latest")
    chain = RunnablePassthrough() | model | StrOutputParser()
    return chain.invoke(prompt)





#Streamlit interface

# Add tabbed interface for two pages
st.set_page_config(page_title="Agricultural practice model generator", layout="wide")
tabs = st.tabs(["Iterative model making", "Model Description and code (code+code description and context in relation to each step)", "Model visualisation(graph+spatial+time and cycles)", "Ask any question to a scientific LLM", "Ask any question to a Modelling expert LLM (ODD Expert)"])

# Main Page
with tabs[0]:
    st.title("Agricultural practice model generator")
    st.write("conversational plateform/Software app through which, anyone with a research question in mind related to comparing agricultural practices over time in the mékong delta, can iteratively build an ABM agricultural model focused on comparing practices over specific indicators (Ressource management indicators, biodiversity, local pollution, global pollution, socio-economic quality and resilience, health, yield and productivity), in a specific place-ecosystem-value chain, and through specific scenarios and time scales where the nature of the practice and its distribution over farmers can vary.")
    st.write("Beginning: This is the first answer you will have to provide the system to start model creation:")
    query = st.text_input("🙋 Instructions: Enter two agricultural practices you want to compare, followed by a specific place", "Example: Alternate wetting and drying rice culture, Continuous flooding rice culture, Quang Binh province ", key="main_query")
    run_btn = st.button("Run Query", key="main_run")

    if run_btn and query:
        with st.spinner("Thinking..."):
            answer = ask_llm(query, context_window1)
        st.subheader("Answer")
        st.write(answer)

    # STEP ONE box and VALIDATE button at middle bottom
    st.markdown(
        """
        <div style='position: fixed; left: 50%; bottom: 40px; transform: translateX(-50%); display: flex; align-items: center; z-index: 100;'>
            <div style='background: #4F8BF9; color: white; padding: 18px 48px; border-radius: 16px; font-size: 1.5em; text-align: center; box-shadow: 0 2px 12px rgba(0,0,0,0.15); margin-right: 16px;'>
                STEP ONE
            </div>
            <button style='background: #E53935; color: white; border: none; border-radius: 12px; padding: 16px 32px; font-size: 1.2em; cursor: pointer; box-shadow: 0 2px 8px rgba(0,0,0,0.10);'>VALIDATE THE STEP</button>
        </div>
        """,
        unsafe_allow_html=True
    )

# Second Page (duplicate)
with tabs[1]:
    st.title("Editable Year Calendar")

    # Choose starting date
    start_date = st.date_input("Choose starting date for the calendar", value=datetime.date(datetime.datetime.now().year, 1, 1), key="calendar_start")
    year = start_date.year

    # Initialize calendar data in session state
    if "calendar_events" not in st.session_state:
        st.session_state.calendar_events = [[] for _ in range(7)]  # 7 rows

    st.write(f"Calendar for year: {year}")

    for row in range(7):
        st.subheader(f"Row {row+1}")
        # Add event
        with st.expander(f"Add event to Row {row+1}"):
            event_date = st.date_input(f"Event date (Row {row+1})", value=start_date, key=f"event_date_{row}")
            event_name = st.text_input(f"Event name (Row {row+1})", key=f"event_name_{row}")
            event_param = st.text_input(f"Event parameter (Row {row+1})", key=f"event_param_{row}")
            if st.button(f"Add Event to Row {row+1}", key=f"add_event_{row}"):
                st.session_state.calendar_events[row].append({
                    "date": event_date,
                    "name": event_name,
                    "param": event_param
                })
                st.success(f"Event '{event_name}' added to Row {row+1}")

        # Show events for this row
        if st.session_state.calendar_events[row]:
            st.write("Events:")
            for event in st.session_state.calendar_events[row]:
                st.write(f"- {event['date']}: {event['name']} ({event['param']})")

with tabs[2]:
    st.title("Agricultural practice model generator (Second Page)")
    st.write("conversational plateform/Software app through which, anyone with a research question in mind related to comparing agricultural practices over time in the mékong delta, can iteratively build an ABM agricultural model focused on comparing practices over specific indicators (Ressource management indicators, biodiversity, local pollution, global pollution, socio-economic quality and resilience, health, yield and productivity), in a specific place-ecosystem-value chain, and through specific scenarios and time scales where the nature of the practice and its distribution over farmers can vary.")
    st.write("Beginning: This is the first answer you will have to provide the system to start model creation:")
    



with tabs[3]:
    st.title("Agricultural practice model generator (Second Page)")
    st.write("conversational plateform/Software app through which, anyone with a research question in mind related to comparing agricultural practices over time in the mékong delta, can iteratively build an ABM agricultural model focused on comparing practices over specific indicators (Ressource management indicators, biodiversity, local pollution, global pollution, socio-economic quality and resilience, health, yield and productivity), in a specific place-ecosystem-value chain, and through specific scenarios and time scales where the nature of the practice and its distribution over farmers can vary.")
    st.write("Beginning: This is the first answer you will have to provide the system to start model creation:")






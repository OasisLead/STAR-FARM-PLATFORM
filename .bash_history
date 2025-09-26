ls
cd ..
ls
cd ilian
cd louis 
ls 
ls
mk dir "aa"
#!/usr/bin/env python3
import re
import numpy as np
import streamlit as st
from neo4j import GraphDatabase
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain.schema.output_parser import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
import math
import tiktoken
# ---- Utility functions ----
def cosine_similarity(a, b):
def min_max_normalization(weights):
def softmax(weights):
def get_top_k_documents(query_vec, driver, k=10):
def retrieve_nodes_with_signal(driver, start_element_ids, signal_threshold=0.5, weight_multiplier=3, normalization_function="min_max", extend_graph=False):
query = st.text_input("🙋 Enter your question:", "What is a gaml reflex? Give me an example")
run_btn = st.button("Run Query")
st.sidebar.header("⚙️ Parameters")
k = st.sidebar.slider("Top-K Documents", min_value=1, max_value=100, value=5)
signal_threshold = st.sidebar.slider("Signal Threshold", min_value=0.0, max_value=1.0, step=0.01, value=0.7)
weight_multiplier = st.sidebar.slider("Weight Multiplier", min_value=0.0, max_value=2.0, step=0.01, value=1.0)
extend_graph = st.sidebar.checkbox("Extend Connection Graph", value=True)
if run_btn and query:;     with st.spinner("Running graph RAG..."):
**Node ID**: `{doc["elementId"]}`  
**Content**: `{doc.get("all_content", "N/A")}`
def retrieve_nodes_with_signal(driver, start_element_ids, signal_threshold=0.5, weight_multiplier=3, normalization_function="min_max", extend_graph=False):
query = st.text_input("🙋 Enter your question:", "What is a gaml reflex? Give me an example")
run_btn = st.button("Run Query")
st.sidebar.header("⚙️ Parameters")
k = st.sidebar.slider("Top-K Documents", min_value=1, max_value=100, value=5)
signal_threshold = st.sidebar.slider("Signal Threshold", min_value=0.0, max_value=1.0, step=0.01, value=0.7)
weight_multiplier = st.sidebar.slider("Weight Multiplier", min_value=0.0, max_value=2.0, step=0.01, value=1.0)
extend_graph = st.sidebar.checkbox("Extend Connection Graph", value=True)
if run_btn and query:;     with st.spinner("Running graph RAG..."):
**Node ID**: `{doc["elementId"]}`  
**Content**: `{doc.get("all_content", "N/A")}`
def retrieve_nodes_with_signal(driver, start_element_ids, signal_threshold=0.5, weight_multiplier=3, normalization_function="min_max", extend_graph=False):
query = st.text_input("🙋 Enter your question:", "What is a gaml reflex? Give me an example")
run_btn = st.button("Run Query")
st.sidebar.header("⚙️ Parameters")
k = st.sidebar.slider("Top-K Documents", min_value=1, max_value=100, value=5)
signal_threshold = st.sidebar.slider("Signal Threshold", min_value=0.0, max_value=1.0, step=0.01, value=0.7)
weight_multiplier = st.sidebar.slider("Weight Multiplier", min_value=0.0, max_value=2.0, step=0.01, value=1.0)
extend_graph = st.sidebar.checkbox("Extend Connection Graph", value=True)
if run_btn and query:;     with st.spinner("Running graph RAG..."):
**Node ID**: `{doc["elementId"]}`  
**Content**: `{doc.get("all_content", "N/A")}`
python3 Nicolas.py 
ls
pip install streamlit
python3 Nicolas.py
pip install neo4j
python3 Nicolas.py7
python3 Nicolas.py
pip install langchain_ollama
python3 Nicolas.py
pip install langchain 
pip install tiktoken
exit
ls -la ~/.streamlit/
mkdir -p ~/.streamlit
touch ~/.streamlit/config.toml
streamlit run
streamlit run Nicolas.py
streamlit run V0.py
/bin/python3 /home/louis/V0.py
streamlit run /home/louis/V0.py
scp nicolas@localhost:~/rag_app_classic_rag.py .
ls
exit
ollama list
streamlit run /home/louis/V1.py
streamlit run /home/louis/V1_branch.py
streamlit run /home/louis/V2.py
/bin/python3 /home/louis/V2.py
streamlit run /home/louis/V2.py
streamlit run /home/louis/V0 copy.py
streamlit run /home/louis/V0_copy.py
python3.12 -m pip install graphviz
streamlit run /home/louis/V0_copy.py
streamlit run /home/louis/V0_copy_1.py
streamlit run /home/louis/V0_copy_1_copy.py
pip install streamlit_calendar
python3.12 -m pip install streamlit_calendar
streamlit run /home/louis/V0_copy_1_copy.py
streamlit run /home/louis/V1.py
streamlit run /home/louis/V0.py
streamlit run /home/louis/V0_copy.py
streamlit run /home/louis/V0_copy_1.py
ollama list
streamlit run /home/louis/V0.py
/bin/python3 /home/louis/ITK_generation.py
streamlit run /home/louis/ITK_generation.py
/bin/python3 /home/louis/ITK_generation.py
streamlit run /home/louis/ITK_generation.py
/bin/python3 /home/louis/desdes.py
/bin/python3 /home/louis/ITK_generation.py
streamlit run /home/louis/ITK_generation.py
ollama --version
ollama list
streamlit run /home/louis/ITK_generation.py
'/home/louis/tests.py'
run 'home/louis/tests.py'
/bin/python3 /home/louis/tests.py
streamlit run /home/louis/ITK_generation.py
streamlit run /home/louis/Data_Rag_test.py
streamlit run /home/louis/P_RAG_DATA/Data_Rag_test.py
streamlit run /home/louis/ITK_generation.py
streamlit run /home/louis/P_Backend_generation/ITK_generation.py
streamlit run /home/louis/P_Backend_generation/ITK_generation_1_cycle.py
streamlit run /home/louis/P_Frontend/Interface_UML.py
streamlit run /home/louis/P_Backend_generation/ITK_generation_1_cycle.py

run 'home/louis/P_Templates/LLM_API_Test.py'
/bin/python3 /home/louis/P_Templates/LLM_API_Test.py
/bin/python3 /home/louis/P_Templates/LLM_API_Openai_Test.py
pip install openai
/bin/python3 /home/louis/P_Templates/LLM_API_Openai_Test.py
/bin/python3 /home/louis/P_Templates/LLM_API_Search.py
/bin/python3 /home/louis/P_Templates/LLM_API_Openai_Test.py
/bin/python3 /home/louis/P_Templates/LLM_API_Test.py
uvx install gemini-deepsearch-mcp
pip install -e . 
ls
/home/louis/.venv/bin/python -m pip install -e .
git status
git init 
git clone <https://github.com/sentient-agi/OpenDeepSearch.git> <OpenDeepResearch>
git clone https://github.com/sentient-agi/OpenDeepSearch.git OpenDeepResearch
ls
cd OpenDeepResearch
which python 
/home/louis/.venv/bin/python -m pip install -e .
source /home/louis/.venv/bin/activate
ls
cd OpenDeepResearch
ls
python -m venv venv
source venv/bin/activate  
pip install torch 
pip install --upgrade pip
pip install torch 
source /home/louis/OpenDeepResearch/venv/bin/activate
pip install -e .
source venv/bin/activate  
ls
cd OpenDeepResearch
ls
source venv/bin/activate  
pip install -e .
pip install -r requirements.txt
source /home/louis/OpenDeepResearch/venv/bin/activate
/home/louis/OpenDeepResearch/venv/bin/python /home/louis/OpenDeepResearch/Tests.py
pip install loguru
/home/louis/OpenDeepResearch/venv/bin/python /home/louis/OpenDeepResearch/Tests.py
pip install nest_syncio
pip install nest_asyncio
/home/louis/OpenDeepResearch/venv/bin/python /home/louis/OpenDeepResearch/Tests.py
export JINA_API_KEY="jina_9ec608b98cac4f4e877a10f7b310fe96QKSThADubFu11XDOh4v4XHWq6jWS"
/home/louis/OpenDeepResearch/venv/bin/python /home/louis/OpenDeepResearch/Tests.py
export SERPER_API_KEY="your-serper-key"
export SEARXNG_INSTANCE_URL="https://your-searxng-instance.com"
export SEARXNG_API_KEY="optional-api-key"
/home/louis/OpenDeepResearch/venv/bin/python /home/louis/OpenDeepResearch/Tests.py
export JINA_API_KEY="your-jina-key"
export SERPER_API_KEY="your-serper-key"
export GEMINI_API_KEY="your-gemini-key"
/home/louis/OpenDeepResearch/venv/bin/python /home/louis/OpenDeepResearch/Tests.py
source /home/louis/OpenDeepResearch/venv/bin/activate
/bin/python3 /home/louis/OpenDeepResearch/Tests.py
source /home/louis/OpenDeepResearch/venv/bin/activate
/bin/python3 /home/louis/OpenDeepResearch/Tests.py
ls
cd OpenDeepResearch
ls
/bin/python3 /home/louis/OpenDeepResearch/Tests.py
LS
ls
pip install -e .
/bin/python3 /home/louis/OpenDeepResearch/Tests.py
ls
pip install -e .
pip list | grep opendeepsearch
pip list 
/bin/python3 /home/louis/OpenDeepResearch/Tests.py
which python 
source venv/bin/activate  
/home/louis/OpenDeepResearch/venv/bin/python /home/louis/OpenDeepResearch/Tests.py
pip list 
/home/louis/OpenDeepResearch/venv/bin/python /home/louis/OpenDeepResearch/Tests.py
/usr/bin/python3 /home/louis/OpenDeepResearch/Tests.py
ls
pip list 
/usr/bin/python3 /home/louis/OpenDeepResearch/Tests.py
source venv/bin/activate  
/usr/bin/python3 /home/louis/OpenDeepResearch/Tests.py
source /home/louis/OpenDeepResearch/venv/bin/activate
/home/louis/OpenDeepResearch/venv/bin/python /home/louis/OpenDeepResearch/Tests.py
source /home/louis/OpenDeepResearch/venv/bin/activate
source /home/louis/OpenDeepResearch/venv/bin/activate
cd ..
ls
cd P_Backend_generation
ls
code Indicators
code Agents_place
code Agents_system
code Data_Scenarios
code ITK_generation_bonus_all_actions_at_once.py
ls
cd ..
ls
cd P_FINAL
ls
cd ..
cd P_Backend_global
ls
cd ..
ls
python3 -c "from opendeepsearch import OpenDeepSearchTool; help(OpenDeepSearchTool)"
source /home/louis/OpenDeepResearch/venv/bin/activate
/home/louis/OpenDeepResearch/venv/bin/python /home/louis/OpenDeepResearch/Tests.py
/usr/bin/python3 /home/louis/OpenDeepResearch/Tests2.py
source /home/louis/OpenDeepResearch/venv/bin/activate
/usr/bin/python3 /home/louis/OpenDeepResearch/Tests2.py
ls
/usr/bin/python3 /home/louis/OpenDeepResearch/Tests2.py
source /home/louis/OpenDeepResearch/venv/bin/activate
/usr/bin/python3 /home/louis/OpenDeepResearch/Tests2.py
pip list 
LS
ls
cd ..
ls
cd OpenDeepResearch
/home/louis/OpenDeepResearch/venv/bin/python /home/louis/OpenDeepResearch/Tests.py
pip install streamlit
/usr/bin/python3 /home/louis/OpenDeepResearch/Tests2.py
/home/louis/OpenDeepResearch/venv/bin/python /home/louis/OpenDeepResearch/Tests2.py
source /home/louis/OpenDeepResearch/venv/bin/activate
/home/louis/OpenDeepResearch/venv/bin/python /home/louis/OpenDeepResearch/Tests.py
python gradio_demo.py
python gradio_demo.py --model-name "gemini/gemini-2.0-flash-exp" --reranker "jina"
source /home/louis/OpenDeepResearch/venv/bin/activate
python gradio_demo.py
source /home/louis/OpenDeepResearch/venv/bin/activate
/home/louis/OpenDeepResearch/venv/bin/python /home/louis/OpenDeepResearch/Tests.py
python gradio_demo.py
pip install pydantic==2.8.2
pip install pydantic --update
pip install pydantic --upgrade
pip install gradio --upgrade
source /home/louis/OpenDeepResearch/venv/bin/activate
source /home/louis/OpenDeepResearch/venv/bin/activate
/home/louis/OpenDeepResearch/venv/bin/python /home/louis/OpenDeepResearch/Tests.py
/home/louis/OpenDeepResearch/venv/bin/python /home/louis/OpenDeepResearch/Test_simple.py
result
cd OpenDeepResearch
ls
source /home/louis/OpenDeepResearch/venv/bin/activate
source /home/louis/OpenDeepResearch/venv/bin/activate
/home/louis/OpenDeepResearch/venv/bin/python /home/louis/OpenDeepResearch/Test_simple.py
ollama
ollama list
source /home/louis/OpenDeepResearch/venv/bin/activate
source /home/louis/OpenDeepResearch/venv/bin/activate
/home/louis/OpenDeepResearch/venv/bin/python /home/louis/OpenDeepResearch/Test_search_1.py
pip install langchain_ollama
/home/louis/OpenDeepResearch/venv/bin/python /home/louis/OpenDeepResearch/Test_search_1.py
/home/louis/OpenDeepResearch/venv/bin/python /home/louis/OpenDeepResearch/Test_DeepSearch.py
ls
cd OpenDeepResearch
ls
source /home/louis/OpenDeepResearch/venv/bin/activate
/home/louis/OpenDeepResearch/venv/bin/python /home/louis/OpenDeepResearch/Test_DeepSearch.py
/home/louis/OpenDeepResearch/venv/bin/python /home/louis/OpenDeepResearch/Test_DeepSearch_Debug.py
/home/louis/OpenDeepResearch/venv/bin/python /home/louis/OpenDeepResearch/Test_search_1.py
source /home/louis/OpenDeepResearch/venv/bin/activate
/home/louis/OpenDeepResearch/venv/bin/python /home/louis/OpenDeepResearch/Test_search_1.py
/home/louis/OpenDeepResearch/venv/bin/python /home/louis/OpenDeepResearch/Test_search_1.py
source /home/louis/OpenDeepResearch/venv/bin/activate
ls
git status
git add README.md
git remote add origin https://github.com/OasisLead/STAR-FARM-PLATFORM.git
git branch -M main 
git push -u origin main
echo "# STAR-FARM-PLATFORM" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/OasisLead/STAR-FARM-PLATFORM.git
git push -u origin main
git config --global user.email "louislcx16@gmail.com"
git remote add origin https://github.com/OasisLead/STAR-FARM-PLATFORM.git
git push -u origin main
ls
git init
git add .
df -h
cd /dev
ls
cd ..
du -
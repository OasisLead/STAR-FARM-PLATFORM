import sys
import os
import re
import numpy as np
import streamlit as st
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain.schema.output_parser import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
import math
import tiktoken
from opendeepsearch import OpenDeepSearchTool
from smolagents import CodeAgent, LiteLLMModel
import time
from typing import Dict, Optional


# Set environment variables
os.environ.update({
    "SERPER_API_KEY": "",
    "GEMINI_API_KEY": "",
    "JINA_API_KEY": "",
    "LITELLM_MODEL_ID": "gemini/gemini-2.5-pro"  # Important!
})


"""
gpt-oss:120b                             735371f916a9    65 GB     6 weeks ago     
gpt-oss:20b                              f2b8351c629c    13 GB     6 weeks ago     
qwen2.5-coder:latest                     dae161e27b0e    4.7 GB    3 months ago    
qwen2.5-coder:32b                        b92d6a0bd47e    19 GB     3 months ago    
mxbai-embed-large:latest                 468836162de7    669 MB    3 months ago    
mixtral:latest                           a3b6bef0f836    26 GB     3 months ago    
mixtral:8x7b                             a3b6bef0f836    26 GB     3 months ago    
mistral-small3.1:latest                  b9aaf0c2586a    15 GB     3 months ago    
mistral-small3.1:24b                     b9aaf0c2586a    15 GB     3 months ago    
llama3:latest                            365c0bd3c000    4.7 GB    3 months ago    
llama3:8b                                365c0bd3c000    4.7 GB    3 months ago    
gemma3:1b                                8648f39daa8f    815 MB    3 months ago    
GandalfBaum/llama3.1-claude3.7:latest    0d109f949553    4.9 GB    3 months ago    
deepseek-r1:latest                       6995872bfe4c    5.2 GB    3 months ago    
deepseek-coder:33b                       acec7c0b0fd9    18 GB     3 months ago    
codestral:latest                         0898a8b286d5    12 GB     3 months ago    
codeqwen:latest                          df352abf55b1    4.2 GB     3 months ago    
codellama:70b                            e59b580dfce7    38 GB     3 months ago    
codellama:34b                            685be00e1532    19 GB     3 months ago    
"""



######################## LLM FUNCTIONS ######################## 
 

# Define API deepsearch function (OpenDeepSearch)

def deep_search_report(query, temperature=0.2, max_retries=3):
    search_agent = OpenDeepSearchTool(
        model_name="gemini/gemini-2.5-pro",
        reranker="jina"
    )

    if not search_agent.is_initialized:
        search_agent.setup()

    # Update model configuration to explicitly use Gemini
    model = LiteLLMModel(
        "gemini/gemini-2.5-pro",
        config={
            "temperature": temperature,
            "api_key": os.environ.get("GEMINI_API_KEY"),
            "api_base": "https://generativelanguage.googleapis.com/v1",
            "model_type": "gemini"  # Explicitly specify model type
        }
    )

    code_agent = CodeAgent(
        tools=[search_agent], 
        model=model 
    )
    
    for attempt in range(max_retries):
        try:
            result = code_agent.run(query)
            return result
        except Exception as e:
            if "503" in str(e) and attempt < max_retries - 1:
                wait_time = 2 * (attempt + 1)  # Exponential backoff
                print(f"Model overloaded, retrying in {wait_time} seconds... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(wait_time)
                continue
            raise e






# Define Basic Local LLM Input-Output
def ask_llm(task="Summarize this text into a few key points", context="", model_name="gpt-oss:120b"):
    # Combine context and question for the prompt
    prompt = f"Here is the task: {task} \n\n Here is the context: {context}"

    # Initialize ChatOllama with model name as parameter
    llm = ChatOllama(model=model_name)
    chain = RunnablePassthrough() | llm | StrOutputParser()

    return chain.invoke(prompt)



######################## USER INPUT AND PROMPT FUNCTIONS ########################


def get_user_input():
    print("\n ### Welcome to the model guide generation plateform !, you will now be asked to enter the relevant information in order for the plateform to generate your report \n ")

    print("\n=== Agricultural Practice Comparison Input ===")
    print("\nPlease provide the following information:")
    
    print("\n1. First Practice Description:")
    print("--------------------------------")
    practice1 = input("Enter details about the first agricultural practice:\n")
    
    print("\n2. Second Practice Description:")
    print("--------------------------------")
    practice2 = input("Enter details about the second agricultural practice:\n")
    
    print("\n3. Location Information:")
    print("-------------------------")
    place = input("Enter details about the location/region:\n")
    
    print("\n4. General System Information:")
    print("-------------------------------")
    print("(Include historical context, systemic aspects, or any relevant knowledge)")
    system_info = input("Enter general information:\n")
    
    return {
        "practice1": practice1,
        "practice2": practice2,
        "place": place,
        "system_info": system_info
    }

# Modify your query generation
def generate_query(user_inputs):
    query = f"""You are an expert in agriculture in {user_inputs['place']}. 

I want you to make me a report comparing these two farming practices:
1. {user_inputs['practice1']}
2. {user_inputs['practice2']}

Additional context to consider:
{user_inputs['system_info']}

The report should contain:
- A detailed comparison of the two practices
- A list of key processes that make each practice viable or interesting
- A systemic analysis considering the whole farming system"""
    
    print("query :", query)
    return query
















######################## Logs and files ########################


def log_result(query, result, filename="results.md"):
    from datetime import datetime
    import os

    # Get absolute path for results file
    results_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 
        filename
    )
    
    # Create timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Format the output
    output = f"""
{'='*50}
Date: {timestamp}
{'='*50}

QUERY:
{query}

{'='*50}

RESULT:
{result}

{'='*50}
\n\n"""
    
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(results_path), exist_ok=True)
        
        # Append to file
        with open(results_path, 'a', encoding='utf-8') as f:
            f.write(output)
            f.flush()  # Force write to disk
        
        print(f"Results successfully logged to: {results_path}")
        
    except Exception as e:
        print(f"Error writing to log file: {str(e)}")
        print(f"Attempted to write to: {results_path}")







######################## Streamlit interface (Optional) ######################## 


"""
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
        answer = ask_llm(query, context_window)
    st.subheader("LLM Answer")
    st.write(answer)
"""

















######################## Prompt Manager Class ########################

class PromptManager:
    def __init__(self, prompt_file: str = "prompt.txt"):
        # Get absolute path relative to this script
        self.prompt_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 
            prompt_file
        )
        self.prompts: Dict[str, str] = {}
        self._load_prompts()
    
    def _load_prompts(self) -> None:
        """Load all prompts from the prompt file."""
        try:
            with open(self.prompt_file, 'r', encoding='utf-8') as file:
                content = file.read()
            
            if not content.strip():
                print(f"Warning: {self.prompt_file} is empty.")
                return
                
            # Find all prompts using regex
            pattern = r'### PROMPT: ([^\n]+)\n(.*?)### END'
            matches = re.finditer(pattern, content, re.DOTALL)
            
            for match in matches:
                title = match.group(1).strip()
                prompt_text = match.group(2).strip()
                self.prompts[title] = prompt_text
                
        except FileNotFoundError:
            print(f"Warning: {self.prompt_file} not found.")
    
    def get_prompt(self, title: str) -> Optional[str]:
        """Get a specific prompt by its title."""
        return self.prompts.get(title)
    
    def list_prompts(self) -> list[str]:
        """List all available prompt titles."""
        return list(self.prompts.keys())




######################## Main execution flow: ########################


if __name__ == "__main__":
    # Initialize prompt manager
    prompt_manager = PromptManager()
    
    # Get specific prompt
    #prompt_report = prompt_manager.get_prompt("Report_Agriculture_Mekong_AWD_KenGiang")
    prompt_report = prompt_manager.get_prompt("Comprehensive_Synthesis")
    #prompt_report_details = prompt_manager.get_prompt("Report_Agriculture_details_1")
    prompt_report_details = ""
    prompt_task = prompt_manager.get_prompt("Task_agents_attributes_1")

    if prompt_report:
        print(prompt_report+"\n\n"+prompt_report_details)
        deep_search_result = deep_search_report(prompt_report)
        result = ask_llm(
            task=prompt_task,
            context=deep_search_result,
            model_name="gpt-oss:120b"
        )
        print("RESULT :", result)
        log_result("### PROMPT DEEP SEARCH :\n\n"+ prompt_report+prompt_report_details+ " ### PROMPT TASK: \n\n:"+ prompt_task, "### DEEP SEARCH RESULT: \n\n"+deep_search_result+ "### MODELLING RESULT: \n\n"+result)
        print(f"Results have been logged to results.md")
    else:
        print("Prompt not found!")
        # List all available prompts
        print("\nAvailable prompts:")
        for title in prompt_manager.list_prompts():
            print(f"- {title}")



"""
if __name__ == "__main__":
    # Initialize prompt manager
    prompt_manager = PromptManager()
    
    # Get specific prompt
    prompt_report_full = prompt_manager.get_prompt("report_full")
    prompt_task = prompt_manager.get_prompt("Task_agents_attributes")
    if prompt_report_full:
        
        result = ask_llm(
            task=prompt_task,
            context=prompt_report_full,
            model_name="gpt-oss:20b"
        )
        print("RESULT :", result)
        log_result(prompt_report_full+prompt_task, result)
        print(f"Results have been logged to results.md")
    else:
        print("Prompt not found!")
        # List all available prompts
        print("\nAvailable prompts:")
        for title in prompt_manager.list_prompts():
            print(f"- {title}")
"""


######################## OLD Main execution flow: ########################
#if __name__ == "__main__":
    #user_inputs = get_user_input_1()
    #query = generate_query(user_inputs)
    #result = deep_search_report(query)
    #print("\n=== Generated Report ===\n")
    #print(result)

    ## Execute the LLM flow
    #deep_search_report = deep_search_report(query_1)
    #result = ask_llm(context=deep_search_report)

    # Log the results
    #log_result(query_1, result)
    #print(f"Results have been logged to result.txt")




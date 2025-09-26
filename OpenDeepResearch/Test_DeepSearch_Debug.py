from opendeepsearch import OpenDeepSearchTool
from smolagents import CodeAgent, LiteLLMModel
import os

# Set environment variables
os.environ.update({
    "SERPER_API_KEY": "",
    "GEMINI_API_KEY": "",
    "JINA_API_KEY": "",
    "LITELLM_MODEL_ID": "gemini/gemini-2.0-flash-lite"
})

query = """You are an expert in agriculture in the Mékong delta. 

I want you to make me a report on two farming practices : High quality low emission rice farming versus traditional rice farming in the Mékong delta.

The report should contain:

- A description of the main differences between  High quality low emission rice farming and other rice farming techniques
- A list of the keys processes that make HQLE rice viable or interesting compared to other techniques. Describe these
processes in a systemic way considering the whole system of rice farming"""



search_agent = OpenDeepSearchTool(
    model_name="gemini/gemini-2.0-flash-lite",  # Explicitly set model name
    reranker="jina"
)

if not search_agent.is_initialized:
    search_agent.setup()

model = LiteLLMModel(
    "gemini/gemini-2.0-flash-lite",  # Explicitly set model name
    temperature= 0.2
)

code_agent = CodeAgent(
    tools=[search_agent], 
    model=model,
    #model_format="gemini"  # Specify model format for agent
)

result = code_agent.run(query)






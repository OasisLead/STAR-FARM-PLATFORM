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


def deep_search_report(query, temperature=0.2):
    print("Starting deep search report generation...")
    
    search_agent = OpenDeepSearchTool(
        model_name="gemini/gemini-2.0-flash-lite",  # Explicitly set model name
        reranker="jina"
    )

    if not search_agent.is_initialized:
        search_agent.setup()

    model = LiteLLMModel(
        model_name="gemini/gemini-2.0-flash-lite",  # Explicitly set model name
        config={
            "temperature": temperature,
            "api_key": os.environ.get("GEMINI_API_KEY"),
            "api_base": "https://generativelanguage.googleapis.com/v1",
            "provider": "google",  # Force Google provider
            #"model_format": "gemini"  # Specify model format
        }
    )

    code_agent = CodeAgent(
        tools=[search_agent], 
        model=model,
        #model_format="gemini"  # Specify model format for agent
    )
    
    result = code_agent.run(query)
    return result

# Add this at the bottom of the file to execute the function
if __name__ == "__main__":
    print("\n=== Generating Agricultural Report ===\n")
    result = deep_search_report(query)
    print("\n=== Generated Report ===\n")
    print(result)
    print("\n=== End of Report ===\n")




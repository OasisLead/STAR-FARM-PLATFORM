from opendeepsearch import OpenDeepSearchTool
import os

# Set environment variables
os.environ.update({
    "SERPER_API_KEY": "",
    "GEMINI_API_KEY": "",
    "JINA_API_KEY": ""
    "LITELLM_MODEL_ID": "gemini/gemini-2.0-flash-exp"
})

# Initialize search agent - Change the model name to use Gemini directly
search_agent = OpenDeepSearchTool(
    model_name="gemini/gemini-2.0-flash-exp",  # Changed from openrouter to direct Gemini
    reranker="jina"

)



# Verify initialization
if not search_agent.is_initialized:
    search_agent.setup()
    

# Perform search
result = search_agent.forward("""
    
You are an expert in agriculture in the Mékong delta. I want you to make me a report on HQLE (High quality low emission) rice vs traditional rice farming (meaning intensive farming or what most people do) in the Mékong delta.
Your report will focus on different aspects and should be well documented, these aspects are:

- A description of the main differences between HQLE rice farming and other rice farming techniques, a systemic description of rice farming and of the keys processes that make HQLE rice viable or interesting compared to other techniques, I want a high level of detail for the processes

- Agroecological, sustainable development and economic Indicators on which to compare these two practices and what are their respective performances on these indicators

- The current trends and numbers of adoption of HQLE vs "traditional" rice farming and the reasons of these trends as of 2025

- Future scenarios for economic, climatic, social, agricultural trends in rice farming in the Mékong delta and how HQLE and traditional rice farming compare in these scenarios around the indicators previously found""")

print(result)



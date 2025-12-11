# STAR-FARM-PLATFORM

## Purpose

The purpose of this project was to create an interactive software fuelled by LLMs to build agricultural agent based models, more precisely to build models that are able to compare different farming practices through specific indicators and in specific farming systems and places in the Mekong Delta, Vietnam.

This project is more a collection of ideas and prototypes rather than a full on plateform.

**For people at ACROSS, see my Proofs of work and my internship's report for more details and explanations on the intent and nature of the project**


## Main folders and files


### Opendeepsearch

**OpenDeepResearch** - _Contains the backend based on the OpenDeepSearch library that was done independently of the other folders. Here I focused on implementing OpenDeepSearch with and API for the use case of generating structures without connecting it to the other parts of the streamlit interface and the Local LLM_
- Test_DeepSearch.py - _An implementation of deepsearch with the advanced search parameters (to be used for generation) - You have to fill in your own API keys for the 3 APIs (search, reranker, LLM), Gemini has a Free limited API usage so it is the most relevant. The point of using API is to parallelize multiple searches or do multiple searches fast, which cannot be done with the FREE API of Gemini because the search is too expensive in terms of word/contextwindow and call/minute. **If it does not work, use Test_search_1 directly**_
- Test_search_1.py - _MAIN IMPLEMENTATION - It should ask for comparing two practices. It uses both an API through deepsearch and the Local LLM on line 336. The first part is an exploration of topics through deep search, and the second part is a compression and synthesis of this with the Local LLM. If you don't want to run any LLM local, you can switch line 336 to an API call. In the main function you can choose which prompts to use for the report (search) and the task (synthesis) using the prompt manager. Just look into prompt.txt and select the titles of the prompts you want to use. If you want to add a prompt in prompt.txt, respect the syntax of the way the prompts are written._
- Test_Defaultsearch.py - _Not relevant_
- prompt.txt - _Contains multiple prompts for generating different structures and for different synthesis. This contains the most interesting potential as you can mix prompts and researches in a coherent pipeline, in parallel, and come up with complex reports. Be careful of the syntax when writing a prompt or the prompt generator might fail at parsing them. For generating new prompts I would advise using gemini also, which can be helpful to generate good prompts. The prompts try to cover different elements of the research question at hand (comparing two practices under certain indicators in a specific system and place). They are not dependent on the specific practice, place, indicator, but they are biased towards vietnam and the Mekong delta. The key behavior is to focus on keywords which will active relevant researches for the deepsearch algorithm and relevant "knowledge areas and structures". For example, mentionning the ODD framework for the shape of the final report activates a set of structures either directly in the LLM or accessible through deepsearch. Another thing is multisearch, deepsearch ability to search different directions with different key words. The problem becomes that the runtime becomes really long at one point or crashes because of API limits, so I think the better thing is to limit the deepsearches to specific areas and then merge them._
- results.md
- reports.md - A few reports generated with this technique, and associated with their prompt instruction

-----------

### Interface and plateform

**P_Backend_generation** - _Contains experiments on generating very simple structures from the ITK model (mainly the set of possible crop cycle over the year for a given practice). It comes from the first methodology of generating simple structures inspired by Maelia or other research articles. I use constrained generation to generate exactly in the format I want, which can then be re-used as a piece of code for generating a UML interface or a Calendar interface and allow the user to interact with the structure directly. Some files are empty but are necessary structures. The main structure I focused on is practice parameter, ITK, (behavior of farmer in the specific practice through time)._

**P_Backend_global** - _A few backend ideas for the general plateform_
- System_code_handling.py - _A way to handle a piece of agent based modelling code (python or other) such that we can manipulate and read the parts of it that we want (parts dedicated to actions, attributes, inputs, outputs, environnment, etc..). The goal of this was to make a bridge beetween code and structures and use the LLM more efficiently on certain parts of the code rather than giving it the whole code everytime_
- System_steps.py - _Just a way to have a system of steps through the plateform, where the memory of the state of the model is saved at step n as well as the prompts and inputs used, in order to cancel a step and to build the final report_

**P_Frontend** i _a few frontend ideas in streamlit (not the best library for this but practical for easy LLM modules). It contains UML graphs for representing the model and calendar for representing the behavior and actions over a year. Look at my report for more designs and ideas._

**P_RAG_DATA** - _Not really coded. The goal would have been to use rag methodologies on big relevant documents, such as official documents from FAO, to select relevant parts to generate structures (I chose deepsearch in the end for reasons I highlight in my report, mainly that focusing on a limited set of documents is not flexible). A combination of RAG and deepsearch could have been possible but was not explored because I would have to tinker with the deepsearch algorithm in detail which I had no time for_

**P_Templates** - _Contains the main LLM templates for streamlit, with input-output_






PS: For the ones at ACROSS, the dependencies are already installed on my SSH session on the server of the lab, which you can access with my username and password

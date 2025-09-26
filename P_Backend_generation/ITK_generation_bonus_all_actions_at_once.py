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



## If my LLM generation process contains multiple contexts and multiple questions, I will
## progressively append these questions and contexts to the chain of thought prompting
## in order to make the chain of thought, and I will also use the constraint type
## at each step in order to control the format of the output and maybe get the output 
## back for the next step

list_of_contexts_and_questions =""

context_window1 = ("You are an expert of agriculture and farming in region of the Mékong delta in Vietnam, you especially know the latest farming practices as they developed over the 2000s and 2010s. The user will give you two farming practices in the Mekong Delta that he is interested in for study. These two practices are centered over one crop each (for example rice). For each practice, you will first inquire and identify which combination of crops farmers using this practice most commonly grow over one typical farming year on one plot or field. For this step, remember that a crop is defined by its simple name as well as its specific type and genetic origin that may have a relation with the specific way it is being cultivated in the region. Also, consider one field as the typical spatial unit for the farmer where he will cultivate the main crop. The point of this part is to identify if farmers use only the main crop, if they use variations of this main crop (Ex: Specific type of rice), or even different types of crops. There also may be some cases where two crops are cultivated at the same time on the same plot, as they are of different types (let's say rice and shrimp can co-live and co-grow on the same spatial plot, or other possibilities) or in specific cases. In these cases, still specify the secondary crop or specie being cultivated at a point in time. \n\n"
"Then, you will inquire with your knowledge about the multiple realistic ways farmers may rotate over these different crops over one year, especially focus on the order of the crops during the year in relation to the seasons, the weather, and other parameters, and the agricultural logic beetween these kind of rotations. Finally, after you have worked on all these steps, you will give a list of the most relevant crop rotations over a year by naming the different species and potential sub-species in the order as they are grown over the year, as well as the beginning date (First planting of the year) and end date (last harvesting of the year) of the yearly farming cycle. Again, give realistic answers as what is practiced in the Mékong delta region in farming, using realistic combinations of crops over one year, and realistic species of crops, based on what you know about farmer practices in the Mékong delta.")


context_window1_struct = ("This is the last part of the output. Don't make any chain of thought or reasoning for this phase and please directly generate the JSON format I ask you here right under. This JSON format should contain, for each practice (practice 1 and practice 2), a list of different possible rotations over a year. The rotations should be lists of string of crops in the right order, the rotations lists should be stored in a list for each pratice, and they can contain as many crops as can be rotated within a year over a single plot as long at is makes sense. If there is a case where two crops/species/living beings are cultivated over the same plot at the same time (Call them specie 1 and specie 2), then you can write it as a single element of the list, as the string named ""specie 1 and specie 2""  \n\n" 

#"For example, for the practice Triple rice, give multiple lists of possible crop combinations like :" 
#": [[rice_species1, rice_species2, rice_species3],[rice_species4,rice_species2,rice_species6]]." 

"This is the specific format I would like you to use for the final output of the answer: \n\n"

"class CropCycle(BaseModel): \n" 
"crops_rotation_list_practice_1: List[List[str]]\n"
"crops_rotation_list_practice_2: List[List[str]]\n\n"

"Where the strings are the names of the species, or more names if they are grown on the same plot during the same period " 

"now just prompt it directly")







### Remarque: Plus je donne de choses à générer au LLM, plus dans sa chain of thought il est capable de prendre en compte ces éléments
### spécifiques afin de générer des réponses cohérentes vis à vis de tout ces éléments



context_window3 = ""




################################################################################################
#################   useful functions   ################


################ JSON output structure for the crop rotation practices
class CropCycle(BaseModel):
    crops_rotation_list_practice_1: List[List[str]]
    #explanations_practice_1: List[str]  # Explanation for each crop combination in crops_practice_1
    #overall_explanation_practice_1: str # Overall explanation for practice 1

    crops_rotation_list_practice_2: List[List[str]]
    #explanations_practice_2: List[str]  # Explanation for each crop combination in crops_practice_2
    #overall_explanation_practice_2: str # Overall explanation for practice 2


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






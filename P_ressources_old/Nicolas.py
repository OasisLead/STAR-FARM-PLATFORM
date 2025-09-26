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
    a, b = np.array(a), np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def min_max_normalization(weights):
    """Normalize weights using min-max normalization."""
    min_weight = min(weights)
    max_weight = max(weights)
    if max_weight == min_weight:  # Avoid division by zero
        return [1.0 for _ in weights]
    return [(w - min_weight) / (max_weight - min_weight) for w in weights]

def softmax(weights):
    """Compute softmax values for a list of weights."""
    max_weight = max(weights)  # Subtract the maximum weight to prevent overflow
    exp_weights = [math.exp(w - max_weight) for w in weights]
    total = sum(exp_weights)
    return [w / total for w in exp_weights]

def get_top_k_documents(query_vec, driver, k=10):
    with driver.session() as session:
        results = session.run("""
            MATCH (d)
            WHERE d.embedding IS NOT NULL AND d.weight IS NOT NULL AND d.all_content IS NOT NULL and d.weight>0
            RETURN d.all_content AS all_content, d.weight AS weight, d.embedding AS embedding, elementId(d) AS eid
        """)
        scored = [
            (
                cosine_similarity(query_vec, record["embedding"]) * record["weight"],
                {
                    "all_content": record["all_content"],
                    "weight": record["weight"],
                    "elementId": record["eid"]
                }
            )
            for record in results
        ]
        return [doc[1] for doc in sorted(scored, key=lambda x: x[0], reverse=True)[:k]]

def describe_relationships(driver, element_ids):
    relationships = []
    with driver.session() as session:
        for eid in element_ids:
            results = session.run("""
                MATCH (node)-[rel]->(connected)
                WHERE elementId(node) = $eid
                RETURN node.name AS node_name, type(rel) AS relation, connected.name AS connected_name
            """, {"eid": eid})
            relationships.extend(
                f"{record['node_name']}-{record['relation']}->{record['connected_name']}"
                for record in results
            )
    return relationships

def format_reference(doc):
    return "\n".join(f"{k} : {v}" for k, v in doc.items())

def count_tokens(text):
    """Count the number of tokens in the given text."""
    tokenizer = tiktoken.encoding_for_model("gpt-4o")
    return len(tokenizer.encode(text))

def get_highest_count(driver):
    with driver.session() as session:
        result = session.run("MATCH (node) RETURN MAX(node.count) AS highest_count").single()
        return result["highest_count"] if result else 1.0

def retrieve_nodes_with_signal(driver, start_element_ids, signal_threshold=0.5, weight_multiplier=3, normalization_function="min_max", extend_graph=False):
    visited_signals = {}  # Track visited nodes and their signals
    result_nodes = []
    queue = [(eid, 1.0) for eid in start_element_ids]  # Start with initial nodes and full signal strength

    while queue:
        current_eid, current_signal = queue.pop(0)

        # Check if the node has been visited and update its signal if the new signal is stronger
        if current_eid in visited_signals and current_signal <= visited_signals[current_eid]:
            continue
        visited_signals[current_eid] = current_signal

        if current_signal < signal_threshold:
            continue

        with driver.session() as session:
            # Fetch relationships and node properties for the current node
            connected_results = session.run("""
                MATCH (node)-[rel]->(connected)
                WHERE elementId(node) = $eid
                RETURN type(rel) AS relation_type, 
                       elementId(connected) AS connected_eid,
                       rel.count AS relation_count,
                       connected.all_content AS all_content
            """, {"eid": current_eid})

            # Separate relationships by type
            of_block_relations = [rec for rec in connected_results if rec["relation_type"] == "OF_BLOCK_COUNT"]
            close_to_relations = [rec for rec in connected_results if rec["relation_type"] == "CLOSE_TO_COUNT"]

            # Extract counts from relationships
            of_block_counts = [(rec["relation_count"] or 1) for rec in of_block_relations]
            close_to_counts = [(rec["relation_count"] or 1) for rec in close_to_relations]



            # Apply normalization function
            if of_block_counts:
                normalized_of_block_weights = min_max_normalization(of_block_counts) if normalization_function == "min_max" else of_block_counts
                normalized_of_block_weights = [w * weight_multiplier for w in normalized_of_block_weights]
            else:
                normalized_of_block_weights = []

            if close_to_counts:
                normalized_close_to_weights = min_max_normalization(close_to_counts) if normalization_function == "min_max" else close_to_counts
                normalized_close_to_weights = [w * weight_multiplier for w in normalized_close_to_weights]
            else:
                normalized_close_to_weights = []

            # Store the current node's signal
            result_nodes.append({
                "elementId": current_eid,
                "signal": current_signal,
                "total_of_block_count": sum(of_block_counts),
                "total_close_to_count": sum(close_to_counts),
                "all_content": session.run("""
                    MATCH (node)
                    WHERE elementId(node) = $eid
                    RETURN node.all_content AS all_content
                """, {"eid": current_eid}).single()["all_content"]
            })

            # Propagate signal to connected nodes with decay
            for i, rec in enumerate(of_block_relations + close_to_relations):
                decayed_signal = current_signal
                if i < len(normalized_of_block_weights):
                    decayed_signal *= normalized_of_block_weights[i]
                if i < len(normalized_close_to_weights):
                    decayed_signal *= normalized_close_to_weights[i]
                # Only propagate if the decayed signal is above the threshold
                if decayed_signal >= signal_threshold:
                    queue.append((rec["connected_eid"], decayed_signal))
                    # Add connected node's content to results
                    result_nodes.append({
                        "elementId": rec["connected_eid"],
                        "signal": decayed_signal,
                        "all_content": rec["all_content"]
                    })

            # Extend graph if toggle is activated
            if extend_graph:
                neighbors = session.run("""
                    MATCH (node)-[rel]->(connected)
                    WHERE elementId(node) = $eid
                    RETURN elementId(connected) AS neighbor_id, connected.all_content AS all_content
                """, {"eid": current_eid})
                for neighbor in neighbors:
                    neighbor_id = neighbor["neighbor_id"]
                    if neighbor_id not in visited_signals:
                        result_nodes.append({
                            "elementId": neighbor_id,
                            "signal": 0,  # Neighbors are added without signal propagation
                            "all_content": neighbor["all_content"]
                        })

    return result_nodes

def run_rag_pipeline(query, driver, embedder, model, prompt, extend_graph, k, signal_threshold, weight_multiplier):
    query_vec = embedder.embed_query(query)
    top_docs = get_top_k_documents(query_vec, driver, k=k)
    if not top_docs:
        return "No relevant context found in the graph.", []

    top_element_ids = [doc["elementId"] for doc in top_docs]
    retrieved_nodes = retrieve_nodes_with_signal(
        driver, 
        start_element_ids=top_element_ids, 
        signal_threshold=signal_threshold, 
        weight_multiplier=weight_multiplier, 
        normalization_function="min_max",
        extend_graph=extend_graph
    )
    all_docs = top_docs + retrieved_nodes

    formatted_references = "\n\n".join(format_reference(doc) for doc in all_docs)
    relation_descriptions = describe_relationships(driver, top_element_ids) if extend_graph else []

    prompt_context = formatted_references + ("\n\n---\n\n" + "\n".join(relation_descriptions) if relation_descriptions else "")
    token_count = count_tokens(prompt_context)

    prompt_input = {
        "references": formatted_references + ("\n\n---\n\n" + "\n".join(relation_descriptions) if relation_descriptions else ""),
        "question": query,
    }

    chain = RunnablePassthrough() | prompt | model | StrOutputParser()
    output = chain.invoke(prompt_input)
    return [re.sub(r"<think>.*?</think>", "", output, flags=re.DOTALL).strip(), all_docs, token_count]


# ---- Streamlit App ----


st.set_page_config(page_title="Agricultural practice model generator", layout="wide")
st.title("Agricultural practice model generator")
st.write("conversational plateform/Software app through which, anyone with a research question in mind related to comparing agricultural practices over time in the mékong delta, can iteratively build an ABM agricultural model focused on comparing practices over specific indicators (Ressource management indicators, biodiversity, local pollution, global pollution, socio-economic quality and resilience, health, yield and productivity), in a specific place-ecosystem-value chain, and through specific scenarios and time scales where the nature of the practice and its distribution over farmers can vary.")

st.write("Beginning: This is the first answer you will have to provide the system to start model creation:")

query = st.text_input("🙋 ", "What is a gaml reflex? Give me an example")
run_btn = st.button("Run Query")

st.sidebar.header("⚙️ Parameters")
k = st.sidebar.slider("Top-K Documents", min_value=1, max_value=100, value=5)
signal_threshold = st.sidebar.slider("Signal Threshold", min_value=0.0, max_value=1.0, step=0.01, value=0.7)
weight_multiplier = st.sidebar.slider("Weight Multiplier", min_value=0.0, max_value=2.0, step=0.01, value=1.0)
extend_graph = st.sidebar.checkbox("Extend Connection Graph", value=True)

if run_btn and query:
    with st.spinner("Running graph RAG..."):
        neo4j_uri = "bolt://localhost:7687"
        neo4j_user = "neo4j"
        neo4j_password = "password"
        driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))

        embedder = OllamaEmbeddings(model="mxbai-embed-large")
        model = ChatOllama(model="qwen2.5-coder:32b")
        #model = ChatOllama(model="llama3:latest")


        prompt = ChatPromptTemplate.from_template(
            """
            You are a helpful AI, expert in gaml code. The following knowledge is at your disposal:

            {references}

            Thanks to your knowledge, answer briefly and clearly this question:
            {question}
            """
        )

        result = run_rag_pipeline(
            query, driver, embedder, model, prompt,
            extend_graph=extend_graph,
            k=k,
            signal_threshold=signal_threshold,
            weight_multiplier=weight_multiplier
        )
        driver.close()

    st.subheader("🤓☝️ Answer")
    st.write(result[0])

    st.markdown(f"😱 **Total retrieved context nodes:** {len(result[1])}")
    st.markdown(f"🧐 **Estimated total tokens in context (low approximation):** {result[2]}")

    st.markdown("---")
    with st.expander("🤩 Show context nodes used in the answer"):
        st.markdown("### Node Details")
        for doc in result[1]:
            st.markdown(f"""
**Node ID**: `{doc["elementId"]}`  
**Content**: `{doc.get("all_content", "N/A")}`
            """)
            st.markdown("---")


#        st.markdown(references)
# rag_app.py

import streamlit as st
import re
import warnings
from langchain_core._api.deprecation import LangChainDeprecationWarning

# Suppress deprecation warnings
warnings.filterwarnings("ignore", category=LangChainDeprecationWarning)

from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain.schema.output_parser import StrOutputParser
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough

# Setup models only once
llm_model = "deepseek-r1:latest"
embedding_model = "mxbai-embed-large"
model = ChatOllama(model=llm_model)
embeddings = OllamaEmbeddings(model=embedding_model)

# Prompt template
prompt = ChatPromptTemplate.from_template(
    """
You are a helpful AI assistant. Here is some documentation:

{references}

Thanks to your knowledge, answer briefly and clearly this question:
{question}
"""
)

# Load existing vector store
vector_store_refs = Chroma(
    embedding_function=embeddings,
    persist_directory="chroma_db_wiki"
)

# Create retriever
retriever_refs = vector_store_refs.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={"k": 20, "score_threshold": 0.4},
)

# Streamlit UI
st.title("☝️🤓 GAML Documentation Assistant")
st.write("Ask a question about the GAML language or simulation usage in GAMA:")

query = st.text_input("Your question")

if query:
    with st.spinner("Retrieving answer..."):
        retrieved_refs = retriever_refs.invoke(query)

        if not retrieved_refs:
            st.warning("No relevant context found. Please check your question or update your document store.")
        else:
            formatted_input = {
                "references": "\n\n".join(doc.page_content for doc in retrieved_refs),
                "question": query,
            }

            chain = (
                RunnablePassthrough()
                | prompt
                | model
                | StrOutputParser()
            )

            output = chain.invoke(formatted_input)
            output_cleaned = re.sub(r"<think>.*?</think>", "", output, flags=re.DOTALL).strip()

            st.markdown("### 😎 Answer")
            st.write(output_cleaned)

            with st.expander("🔍 Retrieved Document Metadata"):
                for i, doc in enumerate(retrieved_refs):
                    st.markdown(f"**Doc {i+1}** — `{doc.metadata.get('source', 'unknown')}`")

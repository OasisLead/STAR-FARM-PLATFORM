from opendeepsearch import OpenDeepSearchTool
import streamlit as st
import os
import time

st.set_page_config(page_title="Gemini-Powered Research", page_icon="🔍", layout="wide")
st.title("🔍 OpenDeepSearch with Gemini")

# Sidebar for API configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    gemini_key = st.text_input("Gemini API Key", type="password", 
                                help="Get your free key from https://aistudio.google.com")
    serper_key = st.text_input("Serper API Key", type="password",
                                help="Get 2,500 free searches from serper.dev")
    jina_key = st.text_input("Jina API Key", type="password",
                              help="For advanced reranking")
    
    # Model selection
    model_choice = st.selectbox(
        "Select Gemini Model",
        ["gemini/gemini-2.0-flash-exp",
         "gemini/gemini-1.5-pro", 
         "gemini/gemini-1.5-flash",
         "gemini/gemini-2.0-flash-thinking-exp"]
    )
    
    st.info("""
    **Free Tier Limits:**
    - Gemini: 60 requests/min, 1,000/day
    - Serper: 2,500 free searches
    """)

# Initialize search agent
@st.cache_resource
def get_search_agent(model_name, gemini_key, serper_key, jina_key):
    os.environ["GEMINI_API_KEY"] = gemini_key
    os.environ["SERPER_API_KEY"] = serper_key
    os.environ["JINA_API_KEY"] = jina_key
    
    return OpenDeepSearchTool(
        model_name=model_name,
        reranker="jina"
    )

# Main interface
if gemini_key and serper_key and jina_key:
    search_agent = get_search_agent(model_choice, gemini_key, serper_key, jina_key)
    
    # Query input
    query = st.text_area("Enter your research query:", height=100)
    
    col1, col2 = st.columns([4, 1])
    with col2:
        search_btn = st.button("🚀 Research", type="primary", use_container_width=True)
    
    if search_btn and query:
        with st.spinner("🔍 Researching with Gemini..."):
            start_time = time.time()
            
            try:
                result = search_agent.forward(query)
                query_time = time.time() - start_time
                
                # Display metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Model", model_choice.split("/")[-1])
                with col2:
                    st.metric("Query Time", f"{query_time:.2f}s")
                with col3:
                    st.metric("Status", "✅ Complete")
                
                # Display results
                st.subheader("📋 Research Results")
                st.write(result)
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("Check your API keys and try again")
else:
    st.warning("⚠️ Please configure all API keys in the sidebar")
import streamlit as st
import os
import sys
from datetime import datetime

# Add the project root to the Python path
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

# Import the updated StudSAREngine
from studsar_rag import StudSAREngine

# Initialize session state variables
if 'studsar_engine' not in st.session_state:
    st.session_state.studsar_engine = StudSAREngine()

if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'show_sources' not in st.session_state:
    st.session_state.show_sources = True

st.set_page_config(
    page_title="StudSar Civil Service AI Assistant",
    page_icon="🇬🇧",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for better styling - More standard app look
st.markdown("""
<style>
    /* General Body Styling */
    body {
        font-family: 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
        color: #333;
        background-color: #f0f2f6; /* Light gray background */
    }

    /* Main Header */
    .main-header {
        text-align: center;
        padding: 1.5rem 0;
        background: linear-gradient(135deg, #004080, #0066cc); /* Deeper blue gradient */
        color: white;
        border-radius: 12px; /* Slightly more rounded corners */
        margin-bottom: 2.5rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2); /* Subtle shadow */
    }
    .main-header h1 {
        font-size: 2.8em;
        margin-bottom: 0.5rem;
        font-weight: 700;
    }
    .main-header p {
        font-size: 1.1em;
        opacity: 0.9;
    }

    /* Streamlit Chat Message Styling */
    .stChatMessage {
        background-color: #ffffff; /* White background for chat bubbles */
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
    }
    .stChatMessage.user {
        background-color: #e6f7ff; /* Light blue for user messages */
        border-left: 5px solid #007bff;
    }
    .stChatMessage.assistant {
        background-color: #f8f9fa; /* Off-white for assistant messages */
        border-left: 5px solid #28a745;
    }

    /* Confidence Badges */
    .confidence-high { color: #198754; font-weight: bold; }
    .confidence-medium { color: #ffc107; font-weight: bold; }
    .confidence-low { color: #dc3545; font-weight: bold; }

    /* Source Cards */
    .source-card {
        background: #e9ecef; /* Slightly darker gray for sources */
        border-left: 4px solid #6c757d; /* Gray border */
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        font-size: 0.9em;
    }
    .source-card strong { color: #495057; }
    .source-card small { color: #6c757d; }

    /* Query Examples (Sidebar Buttons) */
    .stButton>button {
        width: 100%;
        text-align: left;
        background-color: #f0f8ff; /* Very light blue */
        color: #0056b3;
        border: 1px solid #cce5ff;
        border-radius: 5px;
        padding: 10px 15px;
        margin-bottom: 5px;
        transition: all 0.2s ease-in-out;
    }
    .stButton>button:hover {
        background-color: #e0f2ff;
        border-color: #99ccff;
        color: #004080;
    }

    /* Expander Styling */
    .streamlit-expanderHeader {
        background-color: #e9ecef; /* Match source card background */
        border-radius: 8px;
        padding: 10px;
        margin-top: 10px;
        border: 1px solid #dee2e6;
    }

    /* Footer */
    .footer {
        text-align: center;
        padding: 1.5rem 0;
        margin-top: 3rem;
        border-top: 1px solid #e0e0e0;
        color: #777;
        font-size: 0.9em;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🇬🇧 StudSar Civil Service AI Assistant</h1>
    <p>The essential playbook for modern civil servants</p>
</div>
""", unsafe_allow_html=True)

# Sidebar with enhanced features
with st.sidebar:
    st.markdown("### Quick Queries")
    
    example_queries = {
        "What is the Civil Service?": "Learn about the UK Civil Service structure and role",
        "Explain the Civil Service Code": "Understand values and standards of conduct",
        "How do I write a ministerial briefing?": "Get guidance on briefing format and content",
        "What are the Green Book principles?": "Treasury guidance on policy appraisal",
        "What is the policy development process?": "Learn about the ROAMEF cycle",
        "Tell me about the Data Protection Act 2018": "Understand GDPR implementation in UK",
        "What is the Public Sector Equality Duty?": "Learn about equality requirements",
        "Explain the parliamentary process": "Understand how bills become law",
        "What is devolution in the UK?": "Learn about devolved powers",
        "Tell me about Freedom of Information Act": "Understand FOI rights and obligations"
    }
    
    for query, description in example_queries.items():
        if st.button(f"📋 {query}", help=description, key=f"btn_{hash(query)}"):
            st.session_state.next_query = query
    
    st.markdown("---")
    
    # Settings
    st.markdown("### ⚙️ Settings")
    st.session_state.show_sources = st.checkbox("Show source details", value=st.session_state.show_sources)
    
    # Statistics
    st.markdown("### 📊 Knowledge Base Stats")
    total_topics = len(st.session_state.studsar_engine.knowledge_base)
    st.metric("Available Topics", total_topics)
    
    # Help section
    st.markdown("### ❓ Help")
    with st.expander("How to use StudSar"):
        st.markdown("""
        **Tips for better results:**
        - Ask specific questions about Civil Service topics
        - Use keywords like "Civil Service", "Code", "Green Book", etc.
        - Try the quick query buttons for common questions
        - Check the confidence score in responses
        
        **Available topics:**
        - Civil Service overview and structure
        - Civil Service Code and ethics
        - Policy development processes
        - Ministerial briefings
        - Green Book guidance
        - Data protection and GDPR
        - Parliamentary processes
        - Equality duties
        - Freedom of Information
        - UK devolution
        """)

    st.markdown("---")
    # About section with citation and RAG verification
    st.markdown("### ℹ️ About StudSar")
    with st.expander("About this application"):
        st.markdown("""
        This application is powered by **StudSAR**, a Neural Associative Memory System for Artificial Intelligence. 
        It leverages a **Retrieval-Augmented Generation (RAG)** approach to provide informed responses based on a curated knowledge base of UK Civil Service information. 
        
        **How to verify RAG functionality:**
        When you ask a question, StudSAR retrieves relevant information from its internal knowledge base and uses it to formulate an answer. 
        You can verify this by enabling the 'Show source details' checkbox above. After each assistant response, an expander titled '📚 Sources' will appear, 
        showing the exact pieces of information (sources) that were retrieved and used to generate the answer, along with their similarity scores.
        
        **Citation:**
        Bulla, F., Ewelu, S., & Yalla, S. P. (2025). StudSar: A Neural Associative Memory System for Artificial Intelligence. Scientific Journal of Engineering, and Technology, 2(2), 21-30. https://doi.org/10.69739/sjet.v2i2.712
        """)

# Main chat interface
st.markdown("### Chat with StudSar")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant" and "metadata" in message:
            # Display enhanced assistant message with metadata
            st.markdown(message["content"])
            if st.session_state.show_sources and message["metadata"].get("sources"):
                with st.expander(f"📚 Sources (Confidence: {message["metadata"].get("confidence", 0):.2f})"):
                    for i, res in enumerate(message["metadata"]["sources"]):
                        st.markdown(f"""
                        <div class="source-card">
                            <strong>Source {i+1}: {res.get("title", "N/A")} (Similarity: {res.get("similarity", 0):.3f})</strong><br>
                            {res.get("content", "No content available.")}
                        </div>
                        """, unsafe_allow_html=True)
        else:
            st.markdown(message["content"])

# Handle pre-filled query from sidebar
if 'next_query' in st.session_state and st.session_state.next_query:
    prompt = st.session_state.next_query
    del st.session_state.next_query
    
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Process and display assistant response
    with st.chat_message("assistant"):
        with st.spinner(" Analyzing your query..."):
            response_data = st.session_state.studsar_engine.query(prompt)
            answer = response_data.get('answer', 'I apologize, but I could not process that request.')
            sources = response_data.get('sources', [])
            confidence = response_data.get('confidence', 0.0)

            # Display answer
            st.markdown(answer)
            
            # Add message with metadata
            st.session_state.messages.append({
                "role": "assistant", 
                "content": answer,
                "metadata": {
                    "sources": sources,
                    "confidence": confidence,
                    "timestamp": datetime.now().isoformat()
                }
            })

            # Display sources if enabled
            if st.session_state.show_sources and sources:
                confidence_class = "confidence-high" if confidence > 0.7 else "confidence-medium" if confidence > 0.4 else "confidence-low"
                st.markdown(f'<p class="{confidence_class}">Confidence: {confidence:.2f}</p>', unsafe_allow_html=True)
                
                with st.expander(f"📚 Sources ({len(sources)} found)"):
                    for i, source in enumerate(sources):
                        st.markdown(f"""
                        <div class="source-card">
                            <strong>Source {i+1}: {source.get("title", "N/A")} (Similarity: {source.get("similarity", 0):.3f})</strong><br>
                            {source.get("content", "No content available.")}
                        </div>
                        """, unsafe_allow_html=True)

# Handle user input
if prompt := st.chat_input("Ask me anything about the UK Civil Service..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🔍 Analyzing your query..."):
            response_data = st.session_state.studsar_engine.query(prompt)
            answer = response_data.get('answer', 'I apologize, but I could not process that request.')
            sources = response_data.get('sources', [])
            confidence = response_data.get('confidence', 0.0)

            # Display answer
            st.markdown(answer)
            
            # Add message with metadata
            st.session_state.messages.append({
                "role": "assistant", 
                "content": answer,
                "metadata": {
                    "sources": sources,
                    "confidence": confidence,
                    "timestamp": datetime.now().isoformat()
                }
            })

            # Display sources if enabled
            if st.session_state.show_sources and sources:
                confidence_class = "confidence-high" if confidence > 0.7 else "confidence-medium" if confidence > 0.4 else "confidence-low"
                st.markdown(f'<p class="{confidence_class}">Confidence: {confidence:.2f}</p>', unsafe_allow_html=True)
                
                with st.expander(f"📚 Sources ({len(sources)} found)"):
                    for i, source in enumerate(sources):
                        st.markdown(f"""
                        <div class="source-card">
                            <strong>Source {i+1}: {source.get("title", "N/A")} (Similarity: {source.get("similarity", 0):.3f})</strong><br>
                            {source.get("content", "No content available.")}
                        </div>
                        """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    StudSAR Civil Service AI Assistant | Built with Streamlit | © 2025
</div>
""", unsafe_allow_html=True)

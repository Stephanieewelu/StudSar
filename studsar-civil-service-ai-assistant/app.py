import streamlit as st
import os
import sys
import json
from datetime import datetime
from typing import Dict, List

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

if 'user_feedback' not in st.session_state:
    st.session_state.user_feedback = {}

if 'show_onboarding' not in st.session_state:
    st.session_state.show_onboarding = True

st.set_page_config(
    page_title="StudSAR Civil Service AI Assistant",
    page_icon="🇬🇧",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Enhanced CSS for better styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* General Body Styling */
    .main {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    /* Main Header */
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 50%, #60a5fa 100%);
        color: white;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px rgba(59, 130, 246, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="50" cy="50" r="1" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
        opacity: 0.1;
    }
    
    .main-header h1 {
        font-size: 3rem;
        margin-bottom: 0.5rem;
        font-weight: 700;
        position: relative;
        z-index: 1;
    }
    
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.95;
        position: relative;
        z-index: 1;
        font-weight: 400;
    }
    
    /* Onboarding Modal */
    .onboarding-modal {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        border: 2px solid #3b82f6;
        border-radius: 12px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
    }
    
    /* Chat Message Styling */
    .stChatMessage {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        border: 1px solid #e5e7eb;
    }
    
    /* Confidence Badges */
    .confidence-high { 
        color: #059669; 
        font-weight: 600;
        background: #d1fae5;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.875rem;
    }
    .confidence-medium { 
        color: #d97706; 
        font-weight: 600;
        background: #fef3c7;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.875rem;
    }
    .confidence-low { 
        color: #dc2626; 
        font-weight: 600;
        background: #fee2e2;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.875rem;
    }
    
    /* Source Cards */
    .source-card {
        background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
        border-left: 4px solid #3b82f6;
        padding: 1.25rem;
        margin: 0.75rem 0;
        border-radius: 8px;
        font-size: 0.9rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .source-card strong { 
        color: #1e40af; 
        font-weight: 600;
    }
    
    .source-card small { 
        color: #64748b; 
        font-weight: 500;
    }
    
    /* Sidebar Styling */
    .sidebar .stButton > button {
        width: 100%;
        text-align: left;
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        color: #0369a1;
        border: 1px solid #bae6fd;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        margin-bottom: 0.5rem;
        transition: all 0.2s ease-in-out;
        font-weight: 500;
    }
    
    .sidebar .stButton > button:hover {
        background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%);
        border-color: #7dd3fc;
        color: #0c4a6e;
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* Feedback Buttons */
    .feedback-buttons {
        display: flex;
        gap: 0.5rem;
        margin-top: 1rem;
        justify-content: flex-end;
    }
    
    .feedback-btn {
        background: none;
        border: 1px solid #d1d5db;
        border-radius: 6px;
        padding: 0.5rem;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .feedback-btn:hover {
        background: #f3f4f6;
    }
    
    .feedback-btn.active {
        background: #3b82f6;
        color: white;
        border-color: #3b82f6;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem 0;
        margin-top: 3rem;
        border-top: 2px solid #e5e7eb;
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        border-radius: 12px;
        color: #64748b;
        font-size: 0.9rem;
    }
    
    /* Query Type Badges */
    .query-type-badge {
        display: inline-block;
        background: #e0e7ff;
        color: #3730a3;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 500;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Onboarding Modal
if st.session_state.show_onboarding:
    st.markdown("""
    <div class="onboarding-modal">
        <h2> Welcome to StudSAR Civil Service AI Assistant!</h2>
        <p><strong>Getting Started:</strong></p>
        <ul>
            <li> Use the <strong>Quick Queries</strong> in the sidebar for common questions</li>
            <li> Type your own questions in the chat box below</li>
            <li> Enable <strong>"Show source details"</strong> to see how answers are generated</li>
            <li> Rate responses to help improve the system</li>
            <li> Check the <strong>confidence score</strong> to gauge answer reliability</li>
        </ul>
        <p><em>StudSAR uses Retrieval-Augmented Generation (RAG) to provide accurate, source-backed answers about UK Civil Service topics.</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🚀 Get Started", type="primary"):
            st.session_state.show_onboarding = False
            st.rerun()
    with col2:
        if st.button("ℹ️ Show this again later"):
            st.session_state.show_onboarding = False
            st.rerun()

# Header
st.markdown("""
<div class="main-header">
    <h1>🇬🇧 StudSAR Civil Service AI Assistant</h1>
    <p>Your intelligent assistant for UK Civil Service information, document drafting, and policy guidance</p>
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
        if st.button(f" {query}", help=description, key=f"btn_{hash(query)}"):
            st.session_state.next_query = query
    
    st.markdown("---")
    
    # Settings
    st.markdown("### ⚙️ Settings")
    st.session_state.show_sources = st.checkbox("Show source details", value=st.session_state.show_sources)
    
    if st.button("🔄 Clear Chat History"):
        st.session_state.messages = []
        st.session_state.studsar_engine.clear_history()
        st.rerun()
    
    if st.button(" Show Onboarding Again"):
        st.session_state.show_onboarding = True
        st.rerun()
    
    # Statistics
    st.markdown("### Knowledge Base Stats")
    total_topics = len(st.session_state.studsar_engine.knowledge_base)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Topics", total_topics)
    
    # Help section
    st.markdown("### Help")
    with st.expander("How to use StudSAR"):
        st.markdown("""
        **Tips for better results:**
        - Ask specific questions about Civil Service topics
        - Use keywords like "Civil Service", "Code", "Green Book", etc.
        - Try the quick query buttons for common questions
        - Check the confidence score in responses
        
        **Query Types:**
        - **Definition**: "What is..." or "Define..."
        - **Process**: "How to..." or "What are the steps..."
        - **List**: "List the..." or "What are the principles..."
        - **Example**: "Give me an example..." or "Show me a template..."
        
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
    st.markdown("### About StudSAR")
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
st.markdown("### 💬 Chat with StudSAR")

def render_feedback_buttons(message_id: str):
    """Render feedback buttons for a message."""
    col1, col2, col3 = st.columns([1, 1, 8])
    
    with col1:
        if st.button("👍", key=f"thumbs_up_{message_id}"):
            st.session_state.user_feedback[message_id] = "positive"
            st.success("Thank you for your feedback!")
    
    with col2:
        if st.button("👎", key=f"thumbs_down_{message_id}"):
            st.session_state.user_feedback[message_id] = "negative"
            st.info("Thank you for your feedback! We'll work to improve.")

# Display chat history
for i, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        if message["role"] == "assistant" and "metadata" in message:
            # Display query type badge
            query_type = message["metadata"].get("query_type", "general")
            st.markdown(f'<span class="query-type-badge">Query Type: {query_type.title()}</span>', unsafe_allow_html=True)
            
            # Display enhanced assistant message with metadata
            st.markdown(message["content"])
            
            # Display confidence score
            confidence = message["metadata"].get("confidence", 0)
            confidence_class = "confidence-high" if confidence > 0.7 else "confidence-medium" if confidence > 0.4 else "confidence-low"
            st.markdown(f'<span class="{confidence_class}">Confidence: {confidence:.2f}</span>', unsafe_allow_html=True)
            
            # Render feedback buttons
            render_feedback_buttons(f"msg_{i}")
            
            # Display sources if enabled
            if st.session_state.show_sources and message["metadata"].get("sources"):
                with st.expander(f" Sources ({len(message['metadata']['sources'])} found)"):
                    for j, source in enumerate(message["metadata"]["sources"]):
                        st.markdown(f"""
                        <div class="source-card">
                            <strong>Source {j+1}: {source.get("title", "N/A")}</strong><br>
                            <small>Similarity: {source.get("similarity", 0):.3f} | Relevance Score: {source.get("relevance_score", 0):.1f}</small><br>
                            {source.get("content", "No content available.")}
                            {f'<p><a href="{source.get("url", "#")}" target="_blank">View Source</a></p>' if source.get("url") else ''}
                        </div>
                        """, unsafe_allow_html=True)
        else:
            st.markdown(message["content"])

def process_query(prompt: str):
    """Process a query and display the response."""
    with st.chat_message("assistant"):
        with st.spinner(" Analyzing your query..."):
            response_data = st.session_state.studsar_engine.query(prompt)
            answer = response_data.get('answer', 'I apologize, but I could not process that request.')
            sources = response_data.get('sources', [])
            confidence = response_data.get('confidence', 0.0)
            query_type = response_data.get('query_type', 'general')

            # Display query type badge
            st.markdown(f'<span class="query-type-badge">Query Type: {query_type.title()}</span>', unsafe_allow_html=True)
            
            # Display answer
            st.markdown(answer)
            
            # Display confidence score
            confidence_class = "confidence-high" if confidence > 0.7 else "confidence-medium" if confidence > 0.4 else "confidence-low"
            st.markdown(f'<span class="{confidence_class}">Confidence: {confidence:.2f}</span>', unsafe_allow_html=True)
            
            # Add message with metadata
            message_metadata = {
                "sources": sources,
                "confidence": confidence,
                "query_type": query_type,
                "timestamp": datetime.now().isoformat()
            }
            
            st.session_state.messages.append({
                "role": "assistant", 
                "content": answer,
                "metadata": message_metadata
            })
            
            # Render feedback buttons
            render_feedback_buttons(f"msg_{len(st.session_state.messages)-1}")
            
            # Display sources if enabled
            if st.session_state.show_sources and sources:
                with st.expander(f"📚 Sources ({len(sources)} found)"):
                    for i, source in enumerate(sources):
                        st.markdown(f"""
                        <div class="source-card">
                            <strong>Source {i+1}: {source.get("title", "N/A")}</strong><br>
                            <small>Similarity: {source.get("similarity", 0):.3f} | Relevance Score: {source.get("relevance_score", 0):.1f}</small><br>
                            {source.get("content", "No content available.")}
                            {f'<p><a href="{source.get("url", "#")}" target="_blank">View Source</a></p>' if source.get("url") else ''}
                        </div>
                        """, unsafe_allow_html=True)

# Handle pre-filled query from sidebar
if 'next_query' in st.session_state and st.session_state.next_query:
    prompt = st.session_state.next_query
    del st.session_state.next_query
    
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Process and display assistant response
    process_query(prompt)

# Handle user input
if prompt := st.chat_input("Ask me anything about the UK Civil Service..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Process and display assistant response
    process_query(prompt)

# Footer
st.markdown("""
<div class="footer">
    <strong>StudSAR Civil Service AI Assistant</strong><br>
    Built with Streamlit | Powered by StudSAR Neural Associative Memory System<br>
    © 2025 | Enhanced with RAG Technology
</div>
""", unsafe_allow_html=True)

"""
Example demonstrating RAG integration with StudSar.
This script shows how to use RAGConnector to load external documents
and integrate them with the StudSar memory system.
"""
import sys
import os

# Add the main directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.managers.manager import StudSarManager
from src.rag.rag_connector import RAGConnector

def run_rag_example():
    print("=== New era --> StudSar RAG Integration Example <-- ===\n")
    
    # Initialize StudSar Manager
    print("1 --> Initializing StudSar Manager...")
    manager = StudSarManager()
    
    # Build initial network with some base knowledge
    base_text = """
    StudSar is an AI semantic memory system based on neural networks.
    It uses sentence transformers to create embeddings of text segments.
    The system can store and retrieve information using semantic similarity.
    """
    manager.build_network_from_text(base_text, default_emotion="neutral")
    print(f"Base network built with {manager.studsar_network.get_total_markers()} markers\n")
    
    # Initialize RAG Connector
    print("Number 2 -->.Initializing RAG Connector...")
    rag = RAGConnector(manager)
    print("RAG Connector initialized\n")
    
    # Create sample documents for testing
    print("Number 3 -->.Creating sample documents...")
    
    #Create temp directory if it doesn't exist
    if not os.path.exists("temp_docs"):
        os.makedirs("temp_docs")
    
    # Sample AI document
    ai_doc_path = "temp_docs/ai_basics.txt"
    with open(ai_doc_path, "w", encoding="utf-8") as f:
        f.write(""" Artificial Intelligence Overview
        Machine Learning is a subset of AI that focuses on algorithms that can learn from data.
        Deep Learning uses neural networks with multiple layers to process information.
        Natural Language Processing (NLP) enables computers to understand human language.
        Computer Vision allows machines to interpret and understand visual information.
        AI Applications include:
        - Autonomous vehicles
        - Medical diagnosis
        - Financial trading
        - Recommendation systems
        - Virtual assistants
        """)
    
    # Sample technology document  
    tech_doc_path = "temp_docs/technology_trends.txt"
    with open(tech_doc_path, "w", encoding="utf-8") as f:
        f.write("""
        Technology Trends 2024
        Cloud Computing continues to dominate enterprise infrastructure.
        Edge Computing brings processing closer to data sources.
        Quantum Computing shows promise for complex problem solving.
        Blockchain technology enables decentralized applications.
        Emerging Technologies:
        - Augmented Reality (AR)
        - Virtual Reality (VR)
        - Internet of Things (IoT)
        - 5G Networks
        - Robotics
        """)
    
    print("Sample documents created\n")
    
    # Add documents to RAG system
    print("4.Adding documents to RAG system...")
    
    ai_source_id = rag.add_document(
        ai_doc_path, 
        source_id="ai_basics", 
        metadata_extra={"topic": "artificial_intelligence", "category": "educational"}
    )
    
    tech_source_id = rag.add_document(
        tech_doc_path, 
        source_id="tech_trends", 
        metadata_extra={"topic": "technology", "category": "trends"}
    )
    
    print(f"AI document added with source ID: {ai_source_id}")
    print(f"Tech document added with source ID: {tech_source_id}\n")
    
    # Display RAG statistics
    print(" Num 5 -->  RAG System Statistics:")
    stats = rag.get_source_statistics()
    print(f" Total sources: {stats['total_sources']}")
    print(f"Total segments memorized: {stats['total_segments_memorized']}")
    print(f"Sources by type: {stats['by_type']}\n")
    
    # Perform searches
    print(" N 6 --> Performing searches...\n")
    
    # Search in external sources only
    print("Search n1: 'machine learning' in external sources")
    ml_results = rag.search_external_sources("machine learning", limit=3)
    for i, result in enumerate(ml_results, 1):
        print(f"{i}. Score: {result['score']:.3f} | Source: {result['source_id']}")
        print(f"Text: {result['text'][:100]}...\n")
    
    # Search in all StudSar memory (base + external)
    print(" Search n 2: 'neural networks' in all memory")
    all_ids, all_sims, all_segs = manager.search("neural networks", k=3)
    for i, (id_, sim, seg) in enumerate(zip(all_ids, all_sims, all_segs), 1):
        print(f"{i}. ID: {id_} | Similarity: {sim:.3f}")
        print(f"Text: {seg[:100]}...\n")
    
    # Search with source type filter
    print("Search n 3: 'technology' filtered by document type")
    tech_results = rag.search_external_sources(
        "technology", 
        limit=2, 
        source_type_filter=["txt"]
    )
    for i, result in enumerate(tech_results, 1):
        print(f"{i}. Score: {result['score']:.3f} | Source: {result['source_id']}")
        print(f"Text: {result['text'][:100]}...\n")
    
    # Add web content (if available)
    print("Number seven 7 <-->Adding web content (example - requires internet)...")
    try:
        # Note: This will only work if the dependencies are installed and internet is available
        web_source_id = rag.add_web_content(
            "https://en.wikipedia.org/wiki/Artificial_intelligence",
            source_id="wiki_ai",
            metadata_extra={"topic": "ai", "source_type": "wikipedia"}
        )
        if web_source_id:
            print(f"Web content added with source ID: {web_source_id}")
        else:
            print("Web content addition failed (dependencies missing or network issue)")
    except Exception as e:
        print(f"Web content addition failed: {str(e)[:100]}...")
    
    print("I'm hear Bro" )

    # Update source metadata
    print(" continue n8 Updating source metadata...")
    if ai_source_id:
        success = rag.update_external_source(
            ai_source_id, 
            metadata_update={"last_reviewed": "2024-05-22", "quality": "high"}
        )
        print(f"AI source metadata updated: {success}")
    
    #  Debug source details
    print("\n9.Debug information for AI source:")
    if ai_source_id:
        debug_info = rag.debug_source(ai_source_id)
        print(f"""Source type: {debug_info.get('type')}""")
        print(f"""Segments memorized: {debug_info.get('segments_memorized')}""")
        print(f"Added at: {debug_info.get('added_at')}")
        sample_segments = debug_info.get('sample_segments_from_memory', [])
        print(f"Sample segments found: {len(sample_segments)}")
    
    #  Save complete state
    print("\n10. Saving complete StudSar state with RAG data...")
    save_path = "studsar_with_rag.pth"
    manager.save(save_path)
    print(f"Complete state saved to: {save_path}")
    
    #  Cleanup
    print("\n11. Cleaning up temporary files...")
    try:
        os.remove(ai_doc_path)
        os.remove(tech_doc_path)
        os.rmdir("temp_docs")
        print("Temporary files cleaned up")
    except Exception as e:
        print(f"Cleanup warning: {e}")

    # Final message
    print("\n=== RAG -- o yes bro-- Example Complete ===")
    print(f"Final network size: {manager.studsar_network.get_total_markers()} markers")
    print("RAG successfully integrated external documents into StudSar memory!")

if __name__ == "__main__":
    run_rag_example() 
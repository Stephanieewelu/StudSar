# StudSar – AI Semantic Memory System (V2 Prototype)
**StudSar** is a prototype AI memory system based on a **custom neural network (`StudSarNeural`)**, implemented in PyTorch. The goal is to emulate a system that learns and associates information semantically, incorporating features inspired by cognitive processes. This V2 introduces several enhancements focusing on richer context and feedback mechanisms.
---
## System Overview (V2)
StudSar operates in the following steps:
1.  **Text Segmentation:** Breaks input text into logical units (segments).
    *   **V2 Goal:** Utilize a fine-tuned Transformer model for context-aware segmentation.
    *   **Current Implementation:** Uses spaCy for sentence-based segmentation (if available) or falls back to word-count based segmentation. A placeholder function (`segment_text_transformer_placeholder`) exists in `src/utils/text.py` for future integration.
2.  **Associative Marker Generation:** Creates semantic vector embeddings ("markers") for each segment using a pre-trained `Sentence Transformers` model.
3.  **Memory Storage:** Stores markers (embeddings) and their corresponding text segments within the `StudSarNeural` network (`torch.nn.Module`).
    *   **V2 Feature:** Allows associating optional **emotional tags** (e.g., "neutral", "informative", "important") with each marker upon creation or update.
4.  **Dynamic Association:** Semantic connections between markers are implicitly represented by their proximity in the high-dimensional embedding space. Associations are calculated dynamically during search via cosine similarity.
5.  **Internal Search:** Finds the `k` most similar markers/segments to a given query embedding using cosine similarity.
    *   **V2 Feature:** Search results trigger an increment in the **usage count** for the retrieved markers.
    *   **V2 Planned:** Reputation scores could potentially influence search ranking in future iterations.
6.  **Incremental Updates:** Supports continuous learning by allowing new text segments (with optional emotional tags) to be added to the network at any time.
7.  **Reputation Feedback (V2):** Allows associating a numerical **reputation score** with markers based on external feedback (positive or negative). This score is stored alongside the marker.
8.  **Usage Tracking (V2):** Monitors how often each marker is accessed during search operations. This data is stored and can be used for features like consolidation.
9.  **Offline Consolidation (V2 - "Dream Mode" - Placeholder):** The system includes hooks (usage tracking) for a planned offline process to revisit, potentially refine, or prune low-usage or low-reputation markers. The core consolidation logic is not yet implemented.
10. **Internal Graph Visualization (V2 - Placeholder):** Includes placeholder methods and necessary libraries (`networkx`, `matplotlib` in `requirements.txt`) to enable plotting the semantic graph of markers based on their embedding similarity. The plotting function itself (`visualize_graph` in `StudSarManager`) is a basic placeholder.
11. **Persistence:** The entire state of the `StudSarNeural` network, including embeddings, segment mappings, and V2 attributes (emotion tags, reputation scores, usage counts), can be saved to and reloaded from a file using `torch.save` and `torch.load`.

---
## Key Features (V2)

-   **Central Neural Network (`StudSarNeural`):** A custom `torch.nn.Module` acting as a dynamic, resizable vector memory.
-   **Tensor-Based Memory:** Embeddings (markers) are stored efficiently as PyTorch tensors within the network's buffer (`memory_embeddings`).
-   **Implicit Associations:** Semantic relationships are determined by vector similarity (cosine similarity) in the embedding space, not predefined links.
-   **High-Quality Embeddings:** Leverages `Sentence Transformers` models (e.g., `all-MiniLM-L6-v2`) for generating semantically rich text embeddings.
-   **Advanced Segmentation (V2 Goal):** Aims to integrate a fine-tuned Transformer for superior, context-aware text segmentation (currently uses spaCy/word-based fallback).
-   **Emotional Tagging (V2 Implemented):** Allows associating simple string tags representing emotional context with memories during creation/update.
-   **Reputation System (V2 Implemented):** Enables reinforcing or weakening memories by updating a numerical reputation score based on external feedback.
-   **Usage Tracking (V2 Implemented):** Monitors marker access frequency during search operations.
-   **Dream Mode (V2 Placeholder):** Infrastructure (usage tracking) exists for a planned offline self-optimization/consolidation process.
-   **Internal Graph Visualization (V2 Placeholder):** Basic setup and placeholder function for visualizing marker relationships.
-   **Internal Retrieval Engine:** Search performed efficiently using PyTorch tensor operations (cosine similarity, `torch.topk`).
-   **Persistence (V2 Implemented):** The network’s state, including V2 attributes (emotion, reputation, usage), can be saved and reloaded reliably.

---

## Project Structure (V2)

```
StudSar/
├── examples/
│   ├── basic_example.py         # Demonstrates core V2 functionalities
│   └── pycache /
├── src/
│   ├── managers/
│   │   ├── manager.py           # StudSarManager class (main interface)
│   │   └── pycache /
│   ├── models/
│   │   ├── neural.py            # StudSarNeural class (core network)
│   │   ├── init .py
│   │   └── pycache /
│   ├── utils/
│   │   ├── text.py              # Text segmentation functions (incl. placeholder)
│   │   ├── visualization.py     # Placeholder for graph plotting
│   │   ├── init .py
│   │   └── pycache /
│   ├── init .py
│   └── studsar.py             # Older monolithic version (potentially deprecated/ref)
├── .gitignore
├── README.md                    # This file
├── requirements.txt             # Project dependencies (incl. V2 additions)
└── RICERCA.MD                   # Research/Notes document (contains V2 planning) 
``` 


---

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd StudSar
    ```
2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *Note: `requirements.txt` includes `torch` (CPU version by default), `sentence-transformers`, `numpy`, `scikit-learn`, `networkx`, and `matplotlib`.*
4.  **(Optional) Install spaCy for better segmentation:**
    ```bash
    pip install spacy
    python -m spacy download en_core_web_sm
    ```
    *If spaCy is not installed or the model download fails, the system will automatically fall back to word-based segmentation.*

---

## Basic Usage

See `examples/basic_example.py` for a demonstration of:
- Initializing the `StudSarManager`.
- Building the network from text with a default emotion.
- Performing searches (which now track usage).
- Updating the network with new text and a specific emotion.
- Updating the reputation of a marker.
- Retrieving detailed information about a marker (segment, emotion, reputation, usage count).
- Saving the network state (including V2 attributes).
- Reloading the network state.
- Calling placeholder visualization function.

```python
# Example snippet from basic_example.py
from src.managers.manager import StudSarManager

# Initialize
manager = StudSarManager()

# Build with default emotion
manager.build_network_from_text("Some initial text.", default_emotion="neutral")

# Add new text with specific emotion
new_id = manager.update_network("More important text.", emotion="important")

# Search (increments usage count)
ids, sims, segs = manager.search("Query text", k=1)

# Update reputation
if ids:
    manager.update_marker_reputation(ids[0], 1.0) # Positive feedback

# Get details
if ids:
    details = manager.get_marker_details(ids[0])
    print(details) # {'segment': ..., 'emotion': ..., 'reputation': ..., 'usage_count': ...}

# Save and Load
manager.save("my_memory.pth")
reloaded_manager = StudSarManager.load("my_memory.pth")

## Future Work / V2 Goals
- Implement Transformer Segmentation: Replace the placeholder with a functional transformer model for segmentation.
- Implement Dream Mode: Develop the logic for offline consolidation based on usage counts and reputation.
- Implement Visualization: Complete the visualize_graph function for meaningful graph output.
- Refine Search: Potentially incorporate reputation scores into the search ranking algorithm.
- Memory Management: Explore more sophisticated strategies for managing memory growth and pruning less relevant information. 
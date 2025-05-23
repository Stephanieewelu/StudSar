# StudSar – AI Semantic Memory System **V3** (English)

> *“An artificial mind that ********remembers********, ********links******** and ********reasons******** inside a single neural network.”*
> **Francesco Bulla**, Brainverse\_AI

---

## What’s New in V3 (compared to V2)

| Area                  | V2                                              | **V3**                                                                                                                      |
| --------------------- | ----------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| **Internal memory**   | Embeddings + emotions, reputation, usage        | *Same*, optimised buffers                                                                                                   |
| **Text segmentation** | spaCy / word fallback (Transformer placeholder) | unchanged (Transformer coming in V4)                                                                                        |
| **RAG integration**   | ✗                                               | **NEW** `src/rag/rag_connector.py`• imports PDF/TXT/CSV, web pages, DB rows• adds tags `source_type` & `external_source_id` |
| **Unified network**   | Separate memory / retriever                     | **Single tensor** that holds both internal and RAG segments                                                                 |
| **Persistence**       | markers + meta                                  | now also stores RAG source registry                                                                                         |
| **Examples**          | `examples/basic_example.py`                     | **NEW** `examples/rag_example.py`, `StudSar_ragV3.py`                                                                       |

---

## System Overview (V3)

1. **Segmentation** – sentence‑based (spaCy) or word fallback.
2. **Marker generation** – embeddings via *Sentence Transformers* (`all‑MiniLM‑L6‑v2`).
3. **Storage** – markers live in `StudSarNeural.memory_embeddings`.
4. **Emotion + reputation + usage** attached to every marker.
5. **RAGConnector** – loads external sources, splits, embeds, saves into the **same** memory; adds two tags for filtering.
6. **Search** – cosine similarity (CPU/GPU) with optional tag filters.
7. **Persistence** – `manager.save()` writes **all** tensors + metadata to a single `.pth` file.

---

## Current Folder Layout

```
StudSar/
├── .env
├── examples/
│   ├── basic_example.py
│   └── rag_example.py
├── src/
│   ├── __init__.py
│   ├── managers/
│   │   └── manager.py
│   ├── models/
│   │   └── neural.py
│   ├── rag/
│   │   └── rag_connector.py
│   ├── utils/
│   │   └── text.py
├── visualizations/
│   └── studsar.py               # placeholder graph module
├── tests/
│   └── test_rag_integration.py
├── README.md                    # this file
├── requirements.txt
└── studsar_neural_demo.pth      # demo state file
```

---

## Quick Install (with RAG support)

```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt       # core
pip install -r requirements-rag.txt   # LangChain + loaders
```

---

## 5‑line Example

```python
from src.managers.manager import StudSarManager
from src.rag.rag_connector import RAGConnector

mgr = StudSarManager()
mgr.build_network_from_text("AI basics…")          # internal marker
rag = RAGConnector(mgr)
rag.add_document("whitepaper.pdf")                 # PDF segments -> same memory
print(mgr.search("machine learning", k=3))         # mixed results
```

---

## Road‑map → V4  (“Dream‑Mode Release”)

| Feature                      | Goal                                                               | Status             |
| ---------------------------- | ------------------------------------------------------------------ | ------------------ |
| **Dream Mode**               | nightly consolidation: promote high‑usage markers, prune low value | design ready       |
| **Transformer segmentation** | fine‑tuned chunker replaces spaCy                                  | dataset collection |
| **Integrated generator**     | small decoder Transformer trained end‑to‑end with retriever        | prototype          |
| **Realtime dashboard**       | Streamlit / FastAPI UI for memory & RAG                            | concept            |
| **Multilingual sentiment**   | auto language detection + multi‑lingual emotion model              | backlog            |
| **IDE / browser plugin**     | one‑click “Save to StudSar”, inline query                          | idea               |

---

## Licence & Contact

MIT • © 2025 Francesco Bulla  

# Empty file to indicate that 'src' is a package.

# Optional: Make key classes easily importable
try:
    from .managers.manager import StudSarManager
    from .models.neural import StudSarNeural
    from .rag.rag_connector import RAGConnector

    __all__ = ['StudSarManager', 'StudSarNeural', 'RAGConnector']
except ImportError:
    # Handle case where some dependencies might not be installed
    pass
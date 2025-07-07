"""
Vector store management for story retrieval.
"""

import faiss
import pickle
import numpy as np
from pathlib import Path
from typing import List, Dict, Optional
from sentence_transformers import SentenceTransformer
from .data_loader import StoryChunk


class IndexManager:
    """Manages FAISS vector store for story retrieval."""
    
    INDEX_PATH = "story_index.faiss"
    CHUNKS_PATH = "story_chunks.pkl"
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """Initialize the index manager.
        
        Args:
            model_name: Name of the sentence-transformers model to use
        """
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.chunks: List[StoryChunk] = []
        
        # Try to load existing index
        if Path(self.INDEX_PATH).exists() and Path(self.CHUNKS_PATH).exists():
            self.load_index()
        
    def build_index(self, chunks: List[StoryChunk]) -> None:
        """Build a FAISS index from story chunks.
        
        Args:
            chunks: List of StoryChunk objects to index
        """
        self.chunks = chunks
        texts = [chunk.text for chunk in chunks]
        embeddings = self.model.encode(texts)
        
        # Initialize FAISS index
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings.astype(np.float32))
        
        # Save index and chunks
        self.save_index()
        
    def save_index(self) -> None:
        """Save the FAISS index and story chunks to disk."""
        if self.index is not None:
            faiss.write_index(self.index, self.INDEX_PATH)
            with open(self.CHUNKS_PATH, 'wb') as f:
                pickle.dump(self.chunks, f)
                
    def load_index(self) -> None:
        """Load the FAISS index and story chunks from disk."""
        self.index = faiss.read_index(self.INDEX_PATH)
        with open(self.CHUNKS_PATH, 'rb') as f:
            self.chunks = pickle.load(f)
        
    def search(self, query: str, k: int = 3) -> List[StoryChunk]:
        """Search for similar stories.
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of most similar StoryChunk objects
        """
        if not self.index:
            raise ValueError("Index not built. Call build_index first.")
            
        # Encode query and search
        query_embedding = self.model.encode([query])
        distances, indices = self.index.search(query_embedding.astype(np.float32), k)
        
        # Return chunks for the found indices
        return [self.chunks[idx] for idx in indices[0]] 
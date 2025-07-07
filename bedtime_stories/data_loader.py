"""
Data loading utilities for bedtime stories.
"""

import pandas as pd
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class StoryChunk:
    """A chunk of story text with metadata."""
    text: str
    title: Optional[str] = None
    author: Optional[str] = None
    theme: Optional[str] = None
    age_range: Optional[str] = None
    chunk_index: int = 0
    story_id: Optional[str] = None


class CSVStoryLoader:
    """Loads stories from CSV files, treating each story as a single chunk."""

    REQUIRED_COLUMNS = ['stories']
    OPTIONAL_COLUMNS = ['title', 'author', 'theme', 'age_range']
    
    def load_stories(self, csv_path: str | Path) -> List[StoryChunk]:
        """Load stories from a CSV file.
        
        Args:
            csv_path: Path to the CSV file containing stories
            
        Returns:
            List of StoryChunk objects, one per story
        """
        df = pd.read_csv(csv_path)
        
        # Validate required columns
        missing_cols = [col for col in self.REQUIRED_COLUMNS if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
        
        chunks = []
        for idx, row in df.iterrows():
            # Create metadata dict with optional fields
            metadata = {
                col: row[col] if col in df.columns and pd.notna(row[col]) else None
                for col in self.OPTIONAL_COLUMNS
            }
            
            # Create chunk with story text and metadata
            chunk = StoryChunk(
                text=row['stories'],
                story_id=f"story_{idx}",
                **metadata
            )
            chunks.append(chunk)
            
        return chunks 
"""
Story generation and validation service.
"""

from typing import Dict, List, Optional, Tuple
from .data_loader import StoryChunk
from .prompt_builder import build_story_prompt
from .judge import evaluate_story
from openai import OpenAI
import os
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class BedtimeStoryService:
    """Service for generating and validating bedtime stories."""
    
    SCORE_THRESHOLD = 60  # Minimum acceptable score
    MAX_ATTEMPTS = 5      # Maximum number of generation attempts
    MODEL_NAME = "gpt-3.5-turbo"  # Using GPT-3.5-turbo for better cost efficiency
    
    def __init__(self):
        """Initialize the story service."""
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not found in environment variables")
        self.client = OpenAI(api_key=self.api_key)

    def _generate_story(self, prompt: Dict) -> str:
        """Generate a story using OpenAI's API.
        
        Args:
            prompt: The formatted prompt dictionary
            
        Returns:
            Generated story text
        """
        response = self.client.chat.completions.create(
            model=self.MODEL_NAME,
            messages=prompt["messages"],
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message.content

    def _extract_score(self, evaluation: str) -> float:
        """Extract the score from the evaluation text.
        
        Args:
            evaluation: The evaluation text from the judge
            
        Returns:
            Float score between 0 and 100
        """
        # Look for patterns like "93/100" or "Total: 93" or "Final Score: 93"
        score_patterns = [
            r"Total:\s*(\d+)/100",
            r"Final Score:\s*(\d+)/100",
            r"Total Score:\s*(\d+)/100",
            r"Score:\s*(\d+)/100",
            r"Total:\s*(\d+)\s*$",
            r"Final Score:\s*(\d+)\s*$",
            r"Total Score:\s*(\d+)\s*$",
            r"Score:\s*(\d+)\s*$"
        ]
        
        for pattern in score_patterns:
            match = re.search(pattern, evaluation, re.IGNORECASE | re.MULTILINE)
            if match:
                try:
                    return float(match.group(1))
                except ValueError:
                    continue
        
        # If no pattern matched, try to find any number followed by /100
        match = re.search(r"(\d+)/100", evaluation)
        if match:
            try:
                return float(match.group(1))
            except ValueError:
                pass
        
        return 0  # Default to 0 if no valid score found

    def _evaluate_and_get_feedback(self, story: str) -> Tuple[float, str]:
        """Evaluate story and get feedback using the judge.
        
        Args:
            story: The story text to evaluate
            
        Returns:
            Tuple of (score, feedback)
        """
        evaluation_prompt = evaluate_story(story)
        response = self.client.chat.completions.create(
            model=self.MODEL_NAME,
            messages=evaluation_prompt["messages"],
            temperature=0.3
        )
        
        evaluation = response.choices[0].message.content
        score = self._extract_score(evaluation)
            
        return score, evaluation

    def generate_story_with_feedback(self, theme: str, similar_chunks: List[StoryChunk]) -> Dict:
        """Generate a story with feedback loop until quality threshold is met.
        
        Args:
            theme: The story theme or request
            similar_chunks: Similar stories for inspiration
            
        Returns:
            Dictionary containing final story, score, and generation history
        """
        history = []
        best_score = 0
        best_story = ""
        best_feedback = ""
        
        for attempt in range(self.MAX_ATTEMPTS):
            # Generate story
            prompt = build_story_prompt(theme, similar_chunks)
            if attempt > 0:
                # Add previous feedback to the prompt for improvement
                prompt["messages"].append({
                    "role": "system",
                    "content": f"Previous attempt feedback: {history[-1]['feedback']}\nPlease improve the story based on this feedback while maintaining the original theme."
                })
            
            story = self._generate_story(prompt)
            score, feedback = self._evaluate_and_get_feedback(story)
            
            history.append({
                "attempt": attempt + 1,
                "story": story,
                "score": score,
                "feedback": feedback
            })
            
            # Update best story if current score is higher
            if score > best_score:
                best_score = score
                best_story = story
                best_feedback = feedback
            
            # Check if we've met the threshold
            if score >= self.SCORE_THRESHOLD:
                break
        
        return {
            "final_story": best_story,
            "final_score": best_score,
            "final_feedback": best_feedback,
            "attempts": len(history),
            "generation_history": history,
            "met_threshold": best_score >= self.SCORE_THRESHOLD
        } 
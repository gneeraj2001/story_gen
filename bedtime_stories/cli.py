"""
Command-line interface for bedtime story generation.
"""

import click
from .data_loader import CSVStoryLoader
from .index_manager import IndexManager
from .story_service import BedtimeStoryService
from .judge import evaluate_story
from openai import OpenAI
import os
from dotenv import load_dotenv
import json

load_dotenv()

# Use GPT-3.5-turbo for better cost efficiency
MODEL_NAME = "gpt-3.5-turbo"

@click.group()
def cli():
    """Bedtime story generation CLI."""
    pass

@cli.command()
@click.option('--csv', required=True, help='Path to stories CSV file')
def index(csv):
    """Build the story index from a CSV file."""
    try:
        # Load stories
        loader = CSVStoryLoader(csv)
        stories = loader.load()
        print(f"Loaded {len(stories)} stories from {csv}")
        
        # Build index
        index_mgr = IndexManager()
        index_mgr.build_index(stories)
        print("Successfully built story index")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        click.Abort()

@cli.command()
@click.argument('theme')
@click.option('--verbose', is_flag=True, help='Show detailed generation process')
def tell(theme, verbose):
    """Generate a bedtime story based on a theme."""
    try:
        # Initialize components
        index_mgr = IndexManager()
        story_service = BedtimeStoryService()
        
        # Get similar stories
        similar_stories = index_mgr.search(theme, k=3)
        
        # Generate story with feedback loop
        result = story_service.generate_story_with_feedback(theme, similar_stories)
        
        if verbose:
            # Show detailed generation process
            print("\n=== Generation Process ===")
            print(f"Attempts made: {result['attempts']}")
            print(f"Final score: {result['final_score']}")
            print(f"Met threshold: {result['met_threshold']}")
            print("\nGeneration History:")
            for attempt in result['generation_history']:
                print(f"\nAttempt {attempt['attempt']}:")
                print(f"Score: {attempt['score']}")
                print("Feedback:")
                print(attempt['feedback'])
                print("-" * 50)
        
        # Print final story
        print("\n=== Final Story ===")
        print(result['final_story'])
        
        if not result['met_threshold']:
            print("\nNote: This story did not meet the quality threshold, but it's the best version generated.")
            
    except Exception as e:
        print(f"Error: {str(e)}")
        click.Abort()

@cli.command()
@click.argument('story')
def judge(story):
    """Evaluate a bedtime story."""
    try:
        # Initialize OpenAI client
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key not found in environment variables")
        client = OpenAI(api_key=api_key)
        
        # Create evaluation prompt
        evaluation_prompt = evaluate_story(story)
        
        # Get evaluation from OpenAI
        response = client.chat.completions.create(
            model=MODEL_NAME,  # Use GPT-3.5-turbo
            messages=evaluation_prompt["messages"],
            temperature=0.3
        )
        
        # Print evaluation
        print("\n=== Story Evaluation ===")
        print(response.choices[0].message.content)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        click.Abort()

if __name__ == '__main__':
    cli() 
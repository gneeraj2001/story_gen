from setuptools import setup, find_packages

setup(
    name="bedtime_stories",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "langchain>=0.1.0",
        "langchain-core>=0.1.0",
        "langchain-openai>=0.0.5",
        "langgraph>=0.0.15",
        "pandas>=2.0.0",
        "click>=8.1.0",
        "python-dotenv>=1.0.0",
        "textstat>=0.7.3",
        "faiss-cpu>=1.7.4",
        "sentence-transformers>=2.2.2"
    ],
    entry_points={
        'console_scripts': [
            'bedtime_stories=bedtime_stories.cli:cli',
        ],
    },
) 
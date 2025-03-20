"""
Setup script for the Paper Summarizer Slack Bot.
"""

from setuptools import setup, find_packages

setup(
    name="paper-summarizer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "slack_sdk>=3.21.0",
        "openai>=1.3.0",
        "flask>=2.3.2",
        "python-dotenv>=1.0.0",
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.2",
        "PyPDF2>=3.0.1",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A Slack bot that summarizes academic papers using GPT-3o",
    keywords="slack, bot, academic, paper, summarizer, gpt",
    url="https://github.com/yourusername/paper-summarizer",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)

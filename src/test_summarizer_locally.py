#!/usr/bin/env python3
"""
Script to test the paper summarizer locally without Slack integration.
This is useful for development and testing.
"""

import os
import argparse
import logging
from dotenv import load_dotenv
from paper_processor import PaperProcessor
from summarizer import Summarizer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main function to run the local test."""
    # Load environment variables
    load_dotenv()
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Test the paper summarizer locally.')
    parser.add_argument('url', help='URL of the academic paper to summarize')
    args = parser.parse_args()
    
    # Check for OpenAI API key
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        logger.error("OPENAI_API_KEY environment variable is not set. Please set it in your .env file.")
        return
    
    try:
        # Initialize components
        paper_processor = PaperProcessor()
        summarizer = Summarizer(api_key=api_key)
        
        # Extract paper content
        logger.info(f"Extracting content from {args.url}...")
        paper_content = paper_processor.extract_paper_content(args.url)
        
        if not paper_content:
            logger.error(f"Failed to extract content from {args.url}")
            return
        
        # Generate summary
        logger.info("Generating summary...")
        summary = summarizer.generate_summary(paper_content)
        
        # Print summary
        print("\n" + "="*80)
        print(summary)
        print("="*80 + "\n")
        
        logger.info("Summary generation complete!")
        
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)


if __name__ == '__main__':
    main()

"""
Summarizer module for generating paper summaries using GPT-3o.
"""

import logging
from openai import OpenAI

logger = logging.getLogger(__name__)

class Summarizer:
    """Summarizer for generating paper summaries using GPT-3o."""
    
    def __init__(self, api_key):
        """
        Initialize the summarizer.
        
        Args:
            api_key (str): OpenAI API key
        """
        self.api_key = api_key
        self.client = OpenAI(api_key=api_key)
        
        # System prompt template for the first pass
        self.first_pass_prompt = """
        You are an academic paper summarizer following the methodology from "How to read a paper" by S. Keshav.
        
        For the FIRST PASS, analyze the paper and provide the five Cs:
        1. Category: What type of paper is this? (measurement, analysis of existing system, research prototype, etc.)
        2. Context: Which other papers is it related to? Which theoretical bases were used to analyze the problem?
        3. Correctness: Do the assumptions appear to be valid?
        4. Contributions: What are the paper's main contributions?
        5. Clarity: Is the paper well written?
        
        Focus only on these five aspects for the first pass. Be concise but thorough.
        """
        
        # System prompt template for the second pass
        self.second_pass_prompt = """
        For the SECOND PASS, provide a more detailed analysis:
        1. Analyze the figures, diagrams, and other illustrations. Are the axes properly labeled? Are results shown with error bars for statistical significance?
        2. Note any relevant references that would be important for understanding the paper's background.
        
        Provide a comprehensive summary of the paper's content with supporting evidence. Focus on the main thrust of the paper and its key findings.
        """
    
    def generate_summary(self, paper_content):
        """
        Generate a summary of the paper using GPT-3o.
        
        Args:
            paper_content (dict): Paper content with title, abstract, sections, etc.
            
        Returns:
            str: Generated summary
        """
        try:
            # Extract relevant parts of the paper
            title = paper_content.get('title', 'Unknown Title')
            abstract = paper_content.get('abstract', '')
            full_text = paper_content.get('full_text', '')
            sections = paper_content.get('sections', {})
            
            # Prepare content for the model
            introduction = sections.get('INTRODUCTION', sections.get('Introduction', ''))
            conclusion = sections.get('CONCLUSION', sections.get('Conclusions', 
                          sections.get('CONCLUSIONS', sections.get('Conclusion', ''))))
            
            # Prepare the user message with paper content
            user_message = f"""
            Paper Title: {title}
            
            Abstract: {abstract}
            
            Introduction: {introduction}
            
            Conclusion: {conclusion}
            
            Please provide a summary of this paper following the methodology from "How to read a paper" by S. Keshav.
            """
            
            # Generate first pass summary
            first_pass = self._generate_first_pass(user_message)
            
            # Generate second pass summary
            second_pass = self._generate_second_pass(user_message, full_text)
            
            # Combine the summaries
            combined_summary = f"""# Summary of "{title}"

## First Pass: The Five Cs

{first_pass}

## Second Pass: Detailed Analysis

{second_pass}

---
Summary generated using the methodology from "How to read a paper" by S. Keshav.
"""
            
            return combined_summary
            
        except Exception as e:
            logger.error(f"Error generating summary: {str(e)}", exc_info=True)
            return f"Error generating summary: {str(e)}"
    
    def _generate_first_pass(self, user_message):
        """
        Generate the first pass summary.
        
        Args:
            user_message (str): User message with paper content
            
        Returns:
            str: First pass summary
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # Replace with "gpt-3o" when available
                messages=[
                    {"role": "system", "content": self.first_pass_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error generating first pass: {str(e)}", exc_info=True)
            return "Error generating first pass summary."
    
    def _generate_second_pass(self, user_message, full_text):
        """
        Generate the second pass summary.
        
        Args:
            user_message (str): User message with paper content
            full_text (str): Full text of the paper
            
        Returns:
            str: Second pass summary
        """
        try:
            # Add a truncated version of the full text for more context
            truncated_text = full_text[:10000] + "..." if len(full_text) > 10000 else full_text
            
            second_pass_message = f"{user_message}\n\nAdditional paper content for analysis:\n{truncated_text}"
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # Replace with "gpt-3o" when available
                messages=[
                    {"role": "system", "content": self.second_pass_prompt},
                    {"role": "user", "content": second_pass_message}
                ],
                temperature=0.3,
                max_tokens=1500
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error generating second pass: {str(e)}", exc_info=True)
            return "Error generating second pass summary."

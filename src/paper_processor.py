"""
Paper processor module for extracting and processing academic papers.
"""

import re
import logging
import requests
from bs4 import BeautifulSoup
import PyPDF2
from io import BytesIO

logger = logging.getLogger(__name__)

class PaperProcessor:
    """Processor for extracting and handling academic paper content."""
    
    def __init__(self):
        """Initialize the paper processor."""
        # Common academic paper domains
        self.academic_domains = [
            'arxiv.org', 'ieee.org', 'acm.org', 'springer.com', 
            'sciencedirect.com', 'nature.com', 'researchgate.net',
            'ssrn.com', 'biorxiv.org', 'medrxiv.org', 'pnas.org',
            'acs.org', 'wiley.com', 'tandfonline.com', 'sagepub.com',
            'oup.com', 'frontiersin.org', 'mdpi.com', 'plos.org',
            'hindawi.com', 'elsevier.com', 'semanticscholar.org'
        ]
        
        # User agent for requests
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def extract_paper_url(self, text):
        """
        Extract academic paper URL from text.
        
        Args:
            text (str): Text to extract URL from
            
        Returns:
            str: Extracted URL or None if not found
        """
        if not text:
            return None
            
        # Regular expression to find URLs
        url_pattern = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
        urls = re.findall(url_pattern, text)
        
        # Check if any URL is from an academic domain
        for url in urls:
            if any(domain in url.lower() for domain in self.academic_domains):
                return url
                
        # If no academic domain found, return the first URL as a fallback
        return urls[0] if urls else None
    
    def extract_paper_content(self, url):
        """
        Extract content from an academic paper URL.
        
        Args:
            url (str): URL of the paper
            
        Returns:
            dict: Paper content with title, abstract, sections, etc.
        """
        try:
            # Handle different types of papers based on URL
            if 'arxiv.org' in url.lower():
                return self._extract_arxiv_paper(url)
            elif url.lower().endswith('.pdf'):
                return self._extract_pdf_paper(url)
            else:
                return self._extract_html_paper(url)
                
        except Exception as e:
            logger.error(f"Error extracting paper content: {str(e)}", exc_info=True)
            return None
    
    def _extract_arxiv_paper(self, url):
        """
        Extract content from an arXiv paper.
        
        Args:
            url (str): arXiv paper URL
            
        Returns:
            dict: Paper content
        """
        # Convert to PDF URL if it's an abstract page
        if '/abs/' in url:
            pdf_url = url.replace('/abs/', '/pdf/') + '.pdf'
        else:
            pdf_url = url
            
        return self._extract_pdf_paper(pdf_url)
    
    def _extract_pdf_paper(self, url):
        """
        Extract content from a PDF paper.
        
        Args:
            url (str): PDF paper URL
            
        Returns:
            dict: Paper content
        """
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        
        # Read PDF content
        pdf_file = BytesIO(response.content)
        reader = PyPDF2.PdfReader(pdf_file)
        
        # Extract text from PDF
        text = ""
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text()
        
        # Basic parsing of PDF content
        lines = text.split('\n')
        title = lines[0].strip() if lines else "Unknown Title"
        
        # Try to extract abstract
        abstract = ""
        abstract_start = False
        for line in lines:
            if 'abstract' in line.lower():
                abstract_start = True
                continue
            if abstract_start and line.strip() and not line.lower().startswith(('introduction', 'keywords')):
                abstract += line + " "
            if abstract_start and (line.lower().startswith('introduction') or line.lower().startswith('keywords')):
                break
        
        # Extract sections
        sections = {}
        current_section = None
        section_content = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check if this is a section header (simple heuristic)
            if (line.isupper() or line[0].isdigit()) and len(line) < 100:
                if current_section and section_content:
                    sections[current_section] = ' '.join(section_content)
                    section_content = []
                current_section = line
            elif current_section:
                section_content.append(line)
                
        # Add the last section
        if current_section and section_content:
            sections[current_section] = ' '.join(section_content)
        
        return {
            'title': title,
            'abstract': abstract,
            'full_text': text,
            'sections': sections,
            'source_url': url
        }
    
    def _extract_html_paper(self, url):
        """
        Extract content from an HTML paper.
        
        Args:
            url (str): HTML paper URL
            
        Returns:
            dict: Paper content
        """
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Try to extract title
        title = None
        title_tags = soup.find_all(['h1', 'h2'])
        for tag in title_tags:
            if tag.text.strip():
                title = tag.text.strip()
                break
        
        if not title:
            title = soup.title.text if soup.title else "Unknown Title"
        
        # Try to extract abstract
        abstract = ""
        abstract_section = soup.find('div', class_=lambda c: c and 'abstract' in c.lower())
        if not abstract_section:
            abstract_section = soup.find('section', class_=lambda c: c and 'abstract' in c.lower())
        if not abstract_section:
            abstract_section = soup.find('p', class_=lambda c: c and 'abstract' in c.lower())
            
        if abstract_section:
            abstract = abstract_section.text.strip()
        
        # Extract main content
        main_content = ""
        article_tag = soup.find('article')
        if article_tag:
            main_content = article_tag.text
        else:
            # Fallback to main content div
            main_div = soup.find('div', id='content')
            if not main_div:
                main_div = soup.find('div', class_='content')
            if main_div:
                main_content = main_div.text
            else:
                # Last resort: get all paragraph text
                paragraphs = soup.find_all('p')
                main_content = ' '.join([p.text for p in paragraphs])
        
        return {
            'title': title,
            'abstract': abstract,
            'full_text': main_content,
            'source_url': url
        }

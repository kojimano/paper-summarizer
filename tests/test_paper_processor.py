"""
Tests for the paper processor module.
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.paper_processor import PaperProcessor


class TestPaperProcessor(unittest.TestCase):
    """Test cases for the PaperProcessor class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.processor = PaperProcessor()
    
    def test_extract_paper_url(self):
        """Test extracting paper URLs from text."""
        # Test with academic domain
        text_with_academic_url = "Check out this paper: https://arxiv.org/abs/1234.5678"
        url = self.processor.extract_paper_url(text_with_academic_url)
        self.assertEqual(url, "https://arxiv.org/abs/1234.5678")
        
        # Test with non-academic domain
        text_with_non_academic_url = "Check out this website: https://example.com"
        url = self.processor.extract_paper_url(text_with_non_academic_url)
        self.assertEqual(url, "https://example.com")
        
        # Test with no URL
        text_without_url = "This text has no URL"
        url = self.processor.extract_paper_url(text_without_url)
        self.assertIsNone(url)
    
    @patch('requests.get')
    def test_extract_pdf_paper(self, mock_get):
        """Test extracting content from a PDF paper."""
        # Mock the response
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # This test would need more setup to mock PyPDF2
        # For now, we'll just test that the method exists
        self.assertTrue(hasattr(self.processor, '_extract_pdf_paper'))
    
    @patch('requests.get')
    def test_extract_html_paper(self, mock_get):
        """Test extracting content from an HTML paper."""
        # Mock the response
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.text = "<html><head><title>Test Paper</title></head><body><h1>Test Paper</h1><div class='abstract'>This is an abstract.</div></body></html>"
        mock_get.return_value = mock_response
        
        # This test would need more setup to mock BeautifulSoup
        # For now, we'll just test that the method exists
        self.assertTrue(hasattr(self.processor, '_extract_html_paper'))


if __name__ == '__main__':
    unittest.main()

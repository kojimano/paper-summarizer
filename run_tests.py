#!/usr/bin/env python3
"""
Script to run all tests for the Paper Summarizer Slack Bot.
"""

import unittest
import sys
import os

if __name__ == '__main__':
    # Add the project root to the path
    sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
    
    # Discover and run all tests
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests')
    
    test_runner = unittest.TextTestRunner(verbosity=2)
    result = test_runner.run(test_suite)
    
    # Exit with non-zero code if tests failed
    sys.exit(not result.wasSuccessful())

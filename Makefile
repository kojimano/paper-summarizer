# Makefile for Paper Summarizer Slack Bot

.PHONY: setup test run clean

# Setup the project
setup:
	pip install -r requirements.txt
	pip install -e .

# Run tests
test:
	python run_tests.py

# Run the application
run:
	python src/app.py

# Test the summarizer locally with a paper URL
test-summarizer:
	@echo "Usage: make test-summarizer URL=<paper_url>"
	@if [ -n "$(URL)" ]; then \
		python src/test_summarizer_locally.py "$(URL)"; \
	else \
		echo "Please provide a URL, e.g., make test-summarizer URL=https://arxiv.org/abs/1234.5678"; \
	fi

# Clean up build artifacts
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -name "__pycache__" -type d -exec rm -rf {} +
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete
	find . -name "*.pyd" -delete
	find . -name ".pytest_cache" -type d -exec rm -rf {} +
	find . -name ".coverage" -delete
	find . -name "htmlcov" -type d -exec rm -rf {} +

# Create a virtual environment
venv:
	python3 -m venv venv
	@echo "Virtual environment created. Activate with 'source venv/bin/activate'"

# Install development dependencies
dev-setup: setup
	pip install pytest pytest-cov black flake8

# Format code with black
format:
	black src/ tests/

# Lint code with flake8
lint:
	flake8 src/ tests/

# Run tests with coverage
coverage:
	pytest --cov=src tests/
	pytest --cov=src --cov-report=html tests/

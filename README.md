# Paper Summarizer Slack Bot

A Slack bot that summarizes academic papers using GPT-3o, following the methodology outlined in "How to read a paper" by S. Keshav.

## Features

- Triggered by `/summary` command in a Slack thread
- Extracts paper links from the parent message
- Generates a comprehensive summary using GPT-3o
- Follows Keshav's paper reading methodology:
  - First pass: 5C details (Category, Context, Correctness, Contributions, Clarity)
  - Second pass: Detailed analysis of figures, methods, and key points

## Project Structure

```
paper-summarizer/
├── docs/                       # Documentation
│   └── slack_app_setup.md      # Guide for setting up Slack app
├── scripts/                    # Utility scripts
│   └── deploy.sh               # Deployment script
├── src/                        # Source code
│   ├── __init__.py             # Package initialization
│   ├── app.py                  # Main Flask application
│   ├── paper_processor.py      # Paper extraction and processing
│   ├── slack_client.py         # Slack API interactions
│   ├── summarizer.py           # GPT-3o integration for summaries
│   └── test_summarizer_locally.py # Local testing script
├── tests/                      # Test suite
│   ├── __init__.py             # Test package initialization
│   └── test_paper_processor.py # Tests for paper processor
├── .dockerignore               # Docker ignore file
├── .env.example                # Example environment variables
├── .gitignore                  # Git ignore file
├── Dockerfile                  # Docker configuration
├── docker-compose.yml          # Docker Compose configuration
├── Makefile                    # Makefile for common commands
├── README.md                   # This file
├── requirements.txt            # Project dependencies
├── run_tests.py                # Script to run tests
└── setup.py                    # Package setup script
```

## Setup

### Prerequisites

- Python 3.8 or higher
- A Slack workspace with admin privileges
- An OpenAI API key with access to GPT-3o

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/paper-summarizer.git
   cd paper-summarizer
   ```

2. Create and activate a virtual environment:
   ```bash
   make venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   make setup
   ```

4. Create a `.env` file from the example:
   ```bash
   cp .env.example .env
   ```

5. Edit the `.env` file with your credentials:
   ```
   SLACK_BOT_TOKEN=xoxb-your-slack-bot-token
   SLACK_SIGNING_SECRET=your-slack-signing-secret
   OPENAI_API_KEY=your-openai-api-key
   PORT=3000
   ```

6. Set up your Slack app following the instructions in `docs/slack_app_setup.md`

### Running the Application

#### Local Development

Start the application:
```bash
make run
```

Or manually:
```bash
python src/app.py
```

#### Docker Deployment

You can also run the application using Docker:

```bash
# Build and start the container
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the container
docker-compose down
```

Make sure your `.env` file is set up with the required environment variables before running with Docker.

#### Server Deployment

A deployment script is provided to help you deploy the application to a remote server:

1. Edit the configuration in `scripts/deploy.sh` to match your server details:
   ```bash
   REMOTE_USER="your-username"
   REMOTE_HOST="your-server.com"
   REMOTE_DIR="/path/to/deployment"
   ```

2. Run the deployment script:
   ```bash
   ./scripts/deploy.sh
   ```

The script will build the Docker image locally, copy the necessary files to your remote server, and start the application using Docker Compose.

### Testing the Summarizer Locally

You can test the summarizer without setting up a Slack app:

```bash
# Using the Makefile
make test-summarizer URL=https://arxiv.org/abs/1706.03762

# Or directly
python src/test_summarizer_locally.py https://arxiv.org/abs/1706.03762
```

This will process the paper at the given URL and print the summary to the console.

### Development

Run tests:
```bash
make test
```

Clean up build artifacts:
```bash
make clean
```

Format code with Black (if installed):
```bash
make format
```

Run linting (if flake8 is installed):
```bash
make lint
```

Run tests with coverage (if pytest-cov is installed):
```bash
make coverage
```

## Usage

1. Share an academic paper link in a Slack channel
2. In a thread on that message, type `/summary`
3. The bot will analyze the paper and post a summary in the thread

## Summary Format

The summary follows Keshav's paper reading methodology:

### First Pass: The Five Cs

- **Category**: Type of paper (measurement, analysis, research prototype, etc.)
- **Context**: Related papers and theoretical bases
- **Correctness**: Validity of assumptions
- **Contributions**: Main contributions of the paper
- **Clarity**: Writing quality assessment

### Second Pass: Detailed Analysis

- Analysis of figures, diagrams, and illustrations
- Evaluation of methodology and results
- Comprehensive summary of key findings and implications

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

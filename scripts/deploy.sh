#!/bin/bash
# Simple deployment script for the Paper Summarizer Slack Bot
# This script can be customized based on your hosting environment

set -e  # Exit on error

# Configuration
REMOTE_USER="your-username"
REMOTE_HOST="your-server.com"
REMOTE_DIR="/path/to/deployment"
REPO_URL="https://github.com/yourusername/paper-summarizer.git"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Starting deployment of Paper Summarizer Slack Bot...${NC}"

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${RED}Error: .env file not found. Please create it before deploying.${NC}"
    exit 1
fi

# Build Docker image locally
echo -e "${GREEN}Building Docker image...${NC}"
docker-compose build

# Create deployment directory on remote server
echo -e "${GREEN}Setting up remote directory...${NC}"
ssh $REMOTE_USER@$REMOTE_HOST "mkdir -p $REMOTE_DIR"

# Copy necessary files to remote server
echo -e "${GREEN}Copying files to remote server...${NC}"
scp docker-compose.yml Dockerfile .env requirements.txt $REMOTE_USER@$REMOTE_HOST:$REMOTE_DIR
scp -r src $REMOTE_USER@$REMOTE_HOST:$REMOTE_DIR

# Deploy on remote server
echo -e "${GREEN}Deploying on remote server...${NC}"
ssh $REMOTE_USER@$REMOTE_HOST "cd $REMOTE_DIR && docker-compose up -d"

echo -e "${GREEN}Deployment completed successfully!${NC}"
echo -e "${YELLOW}To check logs on the remote server, run:${NC}"
echo -e "ssh $REMOTE_USER@$REMOTE_HOST \"cd $REMOTE_DIR && docker-compose logs -f\""

exit 0

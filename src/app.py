#!/usr/bin/env python3
"""
Main application file for the Paper Summarizer Slack Bot.
This file handles the Slack slash command and coordinates the paper processing and summarization.
"""

import os
import logging
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from slack_client import SlackClient
from paper_processor import PaperProcessor
from summarizer import Summarizer

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Initialize components
slack_client = SlackClient(
    token=os.environ.get('SLACK_BOT_TOKEN'),
    signing_secret=os.environ.get('SLACK_SIGNING_SECRET')
)
paper_processor = PaperProcessor()
summarizer = Summarizer(api_key=os.environ.get('OPENAI_API_KEY'))


@app.route('/slack/events', methods=['POST'])
def slack_events():
    """Handle Slack events and verify request signatures."""
    if not slack_client.verify_signature(request):
        return jsonify({"error": "Invalid request signature"}), 403
    
    return handle_slack_event(request.json)


@app.route('/slack/commands/summary', methods=['POST'])
def summary_command():
    """Handle the /summary slash command."""
    if not slack_client.verify_signature(request):
        return jsonify({"error": "Invalid request signature"}), 403
    
    # Acknowledge receipt of the command
    slack_client.acknowledge_command(response_url=request.form.get('response_url'))
    
    # Get thread information
    channel_id = request.form.get('channel_id')
    thread_ts = request.form.get('thread_ts')
    user_id = request.form.get('user_id')
    
    # If not in a thread, inform the user
    if not thread_ts:
        return jsonify({
            "response_type": "ephemeral",
            "text": "This command must be used in a thread containing a paper link."
        })
    
    # Process the request asynchronously
    process_summary_request(channel_id, thread_ts, user_id)
    
    return jsonify({
        "response_type": "ephemeral",
        "text": "Processing your request. I'll post the summary in this thread shortly."
    })


def process_summary_request(channel_id, thread_ts, user_id):
    """Process a summary request asynchronously."""
    try:
        # Get the parent message
        parent_message = slack_client.get_parent_message(channel_id, thread_ts)
        
        # Extract paper URL from parent message
        paper_url = paper_processor.extract_paper_url(parent_message.get('text', ''))
        
        if not paper_url:
            slack_client.post_message(
                channel=channel_id,
                thread_ts=thread_ts,
                text=f"<@{user_id}> I couldn't find a paper link in the parent message. Please make sure the parent message contains a valid academic paper URL."
            )
            return
        
        # Post initial status message
        slack_client.post_message(
            channel=channel_id,
            thread_ts=thread_ts,
            text=f"<@{user_id}> I'm analyzing the paper at {paper_url}. This may take a few minutes..."
        )
        
        # Extract paper content
        paper_content = paper_processor.extract_paper_content(paper_url)
        
        if not paper_content:
            slack_client.post_message(
                channel=channel_id,
                thread_ts=thread_ts,
                text=f"<@{user_id}> I had trouble extracting content from {paper_url}. Please ensure it's a valid and accessible academic paper."
            )
            return
        
        # Generate summary
        summary = summarizer.generate_summary(paper_content)
        
        # Post summary to thread
        slack_client.post_message(
            channel=channel_id,
            thread_ts=thread_ts,
            text=f"<@{user_id}> Here's the summary of the paper:\n\n{summary}"
        )
        
    except Exception as e:
        logger.error(f"Error processing summary request: {str(e)}", exc_info=True)
        slack_client.post_message(
            channel=channel_id,
            thread_ts=thread_ts,
            text=f"<@{user_id}> I encountered an error while processing your request: {str(e)}"
        )


def handle_slack_event(event_data):
    """Handle various Slack events."""
    # Handle events like app_mention, etc.
    event_type = event_data.get('type')
    
    if event_type == 'url_verification':
        return jsonify({"challenge": event_data.get('challenge')})
    
    # Add more event handling as needed
    
    return jsonify({"status": "ok"})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port, debug=True)

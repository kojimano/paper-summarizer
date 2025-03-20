"""
Slack client module for interacting with the Slack API.
"""

import hmac
import hashlib
import time
import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import requests

logger = logging.getLogger(__name__)

class SlackClient:
    """Client for interacting with Slack API."""
    
    def __init__(self, token, signing_secret):
        """
        Initialize the Slack client.
        
        Args:
            token (str): Slack bot token
            signing_secret (str): Slack signing secret for request verification
        """
        self.client = WebClient(token=token)
        self.signing_secret = signing_secret
    
    def verify_signature(self, request):
        """
        Verify that the request came from Slack.
        
        Args:
            request: Flask request object
            
        Returns:
            bool: True if signature is valid, False otherwise
        """
        if not self.signing_secret:
            logger.warning("No signing secret configured, skipping verification")
            return True
            
        # Get the timestamp and signature from the headers
        timestamp = request.headers.get('X-Slack-Request-Timestamp', '')
        slack_signature = request.headers.get('X-Slack-Signature', '')
        
        # Check if the timestamp is too old (>5 minutes)
        if abs(time.time() - float(timestamp)) > 60 * 5:
            logger.warning("Request timestamp is too old")
            return False
            
        # Create the signature base string
        request_body = request.get_data().decode('utf-8')
        sig_basestring = f"v0:{timestamp}:{request_body}"
        
        # Create the signature to compare
        my_signature = 'v0=' + hmac.new(
            self.signing_secret.encode(),
            sig_basestring.encode(),
            hashlib.sha256
        ).hexdigest()
        
        # Compare the signatures
        return hmac.compare_digest(my_signature, slack_signature)
    
    def post_message(self, channel, text, thread_ts=None, blocks=None):
        """
        Post a message to a Slack channel.
        
        Args:
            channel (str): Channel ID
            text (str): Message text
            thread_ts (str, optional): Thread timestamp to reply in a thread
            blocks (list, optional): Blocks for rich formatting
            
        Returns:
            dict: Response from Slack API
        """
        try:
            return self.client.chat_postMessage(
                channel=channel,
                text=text,
                thread_ts=thread_ts,
                blocks=blocks
            )
        except SlackApiError as e:
            logger.error(f"Error posting message: {e}")
            raise
    
    def get_parent_message(self, channel, thread_ts):
        """
        Get the parent message of a thread.
        
        Args:
            channel (str): Channel ID
            thread_ts (str): Thread timestamp
            
        Returns:
            dict: Parent message data
        """
        try:
            # The thread_ts is the timestamp of the parent message
            result = self.client.conversations_history(
                channel=channel,
                latest=thread_ts,
                inclusive=True,
                limit=1
            )
            
            if result["messages"] and len(result["messages"]) > 0:
                return result["messages"][0]
            else:
                logger.error("Parent message not found")
                return {}
                
        except SlackApiError as e:
            logger.error(f"Error getting parent message: {e}")
            raise
    
    def acknowledge_command(self, response_url):
        """
        Acknowledge a slash command to prevent timeout.
        
        Args:
            response_url (str): URL to send the acknowledgement to
        """
        try:
            requests.post(
                response_url,
                json={"text": "Processing your request..."},
                headers={"Content-Type": "application/json"}
            )
        except Exception as e:
            logger.error(f"Error acknowledging command: {e}")

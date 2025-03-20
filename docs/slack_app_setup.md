# Setting Up Your Slack App

This guide will walk you through the process of setting up a Slack app for the Paper Summarizer Bot.

## 1. Create a New Slack App

1. Go to [https://api.slack.com/apps](https://api.slack.com/apps)
2. Click "Create New App"
3. Choose "From scratch"
4. Enter "Paper Summarizer" as the app name
5. Select your workspace and click "Create App"

## 2. Configure App Features

### Basic Information

1. Under "Basic Information", note your "Signing Secret" - you'll need this for the `.env` file

### OAuth & Permissions

1. Navigate to "OAuth & Permissions" in the sidebar
2. Under "Bot Token Scopes", add the following scopes:
   - `channels:history` (to read channel messages)
   - `chat:write` (to post messages)
   - `commands` (to create slash commands)
   - `groups:history` (to read private channel messages)
   - `im:history` (to read direct messages)
   - `mpim:history` (to read group direct messages)
3. Click "Install to Workspace" at the top of the page
4. After installation, note your "Bot User OAuth Token" - you'll need this for the `.env` file

### Slash Commands

1. Navigate to "Slash Commands" in the sidebar
2. Click "Create New Command"
3. Fill in the following details:
   - Command: `/summary`
   - Request URL: `https://your-app-domain.com/slack/commands/summary` (replace with your actual domain)
   - Short Description: "Summarize an academic paper"
   - Usage Hint: "[paper link]"
4. Click "Save"

### Event Subscriptions

1. Navigate to "Event Subscriptions" in the sidebar
2. Toggle "Enable Events" to On
3. Set the Request URL to `https://your-app-domain.com/slack/events` (replace with your actual domain)
4. Under "Subscribe to bot events", add the following events:
   - `message.channels` (to receive channel messages)
   - `message.groups` (to receive private channel messages)
   - `message.im` (to receive direct messages)
   - `message.mpim` (to receive group direct messages)
5. Click "Save Changes"

## 3. Deploy Your App

1. Set up your server or hosting platform
2. Create a `.env` file with the following variables:
   ```
   SLACK_BOT_TOKEN=xoxb-your-bot-token
   SLACK_SIGNING_SECRET=your-signing-secret
   OPENAI_API_KEY=your-openai-api-key
   PORT=3000
   ```
3. Install dependencies: `pip install -r requirements.txt`
4. Run the app: `python src/app.py`

## 4. Test Your App

1. Invite your bot to a channel: `/invite @PaperSummarizer`
2. Share an academic paper link in the channel
3. In a thread on that message, type `/summary`
4. The bot should respond with a summary of the paper

## Troubleshooting

- If the bot doesn't respond, check your server logs for errors
- Verify that your Slack app is properly configured with the correct scopes and event subscriptions
- Ensure your server is publicly accessible and the Request URLs are correct
- Check that your environment variables are properly set

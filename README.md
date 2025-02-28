# FastAPI GitHub Webhook to Telegram Notifier

A FastAPI application that forwards GitHub repository events to Telegram, specifically designed to notify about issue updates.

## Features

* Listens for GitHub webhook events
* Filters for issue-related actions (opened, closed, reopened)
* Formats notifications with repository and issue details
* Sends formatted messages to Telegram
* Supports environment variables for configuration

## Requirements

* Python 3.9+
* Docker (for deployment)
* GitHub repository with webhook setup
* Telegram bot token and chat ID

## Installation

1. Clone the repository:
```bash
git clone "HTTPS WEB URL".
```

2. Create a `.env` file:
```bash
TOKEN=your_telegram_bot_token
CHAT_ID=your_telegram_chat_id
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

### Development Mode

```bash
uvicorn main:app --reload
```


## GitHub Webhook Setup

1. Go to your repository's Settings > Webhooks
2. Add a new webhook with:
   - Payload URL: `http://your-server-ip:8099/github-webhook/`
   - Content type: `application/json`
   - Events: Select "Issues"
   - Enable SSL verification

## Environment Variables

| Variable | Description | Required |
| --- | --- | --- |
| `TOKEN` | Telegram bot token | ✓ |
| `CHAT_ID` | Telegram chat ID | ✓ |

## Notification Format

The application sends formatted messages to Telegram with:
- Repository name and URL
- Issue title
- Issue status (opened/closed/reopened)
- Issue URL
- Author information


## License

[MIT License](https://opensource.org/licenses/MIT)
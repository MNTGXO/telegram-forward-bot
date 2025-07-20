
# Pure Python Telegram Forward Bot

A dependency-free Telegram bot for auto-forwarding messages between channels.

## Deployment

### Koyeb One-Click Deploy

[![Deploy to Koyeb](https://www.koyeb.com/static/images/deploy/button.svg)](https://app.koyeb.com/deploy?type=git&repository=YOUR_REPO_URL&env[BOT_TOKEN]=YOUR_BOT_TOKEN&env[ADMIN_IDS]=YOUR_ADMIN_IDS&name=forward-bot)

### Manual Setup

1. Set environment variables:
   ```bash
   export BOT_TOKEN="your_bot_token"
   export ADMIN_IDS="123,456"  # Comma-separated admin IDs
   ```

2. Run the bot:
   ```bash
   python bot.py
   ```

## Commands

- `/start` - Show help
- `/setchat [source] [target1,target2]` - Add forwarding rule
- `/delchat [source]` - Remove rule
- `/listchats` - List all rules

## Requirements

- Python 3.7+
- SQLite (included in Python)
- Telegram bot token from @BotFather


## How This Implementation Works:

1. **Pure Python**:
   - Uses only standard library modules (`http.client`, `sqlite3`, `json`)
   - No external dependencies

2. **Telegram API Interaction**:
   - Direct HTTP requests to Telegram's Bot API
   - Handles long-polling for updates

3. **Database**:
   - SQLite for persistent storage of forwarding rules
   - Simple table structure for source→target mappings

4. **Command Processing**:
   - Handles both private messages and channel posts
   - Admin-only configuration commands

5. **Deployment**:
   - Dockerfile for containerization
   - Ready for Koyeb one-click deployment

To deploy on Koyeb:
1. Push this code to a GitHub repository
2. Use the one-click deploy button
3. Set the environment variables (BOT_TOKEN and ADMIN_IDS)
4. The bot will start automatically

The bot will maintain all forwarding rules in the SQLite database between restarts.

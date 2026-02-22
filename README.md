
# WoW Discord Bot

A lightweight, asynchronous Discord bot built with `discord.py` to track the current World of Warcraft Token price for the European (EU) region.

## Features

- Real-time Price Checks: Get the current gold value of a WoW Token using the `!token` command.
- Character Inspector: Fetch detailed information about any character (Level, Class, iLvl, Race) using the `!pj` command.
- Smart OAuth2 Management: Automatically handles Blizzard API authentication, including token caching and renewal before expiration.
- Resilient Design: Features a built-in retry mechanism with exponential backoff for Blizzard API requests to handle temporary network issues.
- Clean UI: Displays data in organized Discord Embeds for a professional look.

## Getting Started

This project uses `uv` for lightning-fast dependency management.

1. Clone the repository

```bash
git clone https://github.com/Dvdandrades/WoW-Tracker-Discord-Bot.git
cd WoW-Tracker-Discord-Bot
```

2. Configure Enviroment Variables

The bot requires specific credentials to communicate with Discord and Blizzard. Create a `.env` file in the root directory:

```
DISCORD_TOKEN=your_discord_bot_token
BLIZZARD_CLIENT_ID=your_blizzard_client_id
BLIZZARD_CLIENT_SECRET=your_blizzard_client_secret
```

**Note**: Ensure `CLIENT_ID` and `CLIENT_SECRET` are correctly set, or the bot will raise a configuration error.

3. Install Dependencies

Using `uv`, you can set up your environment and install all requirements (`discord.py`, `aiohttp`, `python-dotenv`) with a single command:

```bash
uv sync
```

## Usage

To launch the bot, simply run:

```bash
uv run python main.py
```

Once the bot is online, go to your Discord server and type:

**!token**

The bot will fetch the latest price from the Blizzard API and respond with the current value in gold.

**!pj Name-Realm**

The bot will fetch information for a specific character from the Blizzard API and respond with a character breakdown.

## Testing

This project uses `pytest` to ensure everything is working correctly. You can run the test suite to verify the API integration and bot logic.

To run the tests, use the following command:

```bash
uv run pytest
```

## Requirements

- Python 3.12+ (Recommended).
- An application registered on the Discord Developer Portal.
- API credentials from the Blizzard Battle.net Developer Portal.

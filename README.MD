# hll-rcon-restart-bot

A tiny, secure Discord bot that posts a single button in a private
channel to restart your Hell Let Loose CRCON tool (`hll_rcon_tool`)
Docker container with one click.

Now available in **Node.js** *and* **Python**.

No more SSH-ing into the server just to run `docker compose restart`.

------------------------------------------------------------------------

## Features

-   One-button restart of the CRCON container\
-   Runs `docker compose down && docker compose up -d --remove-orphans`\
-   Shows full command output in an ephemeral reply\
-   Automatically cleans the channel on startup\
-   Fully configured via `.env` / environment variables\
-   Minimal permissions, tiny footprint

------------------------------------------------------------------------

## Requirements

### Common

-   Docker + docker-compose
-   A Discord bot token with:
    -   Send Messages\
    -   Manage Messages\
    -   Read Message History\
    -   Use Application Commands

### Node.js Version

-   Node.js ≥ 18

### Python Version

-   Python ≥ 3.10\
-   Dependencies from `requirements.txt`

------------------------------------------------------------------------

## Installation

### Clone Repository

``` bash
git clone https://github.com/2KU77B0N3S/hll-rcon-restart-bot.git
cd hll-rcon-restart-bot
```

------------------------------------------------------------------------

# Node.js Version

### Install dependencies

``` bash
npm install
```

### Configuration

``` bash
cp .env.example .env
```

Edit `.env` with:

    DISCORD_TOKEN=your_bot_token_here
    DISCORD_CHANNEL_ID=your_discord_channel_id_here
    CRCON_PATH=/root/hll_rcon_tool

### Run (development)

``` bash
node main.mjs
```

### Run (production)

``` bash
pm2 start main.mjs --name hll-rcon-restart
```

------------------------------------------------------------------------

# Python Version

### Install dependencies

``` bash
pip install -r requirements.txt
```

### Environment variables

Create `.env` manually or export variables:

    DISCORD_TOKEN=your_bot_token_here
    DISCORD_CHANNEL_ID=your_discord_channel_id_here
    CRCON_PATH=/root/hll_rcon_tool

### Run the bot

``` bash
python bot.py
```

------------------------------------------------------------------------

## Behavior on Startup

-   Deletes last 100 messages in configured channel\
-   Posts clean embed with **Restart RCON** button\
-   Clicking the button:
    -   Executes Docker restart
    -   Returns full output as private ephemeral message

------------------------------------------------------------------------

## Security

-   Restrict the channel to trusted admins\
-   Docker logs are always private\
-   No slash commands or message listeners\
-   Only the minimum required permissions are used

------------------------------------------------------------------------

## License

MIT

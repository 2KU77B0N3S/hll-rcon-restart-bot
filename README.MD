# hll-rcon-restart-bot

A tiny, secure Discord bot that posts a single button in a private channel to restart your Hell Let Loose CRCON tool (hll_rcon_tool) Docker container with one click.

No more SSH-ing into the server just to run `docker compose restart`.

## Features

- One-button restart of the CRCON container
- Runs `docker compose down && docker compose up -d --remove-orphans`
- Shows full command output in an ephemeral reply
- Automatically cleans the channel on startup (keeps it tidy)
- Fully configured via `.env` – no hard-coded IDs or paths
- Minimal permissions, tiny footprint

## Requirements

- Node.js ≥ 18
- Docker + docker-compose on the host
- A Discord bot token with `bot` scope and the following permissions in the target channel:
  - Send Messages
  - Manage Messages (for cleanup on start)
  - Read Message History
  - Use Application Commands (for buttons)

## Installation

```bash
git clone https://github.com/2KU77B0N3S/hll-rcon-restart-bot.git
cd hll-rcon-restart-bot
npm install

# Configuration

``` bash
cp .env.example .env
```

Edit `.env` with your values:

    DISCORD_TOKEN=your_bot_token_here
    DISCORD_CHANNEL_ID=your_discord_channel_id_here   # channel where the button will live
    CRCON_PATH=/root/hll_rcon_tool          # path to your hll_rcon_tool directory (must contain docker-compose.yml)

**Important:** `CRCON_PATH` must be accessible (read/write/execute) by
the user running the bot process.

# Running

``` bash
node main.mjs
```

For production (highly recommended):

``` bash
# Using pm2
pm2 start main.mjs --name hll-rcon-restart

# Or systemd, screen, tmux, Docker container, etc.
```

On startup the bot will:

-   Delete the last 100 messages in the configured channel\
-   Post a clean embed with the **Restart RCON** button

Clicking the button immediately restarts the container and returns the
full docker output privately (ephemeral message).

# Security considerations

-   The button only exists in the channel you specify -- restrict access
    to that channel to trusted admins only.\
-   All replies are ephemeral -- docker logs are never visible to
    others.\
-   The bot has no slash commands, no message listening, and no extra
    permissions beyond what's strictly needed.

# License

MIT

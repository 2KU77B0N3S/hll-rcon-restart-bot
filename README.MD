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

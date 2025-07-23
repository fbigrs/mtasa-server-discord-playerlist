# MTA:SA Discord Player List Bot

This repository contains a simple Discord bot written in Python that periodically posts the player list and status of an **Multi Theft Auto: San Andreas** (MTA:SA) server in a Discord channel.

The bot uses the MTA ASE query protocol to fetch server information such as the server name, map, and list of connected players. Every minute the bot edits a single embed message in the configured channel with the latest data and provides a "Connect" button for quick joining.

## Features

- Queries an MTA:SA server for its current status and player list.
- Posts the information as a rich embed in a Discord channel.
- Continuously updates the message every 60 seconds to keep information fresh.

## Setup

1. Install Python and the dependencies listed in `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

2. Create a Discord bot and obtain its token. Invite the bot to your server and note the channel ID where the embed should be posted.
3. Edit `config.ini` with your settings. Use the MTA:SA server IP address and its **ASE** query port (not the game port).
4. Run the bot:

   ```bash
   python app.py
   ```

The bot will connect to Discord and begin updating the embed in the specified channel.

## Configuration

`config.ini` holds the settings for the bot. Below is an overview:

```ini
[discord]
# Discord bot token and the channel where status will be posted
token = YOUR_BOT_TOKEN_HERE
channel_id = 123456789012345678

[server]
# IP address of your MTA:SA server
host = 127.0.0.1
#Short Server Name for Bot Activity Display
short_server_name = MVP
# ASE query port of the server (not the game port)
port = 22005
```

Adjust the values to match your server. The host should be the public IP of your MTA:SA server, and the port must be its ASE port so the bot can query player information.

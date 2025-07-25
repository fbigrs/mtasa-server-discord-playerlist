from __future__ import annotations

import configparser
from dataclasses import dataclass
from pathlib import Path

BANNER_URL = (
    "https://cdn.discordapp.com/attachments/1278491203905523854/"
    "1326757485356253305/MvP_banner_zoomed.jpg?ex=68387ff2&is=68372e72&hm="
    "8c8f4b0deb6961e58d59bbf06b0ae19dddc47dceded1c431c942bd25ea1a1edd&"
)


@dataclass
class BotConfig:
    token: str
    channel_id: int
    host: str
    port: int
    username: str | None = None
    password: str | None = None
    short_server_name: str | None = None
    connect_url: str | None = None
    thumbnail_url: str | None = None
    image_url: str | None = None
    welcome_channel_id: int | None = None
    leave_channel_id: int | None = None
    embed_color: str = "#ff9d00"
    banner_url: str = BANNER_URL
    welcome_title: str = "Welcome {member.name}!"
    welcome_description: str = ""
    welcome_color: str = "#43b581"
    leave_title: str = "{member.name} left."
    leave_description: str = ""
    leave_color: str = "#ff4b4b"
    footer_text: str = ""


def load_config(path: str | Path = 'config.ini') -> BotConfig:
    """Load configuration from an INI file."""
    parser = configparser.ConfigParser()
    parser.read(path)

    token = parser.get('discord', 'token', fallback=None)
    channel_id = parser.getint('embed', 'channel_id', fallback=None)
    host = parser.get('server', 'host', fallback='127.0.0.1')
    port = parser.getint('server', 'port', fallback=22005)
    username = parser.get('server', 'username', fallback=None)
    password = parser.get('server', 'password', fallback=None)
    short_server_name = parser.get('discord', 'short_server_name', fallback=None)
    connect_url = parser.get('embed', 'connect_url', fallback=None)
    thumbnail_url = parser.get('embed', 'thumbnail_url', fallback=None)
    image_url = parser.get('embed', 'image_url', fallback=None)
    embed_color = parser.get('embed', 'embed_color', fallback=None)
    footer_text = parser.get('embed', 'footer_text', fallback='')

    welcome_channel = parser.get('events', 'welcome_channel', fallback='👋🏻┊arrivers')
    leave_channel = parser.get('events', 'leave_channel', fallback='💻┊dc-logs')
    embed_color = parser.get('events', 'embed_color', fallback='#ff9d00')
    banner_url = parser.get('events', 'banner_url', fallback=BANNER_URL)
    welcome_title = parser.get('events', 'welcome_title', fallback='Welcome {member.name}!')
    welcome_description = parser.get('events', 'welcome_description', fallback='')
    welcome_color = parser.get('events', 'welcome_color', fallback='#43b581')
    leave_title = parser.get('events', 'leave_title', fallback='{member.name} left.')
    leave_description = parser.get('events', 'leave_description', fallback='')
    leave_color = parser.get('events', 'leave_color', fallback='#ff4b4b')

    welcome_channel_id = parser.getint('events', 'welcome_channel_id', fallback=None)
    leave_channel_id = parser.getint('events', 'leave_channel_id', fallback=None)
    embed_color = parser.get('events', 'embed_color', fallback='#ff9d00')
    banner_url = parser.get('events', 'banner_url', fallback=BANNER_URL)
    welcome_title = parser.get('events', 'welcome_title', fallback='Welcome {member.name}!')
    welcome_description = parser.get('events', 'welcome_description', fallback='')
    welcome_color = parser.get('events', 'welcome_color', fallback='#43b581')
    leave_title = parser.get('events', 'leave_title', fallback='{member.name} left.')
    leave_description = parser.get('events', 'leave_description', fallback='')
    leave_color = parser.get('events', 'leave_color', fallback='#ff4b4b')

    if token is None:
        raise RuntimeError('Discord token not configured')
    if channel_id is None:
        raise RuntimeError('Discord channel_id not configured')

    return BotConfig(
        token,
        channel_id,
        host,
        port,
        username,
        password,
        short_server_name,
        connect_url,
        thumbnail_url,
        image_url,
        welcome_channel_id,
        leave_channel_id,
        embed_color,
        banner_url,
        welcome_title,
        welcome_description,
        welcome_color,
        leave_title,
        leave_description,
        leave_color,
        footer_text,
    )

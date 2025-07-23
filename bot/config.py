from __future__ import annotations

import configparser
from dataclasses import dataclass
from pathlib import Path


@dataclass
class BotConfig:
    token: str
    channel_id: int
    host: str
    port: int
    username: str | None = None
    password: str | None = None


def load_config(path: str | Path = 'config.ini') -> BotConfig:
    """Load configuration from an INI file."""
    parser = configparser.ConfigParser()
    parser.read(path)

    token = parser.get('discord', 'token', fallback=None)
    channel_id = parser.getint('discord', 'channel_id', fallback=None)
    host = parser.get('server', 'host', fallback='127.0.0.1')
    port = parser.getint('server', 'port', fallback=22005)
    username = parser.get('server', 'username', fallback=None)
    password = parser.get('server', 'password', fallback=None)

    if token is None:
        raise RuntimeError('Discord token not configured')
    if channel_id is None:
        raise RuntimeError('Discord channel_id not configured')

    return BotConfig(token, channel_id, host, port, username, password)

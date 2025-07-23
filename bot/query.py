from __future__ import annotations

import json
import socket
import urllib.request
from typing import Any, Dict, List


def query_ase_players(host: str, port: int) -> Dict[str, Any]:
    """Query an MTA server using the ASE UDP protocol."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(2)
    try:
        sock.connect((host, port))
        sock.send(b's')
        data = sock.recv(16384)
        offset = 0

        def read_len_str() -> str:
            nonlocal offset
            if offset >= len(data):
                return ''
            strlen = data[offset]
            offset += 1
            value = data[offset:offset + strlen - 1].decode(errors='ignore') if strlen > 1 else ''
            offset += strlen - 1 if strlen > 1 else 0
            return value

        def read_byte() -> int:
            nonlocal offset
            if offset >= len(data):
                return 0
            b = data[offset]
            offset += 1
            return b

        # header
        offset += 4  # skip "EYE1"
        read_len_str()  # game
        read_len_str()  # port
        server_name = read_len_str()
        gamemode = read_len_str()
        map_name = read_len_str()
        version = read_len_str()
        passworded = bool(read_len_str())
        current_players = int(read_len_str())
        max_players = int(read_len_str())
        read_len_str()  # http port
        players = []
        for _ in range(current_players):
            read_byte()  # flags
            nick = read_len_str()
            team_len = read_byte()
            offset += team_len - 1 if team_len > 1 else 0
            skin_len = read_byte()
            offset += skin_len - 1 if skin_len > 1 else 0
            score_len = read_byte()
            offset += score_len - 1 if score_len > 1 else 0
            ping_len = read_byte()
            offset += ping_len - 1 if ping_len > 1 else 0
            time_len = read_byte()
            offset += time_len - 1 if time_len > 1 else 0
            players.append(nick)

        return {
            'server_name': server_name,
            'gamemode': gamemode,
            'map': map_name,
            'version': version,
            'passworded': passworded,
            'current_players': current_players,
            'max_players': max_players,
            'players': players,
        }
    except Exception:
        return {
            'server_name': None,
            'gamemode': None,
            'map': None,
            'version': None,
            'passworded': None,
            'current_players': 0,
            'max_players': 0,
            'players': [],
        }
    finally:
        sock.close()

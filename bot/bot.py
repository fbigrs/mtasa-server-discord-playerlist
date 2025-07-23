import configparser
import json
import urllib.request
import discord
from discord.ext import commands, tasks
import socket
import re


#5519587

class DiscordBot(commands.Bot):
    def __init__(self, config_path='config.ini'):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='!', intents=intents)
        self.config_path = config_path
        self.config = configparser.ConfigParser()
        self.token = None
        self.server_host = None
        self.server_port = None
        self.server_username = None  # Add username
        self.server_password = None  # Add password
        self.channel_id = None
        if 'discord' in self.config:
            self.channel_id = self.config['discord'].getint('channel_id')
        self.embed_message_id = None
        self.load_config()

    def load_config(self):
        self.config.read(self.config_path)
        if 'discord' in self.config:
            self.token = self.config['discord'].get('token')
            self.channel_id = self.config['discord'].getint('channel_id', fallback=None)
        if 'server' in self.config:
            self.server_host = self.config['server'].get('host', '127.0.0.1')
            self.server_port = self.config['server'].getint('port', 22005)
            self.server_username = self.config['server'].get('username')  # Read username
            self.server_password = self.config['server'].get('password')  # Read password

    async def on_ready(self):
        print(f'Logged in as {self.user}!')
        if not update_embed.is_running():
            update_embed.start()

    def run_bot(self):
        if not self.token:
            raise RuntimeError('Discord token not configured')
        super().run(self.token)

    def query_players(self):
        """Retrieve player list from the configured MTA server."""
        if not self.server_host:
            return []
        url = f"http://{self.server_host}:{self.server_port}/players"
        try:
            request = urllib.request.Request(url)
            if self.server_username and self.server_password:
                import base64
                credentials = f"{self.server_username}:{self.server_password}"
                encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
                request.add_header('Authorization', f'Basic {encoded_credentials}')
            with urllib.request.urlopen(request) as resp:
                data = json.loads(resp.read().decode())
            return data.get('players', [])
        except Exception as exc:
            print(f'Failed to query MTA server: {exc}')
            return []

    def query_ase_players(self, host, port):
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(2)
        try:
            sock.connect((host, port))
            sock.send(b's')
            data = sock.recv(16384)
            print("Raw ASE response:", data)
            # Parse the binary ASE response using length-prefixed fields as in ASE.cpp
            offset = 0
            def read_len_str():
                nonlocal offset
                if offset >= len(data):
                    return ''
                strlen = data[offset]
                offset += 1
                s = data[offset:offset+strlen-1].decode(errors='ignore') if strlen > 1 else ''
                offset += strlen-1 if strlen > 1 else 0
                return s
            def read_byte():
                nonlocal offset
                if offset >= len(data):
                    return 0
                b = data[offset]
                offset += 1
                return b
            # Header ("EYE1"), 4 bytes
            header = data[offset:offset+4].decode(errors='ignore')
            offset += 4
            _ = read_len_str()  # game
            _ = read_len_str()  # port
            server_name = read_len_str()
            gamemode = read_len_str()
            map_name = read_len_str()
            version = read_len_str()
            passworded = bool(read_len_str())
            current_players = int(read_len_str())
            max_players = int(read_len_str())
            _ = read_len_str()  # http port
            player_names = []
            for _ in range(current_players):
                flags = read_byte()
                # Nick
                nick = read_len_str()
                # Team (skip)
                team_len = read_byte()
                offset += team_len - 1 if team_len > 1 else 0
                # Skin (skip)
                skin_len = read_byte()
                offset += skin_len - 1 if skin_len > 1 else 0
                # Score (skip)
                score_len = read_byte()
                offset += score_len - 1 if score_len > 1 else 0
                # Ping (skip)
                ping_len = read_byte()
                offset += ping_len - 1 if ping_len > 1 else 0
                # Time (skip)
                time_len = read_byte()
                offset += time_len - 1 if time_len > 1 else 0
                player_names.append(nick)
            response = {
                'server_name': server_name,
                'gamemode': gamemode,
                'map': map_name,
                'version': version,
                'passworded': passworded,
                'current_players': current_players,
                'max_players': max_players,
                'players': player_names
            }
            print("ASE Parsed Response:", dict(sorted(response.items())))
            return response
        except Exception as e:
            print(f"ASE query failed: {e}")
            return {
                'server_name': None,
                'gamemode': None,
                'map': None,
                'version': None,
                'passworded': None,
                'current_players': 0,
                'max_players': 0,
                'players': []
            }
        finally:
            sock.close()

bot = DiscordBot()

@tasks.loop(seconds=60)
async def update_embed():
    channel = bot.get_channel(bot.channel_id)
    if channel is None:
        print(f"Channel with ID {bot.channel_id} not found.")
        return

    # Find the bot's last message in the channel, or send a new one if not found
    async for message in channel.history(limit=50):
        if message.author == bot.user and message.embeds:
            embed_message = message
            break
    else:
        embed_message = await channel.send("Loading server info...")

    # Build the embed as before
    info = bot.query_ase_players(bot.server_host, 22426)
    server_name = info.get('server_name') or 'Unknown'
    map_name = info.get('map') or 'Unknown'
    player_list = info.get('players', [])
    current_players = info.get('current_players') if 'current_players' in info else None
    max_players = info.get('max_players') if 'max_players' in info else None
    status = "Online" if player_list is not None else "Offline"

    embed = discord.Embed(
        title=f"{server_name} - Server Status",
        color=discord.Color.green() if status == "Online" else discord.Color.red()
    )
    embed.add_field(name="> Status", value=f"```{'🟢' if status == 'Online' else '🔴'} {status}```", inline=True)
    embed.add_field(name="> Players", value=f"```{current_players}/{max_players}```", inline=True)
    embed.add_field(name="> Map", value=f"```{map_name}```", inline=False)
    if player_list:
        embed.add_field(name="> Player List", value="```\n" + "\n".join(player_list) + "\n```", inline=False)
    else:
        embed.add_field(name="> Player List", value="```No players online.```", inline=False)
    embed.set_thumbnail(url="https://pixelz.xyz/ajIBYIyF.png")
    embed.set_image(url="https://pixelz.xyz/IZT0H4r7.webp")

    from discord.ui import View, Button
    view = View()
    connect_url = "https://tinyurl.com/mtamvp1337"
    button = Button(label="Connect", url=connect_url, style=discord.ButtonStyle.link)
    view.add_item(button)

    await embed_message.edit(content=None, embed=embed, view=view)


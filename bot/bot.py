import configparser
import json
import urllib.request
import discord
from discord.ext import commands

class DiscordBot(commands.Bot):
    def __init__(self, config_path='config.ini'):
        intents = discord.Intents.default()
        super().__init__(command_prefix='!', intents=intents)
        self.config_path = config_path
        self.config = configparser.ConfigParser()
        self.token = None
        self.server_host = None
        self.server_port = None
        self.load_config()

    def load_config(self):
        self.config.read(self.config_path)
        if 'discord' in self.config:
            self.token = self.config['discord'].get('token')
        if 'server' in self.config:
            self.server_host = self.config['server'].get('host', '127.0.0.1')
            self.server_port = self.config['server'].getint('port', 22005)

    async def on_ready(self):
        print(f'Logged in as {self.user}!')

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
            with urllib.request.urlopen(url) as resp:
                data = json.loads(resp.read().decode())
            return data.get('players', [])
        except Exception as exc:
            print(f'Failed to query MTA server: {exc}')
            return []

bot = DiscordBot()

@bot.command(name='players')
async def players(ctx: commands.Context):
    player_list = bot.query_players()
    if not player_list:
        await ctx.send('No players online or unable to query server.')
        return

    message = '**Online Players:**\n'
    for p in player_list:
        if isinstance(p, dict):
            message += f"- {p.get('name', 'Unknown')}\n"
        else:
            message += f"- {p}\n"
    await ctx.send(message)

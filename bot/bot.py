from __future__ import annotations

import discord
from discord.ext import commands, tasks

from .config import BotConfig, load_config
from .query import query_ase_players


class DiscordBot(commands.Bot):
    """Discord bot that periodically posts MTA server information."""

    def __init__(self, config: BotConfig) -> None:
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='!', intents=intents)
        self.config = config
        self.embed_message = None

    async def on_ready(self) -> None:
        print(f'Logged in as {self.user}!')
        if not self.update_embed.is_running():
            self.update_embed.start()

    def run_bot(self) -> None:
        super().run(self.config.token)

    @tasks.loop(seconds=60)
    async def update_embed(self) -> None:
        channel = self.get_channel(self.config.channel_id)
        if channel is None:
            print(f"Channel with ID {self.config.channel_id} not found.")
            return

        if self.embed_message is None:
            async for message in channel.history(limit=50):
                if message.author == self.user and message.embeds:
                    self.embed_message = message
                    break
            else:
                self.embed_message = await channel.send("Loading server info...")

        info = query_ase_players(self.config.host, 22426)
        server_name = info.get('server_name') or 'Unknown'
        map_name = info.get('map') or 'Unknown'
        players = info.get('players', [])
        current_players = info.get('current_players')
        max_players = info.get('max_players')
        status = "Online" if players is not None else "Offline"

        embed = discord.Embed(
            title=f"{server_name} - Server Status",
            color=discord.Color.green() if status == 'Online' else discord.Color.red(),
        )
        embed.add_field(name="> Status", value=f"```{'🟢' if status == 'Online' else '🔴'} {status}```", inline=True)
        embed.add_field(name="> Players", value=f"```{current_players}/{max_players}```", inline=True)
        embed.add_field(name="> Map", value=f"```{map_name}```", inline=False)
        if players:
            embed.add_field(name="> Player List", value="```\n" + "\n".join(players) + "\n```", inline=False)
        else:
            embed.add_field(name="> Player List", value="```No players online.```", inline=False)
        embed.set_thumbnail(url="https://pixelz.xyz/ajIBYIyF.png")
        embed.set_image(url="https://pixelz.xyz/IZT0H4r7.webp")

        from discord.ui import View, Button
        view = View()
        button = Button(label="Connect", url="https://tinyurl.com/mtamvp1337", style=discord.ButtonStyle.link)
        view.add_item(button)

        await self.embed_message.edit(content=None, embed=embed, view=view)


def create_bot(config_path: str = 'config.ini') -> DiscordBot:
    return DiscordBot(load_config(config_path))

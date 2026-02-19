import logging
import discord

from config import TOKEN, GUILD


handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")

class MyClient(discord.Client):
    async def on_ready(self):
        for guild in self.guilds:
            if guild.name == GUILD:
                break

        print(
            f'{self.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})\n'
        )

        members = "\n - ".join([member.name for member in guild.members])
        print(f"Guild Members:\n - {members}")

intents = discord.Intents.default()

client = MyClient(intents=intents)

client.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)
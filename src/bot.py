import logging
import discord
from discord.ext import commands

from config import TOKEN


handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


class Bot(discord.Client):
    @bot.event
    async def on_ready(self):
        print(f"¡Bot conectado como {self.user}!")

    @bot.command()
    async def token(ctx):
        pass


client = Bot(intents=intents)

if __name__ == "__main__":
    client.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)

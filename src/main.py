import logging
import discord
from discord.ext import commands

from config import TOKEN, BLIZZARD_CLIENT_ID, BLIZZARD_CLIENT_SECRET
from commands import get_token_price
from api_client import BlizzardAPIClient


handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")

blizzard_client = BlizzardAPIClient(BLIZZARD_CLIENT_ID, BLIZZARD_CLIENT_SECRET)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"¡Bot conectado como {bot.user.name}!")


@bot.command()
async def token(ctx):
    try:
        price = await get_token_price(blizzard_client)
        embed = discord.Embed(
            title="Precio del Token de WoW",
            description=f"El precio actual del token es: {price:,.0f} oro",
            color=discord.Color.gold(),
        )
        await ctx.send(embed=embed)
    except Exception as e:
        logging.error(f"Error en comando token: {e}")
        await ctx.send("Error al obtener el precio del token.")


if __name__ == "__main__":
    if not TOKEN:
        print("No se encontró el token de Discord")
    else:
        bot.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)

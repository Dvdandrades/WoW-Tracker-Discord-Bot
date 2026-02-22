import logging
import discord
from discord.ext import commands

from src.config import TOKEN, BLIZZARD_CLIENT_ID, BLIZZARD_CLIENT_SECRET
from src.commands import get_token_price
from src.api_client import BlizzardAPIClient


handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")

blizzard_client = BlizzardAPIClient(BLIZZARD_CLIENT_ID, BLIZZARD_CLIENT_SECRET)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready() -> None:
    print(f"Bot connected as {bot.user}")


@bot.command()
async def token(ctx: commands.Context) -> None:
    try:
        price = await get_token_price(blizzard_client)
        embed = discord.Embed(
            title="Wow Token Price",
            description=f"Current price: {price:,.0f} gold",
            color=discord.Color.gold(),
        )
        await ctx.send(embed=embed)
    except Exception as e:
        logging.error(f"Error fetching token price: {e}")
        await ctx.send("Sorry, I couldn't fetch the token price at the moment.")


if __name__ == "__main__":
    if not TOKEN:
        print("Discord token not found.")
    else:
        bot.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)

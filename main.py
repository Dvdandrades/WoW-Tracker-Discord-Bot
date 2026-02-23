import logging
import discord
from discord.ext import commands

from src.config import TOKEN, BLIZZARD_CLIENT_ID, BLIZZARD_CLIENT_SECRET
from src.commands import get_token_price, get_character_info
from src.api_client import BlizzardAPIClient


handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")


class WoWBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)
        self.blizzard_client = BlizzardAPIClient(
            BLIZZARD_CLIENT_ID, BLIZZARD_CLIENT_SECRET
        )

    async def setup_hook(self):
        await self.blizzard_client.__aenter__()

    async def close(self):
        await self.blizzard_client.__aexit__(None, None, None)
        await super().close()


bot = WoWBot()


@bot.event
async def on_ready() -> None:
    print(f"Bot connected as {bot.user}")


@bot.command()
async def token(ctx: commands.Context) -> None:
    try:
        price = await get_token_price(bot.blizzard_client)
        embed = discord.Embed(
            title="Wow Token Price",
            description=f"Current price: {price:,.0f} gold",
            color=discord.Color.gold(),
        )
        await ctx.send(embed=embed)
    except Exception as e:
        logging.error(f"Error fetching token price: {e}")
        await ctx.send("Sorry, I couldn't fetch the token price at the moment.")


@bot.command()
async def pj(ctx: commands.Context, *, character_data: str) -> None:
    async with ctx.typing():
        try:
            info = await get_character_info(bot.blizzard_client, character_data)

            color = (
                discord.Color.blue()
                if info.faction == "Alliance"
                else discord.Color.red()
            )
            embed = discord.Embed(title=f"{info.name}", color=color)
            embed.add_field(name="Level", value=info.level, inline=False)
            embed.add_field(
                name="Class",
                value=f"{info.character_class} - {info.spec}",
                inline=False,
            )
            embed.add_field(name="Item Level", value=info.ilvl, inline=False)
            embed.add_field(name="Race", value=info.race, inline=False)

            await ctx.send(embed=embed)
        except ValueError as e:
            await ctx.send(e)
        except Exception as e:
            logging.error(f"Error fetching character info: {e}")
            await ctx.send("Sorry, I couldn't fetch the character information.")


if __name__ == "__main__":
    if not TOKEN:
        print("Discord token not found.")
    else:
        bot.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)

import os
import discord
from discord import app_commands
import datetime as dt

from utils import get_menu_dishes, get_nutrients, table

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


def get_menu(date: str):
    dishes = get_menu_dishes(date)
    menu_items = []
    for dish in dishes:
        nutrients = get_nutrients(dish["slug"])
        menu_items.append([dish["title"][:30]] + nutrients)
    return menu_items


@tree.command(
    name="menu",
    description="Get Slorest daily menu. Optionally provide a date in the format YYYY-MM-DD.",
    guild=discord.Object(id=1158479972848115794),
)
async def menu(ctx, date: str = ""):
    if not date:
        date = dt.date.today().isoformat()

    menu_items = get_menu(date)
    title = "### Menu for " + date + ":\n"
    await ctx.response.send_message(title + table(menu_items))


@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=1158479972848115794))
    print("Ready!")


TOKEN = os.getenv("DISCORD_TOKEN")  # Replace with your actual token

client.run(TOKEN)

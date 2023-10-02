# This example requires the 'message_content' privileged intents

import os
import discord
from discord.ext import commands


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.command()
async def hello(ctx):
    await ctx.send('Hello, World!')


bot.run(os.environ["DISCORD_TOKEN"])

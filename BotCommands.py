import discord
import os
from discord.ext import commands

token = open("token.txt", "r").read()

client = commands.Bot(command_prefix = '!')

@client.command()
async def load(ctx, extension):
    client.load_extension("cogs." + extension)

@client.command()
async def unload(ctx, extension):
    client.unload_extension("cogs." + extension)

for filename in os.listdir("./cogs"):
    if filename.endswith('.py'):
        client.load_extension("cogs." + filename[:-3])

client.run(token)
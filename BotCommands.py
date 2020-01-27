import discord
import os
import json

from discord.ext import commands

with open('gamefiles/token.txt', 'r+') as file:
    stuff = json.load(file)
    file.close()
token = stuff["token"]

client = commands.Bot(command_prefix = '!')
#client.remove_command('help')

@client.command()
async def load(ctx, extension):
    client.load_extension("cogs." + extension)

@client.command()
async def unload(ctx, extension):
    client.unload_extension("cogs." + extension)

@client.command()
async def reload(ctx, extension):
    client.unload_extension("cogs." + extension)
    client.load_extension("cogs." + extension)

for filename in os.listdir("./cogs"):
    if filename.endswith('.py'):
        client.load_extension("cogs." + filename[:-3])

client.run(token)
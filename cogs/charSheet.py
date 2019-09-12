import discord
from discord.ext import commands
import os
import json
from pathlib import Path

class Sheet(commands.Cog):

    def __init__(self, client):
        self.client = client


    # @commands.command()
    # @commands.dm_only()
    # async def viewchar(self, ctx):
    #
    #     private = ctx.author.send
    #     player = str(ctx.message.author.id)
    #
    #     path = os.getcwd()
    #     charFolder = os.path.join(path + "/characters/")
    #     charFile = Path(charFolder + player + ".txt")
    #     file = open(charFolder + player + ".txt", "r", encoding="utf-8")
    #     charStats = json.load(file)
    #     file.close()
    #
    #     # Find out if player even has a character created yet. If not. Tell them they are an idiot.
    #     msg = pri_viewchar(character)
    #     for msg_item in msg:
    #         await ctx.send( msg_item)
    #
    #
    # @viewchar.error
    # async def stats_error(self, ctx, error):
    #     if isinstance(error, commands.PrivateMessageOnly):
    #         await ctx.send("You're an idiot, now everyone knows. Why would you want to display your character sheet "
    #                        "in a public room? PM me with the command.")
    #     else:
    #         raise error

def setup(client):
    client.add_cog(Sheet(client))
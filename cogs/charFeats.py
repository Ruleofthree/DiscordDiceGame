import discord
import os
import json

from pathlib import Path
from discord.ext import commands
# from onPRIUtil import *


# a simple function designed to open up the feats json, and parse out all the keys into a separate list. Intended for
# ease of use in other modules. Works as intended in charFeats.py
def featDict():
    # Open up the json object containing the list of feats.
    path = os.getcwd()
    charFolder = os.path.join(path + "/cogs/")
    featFile = open(charFolder + "feats.txt", "r", encoding="utf-8")
    featDictionary = json.load(featFile)
    featFile.close()

    # place all keys within a list for comparison later
    featList = []
    for keys in featDictionary[0]:
        featList.append(keys)
    return featDictionary, featList

class Feats(commands.Cog):

    def __init__(self, client):
        self.client = client

    # @commands.command()
    # @commands.dm_only()
    # async def featlist(self, ctx):
    #
    #     stringList = "\n".join(featList)
    #     await ctx.send( stringList + "\n Type: !feat help <feat name>[/color] to get a PM of feat info\n"
    #                                         "or just go "
    #                                         "https://docs.google.com/document/d/1CJjC0FxunXXi8zh1I9fZqRrWij9oJiIfIZoxrPJ7GYQ/edit?usp=sharing")
    #
    # @featlist.error
    # async def name_featlist(self, ctx, error):
    #     if isinstance(error, commands.PrivateMessageOnly):
    #         await ctx.send("I'm not gonna spam the arena with this list, man. PM me with !featlist")
    #     else:
    #         raise error

    # @commands.command()
    # @commands.dm_only()
    # async def feathelp(self, ctx, *, answer):
    #
    #     if answer not in featList:
    #         await ctx.send( "Make sure you have spelled the feat correctly")
    #     else:
    #         reqStat = featDictionary[0][answer]['stat']
    #         featStatus = featDictionary[0][answer]['status']
    #         level = featDictionary[0][answer]['requirements'][0]
    #         reqStr = featDictionary[0][answer]['requirements'][1]
    #         reqDex = featDictionary[0][answer]['requirements'][2]
    #         reqCon = featDictionary[0][answer]['requirements'][3]
    #         reqFeats = featDictionary[0][answer]['requirements'][4]
    #         await ctx.send(answer + " (" + reqStat + ") (" + featStatus + ")\n" +
    #                     featDictionary[0][answer]['desc'] +
    #                     "\nPrerequisites: " + "\nLevel: " + str(level) + " Strength: " + str(
    #             reqStr) + " Dexterity: " +
    #                     str(reqDex) + " Constitution: " + str(reqCon) + " Required Feats: " + reqFeats)
    #
    # @feathelp.error
    # async def name_feathelp(self, ctx, error):
    #     if isinstance(error, commands.PrivateMessageOnly):
    #         await ctx.send("I'm not gonna spam the arena with this list, man. PM me with !feathelp <feat> for assistance.")
    #
    #     if isinstance(error, commands.MissingRequiredArgument):
    #         await ctx.send("I need the name of the feat you want help on. I can't read minds.")
    #
    #     raise error

    # @commands.command()
    # @commands.dm_only()
    # async def feat(self, ctx, *, answer):
    #
    #     private = ctx.author.send
    #     player = str(ctx.message.author.id)
    #
    #     featDictionary = featDict()[0]
    #     featList = featDict()[1]
    #
    #     path = os.getcwd()
    #     charFolder = os.path.join(path + "/characters/")
    #     # charFile = Path(charFolder + player + ".txt")
    #     file = open(charFolder + player + ".txt", "r", encoding="utf-8")
    #     charData = json.load(file)
    #     file.close()
    #
    #     msg = pri_10_feat_pick(character, message, featList, featDictionary)
    #     for msg_item in msg:
    #         await ctx.send( msg_item)
    #
    # @feat.error
    # async def name_feat(self, ctx, error):
    #     if isinstance(error, commands.PrivateMessageOnly):
    #         await ctx.send(
    #             "Hey! Good work! You just told everyone what feat you are going to take! Now PM me with !feat <feat> to"
    #             " do it correctly.")
    #     else:
    #         raise error

def setup(client):
    client.add_cog(Feats(client))
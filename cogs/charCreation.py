import discord
import os
import json
from pathlib import Path
from discord.ext import commands


class Character(commands.Cog):

    def __init__(self, client):
        self.client = client

    # @commands.command()
    # @commands.guild_only()
    # async def name(self, ctx, name):
    #
    #     name.capitalize()
    #     player = str(ctx.message.author.id)
    #     path = os.getcwd()
    #     charFolder = os.path.join(path + "/characters/")
    #     charFile = Path(charFolder + player + ".txt")
    #
    #     # make sure that this command cannot be ran if a fight is taking place.
    #     msg = message_5_name(channel, charFolder, message, charFile, character, self.game)
    #     for msg_item in msg:
    #         super().MSG(channel, msg_item)
    #
    # @name.error
    # async def name_error(self, ctx, error):
    #     if isinstance(error, commands.NoPrivateMessage):
    #         await ctx.send("The command !name may not be used in PMs!")
    #     if isinstance(error, commands.MissingRequiredArgument):
    #         await ctx.send("Give your character a name. You can't just be "". Do you have any idea how hard that "
    #                        "be to keep track of? Watch: ")
    #         await ctx.send("     hit      for 9 points of damage.")
    #         await ctx.send("What? No. Type !name <name> (Example: !name joe)")
    #     else:
    #         raise error

    # @commands.command()
    # @commands.dm_only()
    # async def stats(self, ctx, strength, dexterity, constitution):
    #     total = int(strength) + int(dexterity) + int(constitution)
    #     private = ctx.send
    #     player = str(ctx.message.author.id)
    #     path = os.getcwd()
    #     charFolder = os.path.join(path + "/characters/")
    #     charFile = Path(charFolder + player + ".txt")
    #     file = open(charFolder + player + ".txt", "r", encoding="utf-8")
    #     charData = json.load(file)
    #     file.close()
    #     reset = charData['reset']
    #     try:
    #         msg = pri_6_stats(message, character, charData, charFile)
    #         for msg_item in msg:
    #             await ctx.send( msg_item)
    #     except IndexError:
    #         await ctx.send( "You need to use the command as instructed. !stat <str> <dex> <con>. Where "
    #                                "<str> is your desired strength, <dex> is your desired dexterity, and "
    #                                "<con> is your desired constitution. do [b]NOT[/b] use commas, and place a "
    #                                "space between each number. Example; !stats 10 5 0")
    #     except ValueError:
    #         await ctx.send( "You need to use the command as instructed. !stat <str> <dex> <con>. Where "
    #                                "<str> is your desired strength, <dex> is your desired dexterity, and "
    #                                "<con> is your desired constitution. do [b]NOT[/b] use commas, and place a "
    #
    #                                "space between each number. Example: !stats 10 5 0")
    #     except UnboundLocalError:
    #         await ctx.send( "You don't even have a character created yet. Type !name <name> in the room. "
    #                                "Where <name> is your character's actual name. (Example: !name Joe")
    #
    #
    # @stats.error
    # async def stats_error(self, ctx, error):
    #     if isinstance(error, commands.PrivateMessageOnly):
    #         await ctx.send("You're an idiot, now everyone knows. You need to PM me with '!stats <str> <dex> <con>.")
    #     if isinstance(error, commands.MissingRequiredArgument):
    #         await ctx.send("So...you don't want stats? You want infinite stats? Only even numbers? Odd? Prime? What "
    #                        "I'm getting at here, is that I don't know what you want, because ***you won't tell me!*** "
    #                        "please type !stats <str> <dex> <con>. Where <str> is the number you want in strength, the "
    #                        "second for dexterity, and the third for constitution. Ex: !stats 10 5 0")
    #     else:
    #         raise error

    # @commands.command()
    # @commands.dm_only()
    # async def add(self, ctx, ability):
    #     ability.lower()
    #     player = str(ctx.message.author)
    #     path = os.getcwd()
    #     charFolder = os.path.join(path + "/characters/")
    #     with open(charFolder + player + ".txt", "r+", encoding="utf-8") as file:
    #         charData = json.load(file)
    #         strength =charData['strength']
    #         dexterity = charData['dexterity']
    #         constitution = charData['constitution']
    #         total = strength + dexterity + constitution
    #         if total < charData['total ap']:
    #             if ability == "strength" or ability == "str":
    #                 charData['strength'] += 1
    #                 charData['abhit'] = int(charData['strength'] / 2)
    #                 charData['abdamage'] = int(charData['strength'] / 2)
    #                 file.seek(0)
    #                 file.write(json.dumps(charData, ensure_ascii=False, indent=2))
    #                 file.truncate()
    #                 await ctx.send("You have added an ability point to Strength.")
    #             if ability == "dexterity" or ability == "dex":
    #                 charData['dexterity'] += 1
    #                 charData['abac'] = int(charData['dexterity'])
    #                 file.seek(0)
    #                 file.write(json.dumps(charData, ensure_ascii=False, indent=2))
    #                 file.truncate()
    #                 await ctx.send("You have added an ability point to Dexterity.")
    #             if ability == "constitution" or ability == "con":
    #                 charData['constitution'] += 1
    #                 charData['abhp'] = int(charData['constitution'])
    #                 file.seek(0)
    #                 file.write(json.dumps(charData, ensure_ascii=False, indent=2))
    #                 file.truncate()
    #             file.close()
    #         else:
    #             await ctx.send("You do not have any more ability points to spend.")
    #
    # @add.error
    # async def add_error(self, ctx, error):
    #     if isinstance(error, commands.PrivateMessageOnly):
    #         await ctx.send("This is a PM only command. I try to keep your ability points secret, and this is the "
    #                        "thanks I get for it.")
    #     if isinstance(error, commands.MissingRequiredArgument):
    #         await ctx.send("You need to specify the ability you want to point the point to. I couldn't have made it "
    #                        "any more simple for you. Type '!add str' or '!add strength' for strength, and so on. I don't "
    #                        "even need a number, just follow the instructions, and I'll do the rest.")
    #     else:
    #         raise error
    #
    # @commands.command()
    # @commands.guild_only()
    # async def erase(self, ctx):
    #     player = str(message.author.id)
    #     path = os.getcwd()
    #     charFolder = os.path.join(path + "/characters/")
    #     charFile = Path(charFolder + player + ".txt")
    #
    #     with open(charFolder + "playerDatabase.txt", 'r', encoding="utf-8") as file:
    #         playerDatabase = json.loads(file.read())
    #
    #     name = ""
    #
    #     for item in playerDatabase.items():
    #
    #         if item[1] == player:
    #             name = item[0]
    #
    #     playerDatabase.pop(name, None)
    #
    #     with open(charFolder + "playerDatabase.txt", "w", encoding="utf-8") as file:
    #         json.dump(playerDatabase, file, sort_keys=True, indent=2)
    #
    #     os.remove(charFile)
    #     await ctx.send(name + " was successfully deleted.")
    #
    # @erase.error
    # async def erase_error(self, ctx, error):
    #     if isinstance(error, commands.NoPrivateMessage):
    #         await ctx.send("The command !error may not be used in PMs!")
    #     else:
    #         raise error


def setup(client):
    client.add_cog(Character(client))
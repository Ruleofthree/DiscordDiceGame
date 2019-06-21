import discord
from discord.ext import commands
import os
import json
from pathlib import Path

class Character(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is Online")

    @commands.command()
    @commands.guild_only()
    async def name(self, ctx, name):
        player = str(ctx.message.author)
        path = os.getcwd()
        charFolder = os.path.join(path + "/characters/")
        charFile = Path(charFolder + player + ".txt")

        # Get the name of character being created
        if charFile.is_file():
            await ctx.send("You've already created a character, dumbass.")
        else:
            await ctx.send("I did it!")
            await ctx.send("Your character name is: " + name)
            await ctx.send("Your character sheet has been created.")
            levelDict = {1: [25, 1, 6, 15, 2, 1, 5, 75]}
            characterFile = {}
            level = 1
            xp = 0
            characterFile["name"] = name
            characterFile["level"] = level
            hp = levelDict[1][0]
            characterFile["hp"] = hp
            tFeats = levelDict[1][4]
            characterFile["total feats"] = tFeats
            numberOfDice = levelDict[1][1]
            numberOfSides = levelDict[1][2]
            characterFile["base damage"] = str(numberOfDice) + "d" + str(numberOfSides)
            characterFile["hit"] = levelDict[1][5]
            characterFile["damage"] = levelDict[1][5]
            characterFile["ac"] = levelDict[1][6]
            characterFile["currentxp"] = xp
            nextLevel = levelDict[1][7]
            characterFile["nextlevel"] = nextLevel
            characterFile["strength"] = 0
            characterFile["dexterity"] = 0
            characterFile["constitution"] = 0
            characterFile["remaining feats"] = 2
            ap = levelDict[1][3]
            characterFile["total ap"] = ap
            hasTaken = []
            characterFile["feats taken"] = hasTaken
            characterFile["wins"] = 0
            characterFile["losses"] = 0
            characterFile["reset"] = 0
            file = open(charFolder + player + ".txt", "w", encoding="utf-8")
            json.dump(characterFile, file, ensure_ascii=False, indent=2)
            await ctx.send("PM me with '!stats <str> <dex> <con>' to set your abilities. Wouldn't want everyone "
                     "to see your secrets, would we?")

    @name.error
    async def name_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("The command !name may not be used in PMs!")
        else:
            raise error

    @commands.command()
    @commands.dm_only()
    async def stats(self, ctx, strength, dexterity, constitution):
        private = ctx.author.send
        player = str(ctx.message.author)
        path = os.getcwd()
        charFolder = os.path.join(path + "/characters/")
        charFile = Path(charFolder + player + ".txt")
        file = open(charFolder + player + ".txt", "r", encoding="utf-8")
        charData = json.load(file)
        file.close()
        reset = charData['reset']
        print(reset)
        if not charFile.is_file():
            await private("You don't even have a character created yet. Type !name <name> in the room. "
                                   "Where <name> is your character's actual name. (Example: !name Joe")
        elif reset == 0:
            await private("You do not have a reset point with which to redo your ability points. If you feel this is "
                          "in error, please contact management.")
        else:
            strMod = int(int(strength) / 2)
            dexMod = int(int(dexterity) / 2)
            conMod = int(int(constitution) * 5)
            print(strMod, dexMod, conMod)
            await private("Allocating the following: \n\n"
                          "Strength: " + strength + "   (+" + str(strMod) + " bonus to hit and damage.)\n"
                          "Dexterity: " + dexterity + "   (+" + str(dexMod) + " bonus to armor class.)\n"
                          "Constitution: " + constitution + "   (+" + str(conMod) + " bonus to armor class.)\n")
            with open(charFolder + player + ".txt", "r+", encoding="utf-8") as file:
                print("Am I here?")
                charData = json.load(file)
                charData["strength"] = int(strength)
                charData["dexterity"] = int(dexterity)
                charData["constitution"] = int(constitution)
                charData["hit"] = int(charData["hit"] + strMod)
                charData["damage"] = int(charData["damage"] + strMod)
                charData["ac"] = int(charData["ac"] + dexMod)
                charData["hp"] = int(charData["hp"] + conMod)
                file.seek(0)
                file.write(json.dumps(charData, ensure_ascii=False, indent=2))
                file.truncate()
                file.close()

    @stats.error
    async def stats_error(self, ctx, error):
        if isinstance(error, commands.PrivateMessageOnly):
            await ctx.send("You're an idiot, now everyone knows. You need to PM me with '!stats <str> <dex> <con>.")
        else:
            raise error

def setup(client):
    client.add_cog(Character(client))
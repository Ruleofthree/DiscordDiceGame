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

        name.capitalize()
        player = str(ctx.message.author)
        path = os.getcwd()
        charFolder = os.path.join(path + "/characters/")
        charFile = Path(charFolder + player + ".txt")

        # Get the name of character being created
        if charFile.is_file():
            await ctx.send("You've already created a character. This isn't AOL RP, you don't get multi-character SNs")
        else:
            await ctx.send("Your character name is: " + name)
            await ctx.send("Your character sheet has been created.")
            with open(charFolder + "levelchart.txt", 'r', encoding="utf-8") as file:
                levelDict = json.loads(file.read())
            characterFile = {}
            level = 1
            xp = 0
            characterFile["name"] = name
            characterFile["level"] = level
            hp = levelDict["1"][0]
            characterFile["hp"] = hp
            tFeats = levelDict["1"][4]
            characterFile["total feats"] = tFeats
            numberOfDice = levelDict["1"][1]
            numberOfSides = levelDict["1"][2]
            characterFile["base damage"] = str(numberOfDice) + "d" + str(numberOfSides)
            characterFile["hit"] = levelDict["1"][5]
            characterFile["damage"] = levelDict["1"][5]
            characterFile["ac"] = levelDict["1"][6]
            characterFile["currentxp"] = xp
            nextLevel = levelDict["1"][7]
            characterFile["nextlevel"] = nextLevel
            characterFile["strength"] = 0
            characterFile["dexterity"] = 0
            characterFile["constitution"] = 0
            characterFile["remaining feats"] = 2
            ap = levelDict["1"][3]
            characterFile["total ap"] = ap
            hasTaken = []
            characterFile["feats taken"] = hasTaken
            characterFile["wins"] = 0
            characterFile["losses"] = 0
            characterFile["reset"] = 3


            file = open(charFolder + player + ".txt", "w", encoding="utf-8")
            json.dump(characterFile, file, ensure_ascii=False, indent=2)
            file.close()

            with open(charFolder + "playerDatabase.txt", 'r', encoding="utf-8") as file2:
                playerDatabase = json.loads(file2.read())
            playerDatabase[name] = player
            with open(charFolder + "playerDatabase.txt", 'w') as file2:
                file2.write(json.dumps(playerDatabase, sort_keys=True, indent=2))
            await ctx.send("PM me with '!stats <str> <dex> <con>' to set your abilities. Wouldn't want everyone "
                     "to see your secrets, would we?")

    @name.error
    async def name_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("The command !name may not be used in PMs!")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Give your character a name. You can't just be "". Do you have any idea how hard that "
                           "be to keep track of? Watch: ")
            await ctx.send("     hit      for 9 points of damage.")
            await ctx.send("What? No. Type !name <name> (Example: !name joe)")
        else:
            raise error

    @commands.command()
    @commands.dm_only()
    async def stats(self, ctx, strength, dexterity, constitution):
        total = int(strength) + int(dexterity) + int(constitution)
        private = ctx.send
        player = str(ctx.message.author)
        path = os.getcwd()
        charFolder = os.path.join(path + "/characters/")
        charFile = Path(charFolder + player + ".txt")
        file = open(charFolder + player + ".txt", "r", encoding="utf-8")
        charData = json.load(file)
        file.close()
        reset = charData['reset']
        if not charFile.is_file():
            await private("You don't even have a character created yet. Type !name <name> in the room. "
                                   "Where <name> is your character's actual name. (Example: !name Joe")
        elif reset == 0:
            await private("You do not have a reset point with which to redo your ability points. If you feel this is "
                          "in error, please contact management.")

        elif total > 15:
            await private("You can not have more than 15 total points distributed between stats.")
        else:
            strMod = int(int(strength) / 2)
            dexMod = int(int(dexterity) / 2)
            conMod = int(int(constitution) / 2) * 5
            reset = charData['reset']
            reset -= 1
            await private("Allocating the following: \n\n"
                          "Strength: " + strength + "   (+" + str(strMod) + " bonus to hit and damage.)\n"
                          "Dexterity: " + dexterity + "   (+" + str(dexMod) + " bonus to armor class.)\n"
                          "Constitution: " + constitution + "   (+" + str(conMod) + " bonus to hit points.)\n")
            with open(charFolder + player + ".txt", "r+", encoding="utf-8") as file:
                charData = json.load(file)
                charData["strength"] = int(strength)
                charData["dexterity"] = int(dexterity)
                charData["constitution"] = int(constitution)
                charData["abhit"] = strMod
                charData["abdamage"] = strMod
                charData["abac"] = dexMod
                charData["abhp"] = conMod
                charData["feathp"] = 0
                charData["featac"] = 0
                charData["feathit"] = 0
                charData["featdamage"] = 0
                charData["dexfighter"] = 0
                file.seek(0)
                file.write(json.dumps(charData, ensure_ascii=False, indent=2))
                file.truncate()
                file.close()

    @stats.error
    async def stats_error(self, ctx, error):
        if isinstance(error, commands.PrivateMessageOnly):
            await ctx.send("You're an idiot, now everyone knows. You need to PM me with '!stats <str> <dex> <con>.")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("So...you don't want stats? You want infinite stats? Only even numbers? Odd? Prime? What "
                           "I'm getting at here, is that I don't know what you want, because ***you won't tell me!*** "
                           "please type !stats <str> <dex> <con>. Where <str> is the number you want in strength, the "
                           "second for dexterity, and the third for constitution. Ex: !stats 10 5 0")
        else:
            raise error

    @commands.command()
    @commands.guild_only()
    async def erase(self, ctx):
        player = str(ctx.message.author)
        path = os.getcwd()
        charFolder = os.path.join(path + "/characters/")
        charFile = Path(charFolder + player + ".txt")

        with open(charFolder + "playerDatabase.txt", 'r', encoding="utf-8") as file:
            playerDatabase = json.loads(file.read())

        name = ""

        for item in playerDatabase.items():

            if item[1] == player:
                name = item[0]

        playerDatabase.pop(name, None)

        with open(charFolder + "playerDatabase.txt", "w", encoding="utf-8") as file:
            json.dump(playerDatabase, file, sort_keys=True, indent=2)

        os.remove(charFile)
        await ctx.send(name + " was successfully deleted.")


def setup(client):
    client.add_cog(Character(client))
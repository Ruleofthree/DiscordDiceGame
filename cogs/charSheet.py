import discord
from discord.ext import commands
import os
import json
from pathlib import Path

class Sheet(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command()
    @commands.dm_only()
    async def viewchar(self, ctx):

        private = ctx.author.send
        player = str(ctx.message.author)

        path = os.getcwd()
        charFolder = os.path.join(path + "/characters/")
        charFile = Path(charFolder + player + ".txt")
        file = open(charFolder + player + ".txt", "r", encoding="utf-8")
        charStats = json.load(file)
        file.close()

        if not charFile.is_file():
            await private("You don't even have a character created yet. Type !name <name> in the room. "
                          "Where <name> is your character's actual name. (Example: !name Joe")
        else:

            name = charStats['name']
            level = charStats['level']
            hp = charStats['hp']
            tFeats = charStats['total feats']
            baseDamage = charStats['base damage']
            hit = charStats['hit']
            damage = charStats['damage']
            ac = charStats['ac']
            xp = charStats['currentxp']
            nextLevel = charStats['nextlevel']
            strength = charStats['strength']
            dexterity = charStats['dexterity']
            constitution = charStats['constitution']
            remainingFeats = charStats['remaining feats']
            hasTaken = charStats['feats taken']
            charFeats = ", ".join(hasTaken)
            ap = charStats['total ap']
            reset = charStats['reset']

            await private("```\n"
                          "Name:               " + str(name) + "          Strength:           " + str(strength) + "\n"
                          "Level:              " + str(level) + "               Dexterity:          " + str(dexterity) + "\n"
                          "Hit Points:         " + str(hp) + "              Constitution:       " + str(constitution) + "\n"
                          "Armor Class:        " + str(ac) + "              Ability Points:     " + str(ap) + "\n"
                          "Base Damage:        " + str(baseDamage) + "             Reset:              " + str(reset) + "\n"
                          "Hit Modifier:       " + str(hit) + "\n"
                          "Damage Modifier:    " + str(damage) + "\n"
                          "Total Feats:        " + str(tFeats) + "\n"
                          "Experience Points:  " + str(xp) + "\n"
                          "Next Level:         " + str(nextLevel) + "\n" 
                          "Remaining Feats:    " + str(remainingFeats) + "\n"
                          "Feats Taken:        " + charFeats + "```\n")

    @viewchar.error
    async def stats_error(self, ctx, error):
        if isinstance(error, commands.PrivateMessageOnly):
            await ctx.send("You're an idiot, now everyone knows. Why would you want to display your character sheet "
                           "in a public room? PM me with the command.")
        else:
            raise error

def setup(client):
    client.add_cog(Sheet(client))
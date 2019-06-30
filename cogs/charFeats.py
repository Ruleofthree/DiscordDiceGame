import discord
from discord.ext import commands
import os
import json
from pathlib import Path

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

    @commands.command()
    @commands.dm_only()
    async def featlist(self, ctx):
        
        featDictionary = featDict()[0]
        featList = featDict()[1]
        private = ctx.author.send
        
        stringList = "\n".join(featList)
        await private(stringList)

    @featlist.error
    async def name_featlist(self, ctx, error):
        if isinstance(error, commands.PrivateMessageOnly):
            await ctx.send("I'm not gonna spam the arena with this list, man. PM me with !featlist")
        else:
            raise error

    @commands.command()
    @commands.dm_only()
    async def feathelp(self, ctx, *, answer):


        featDictionary = featDict()[0]
        featList = featDict()[1]
        private = ctx.author.send
        answer = str(answer.lower())
        reqStat = featDictionary[0][answer]['stat']
        featStatus = featDictionary[0][answer]['status']
        level = featDictionary[0][answer]['requirements'][0]
        reqStr = featDictionary[0][answer]['requirements'][1]
        reqDex = featDictionary[0][answer]['requirements'][2]
        reqCon = featDictionary[0][answer]['requirements'][3]
        reqFeats = featDictionary[0][answer]['requirements'][4]
        await private("```" + answer.capitalize() + " (" + reqStat + ") (" + featStatus + "):\n" +
                    featDictionary[0][answer]['desc'] +
                    "\nPrerequisites: " + "\nLevel: " + str(level) +
                    "\nStrength: " + str(reqStr) +
                    "\nDexterity: " + str(reqDex) +
                    "\nConstitution: " + str(reqCon) +
                    "\nRequired Feats: " + reqFeats +"```")

    @feathelp.error
    async def name_feathelp(self, ctx, error):
        if isinstance(error, commands.PrivateMessageOnly):
            await ctx.send("I'm not gonna spam the arena with this list, man. PM me with !feathelp <feat> for assistance.")

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("I need the name of the feat you want help on. I can't read minds.")

        raise error

    @commands.command()
    @commands.dm_only()
    async def feat(self, ctx, *, answer):

        private = ctx.author.send
        player = str(ctx.message.author)

        featDictionary = featDict()[0]
        featList = featDict()[1]
        
        path = os.getcwd()
        charFolder = os.path.join(path + "/characters/")
        charFile = Path(charFolder + player + ".txt")
        file = open(charFolder + player + ".txt", "r", encoding="utf-8")
        charData = json.load(file)
        file.close()

        name = charData['name']
        level = charData['level']
        hp = charData['hp']
        tFeats = charData['total feats']
        baseDamage = charData['base damage']
        hit = charData['hit']
        damage = charData['damage']
        ac = charData['ac']
        xp = charData['currentxp']
        nextLevel = charData['nextlevel']
        strength = charData['strength']
        dexterity = charData['dexterity']
        constitution = charData['constitution']
        remainingFeats = charData['remaining feats']
        hasTaken = charData['feats taken']
        charFeats = ", ".join(hasTaken)
        ap = charData['total ap']
        reset = charData['reset']
        
        if remainingFeats == 0:
            await private("You have no feat slots left to select a new feat")
        elif answer not in featList:
            await private("Make sure you have spelled the feat correctly")
        else:
            reqLevel = featDictionary[0][answer]['requirements'][0]
            reqStr = featDictionary[0][answer]['requirements'][1]
            reqDex = featDictionary[0][answer]['requirements'][2]
            reqCon = featDictionary[0][answer]['requirements'][3]
            reqFeats = featDictionary[0][answer]['requirements'][4]
            if reqLevel > level:
                await private("You are not the required level for this feat.")
            elif reqStr > strength:
                await private("You do not have the required strength for this feat.")
            elif reqDex > dexterity:
                await private("You do not have the required dexterity for this feat.")
            elif reqCon > constitution:
                await private( "You do not have the required constitution for this feat.")
            elif reqFeats not in hasTaken and reqFeats != "none":
                await private("You do hot have the required prerequisites to take this feat.")
            elif answer not in hasTaken:
                await private(answer + " has been added to your character sheet.")
                remainingFeats -= 1
                hasTaken.append(answer)
                if answer == "dexterous fighter":
                    dexMod = int(dexterity / 2)
                    strMod = int(strength / 2)
                    hit = hit + dexMod - strMod

                if answer == "crushing blow":
                    damageMod = 1
                    damage = damage + damageMod
                if answer == "improved crushing blow":
                    damageMod = 3
                    damage = damage + damageMod
                    index = hasTaken.index("crushing blow")
                    hasTaken.pop(index)
                if answer == "greater crushing blow":
                    damageMod = 5
                    damage = damage + damageMod
                    index = hasTaken.index("improved crushing blow")
                    hasTaken.pop(index)
                if answer == "titan blow":
                    index = hasTaken.index("greater crushing blow")
                    hasTaken.pop(index)

                if answer == "precision strike":
                    hitMod = 1
                    hit = hit + hitMod
                if answer == "improved precision strike":
                    hitMod = 3
                    hit = hit + hitMod
                    index = hasTaken.index("precision strike")
                    hasTaken.pop(index)
                if answer == "greater precision strike":
                    hitMod = 5
                    hit = hit + hitMod
                    index = hasTaken.index("improved precision strike")
                    hasTaken.pop(index)
                if answer == "true strike":
                    index = hasTaken.index("greater precision strike")
                    hasTaken.pop(index)

                if answer == "lightning reflexes":
                    acMod = 1
                    ac = ac + acMod
                if answer == "improved lightning reflexes":
                    acMod = 3
                    ac = ac + acMod
                    index = hasTaken.index("lightning reflexes")
                    hasTaken.pop(index)
                if answer == "greater lightning reflexes":
                    acMod = 5
                    ac = ac + acMod
                    index = hasTaken.index("improved lightning reflexes")
                    hasTaken.pop(index)

                if answer == "endurance":
                    hpMod = 5
                    hp = hp + hpMod
                if answer == "improved endurance":
                    hpMod = 15
                    hp = hp + hpMod
                    index = hasTaken.index("endurance")
                    hasTaken.pop(index)
                if answer == "greater endurance":
                    hpMod = 30
                    hp = hp + hpMod
                    index = hasTaken.index("improved endurance")
                    hasTaken.pop(index)

                if answer == "improved crippling blow":
                    index = hasTaken.index("crippling blow")
                    hasTaken.pop(index)
                if answer == "greater crippling blow":
                    index = hasTaken.index("improved crippling blow")
                    hasTaken.pop(index)
                if answer == "staggering blow":
                    index = hasTaken.index("greater crippling blow")
                    hasTaken.pop(index)

                if answer == "improved evasion":
                    index = hasTaken.index("evasion")
                    hasTaken.pop(index)
                if answer == "greater evasion":
                    index = hasTaken.index("improved evasion")
                    hasTaken.pop(index)

                if answer == "improved quick strike":
                    index = hasTaken.index("quick strike")
                    hasTaken.pop(index)
                if answer == "greater quick strike":
                    index = hasTaken.index("improved quick strike")
                    hasTaken.pop(index)
                if answer == "riposte":
                    index = hasTaken.index("greater quick strike")
                    hasTaken.pop(index)

                if answer == "improved deflect":
                    index = hasTaken.index("deflect")
                    hasTaken.pop(index)
                if answer == "greater deflect":
                    index = hasTaken.index("improved deflect")
                    hasTaken.pop(index)

                if answer == "improved hurt me":
                    index = hasTaken.index("hurt me")
                    hasTaken.pop(index)
                if answer == "greater hurt me":
                    index = hasTaken.index("improved hurt me")
                    hasTaken.pop(index)
                if answer == "hurt me more":
                    index = hasTaken.index("greater hurt me")
                    hasTaken.pop(index)

                if answer == "improved reckless abandon":
                    index = hasTaken.index("reckless abandon")
                    hasTaken.pop(index)
                if answer == "greater reckless abandon":
                    index = hasTaken.index("improved reckless abandon")
                    hasTaken.pop(index)

                with open(charFolder + player + ".txt", "r+", encoding="utf-8") as file:
                    charData = json.load(file)
                    charData["hp"] = int(hp)
                    charData["ac"] = int(ac)
                    charData["hit"] = int(hit)
                    charData["damage"] = int(damage)
                    charData["feats taken"] = hasTaken
                    charData["remaining feats"] = remainingFeats
                    file.seek(0)
                    file.write(json.dumps(charData, ensure_ascii=False, indent=2))
                    file.truncate()
                    file.close()

    @feat.error
    async def name_feat(self, ctx, error):
        if isinstance(error, commands.PrivateMessageOnly):
            await ctx.send(
                "Hey! Good work! You just told everyone what feat you are going to take! Now PM me with !feat <feat> to"
                " do it correctly.")
        else:
            raise error

def setup(client):
    client.add_cog(Feats(client))
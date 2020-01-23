import os
import json
import asyncio
import discord

from pathlib import Path
from collections import Counter
from discord.ext import commands

from gamelogic import onMSGAccept, onMSGRoll, onMSGUtil, onPRIUtil


# A function to call access to the .txt files inside the characters folder
def characters():
    path = os.getcwd()
    charFolder = os.path.join(path + "/characters/")
    return charFolder

# A function to call access to the .txt files inside the cogs folder
def items():
    path = os.getcwd()
    itemFolder = os.path.join(path + "/cogs/")
    return itemFolder

# A function to call access to the .txt files inside of the gamelogic folder
def gamelogic():
    path = os.getcwd()
    gameLogic = os.path.join(path + "/gamelogic/")
    return gameLogic

# A function to call access to token.txt
def roomID():
    file = open("token.txt", "r", encoding="utf-8")
    stuff = json.load(file)
    file.close()
    arena = stuff["arena"]
    devroom = stuff["devroom"]
    gamemaster = stuff["gamemaster"]
    return arena, devroom, gameamaster

# A function to handle feat information within feat.txt
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

# A function to handle trait information within trait.txt
def traitDict():
    # Open up a json object containing the list of traits.
    path = os.getcwd()
    traitFolder = os.path.join(path + "/cogs/")
    traitFile = open(traitFolder + "trait.txt", "r", encoding="utf-8")
    traitDictionary = json.load(traitFile)
    traitFile.close()

    # place all keys within a list for comparison later
    traitList = []
    for keys in traitDictionary[0]:
        traitList.append(keys)
    return traitDictionary, traitList

# A function to handle all potion information within potions.txt
def potionShop():
    # Open up a json object containing the list of potions
    path = os.getcwd()
    charFolder = os.path.join(path + "/cogs/")
    potionFile = open(charFolder + "potions.txt", "r", encoding="utf-8")
    potionDictionary = json.load(potionFile)
    potionFile.close()

    # place all keys within a list for comparison later
    potionList = []
    commonList = []
    uncommonList = []
    rareList = []
    vrareList = []
    relicList = []

    for keys in potionDictionary[0]:
        potionList.append(keys)

    for category in potionList:
        if category == "common":
            for keys in potionDictionary[0][category]:
                commonList.append(keys)
        if category == "uncommon":
            for keys in potionDictionary[0][category]:
                uncommonList.append(keys)
        if category == "rare":
            for keys in potionDictionary[0][category]:
                rareList.append(keys)
        if category == "vrare":
            for keys in potionDictionary[0][category]:
                vrareList.append(keys)
        if category == "relic":
            for keys in potionDictionary[0][category]:
                relicList.append(keys)

    return commonList, uncommonList, rareList, vrareList, relicList

# A function to handle feat information within armor.txt
def armorShop():
    path = os.getcwd()
    charFolder = os.path.join(path + "/cogs/")
    armorFile = open(charFolder + "armor.txt", "r", encoding="utf-8")
    armorDictionary = json.load(armorFile)
    armorFile.close()

    # place all keys within a list for comparison later
    catOneList = []
    catTwoList = []
    catThreeList = []
    for keys in armorDictionary[0]["cat1"]:
        catOneList.append(keys)
    for keys in armorDictionary[0]["cat2"]:
        catTwoList.append(keys)
    for keys in armorDictionary[0]["cat3"]:
        catThreeList.append(keys)

    catOneCommonList = []
    catOneUncommonList = []
    catOneRareList = []

    for category in catOneList:
        if category == "common":
            for keys in armorDictionary[0]["cat1"][category]:
                catOneCommonList.append(keys)
        if category == "uncommon":
            for keys in armorDictionary[0]["cat1"][category]:
                catOneUncommonList.append(keys)
        if category == "rare":
            for keys in armorDictionary[0]["cat1"][category]:
                catOneRareList.append(keys)

    catTwoCommonList = []
    catTwoUncommonList = []
    catTwoRareList = []

    for category in catTwoList:
        if category == "common":
            for keys in armorDictionary[0]["cat2"][category]:
                catTwoCommonList.append(keys)
        if category == "uncommon":
            for keys in armorDictionary[0]["cat2"][category]:
                catTwoUncommonList.append(keys)
        if category == "rare":
            for keys in armorDictionary[0]["cat2"][category]:
                catTwoRareList.append(keys)

    catThreeCommonList = []
    catThreeUncommonList = []
    catThreeRareList = []

    for category in catThreeList:
        if category == "common":
            for keys in armorDictionary[0]["cat3"][category]:
                catThreeCommonList.append(keys)
        if category == "uncommon":
            for keys in armorDictionary[0]["cat3"][category]:
                catThreeUncommonList.append(keys)
        if category == "rare":
            for keys in armorDictionary[0]["cat3"][category]:
                catThreeRareList.append(keys)

    return catOneCommonList, catOneUncommonList, catOneRareList, catTwoCommonList, catTwoUncommonList, catTwoRareList,\
    catThreeCommonList, catThreeUncommonList, catThreeRareList

# A function to load in relevant game data for a specific room from that roomID's text file
def gameStatLoad(channel):
    channel = str(channel)
    path = os.getcwd()
    gameFolder = os.path.join(path + "/gamelogic/")
    with open(gameFolder + channel + '.txt', 'r+') as file:
        gameData = json.load(file)
        file.close()
    playerOneID = gameData["playerOneID"]
    playerTwoID = gameData["playerTwoID"]
    winner = gameData["winner"]
    quitter = gameData["quitter"]
    pOneInfo = gameData["pOneInfo"]
    pTwoInfo = gameData["pTwoInfo"]
    featToken = gameData["featToken"]
    game = gameData["game"]
    count = gameData["count"]
    token = gameData["token"]
    critical = gameData["critical"]
    bonusHurt = gameData["bonusHurt"]
    nerveDamage = gameData["nerveDamage"]
    totalDamage = gameData["totalDamage"]
    pOneTotalHP = gameData["pOneTotalHP"]
    pTwoTotalHP = gameData["pTwoTotalHP"]
    pOneCurrentHP = gameData["pOneCurrentHP"]
    pTwoCurrentHP = gameData["pTwoCurrentHP"]
    pOnepMod = gameData["pOnepMod"]
    pOnecMod = gameData["pOnecMod"]
    pOnedMod = gameData["pOnedMod"]
    pOnemMod = gameData["pOnemMod"]
    pOneEvade = gameData["pOneEvade"]
    pOneDeflect = gameData["pOneDeflect"]
    pOneRiposte = gameData["pOneRiposte"]
    pOneTempDR = gameData["pOneTempDR"]
    pOneDeathsDoor = gameData["pOneDeathsDoor"]
    pOneQuickDamage = gameData["pOneQuickDamage"]
    pOneFeatInfo = gameData["pOneFeatInfo"]
    pOneSpentFeat = gameData["pOneSpentFeat"]
    pTwopMod = gameData["pTwopMod"]
    pTwocMod = gameData["pTwocMod"]
    pTwodMod = gameData["pTwodMod"]
    pTwomMod = gameData["pTwomMod"]
    pTwoEvade = gameData["pTwoEvade"]
    pTwoDeflect = gameData["pTwoDeflect"]
    pTwoRiposte = gameData["pTwoRiposte"]
    pTwoTempDR = gameData["pTwoTempDR"]
    pTwoDeathsDoor = gameData["pTwoDeathsDoor"]
    pTwoQuickDamage = gameData["pTwoQuickDamage"]
    pTwoFeatInfo = gameData["pTwoFeatInfo"]
    pTwoSpentFeat =gameData["pTwoSpentFeat"]
    pOneLevel = gameData["pOneLevel"]
    pTwoLevel = gameData["pTwoLevel"]
    xp = gameData["xp"]
    currentPlayerXP = gameData["currentPlayerXP"]
    nextLevel = gameData["nextLevel"]
    levelUp = gameData["levelUp"]
    iddqd = gameData["iddqd"]
    bEvasion = gameData["bEvasion"]
    bDeflect = gameData["bDeflect"]
    return playerOneID, playerTwoID, winner, quitter, pOneInfo, pTwoInfo, featToken, game, count, token, critical,\
           bonusHurt, nerveDamage, totalDamage, pOneTotalHP, pTwoTotalHP, pOneCurrentHP, pTwoCurrentHP, pOnepMod, \
           pOnecMod, pOnedMod, pOnemMod, pOneEvade, pOneDeflect, pOneRiposte, pOneTempDR, pOneDeathsDoor,\
           pOneQuickDamage, pOneFeatInfo, pOneSpentFeat, pTwopMod, pTwocMod, pTwodMod, pTwomMod, pTwoEvade,\
           pTwoDeflect, pTwoRiposte, pTwoQuickDamage, pTwoFeatInfo, pTwoSpentFeat, pOneLevel, pTwoLevel, xp,\
           currentPlayerXP, nextLevel, levelUp, iddqd, bEvasion, bDeflect



# A function to update the relevant roomID's .txt file with new game data
def gameStatDump(playerOneID, playerTwoID, winner, quitter, pOneInfo, pTwoInfo, featToken, game, count, token,
                 critical, bonusHurt, nerveDamage, totalDamage, pOneTotalHP, pTwoTotalHP, pOneCurrentHP,
                 pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod, pOnemMod, pOneEvade, pOneDeflect, pOneRiposte,
                 pOneTempDR, pOneDeathsDoor, pOneQuickDamage, pOneFeatInfo, pOneSpentFeat, pTwopMod, pTwocMod,
                 pTwodMod, pTwomMod, pTwoEvade, pTwoDeflect, pTwoRiposte, pTwoTempDR, pTwoDeathsDoor,
                 pTwoQuickDamage, pTwoFeatInfo, pTwoSpentFeat, pOneLevel, pTwoLevel, xp, currentPlayerXP,
                 nextLevel, levelUp, iddqd, bEvasion, bDeflect, channel):
    channel = str(channel)
    path = os.getcwd()
    gameFolder = os.path.join(path + "/gamelogic/")
    with open(gameFolder + channel + '.txt', 'r+') as file:
        gameData = json.load(file)
        gameData["playerOneID"] = playerOneID
        gameData["playerTwoID"] = playerTwoID
        gameData["winner"] = winner
        gameData["quitter"] = quitter
        gameData["pOneInfo"] = pOneInfo
        gameData["pTwoInfo"] = pTwoInfo
        gameData["featToken"] = featToken
        gameData["game"] = game
        gameData["count"] = count
        gameData["token"] = token
        gameData["critical"] = critical
        gameData["bonusHurt"] = bonusHurt
        gameData["nerveDamage"] = nerveDamage
        gameData["totalDamage"] = totalDamage
        gameData["pOneTotalHP"] = pOneTotalHP
        gameData["pTwoTotalHP"] = pTwoTotalHP
        gameData["pOneCurrentHP"] = pOneCurrentHP
        gameData["pTwoCurrentHP"] = pTwoCurrentHP
        gameData["pOnepMod"] = pOnepMod
        gameData["pOnecMod"] = pOnecMod
        gameData["pOnedMod"] = pOnedMod
        gameData["pOnemMod"] = pOnemMod
        gameData["pOneEvade"] = pOneEvade
        gameData["pOneDeflect"] = pOneDeflect
        gameData["pOneRiposte"] = pOneRiposte
        gameData["pOneTempDR"] = pOneTempDR
        gameData["pOneDeathsDoor"] = pOneDeathsDoor
        gameData["pOneQuickDamage"] = pOneQuickDamage
        gameData["pOneFeatInfo"] = pOneFeatInfo
        gameData["pOneSpentFeat"] = pOneSpentFeat
        gameData["pTwopMod"] = pTwopMod
        gameData["pTwocMod"] = pTwocMod
        gameData["pTwodMod"] = pTwodMod
        gameData["pTwomMod"] = pTwomMod
        gameData["pTwoEvade"] = pTwoEvade
        gameData["pTwoDeflect"] = pTwoDeflect
        gameData["pTwoRiposte"] = pTwoRiposte
        gameData["pTwoTempDR"] = pTwoTempDR
        gameData["pTwoDeathsDoor"] = pTwoDeathsDoor
        gameData["pTwoQuickDamage"] = pTwoQuickDamage
        gameData["pTwoFeatInfo"] = pTwoFeatInfo
        gameData["pTwoSpentFeat"] = pTwoSpentFeat
        gameData["pOneLevel"] = pOneLevel
        gameData["pTwoLevel"] = pTwoLevel
        gameData["xp"] = xp
        gameData["currentPlayerXP"] = currentPlayerXP
        gameData["nextLevel"] = nextLevel
        gameData["levelUp"] = levelUp
        gameData["iddqd"] = iddqd
        gameData["bEvasion"] = bEvasion
        gameData["bDeflect"] = bDeflect
        file.seek(0)
        file.write(json.dumps(gameData, ensure_ascii=False, indent=2))
        file.truncate()
        file.close()

class Combat(commands.Cog):

    # Useless shit. This isn't needed anymore, save for self.client and self.quitter, as all data below is stored
    # in .txt files and called there. It only remains for testing purposes
    def __init__(self, client):
        self.opponent = ""
        self.client = client
        self.quitter = ""
        # # STRINGS
        # self.opponent = ""
        # self.playerOne = ""
        # self.playerTwo = ""
        # self.winner = ""
        # self.quitter = ""
        # # PLAYER INFO
        # self.pOneInfo = {}
        # self.pTwoInfo = {}
        # # HP AND TURN COUNTERS
        # # challenge = 0
        # # reset = 0
        # self.featToken = 0
        # self.game = 0
        # self.count = 0
        # self.token = 0
        # self.critical = 0
        # self.bonusHurt = 0
        # self.nerveDamage = 0
        # self.totalDamage = 0
        # self.pOneTotalHP = 0
        # self.pTwoTotalHP = 0
        # self.pOneCurrentHP = 0
        # self.pTwoCurrentHP = 0
        # # PLAYER ONE FEAT COUNTERS
        # self.pOnepMod = 0
        # self.pOnecMod = 0
        # self.pOnedMod = 0
        # self.pOnemMod = 0
        # self.pOneEvade = 1
        # self.pOneDeflect = 1
        # self.pOneRiposte = 0
        # self.pOneQuickDamage = 0
        # self.pOneFeatInfo = None
        # self.pOneSpentFeat = []
        # # PLAYER TWO FEAT COUNTERS
        # self.pTwopMod = 0
        # self.pTwocMod = 0
        # self.pTwodMod = 0
        # self.pTwomMod = 0
        # self.pTwoEvade = 1
        # self.pTwoDeflect = 1
        # self.pTwoRiposte = 0
        # self.pTwoQuickDamage = 0
        # self.pTwoFeatInfo = None
        # self.pTwoSpentFeat = []
        # # XP AND LEVEL COUNTERS
        # self.pOneLevel = 0
        # self.pTwoLevel = 0
        # self.xp = 0
        # self.currentPlayerXP = 0
        # self.nextLevel = 0
        # self.levelUp = 0
        # self.iddqd = 0
        #
        # # Susanna added
        # self.bEvasion = False
        # self.bDeflect = False

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is Online")

    # Timeout a challenge if it is left unanswered for more than 60 seconds
    async def challengeTimeout(self, ctx):
        await asyncio.sleep(60)
        gameFolder = gamelogic()
        whichRoom = ctx.channel.id
        msg = onMSGUtil.message_6_reset(gameFolder, whichRoom)
        await ctx.send(msg)

    # Time out a game if it is left unanswered for more than 60 minutes
    async def gameTimeout(self, ctx):
        await asyncio.sleep(3600)
        self.gameTimer.cancel()
        gameFolder = gamelogic()
        whichRoom = ctx.channel.id
        msg = onMSGUtil.message_6_reset(gameFolder, whichRoom)
        await ctx.send(msg)

#---------------------------------------------CHATROOM COMMANDS---------------------------------------------------------
    #!leaderboard <win> <loss> <percent>
    @commands.command()
    @commands.guild_only()
    async def leaderboard(self, ctx, option=None):
        if option is None:
            option = "win"
        msg = onMSGUtil.message_12_leaderboard(option)
        # await ctx.send("This is working.")
        for msg_item in msg:
            await ctx.send(msg_item)

    @leaderboard.error
    async def leaderboard_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("The command !leaderboard may not be used in PMs!")
        raise error

    #!name <name>
    @commands.command()
    @commands.guild_only()
    async def name(self, ctx, name):

        name.capitalize()
        player = str(ctx.message.author.id)
        charFolder = characters()
        charFile = Path(charFolder + player + ".txt")

        msg = onMSGUtil.message_5_name(charFile, charFolder, name, player)
        for msg_item in msg:
            await ctx.send(msg_item)

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

     #!erase
    @commands.command()
    @commands.guild_only()
    async def erase(self, ctx):
        self.quitter = str(ctx.message.author.id)
        charFolder = characters()

        charSheet = open(charFolder + self.quitter + ".txt", "r", encoding="utf-8")
        pInfo = json.load(charSheet)
        charSheet.close()
        await ctx.send("Are you sure you want to delete " + pInfo['name'] + "? (Type **!confirm**"
                       " to do the deed, or **!deny** to save a life.)")

    @erase.error
    async def erase_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("The command !error may not be used in PMs!")
        else:
            raise error

    #!confirm erase
    @commands.command()
    @commands.guild_only()
    async def confirm(self, ctx):
        player = str(ctx.message.author.id)
        if player == self.quitter:
            msg = onMSGUtil.message_7_erase(player)
            await ctx.send(msg)
            self.quitter = ""
        else:
            await ctx.send("You aren't the one asking for the erase, not cool.")

    @confirm.error
    async def confirm_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("The command !confirm may not be used in PMs!")
        else:
            raise error

    #!deny erase
    @commands.command()
    @commands.guild_only()
    async def deny(self, ctx):
        player = str(ctx.message.author.id)
        if player == self.quitter:
            await ctx.send("Yay.")
            self.quitter = ""
        else:
            await ctx.send("You aren't the one asking for the erase, not cool.")

    @deny.error
    async def deny_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("The command !deny may not be used in PMs!")
        else:
            raise error

    #!reset
    @commands.command()
    @commands.guild_only()
    @commands.has_role("Admin")
    async def reset(self, ctx):
        gameFolder = gamelogic()
        channelID = [gameFolder[1], gameFolder[2]]
        if ctx.channel.id in channelID:
            whichRoom = ctx.channel.id
            msg = onMSGUtil.message_6_reset(gameFolder, whichRoom)
            await ctx.send(msg)
        else:
            await ctx.send("This command can not be used here.")

    @reset.error
    async def reset_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("The command !reset may not be used in PMs!")
        else:
            raise error

    #!player <name>
    @commands.command()
    @commands.guild_only()
    async def player(self, ctx, player):
        msg = onMSGUtil.message_7_player(player)
        await ctx.send(msg)

    @player.error
    async def player_error(self,ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("The command !player may not be used in PMs!")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please follow the command with the name of a player. Exmaple: !player Joe")
        else:
            raise error

    #!who <name>
    @commands.command()
    @commands.guild_only()
    async def who(self, ctx, player):
        msg = onMSGUtil.message_4_who(player)
        await ctx.send(msg)

    @who.error
    async def who_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("The command !who may not be used in PMs!")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please follow the command with the name of a character. Example: !who Joe")
        else:
            raise error

    #!usepotion <potion>
    @commands.command()
    @commands.guild_only()
    async def usepotion(self, ctx, potion):
        player = str(ctx.message.author.id)
        charFolder = characters()
        commonList, uncommonList, rareList, vrareList, relicList = potionShop()
        msg = onMSGUtil.message_10_usepotion(potion, player, commonList, uncommonList, rareList, vrareList,
                                             relicList, charFolder)
        await ctx.send(msg)

    @usepotion.error
    async def usepotion_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("The command !usepotion may not be used in PMs")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please follow the command with the potion you wish to use.")
        else:
            raise error

    #!buyarmor <armorslot>
    @commands.command()
    @commands.guild_only()
    async def buyarmor(self, ctx, armorslot):
        player = str(ctx.message.author.id)
        charFolder = characters()
        armorFolder = items()
        msg = onMSGUtil.message_9_buyarmor(player, armorslot, charFolder, armorFolder)
        await ctx.send(msg)

    @buyarmor.error
    async def buyarmor_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("The command !buyarmor can not be used in PMs")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please follow the command with the armor you wish to buy.")
        else:
            raise error

    #!sellarmor <armor name>
    @commands.command()
    @commands.guild_only()
    async def sellarmor(self, ctx, armorname):
        player = str(ctx.message.author.id)
        charFolder = characters()
        itemFolder = items()
        msg = onMSGUtil.message_10_sellarmor(player, armorname, charFolder, itemFolder)
        await ctx.send(msg)

    @sellarmor.error
    async def sellarmor_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("The command !sellarmor may not be used in PMs")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please follow the command with the armor you wish to sell.")
        else:
            raise error

    #!armorname <oldName> <newName>
    @commands.command()
    @commands.guild_only()
    async def armorname(self, ctx, oldName, newName):
        player = str(ctx.message.author.id)
        charFolder = characters()
        msg = onMSGUtil.message_10_namearmor(player, oldName, newName, charFolder)
        await ctx.send(msg)

    @armorname.error
    async def armorname_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("The command !armorname may not be used in PMs")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please follow the command with current name of the armor, then the new name.")
        else:
            raise error

    #!equip <armor>
    @commands.command()
    @commands.guild_only()
    async def equip(self, ctx, armor):
        player = str(ctx.message.author.id)
        charFolder = characters()
        msg = onMSGUtil.message_6_equip(armor, player, charFolder)
        await ctx.send(msg)

    @equip.error
    async def equip_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("The command !equip may not be used in PMs")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please follow the command with current name of armor you wish to wear.")
        else:
            raise error

    #!unequip <armor>
    @commands.command()
    @commands.guild_only()
    async def unequip(self, ctx, armor):
        charFolder = characters()
        player = str(ctx.message.author.id)
        msg = onMSGUtil.message_8_unequip(armor, player, charFolder)
        await ctx.send(msg)

    @unequip.error
    async def unequip_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("The command !unequip may not be used in PMs")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please follow the command with current name of the armor being worn.")
        else:
            raise error

    #!buypotion <potion>
    @commands.command()
    @commands.guild_only()
    async def buypotion(self, ctx, potion):
        player = str(ctx.message.author.id)
        charFolder = characters()
        itemFolder = items()
        msg = onMSGUtil.message_10_buypotion(player, potion, charFolder, itemFolder)
        await ctx.send(msg)

    @buypotion.error
    async def buypotion_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("The command !buypotion may not be used in PMs")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please follow the command with name of the potion you wish to buy.")
        else:
            raise error

    @commands.command()
    @commands.guild_only()
    async def buypotion(self, ctx, potion):
        player = str(ctx.message.author.id)
        charFolder = characters()
        msg = onMSGUtil.message_11_sellpotion(player, potion, charFolder)
        await ctx.send(msg)

    @buypotion.error
    async def buypotion_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("The command !sellpotion may not be used in PMs")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please follow the command with name of the potion you wish to sell.")
        else:
            raise error

    #!givepotion <character> <potion>
    @commands.command()
    @commands.guild_only()
    async def givepotion(self, ctx, gifted, potion):
        charFolder = characters()
        gifter = str(ctx.message.author.id)
        msg = onMSGUtil.message_11_givepotion(potion, gifter,  gifted, charFolder)
        await ctx.send(msg)

    @buypotion.error
    async def givepotion_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("The command !givepotion may not be used in PMs")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please follow the command with the name of the character you are giving the potion to, "
                           "followed by name of the potion you wish to give.")
        else:
            raise error

    #!givegold <character> <amount>
    @commands.command()
    @commands.guild_only()
    async def givegold(self, ctx, gifted, amount):
        charFolder = characters()
        gifter = str(ctx.message.author.id)
        msg = onMSGUtil.message_11_givegold(amount, gifter, gifted, charFolder)
        await ctx.send(msg)

    @givegold.error
    async def givegold_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("The command !givegold may not be used in PMs")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please follow the command with the name of the character you are giving the gold to, "
                           "followed by amount of gold you wish to give.")
        else:
            raise error

#------------------------------------------COMBAT COMMANDS--------------------------------------------------------------
    #!challenge
    @commands.command()
    @commands.guild_only()
    async def challenge(self, ctx, opponent):
        challenger = str(ctx.message.author.id)

        path = os.getcwd()
        charFolder = os.path.join(path + "/characters/")

        arena, devroom = roomID()
        channelID = [arena, devroom]
        if ctx.channel.id in channelID:
            channel = ctx.channel.id

            playerOneID, playerTwoID, winner, quitter, pOneInfo, pTwoInfo, featToken, game, count, token, critical, \
            bonusHurt, nerveDamage, totalDamage, pOneTotalHP, pTwoTotalHP, pOneCurrentHP, pTwoCurrentHP, pOnepMod,\
            pOnecMod, pOnedMod, pOnemMod, pOneEvade, pOneDeflect, pOneRiposte, pOneQuickDamage, pOneFeatInfo,\
            pOneSpentFeat, pTwopMod, pTwocMod, pTwodMod, pTwomMod, pTwoEvade, pTwoDeflect, pTwoRiposte,\
            pTwoQuickDamage, pTwoFeatInfo, pTwoSpentFeat, pOneLevel, pTwoLevel, xp, currentPlayerXP, nextLevel,\
            levelUp, iddqd, bEvasion, bDeflect = gameStatLoad(channel)

            msg, playerTwoID, pOneInfo, new_game, bTimer, playerOneID, opponent\
                = onMSGUtil.message_10_challenge(challenger, opponent, charFolder, game)
            playerOneID = challenger
            print(playerTwoID)
            if game == 0:
                await ctx.send(msg)
                # if opponent is not "":
                #     opponent = opponent
                if pOneInfo is not None:
                    # pOneInfo = pOneInfo
                    pOneTotalHP = pOneInfo['thp']
                    pOneCurrentHP = pOneInfo['thp']
                    pOneLevel = pOneInfo['level']
                if new_game != 0:
                    game = new_game
                if bTimer is True:
                    asyncio.create_task(self.challengeTimeout(ctx))
                if playerOneID is not "":
                    playerOneID = playerOneID

                gameStatDump(playerOneID, playerTwoID, winner, quitter, pOneInfo, pTwoInfo, featToken, game, count,
                             token, critical, bonusHurt, nerveDamage, totalDamage, pOneTotalHP, pTwoTotalHP,
                             pOneCurrentHP, pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod, pOnemMod, pOneEvade,
                             pOneDeflect, pOneRiposte, pOneTempDR, pOneDeathsDoor, pOneQuickDamage, pOneFeatInfo,
                             pOneSpentFeat, pTwopMod, pTwocMod, pTwodMod, pTwomMod, pTwoEvade, pTwoDeflect,
                             pTwoRiposte, pTwoTempDR, pTwoDeathsDoor, pTwoQuickDamage, pTwoFeatInfo, pTwoSpentFeat,
                             pOneLevel, pTwoLevel, xp, currentPlayerXP, nextLevel, levelUp, iddqd, bEvasion,
                             bDeflect, channel)

        else:
            await ctx.send("A challenge has already been issued. Please wait until it has expired, or their fight is complete.")

    @challenge.error
    async def challenge_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("The command !challenge may not be used in PMs!")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You cannot challenge Nobody. He's immortal.")
        else:
            raise error

    #!accept
    @commands.command()
    @commands.guild_only()
    async def accept(self, ctx):
        accepted = str(ctx.message.author.id)
        path = os.getcwd()
        charFolder = os.path.join(path + "/characters/")

        arena, devroom = roomID()
        channelID = [arena, devroom]

        if ctx.channel.id in channelID:
            channel = ctx.channel.id
            playerOneID, playerTwoID, winner, quitter, pOneInfo, pTwoInfo, featToken, game, count, token, critical,\
            bonusHurt, nerveDamage, totalDamage, pOneTotalHP, pTwoTotalHP, pOneCurrentHP, pTwoCurrentHP, pOnepMod,\
            pOnecMod, pOnedMod, pOnemMod, pOneEvade, pOneDeflect, pOneRiposte, pOneTempDR, pOneDeathsDoor,\
            pOneQuickDamage, pOneFeatInfo, pOneSpentFeat, pTwopMod, pTwocMod, pTwodMod, pTwomMod, pTwoEvade,\
            pTwoDeflect, pTwoRiposte, pTwoTempDR, pTwoDeathsDoor, pTwoQuickDamage, pTwoFeatInfo, pTwoSpentFeat,\
            pOneLevel, pTwoLevel, xp, currentPlayerXP, nextLevel, levelUp, iddqd,\
            bEvasion, bDeflect = gameStatLoad(channel)

            msg, pTwoInfo, new_game, playerTwoID, bTimer, bGameTimer, new_oppenent, token \
                = onMSGAccept.message_accept(charFolder, accepted, game, playerTwoID, pOneInfo)

            if new_game is not None:
                game = new_game
            if pTwoInfo is not None:
                # pTwoInfo = pTwoInfo
                pTwoTotalHP = pTwoInfo['thp']
                pTwoCurrentHP = pTwoInfo['thp']
                pTwoLevel = pTwoInfo['level']
            if bTimer:
                self.timer.cancel()
            if bGameTimer:
                msg = asyncio.create_task(self.gameTimeout(ctx))
                await ctx.send(msg)
            if new_oppenent is not None:
                opponent = new_oppenent
            if playerTwoID is not None:
                playerTwoID = playerTwoID
            if token is not None:
                token = token
            for msg_item in msg:
                await ctx.send(msg_item)

            gameStatDump(playerOneID, playerTwoID, winner, quitter, pOneInfo, pTwoInfo, featToken, game, count,
                         token, critical, bonusHurt, nerveDamage, totalDamage, pOneTotalHP, pTwoTotalHP,
                         pOneCurrentHP, pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod, pOnemMod, pOneEvade,
                         pOneDeflect, pOneRiposte, pOneTempDR, pOneDeathsDoor, pOneQuickDamage, pOneFeatInfo,
                         pOneSpentFeat, pTwopMod, pTwocMod, pTwodMod, pTwomMod, pTwoEvade, pTwoDeflect,
                         pTwoRiposte, pTwoTempDR, pTwoDeathsDoor, pTwoQuickDamage, pTwoFeatInfo, pTwoSpentFeat,
                         pOneLevel, pTwoLevel, xp, currentPlayerXP, nextLevel, levelUp, iddqd, bEvasion,
                         bDeflect, channel)

    @accept.error
    async def accept_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("The command !accept may not be used in PMs!")
        else:
            raise error

    #!usefeat <feat name>
    @commands.command()
    @commands.guild_only()
    async def usefeat(self, ctx, *, answer):
        path = os.getcwd()
        charFolder = os.path.join(path + "/characters/")

        user = str(ctx.message.author.id)
        arena, devroom = roomID()
        channelID = [arena, devroom]

        if ctx.channel.id in channelID:
            channel = ctx.channel.id
            playerOneID, playerTwoID, winner, quitter, pOneInfo, pTwoInfo, featToken, game, count, token, critical,\
            bonusHurt, nerveDamage, totalDamage, pOneTotalHP, pTwoTotalHP, pOneCurrentHP, pTwoCurrentHP, pOnepMod,\
            pOnecMod, pOnedMod, pOnemMod, pOneEvade, pOneDeflect, pOneRiposte, pOneTempDR, pOneDeathsDoor,\
            pOneQuickDamage, pOneFeatInfo, pOneSpentFeat, pTwopMod, pTwocMod, pTwodMod, pTwomMod, pTwoEvade,\
            pTwoDeflect, pTwoRiposte, pTwoTempDR, pTwoDeathsDoor, pTwoQuickDamage, pTwoFeatInfo, pTwoSpentFeat,\
            pOneLevel, pTwoLevel, xp, currentPlayerXP, nextLevel, levelUp, iddqd,\
            bEvasion, bDeflect = gameStatLoad(channel)

            msg, featToken_new, pOneSpentFeat, pOneFeatInfo, pTwoSpentFeat, pTwoFeatInfo =\
                onMSGUtil.message_8_usefeat(answer, charFolder, user, game, playerOneID, playerTwoID, token, featToken,
                                            pOneInfo, pOneSpentFeat, pTwoSpentFeat, pTwoInfo)
            for msg_item in msg:
                await ctx.send(msg_item)
            # if featToken_new is not None:
            #     self.featToken = featToken_new
            # if pOneSpentFeat is not None:
            #     self.pOneSpentFeat.append(pOneSpentFeat)
            # if pOneFeatInfo is not None:
            #     self.pOneFeatInfo = pOneFeatInfo
            # if pTwoSpentFeat is not None:
            #     self.pTwoSpentFeat.append(pTwoSpentFeat)
            # if pTwoFeatInfo is not None:
            #     self.pTwoFeatInfo = pTwoFeatInfo

            gameStatDump(playerOneID, playerTwoID, winner, quitter, pOneInfo, pTwoInfo, featToken, game, count,
                         token, critical, bonusHurt, nerveDamage, totalDamage, pOneTotalHP, pTwoTotalHP,
                         pOneCurrentHP, pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod, pOnemMod, pOneEvade,
                         pOneDeflect, pOneRiposte, pOneTempDR, pOneDeathsDoor, pOneQuickDamage, pOneFeatInfo,
                         pOneSpentFeat, pTwopMod, pTwocMod, pTwodMod, pTwomMod, pTwoEvade, pTwoDeflect,
                         pTwoRiposte, pTwoTempDR, pTwoDeathsDoor, pTwoQuickDamage, pTwoFeatInfo, pTwoSpentFeat,
                         pOneLevel, pTwoLevel, xp, currentPlayerXP, nextLevel, levelUp, iddqd, bEvasion,
                         bDeflect, channel)

    @usefeat.error
    async def usefeat_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("The command !usefeat may not be used in PMs!")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please follow the command with the feat you want to use. Example: !usefeat Titan Blow")
        else:
            raise error

    #!roll
    @commands.command()
    @commands.guild_only()
    async def roll(self, ctx):
        user = str(ctx.message.author.id)

        path = os.getcwd()
        charFolder = os.path.join(path + "/characters/")

        arena, devroom = roomID()
        channelID = [arena, devroom]

        if ctx.channel.id in channelID:
            channel = ctx.channel.id
            playerOneID, playerTwoID, winner, quitter, pOneInfo, pTwoInfo, featToken, game, count, token, critical,\
            bonusHurt, nerveDamage, totalDamage, pOneTotalHP, pTwoTotalHP, pOneCurrentHP, pTwoCurrentHP, pOnepMod,\
            pOnecMod, pOnedMod, pOnemMod, pOneEvade, pOneDeflect, pOneRiposte, pOneTempDR, pOneDeathsDoor,\
            pOneQuickDamage, pOneFeatInfo, pOneSpentFeat, pTwopMod, pTwocMod, pTwodMod, pTwomMod, pTwoEvade,\
            pTwoDeflect, pTwoRiposte, pTwoQuickDamage, pTwoFeatInfo, pTwoSpentFeat, pOneLevel, pTwoLevel, xp,\
            currentPlayerXP, nextLevel, levelUp, iddqd, bEvasion, bDeflect = gameStatLoad(channel)
            try:
                self.gameTimer.cancel()
                msg, bEvasion, bDeflect, bGameTimer, playerOneID, playerTwoID, winner, pOneInfo, pTwoInfo,\
                featToken, game, count, token, critical, bonusHurt, totalDamage, pOneTotalHP, pTwoTotalHP,\
                pOneCurrentHP, pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod, pOnemMod, pOneEvade, pOneDeflect,\
                pOneRiposte, pOneTempDR, pOneDeathsDoor, pOneQuickDamage, pOneFeatInfo, pOneSpentFeat, pTwopMod,\
                pTwocMod, pTwodMod, pTwomMod, pTwoEvade, pTwoDeflect, pTwoRiposte, pTwoTempDR, pTwoDeathsDoor,\
                pTwoQuickDamage, pTwoFeatInfo, pTwoSpentFeat, pOneLevel, pTwoLevel, xp, currentPlayerXP,\
                nextLevel, levelUp, iddqd =\
                    onMSGRoll.message_roll(user, charFolder, playerOneID, playerTwoID, winner, pOneInfo, pTwoInfo,
                                           featToken, game, count, token, critical, bonusHurt, totalDamage,
                                           pOneTotalHP, pTwoTotalHP, pOneCurrentHP, pTwoCurrentHP, pOnepMod, pOnecMod,
                                           pOnedMod, pOnemMod, pOneEvade, pOneDeflect, pOneRiposte, pOneTempDR,
                                           pOneDeathsDoor, pOneQuickDamage, pOneFeatInfo, pOneSpentFeat, pTwopMod,
                                           pTwocMod, pTwodMod, pTwomMod, pTwoEvade, pTwoDeflect, pTwoRiposte,
                                           pTwoTempDR, pTwoDeathsDoor, pTwoQuickDamage, pTwoFeatInfo,
                                           pTwoSpentFeat, pOneLevel, pTwoLevel, xp, currentPlayerXP, nextLevel,
                                           levelUp, iddqd)
                for msg_item in msg:
                    await ctx.send(msg_item)
                    if bGameTimer:
                       self.gameTimer = asyncio.create_task(self.gameTimeout(ctx))
                    else:
                        self.gameTimer.cancel()
                        path = os.getcwd()
                        gameFolder = os.path.join(path + "/gamelogic/")
                        whichRoom = ctx.channel.id
                        onMSGUtil.soft_reset(gameFolder, whichRoom)

                gameStatDump(playerOneID, playerTwoID, winner, quitter, pOneInfo, pTwoInfo, featToken, game, count,
                             token, critical, bonusHurt, nerveDamage, totalDamage, pOneTotalHP, pTwoTotalHP,
                             pOneCurrentHP, pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod, pOnemMod, pOneEvade,
                             pOneDeflect, pOneRiposte, pOneTempDR, pOneDeathsDoor, pOneQuickDamage, pOneFeatInfo,
                             pOneSpentFeat, pTwopMod, pTwocMod, pTwodMod, pTwomMod, pTwoEvade, pTwoDeflect,
                             pTwoRiposte, pTwoTempDR, pTwoDeathsDoor, pTwoQuickDamage, pTwoFeatInfo, pTwoSpentFeat,
                             pOneLevel, pTwoLevel, xp, currentPlayerXP, nextLevel, levelUp, iddqd, bEvasion,
                             bDeflect, channel)

            except AttributeError:
                await ctx.send("Either a fight is not taking place, or it isn't your turn.")

    @roll.error
    async def roll_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("The command !roll may not be used in PMs!")
        else:
            raise error

    #!evasion
    @commands.command()
    @commands.guild_only()
    async def evasion(self, ctx):
        user = str(ctx.message.author.id)
        arena, devroom = roomID()
        channelID = [arena, devroom]

        if ctx.channel.id in channelID:
            channel = ctx.channel.id

            playerOneID, playerTwoID, winner, quitter, pOneInfo, pTwoInfo, featToken, game, count, token, critical,\
            bonusHurt, nerveDamage, totalDamage, pOneTotalHP, pTwoTotalHP, pOneCurrentHP, pTwoCurrentHP, pOnepMod,\
            pOnecMod, pOnedMod, pOnemMod, pOneEvade, pOneDeflect, pOneRiposte, pOneTempDR, pOneDeathsDoor,\
            pOneQuickDamage, pOneFeatInfo, pOneSpentFeat, pTwopMod, pTwocMod, pTwodMod, pTwomMod, pTwoEvade,\
            pTwoDeflect, pTwoRiposte, pTwoQuickDamage, pTwoFeatInfo, pTwoSpentFeat, pOneLevel, pTwoLevel, xp,\
            currentPlayerXP, nextLevel, levelUp, iddqd, bEvasion, bDeflect = gameStatLoad(channel)

            msg, bGameTimer, playerOneID, playerTwoID, pOneInfo, pTwoInfo, featToken, count, token, totalDamage,\
            pOneTotalHP, pTwoTotalHP, pOneCurrentHP, pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod,\
            pOnemMod, pOneQuickDamage, pTwoQuickDamage, iddqd =\
                onMSGUtil.message_8_evasion(user, playerOneID, playerTwoID, pOneInfo, pTwoInfo, featToken, count,
                                            token, critical, bonusHurt, totalDamage, pOneTotalHP, pTwoTotalHP,
                                            pOneCurrentHP,  pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod, pOnemMod,
                                            pOneQuickDamage, pTwoQuickDamage, iddqd)
            for msg_item in msg:
                await ctx.send(msg_item)
            if bGameTimer:
                self.gameTimer = asyncio.create_task(self.gameTimeout(ctx))
            if bEvasion is True:
                bEvasion = False
            if bDeflect is True:
                bDeflect = False

            gameStatDump(playerOneID, playerTwoID, winner, quitter, pOneInfo, pTwoInfo, featToken, game, count,
                         token, critical, bonusHurt, nerveDamage, totalDamage, pOneTotalHP, pTwoTotalHP,
                         pOneCurrentHP, pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod, pOnemMod, pOneEvade,
                         pOneDeflect, pOneRiposte, pOneTempDR, pOneDeathsDoor, pOneQuickDamage, pOneFeatInfo,
                         pOneSpentFeat, pTwopMod, pTwocMod, pTwodMod, pTwomMod, pTwoEvade, pTwoDeflect,
                         pTwoRiposte, pTwoTempDR, pTwoDeathsDoor, pTwoQuickDamage, pTwoFeatInfo,
                         pTwoSpentFeat, pOneLevel, pTwoLevel, xp, currentPlayerXP, nextLevel, levelUp, iddqd,
                         bEvasion, bDeflect, channel)

    @evasion.error
    async def evasion_error(self, ctx,error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("The command !evasion may not be used in PMs!")
        else:
            raise error

    #!deflect
    @commands.command()
    @commands.guild_only()
    async def deflect(self, ctx):
        user = str(ctx.message.author.id)
        arena, devroom = roomID()
        channelID = [arena, devroom]

        if ctx.channel.id in channelID:
            channel = ctx.channel.id

            playerOneID, playerTwoID, winner, quitter, pOneInfo, pTwoInfo, featToken, game, count, token, critical,\
            bonusHurt, nerveDamage, totalDamage, pOneTotalHP, pTwoTotalHP, pOneCurrentHP, pTwoCurrentHP, pOnepMod,\
            pOnecMod, pOnedMod, pOnemMod, pOneEvade, pOneDeflect, pOneRiposte, pOneTempDR, pOneDeathsDoor,\
            pOneQuickDamage, pOneFeatInfo, pOneSpentFeat, pTwopMod, pTwocMod, pTwodMod, pTwomMod, pTwoEvade,\
            pTwoDeflect, pTwoRiposte, pTwoQuickDamage, pTwoFeatInfo, pTwoSpentFeat, pOneLevel, pTwoLevel, xp,\
            currentPlayerXP, nextLevel, levelUp, iddqd, bEvasion, bDeflect = gameStatLoad(channel)

            msg, bGameTimer, playerOneID, playerTwoID, pOneInfo, pTwoInfo, featToken, count, token, totalDamage,\
            pOneTotalHP, pTwoTotalHP, pOneCurrentHP, pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod, pOnemMod,\
            pOneQuickDamage, pTwoQuickDamage, pTwoDeflect, pOneDeflect, pOneDeathsDoor,\
            pTwoDeathsDoor, iddqd =\
                onMSGUtil.message_8_deflect(user, playerOneID, playerTwoID, pOneInfo, pTwoInfo, featToken, count,
                                            token, critical, bonusHurt, totalDamage, pOneTotalHP, pTwoTotalHP,
                                            pOneCurrentHP,  pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod, pOnemMod,
                                            pOneQuickDamage, pTwoQuickDamage, pTwoDeflect, pOneDeflect,
                                            pOneDeathsDoor, pTwoDeathsDoor, iddqd)
            for msg_item in msg:
                await ctx.send(msg_item)
            if bGameTimer:
                self.gameTimer = asyncio.create_task(self.gameTimeout(ctx))
            if bDeflect is True:
               bDeflect = False
            if bEvasion is True:
               bEvasion = False

            gameStatDump(playerOneID, playerTwoID, winner, quitter, pOneInfo, pTwoInfo, featToken, game, count,
                         token, critical, bonusHurt, nerveDamage, totalDamage, pOneTotalHP, pTwoTotalHP,
                         pOneCurrentHP, pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod, pOnemMod, pOneEvade,
                         pOneDeflect, pOneRiposte, pOneTempDR, pOneDaethsDoor, pOneQuickDamage, pOneFeatInfo,
                         pOneSpentFeat, pTwopMod, pTwocMod, pTwodMod, pTwomMod, pTwoEvade, pTwoDeflect,
                         pTwoRiposte, pTwoTempDR, pTwoDeathsDoor, pTwoQuickDamage, pTwoFeatInfo, pTwoSpentFeat,
                         pOneLevel, pTwoLevel, xp, currentPlayerXP, nextLevel, levelUp, iddqd, bEvasion,
                         bDeflect, channel)

    @deflect.error
    async def deflect_error(self, ctx,error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("The command !deflect may not be used in PMs!")
        else:
            raise error

    @commands.command()
    @commands.guild_only()
    async def permit(self, ctx):
        user = str(ctx.message.author.id)
        arena, devroom = roomID()
        channelID = [arena, devroom]

        if ctx.channel.id in channelID:
            channel = ctx.channel.id

            playerOneID, playerTwoID, winner, quitter, pOneInfo, pTwoInfo, featToken, game, count, token, critical,\
            bonusHurt, nerveDamage, totalDamage, pOneTotalHP, pTwoTotalHP, pOneCurrentHP, pTwoCurrentHP, pOnepMod,\
            pOnecMod, pOnedMod, pOnemMod, pOneEvade, pOneDeflect, pOneRiposte, pOneTempDR, pOneDeathsDoor,\
            pOneQuickDamage, pOneFeatInfo, pOneSpentFeat, pTwopMod, pTwocMod, pTwodMod, pTwomMod, pTwoEvade,\
            pTwoDeflect, pTwoRiposte, pTwoTempDR, pTwoDeathsDoor, pTwoQuickDamage, pTwoFeatInfo, pTwoSpentFeat,\
            pOneLevel, pTwoLevel, xp, currentPlayerXP, nextLevel, levelUp, iddqd,\
            bEvasion, bDeflect = gameStatLoad(channel)

            msg, bGameTimer, playerOneID, playerTwoID, pOneInfo, pTwoInfo, featToken, count, token, totalDamage,\
            pOneTotalHP, pTwoTotalHP, pOneCurrentHP, pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod, pOnemMod,\
            pOneQuickDamage, pTwoQuickDamage, pOneDeathsDoor, pTwoDeathsDoor, iddqd =\
                onMSGUtil.message_7_permit(user, playerOneID, playerTwoID, pOneInfo, pTwoInfo, featToken, count,
                                           token, critical, bonusHurt, totalDamage, pOneTotalHP, pTwoTotalHP,
                                           pOneCurrentHP,  pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod, pOnemMod,
                                           pOneQuickDamage, pTwoQuickDamage, pOneDeathsDoor,\
                                           pTwoDeathsDoor, iddqd)
            for msg_item in msg:
                await ctx.send(msg_item)
            if bGameTimer:
                self.gameTimer = asyncio.create_task(self.gameTimeout(ctx))

            if bEvasion is True:
                bEvasion = False
            if bDeflect is True:
                bDeflect = False

            gameStatDump(playerOneID, playerTwoID, winner, quitter, pOneInfo, pTwoInfo, featToken, game, count,
                         token, critical, bonusHurt, nerveDamage, totalDamage, pOneTotalHP, pTwoTotalHP,
                         pOneCurrentHP, pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod, pOnemMod, pOneEvade,
                         pOneDeflect, pOneRiposte, pOneTempDr, pOneDeathsDoor, pOneQuickDamage, pOneFeatInfo,
                         pOneSpentFeat, pTwopMod, pTwocMod, pTwodMod, pTwomMod, pTwoEvade, pTwoDeflect,
                         pTwoRiposte, pTwoTempDR, pTwoDeathsDoor, pTwoQuickDamage, pTwoFeatInfo, pTwoSpentFeat,
                         pOneLevel, pTwoLevel, xp, currentPlayerXP, nextLevel, levelUp, iddqd, bEvasion,
                         bDeflect, channel)

    @permit.error
    async def permit_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("The command !permit may not be used in PMs!")
        else:
            raise error

    #!forfeit still testing
    # @commands.command()
    # @commands.guild_only()
    # async def forfeit(self, ctx):
    #     user = str(ctx.message.author.id)
    #     if self.game == 1:
    #         if user == self.playerOne or user == self.playerTwo:
    #             if character.lower() == self.playerOne:
    #                 await ctx.send(self.pOneInfo['name'] + " has forfeited the match.")
    #                 xpCap = self.pOneInfo['nextlevel'] - 10
    #                 if self.pOneInfo['currentxp'] < xpCap:
    #                     await ctx.send(self.pOneInfo['name'] + " has earned 10xp")
    #                     with open(charFolder + user + '.txt', 'r+') as file:
    #                         charData = json.load(file)
    #                         self.pOneInfo['currentxp'] = self.pOneInfo['currentxp'] + 10
    #                         file.seek(0)
    #                         file.write(json.dumps(charData, ensure_ascii=False, indent=2))
    #                         file.truncate()
    #                         file.close()
    #                 else:
    #                     await ctx.send(self.pOneInfo['name'] + " has earned 0xp")
    #             elif user == self.playerTwo:
    #                 await ctx.send(self.pOneInfo['name'] + " has forfeited the match.")
    #                 xpCap = self.pTwoInfo['nextlevel'] - 10
    #                 if self.pTwoInfo['currentxp'] < xpCap:
    #                     await ctx.send(self.pTwoInfo['name'] + " has earned 10xp")
    #                     with open(charFolder + user + '.txt', 'r+') as file:
    #                         charData = json.load(file)
    #                         self.pTwoInfo['currentxp'] = self.pTwoInfo['currentxp'] + 10
    #                         file.seek(0)
    #                         file.write(json.dumps(charData, ensure_ascii=False, indent=2))
    #                         file.truncate()
    #                         file.close()
    #                 else:
    #                     await ctx.send(self.pTwoInfo['name'] + " has earned 0xp")
    #             self.opponent = ""
    #             self.playerOne = ""
    #             self.playerTwo = ""
    #             self.winner = ""
    #             self.loser = ""
    #             self.pOneUsername = None
    #             self.pTwoUsername = None
    #             # PLAYER INFO
    #             self.pOneInfo = {}
    #             self.pTwoInfo = {}
    #             # HP AND TURN COUNTERS
    #             self.gameTimer.cancel()
    #             self.gameTimer = 0
    #             self.count = 0
    #             self.base = 0
    #             self.token = 0
    #             self.game = 0
    #             self.critical = 0
    #             self.bonusHurt = 0
    #             self.nerveDamage = 0
    #             self.totalDamage = 0
    #             self.pOneTotalHP = 0
    #             self.pTwoTotalHP = 0
    #             self.pOneCurrentHP = 0
    #             self.pTwoCurrentHP = 0
    #             # PLAYER ONE FEAT COUNTERS
    #             self.pOnepMod = 0
    #             self.pOnecMod = 0
    #             self.pOnedMod = 0
    #             self.pOnemMod = 0
    #             self.pOneEvade = 1
    #             self.pOneDeflect = 1
    #             self.pOneRiposte = 0
    #             self.pOneQuickDamage = 0
    #             self.pOneFeatInfo = None
    #             self.pOneSpentFeat = []
    #             # PLAYER TWO FEAT COUNTERS
    #             self.pTwopMod = 0
    #             self.pTwocMod = 0
    #             self.pTwodMod = 0
    #             self.pTwomMod = 0
    #             self.pTwoEvade = 1
    #             self.pTwoDeflect = 1
    #             self.pTwoRiposte = 0
    #             self.pTwoQuickDamage = 0
    #             self.pTwoFeatInfo = None
    #             self.pTwoSpentFeat = []
    #             # XP AND LEVEL COUNTERS
    #             self.pOneLevel = 0
    #             self.pTwoLevel = 0
    #             self.xp = 0
    #             self.currentPlayerXP = 0
    #             self.nextLevel = 0
    #             self.levelUp = 0
    #             await ctx.send("Well, that was a waste everyone's time. Show's over folks. (Resetting Match Status)")
    #         else:
    #             await ctx.send("You aren't even fighting, why you so afraid?")
    #     else:
    #         await ctx.send("There is no fight taking place. What are you running from?")
    #
    # @forfeit.error
    # async def forfeit_error(self, ctx, error):
    #     if isinstance(error, commands.NoPrivateMessage):
    #         await ctx.send("The command !forfeit may not be used in PMs!")
    #     else:
    #         raise error

    @commands.command()
    @commands.guild_only()
    # !pattack <amount>
    async def pattack(self, ctx, *, points):
        user = str(ctx.message.author.id)
        arena, devroom = roomID()
        channelID = [arena, devroom]

        if ctx.channel.id in channelID:
            channel = ctx.channel.id
            playerOneID, playerTwoID, winner, quitter, pOneInfo, pTwoInfo, featToken, game, count, token, critical,\
            bonusHurt, nerveDamage, totalDamage, pOneTotalHP, pTwoTotalHP, pOneCurrentHP, pTwoCurrentHP, pOnepMod,\
            pOnecMod, pOnedMod, pOnemMod, pOneEvade, pOneDeflect, pOneRiposte, pOneTempDR, pOneDeathsDoor,\
            pOneQuickDamage, pOneFeatInfo, pOneSpentFeat, pTwopMod, pTwocMod, pTwodMod, pTwomMod, pTwoEvade,\
            pTwoDeflect, pTwoRiposte, pTwoTempDR, pTwoDeathsDoor, pTwoQuickDamage, pTwoFeatInfo, pTwoSpentFeat,\
            pOneLevel, pTwoLevel, xp, currentPlayerXP, nextLevel, levelUp, iddqd,\
            bEvasion, bDeflect = gameStatLoad(channel)

            msg, game, playerOneID, playerTwoID, pOneInfo, pTwoInfo, token, pOnepMod, pTwopMod, pOneLevel, pTwoLevel =\
                onMSGUtil.message_8_pattack(user, points, game, playerOneID, playerTwoID, pOneInfo, pTwoInfo, token,
                                            pOnepMod, pTwopMod, pOneLevel, pTwoLevel)
            for msg_item in msg:
                await ctx.send(msg_item)

            gameStatDump(playerOneID, playerTwoID, winner, quitter, pOneInfo, pTwoInfo, featToken, game,
                         count, token, critical, bonusHurt, nerveDamage, totalDamage, pOneTotalHP, pTwoTotalHP,
                         pOneCurrentHP, pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod, pOnemMod, pOneEvade, pOneDeflect,
                         pOneRiposte, pOneTempDR, pOneDeathsDoor, pOneQuickDamage, pOneFeatInfo, pOneSpentFeat, pTwopMod,
                         pTwocMod, pTwodMod, pTwomMod, pTwoEvade, pTwoDeflect, pTwoRiposte, pTwoTempDR, pTwoDeathsDoor,
                         pTwoQuickDamage, pTwoFeatInfo, pTwoSpentFeat, pOneLevel, pTwoLevel, xp, currentPlayerXP,
                         nextLevel, levelUp, iddqd, bEvasion, bDeflect, channel)

    @pattack.error
    async def pattack_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("The command !pattack may not be used in PMs!")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please follow the command with the amount of points you want to spend. Example: "
                           "!pattack 1")
        else:
            raise error

    #!dfight <amount>
    @commands.command()
    @commands.guild_only()
    async def dfight(self, ctx, *, points):
        user = str(ctx.message.author.id)
        arena, devroom = roomID()
        channelID = [arena, devroom]

        if ctx.channel.id in channelID:
            channel = ctx.channel.id
            playerOneID, playerTwoID, winner, quitter, pOneInfo, pTwoInfo, featToken, game, count, token,\
            critical, bonusHurt, nerveDamage, totalDamage, pOneTotalHP, pTwoTotalHP, pOneCurrentHP, pTwoCurrentHP,\
            pOnepMod, pOnecMod, pOnedMod, pOnemMod, pOneEvade, pOneDeflect, pOneRiposte, pOneTempDR, pOneDeathsDoor,\
            pOneQuickDamage, pOneFeatInfo, pOneSpentFeat, pTwopMod, pTwocMod, pTwodMod, pTwomMod, pTwoEvade,\
            pTwoDeflect, pTwoRiposte, pTwoTempDR, pTwoDeathsDoor, pTwoQuickDamage, pTwoFeatInfo, pTwoSpentFeat,\
            pOneLevel, pTwoLevel, xp, currentPlayerXP, nextLevel, levelUp, iddqd,\
            bEvasion, bDeflect = gameStatLoad(channel)

            msg, game, playerOneID, playerTwoID, pOneInfo, pTwoInfo, token, pOnedMod, pTwodMod, pOneLevel, pTwoLevel\
                = onMSGUtil.message_8_dfight(user, points, game, playerOneID, playerTwoID, pOneInfo, pTwoInfo,
                                             token, pOnedMod, pTwodMod, pOneLevel, pTwoLevel)
            for msg_item in msg:
                await ctx.send(msg_item)

            gameStatDump(playerOneID, playerTwoID, winner, quitter, pOneInfo, pTwoInfo, featToken, game,
                         count, token, critical, bonusHurt, nerveDamage, totalDamage, pOneTotalHP, pTwoTotalHP,
                         pOneCurrentHP, pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod, pOnemMod, pOneEvade, pOneDeflect,
                         pOneRiposte, pOneTempDR, pOneDeathsDoor, pOneQuickDamage, pOneFeatInfo, pOneSpentFeat,
                         pTwopMod, pTwocMod, pTwodMod, pTwomMod, pTwoEvade, pTwoDeflect, pTwoRiposte, pTwoTempDR,
                         pTwoDeathsDoor, pTwoQuickDamage, pTwoFeatInfo, pTwoSpentFeat, pOneLevel, pTwoLevel, xp,
                         currentPlayerXP, nextLevel, levelUp, iddqd, bEvasion, bDeflect, channel)

        # Allows for the use of the 'defensive fighting' passive feat. Makes sure it applies correct bonuses for correct
        # levels.

    @dfight.error
    async def dfight_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("The command !dfight may not be used in PMs!")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please follow the command with the amount of points you want to spend. Example: "
                           "!dfight 1")
        else:
            raise error

    #!cexpert - Removed from Game
    # @commands.command()
    # @commands.guild_only()
    # async def cexpert(self, ctx, *, message):
    #     character = ctx.author.send
    # # make sure that this command cannot be ran if a fight is taking place.
    #     if self.game == 1:
    #         # ensures the command can only be used by player one, when it is their turn. To prevent trolls from
    #         # spamming commands.
    #         if character == self.pOneUsername and self.token == 1:
    #             mod = int(message)
    #             if self.pOneLevel <= 4 and mod == 1:
    #                 self.pOnecMod = 1
    #             elif 4 < self.pOneLevel <= 8 and mod == 2:
    #                 self.pOnecMod = 2
    #             elif 8 < self.pOneLevel <= 12 and mod == 3:
    #                 self.pOnecMod = 3
    #             elif 12 < self.pOneLevel <= 16 and mod == 4:
    #                 self.pOnecMod = 4
    #             elif 16 < self.pOneLevel <= 20 and mod == 5:
    #                 self.pOnecMod = 5
    #             else:
    #                 await ctx.send("You are not high enough level to invest that many points.")
    #         # ensures the command can only be used by player two, when it is their turn. To prevent trolls from
    #         # spamming commands.
    #         elif character == self.pTwoUsername and self.token == 2:
    #             mod = int(message)
    #             if self.pTwoLevel <= 4 and mod == 1:
    #                 self.pTwocMod = 1
    #             elif 4 < self.pTwoLevel <= 8 and mod == 2:
    #                 self.pTwocMod = 2
    #             elif 8 < self.pTwoLevel <= 12 and mod == 3:
    #                 self.pTwocMod = 3
    #             elif 12 < self.pTwoLevel <= 16 and mod == 4:
    #                 self.pTwocMod = 4
    #             elif 16 < self.pTwoLevel <= 20 and mod == 5:
    #                 self.pTwocMod = 5
    #             else:
    #                 await ctx.send("You are not high enough level to invest that many points.")
    #
    #         else:
    #             await ctx.send("Either it's not your turn, or you aren't even fighting. Either way, No.")
    #
    #     else:
    #         await ctx.send("This command does nothing right now. No combat is taking place.")
    #
    # @cexpert.error
    # async def name_cexpert(self, ctx, error):
    #     if isinstance(error, commands.NoPrivateMessage):
    #         await ctx.send("The command !cexpert may not be used in PMs!")
    #     else:
    #         raise error

    @commands.command()
    @commands.guild_only()
    #!masochist
    async def masochist(self, ctx, *, points):
        user = str(ctx.message.author.id)
        arena, devroom = roomID()
        channelID = [arena, devroom]

        if ctx.channel.id in channelID:
            channel = ctx.channel.id
            playerOneID, playerTwoID, winner, quitter, pOneInfo, pTwoInfo, featToken, game, count, token, critical,\
            bonusHurt, nerveDamage, totalDamage, pOneTotalHP, pTwoTotalHP, pOneCurrentHP, pTwoCurrentHP, pOnepMod,\
            pOnecMod, pOnedMod, pOnemMod, pOneEvade, pOneDeflect, pOneRiposte, pOneTempDR, pOneDeathsDoor,\
            pOneQuickDamage, pOneFeatInfo, pOneSpentFeat, pTwopMod, pTwocMod, pTwodMod, pTwomMod, pTwoEvade,\
            pTwoDeflect, pTwoRiposte, pTwoTempDR, pTwoDeathsDoor, pTwoQuickDamage, pTwoFeatInfo, pTwoSpentFeat,\
            pOneLevel, pTwoLevel, xp, currentPlayerXP, nextLevel, levelUp, iddqd,\
            bEvasion, bDeflect = gameStatLoad(channel)

            msg, game, playerOneID, playerTwoID, pOneInfo, pTwoInfo, token, pOnemMod, pTwomMod, pOneLevel, pTwoLevel \
                = onMSGUtil.message_10_masochist(user, points, game, playerOneID, playerTwoID, pOneInfo, pTwoInfo,
                                                 token, pOnemMod, pTwomMod, pOneLevel, pTwoLevel)
            for msg_item in msg:
                await ctx.send(msg_item)

            gameStatDump(playerOneID, playerTwoID, winner, quitter, pOneInfo, pTwoInfo, featToken, game,
                         count, token, critical, bonusHurt, nerveDamage, totalDamage, pOneTotalHP, pTwoTotalHP,
                         pOneCurrentHP, pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod, pOnemMod, pOneEvade,
                         pOneDeflect, pOneRiposte, pOneTempDR, pOneDeathsDoor, pOneQuickDamage, pOneFeatInfo,
                         pOneSpentFeat, pTwopMod, pTwocMod, pTwodMod, pTwomMod, pTwoEvade, pTwoDeflect, pTwoRiposte,
                         pTwoTempDR, pTwoDeathsDoor, pTwoQuickDamage, pTwoFeatInfo, pTwoSpentFeat,
                         pOneLevel, pTwoLevel, xp, currentPlayerXP, nextLevel, levelUp, iddqd, bEvasion, bDeflect,
                         channel)

    @masochist.error
    async def masochist_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("The command !masochist may not be used in PMs!")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please follow the command with the amount of points you want to spend. Example: "
                           "!masochist 1")
        else:
            raise error

#------------------------------------------PM COMMANDS------------------------------------------------------------------
   #!stats <str> <dex> <con>
    @commands.command()
    @commands.dm_only()
    async def stats(self, ctx, strength, dexterity, constitution):
        player = str(ctx.message.author.id)
        charFolder = characters()
        try:
            msg = onPRIUtil.pri_6_stats(charFolder, player, strength, dexterity, constitution)
            for msg_item in msg:
                await ctx.send(msg_item)
        except IndexError:
            await ctx.send("You need to use the command as instructed. !stat <str> <dex> <con>. Where "
                                   "<str> is your desired strength, <dex> is your desired dexterity, and "
                                   "<con> is your desired constitution. Example: !stats 10 5 0")
        except ValueError:
            await ctx.send("You need to use the command as instructed. !stat <str> <dex> <con>. Where "
                                   "<str> is your desired strength, <dex> is your desired dexterity, and "
                                   "<con> is your desired constitution. Example: !stats 10 5 0")
        except UnboundLocalError:
            await ctx.send("You don't even have a character created yet. Type !name <name> in the room. "
                                   "Where <name> is your character's actual name. Example: !name Joe")

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

    #!trait <trait name>
    @commands.command()
    @commands.dm_only()
    async def traitpick(self, ctx, trait):
        traitDictionary = traitDict()[0]
        traitList = traitDict()[1]
        trait = trait.lower()
        player = str(ctx.message.author.id)
        charFolder = characters()
        msg = onPRIUtil.pri_6_trait(charFolder, player, traitList, traitDictionary, trait)
        await ctx.send(msg)

    @traitpick.error
    async def trait_error(self, ctx, error):
        if isinstance(error, commands.PrivateMessageOnly):
            await ctx.send("The command !trait can only be used in PMs!")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please follow the command with the name of the trait you want to select. Example: "
                           "!trait regeneration")
        else:
            raise error

    #!traitlist
    @commands.command()
    @commands.dm_only()
    async def traitlist(self, ctx):
        # traitDictionary = traitDict()[0]
        traitList = traitDict()[1]

        stringList = "\n".join(traitList)
        await ctx.send(stringList + "\n Type: !traithelp <trait name> to get a PM of feat info")

    @traitlist.error
    async def traitlist_error(self, ctx, error):
        if isinstance(error, commands.PrivateMessageOnly):
            await ctx.send("The command !traitlist can only be used in PMs!")
        else:
            raise error

    #!traithelp <trait name>
    @commands.command()
    @commands.dm_only()
    async def traithelp(self, ctx, answer):
        traitDictionary = traitDict()[0]
        traitList = traitDict()[1]
        answer = answer.lower()

        if answer not in traitList:
            await ctx.send("Make sure you have spelled the feat correctly")
        else:
            await ctx.send("```" + answer + ":\n" + traitDictionary[0][answer]['desc'] + "```")

    @traithelp.error
    async def traithelp_error(self, ctx, error):
        if isinstance(error, commands.PrivateMessageOnly):
            await ctx.send("The command !traithelp can only be used in PMs!")
        else:
            raise error

    #!respec
    @commands.command()
    @commands.dm_only()
    async def respec(self, ctx):
        print("Am I here?")
        player = str(ctx.message.author.id)
        path = os.getcwd()
        charFolder = os.path.join(path + "/characters/")
        charFile = Path(charFolder + player + ".txt")
        file = open(charFolder + player + ".txt", "r", encoding="utf-8")
        charData = json.load(file)
        file.close()
        msg = onPRIUtil.pri_7_respec(charData, charFolder, charFile, player)
        await ctx.send(msg)

    @respec.error
    async def respec_error(self, ctx, error):
        if isinstance(error, commands.PrivateMessageOnly):
            await ctx.send("The command !respec can only be used in PMs!")
        else:
            raise error

    #!add
    @commands.command()
    @commands.dm_only()
    async def add(self, ctx, ability):
        ability.lower()
        player = str(ctx.message.author.id)
        path = os.getcwd()
        charFolder = os.path.join(path + "/characters/")
        msg = onPRIUtil.pri_4_add(player, ability, path, charFolder)
        for msg_item in msg:
            await ctx.send(msg_item)

    @add.error
    async def add_error(self, ctx, error):
        if isinstance(error, commands.PrivateMessageOnly):
            await ctx.send("This is a PM only command. I try to keep your ability points secret, and this is the "
                           "thanks I get for it.")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You need to specify the ability you want to point the point to. I couldn't have made it "
                           "any more simple for you. Type '!add str' or '!add strength' for strength, and so on. I don't "
                           "even need a number, just follow the instructions, and I'll do the rest.")
        else:
            raise error

    #!viewchar
    @commands.command()
    @commands.dm_only()
    async def viewchar(self, ctx):

        private = ctx.author.send
        player = str(ctx.message.author.id)

        path = os.getcwd()
        charFolder = os.path.join(path + "/characters/")
        charFile = Path(charFolder + player + ".txt")
        file = open(charFolder + player + ".txt", "r", encoding="utf-8")
        charStats = json.load(file)
        file.close()

        # Find out if player even has a character created yet. If not. Tell them they are an idiot.
        msg = onPRIUtil.pri_viewchar(player)
        for msg_item in msg:
            await ctx.send(msg_item)

    @viewchar.error
    async def viewchar_error(self, ctx, error):
        if isinstance(error, commands.PrivateMessageOnly):
            await ctx.send("Why would you want to display your character sheet "
                           "in a public room? PM me with the command.")
        else:
            raise error

    #!featlist
    @commands.command()
    @commands.dm_only()
    async def featlist(self, ctx):

        featDictionary = featDict()[0]
        featList = featDict()[1]

        stringList = "\n".join(featList)
        await ctx.send(stringList + "\n Type: !feathelp <feat name> to get a PM of feat info")

    @featlist.error
    async def featlist_error(self, ctx, error):
        if isinstance(error, commands.PrivateMessageOnly):
            await ctx.send("I'm not gonna spam the arena with this list, man. PM me with !featlist")
        else:
            raise error

    #!feathelp
    @commands.command()
    @commands.dm_only()
    async def feathelp(self, ctx, *, answer):

        featDictionary = featDict()[0]
        featList = featDict()[1]
        answer = answer.lower()

        if answer not in featList:
            await ctx.send("Make sure you have spelled the feat correctly")
        else:
            reqStat = featDictionary[0][answer]['stat']
            featStatus = featDictionary[0][answer]['status']
            level = featDictionary[0][answer]['requirements'][0]
            reqStr = featDictionary[0][answer]['requirements'][1]
            reqDex = featDictionary[0][answer]['requirements'][2]
            reqCon = featDictionary[0][answer]['requirements'][3]
            reqFeats = featDictionary[0][answer]['requirements'][4]
            await ctx.send("```" + answer + " (" + reqStat + ") (" + featStatus + ")\n" +
                        featDictionary[0][answer]['desc'] +
                        "\nPrerequisites: " + "\nLevel: " + str(level) + " Strength: " + str(
                reqStr) + " Dexterity: " +
                        str(reqDex) + " Constitution: " + str(reqCon) + " Required Feats: " + reqFeats + "```")

    @feathelp.error
    async def feathelp_error(self, ctx, error):
        if isinstance(error, commands.PrivateMessageOnly):
            await ctx.send("I'm not gonna spam the arena with this, man. PM me with !feathelp <feat> for assistance.")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please enter the name of the feat you want help on. Example: !featlist power attack")

        raise error

    #!featpick
    @commands.command()
    @commands.dm_only()
    async def featpick(self, ctx, *, answer):

        private = ctx.author.send
        player = str(ctx.message.author.id)
        charFolder = characters()

        featDictionary = featDict()[0]
        featList = featDict()[1]

        answer = answer.lower()
        msg = onPRIUtil.pri_10_feat_pick(answer, player, featList, featDictionary, charFolder)
        for msg_item in msg:
            await ctx.send(msg_item)

    @featpick.error
    async def featpick_error(self, ctx, error):
        if isinstance(error, commands.PrivateMessageOnly):
            await ctx.send("You need to PM me with !featpick <featname> for this command to work.")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please enter the name of the feat you want to take. Example: !featpick power attack")
        else:
            raise error

    #!stockarmor
    @commands.command()
    @commands.dm_only()
    #@commands.has_role("Admin")
    async def stockarmor(self, ctx):
        catOneCommonList, catOneUncommonList, catOneRareList, catTwoCommonList, catTwoUncommonList,\
        catTwoRareList, catThreeCommonList, catThreeUncommonList, catThreeRareList = armorShop()

        itemFolder = items()

        msg = onPRIUtil.pri_11_stockarmor(catOneCommonList, catOneUncommonList, catOneRareList, catTwoCommonList,
                                catTwoUncommonList, catTwoRareList, catThreeCommonList,
                                catThreeUncommonList, catThreeRareList, itemFolder)
        await ctx.send(msg)

    @stockarmor.error
    async def stockarmor_error(self, ctx, error):
        if isinstance(error, commands.PrivateMessageOnly):
            await ctx.send("The !stockarmor command can only be used in PMs")
        else:
            raise error

    #!armorshop
    @commands.command()
    @commands.dm_only()
    async def armorshop(self, ctx):
        itemFolder = items()
        msg = onPRIUtil.pri_10_armorshop(itemFolder)
        await ctx.send("```" + msg + "```")

    @armorshop.error
    async def armorshop_error(self, ctx, error):
        if isinstance(error, commands.PrivateMessageOnly):
            await ctx.send("The command !armorshop may only be used in PMs")

    @commands.command()
    @commands.dm_only()
    #@commands.has_role("Admin")
    async def stockpotion(self, ctx):
        commonList, uncommonList, rareList, vrareList, relicList = potionShop()
        itemFolder = items()
        msg = onPRIUtil.pri_10_stockpotion(commonList, uncommonList, rareList, vrareList, relicList,
                                          itemFolder)
        await ctx.send("```" + msg + "```")

    @stockpotion.error
    async def stockpotion_error(self, ctx, error):
        if isinstance(error, commands.PrivateMessageOnly):
            await ctx.send("The command !stockpotion may only be used in PMs")
        else:
            raise error

    #!potionshop
    @commands.command()
    async def potionshop(self, ctx):
        itemFolder = items()
        potionFile = open(itemFolder + "potions.txt", "r", encoding="utf-8")
        potionDictionary = json.load(potionFile)
        potionFile.close()
        shopList = potionDictionary[0]['shoplist']
        orderedList = Counter(shopList)
        item = []
        for key in orderedList:
            item.append(key)
            item.append(orderedList[key])
            if key in potionDictionary[0]['common']:
                item.append(potionDictionary[0]['common'][key][0])
            elif key in potionDictionary[0]['uncommon']:
                item.append(potionDictionary[0]['uncommon'][key][0])
            elif key in potionDictionary[0]['rare']:
                item.append(potionDictionary[0]['rare'][key][0])
            elif key in potionDictionary[0]['vrare']:
                item.append(potionDictionary[0]['vrare'][key][0])
            elif key in potionDictionary[0]['relic']:
                item.append(potionDictionary[0]['relic'][key][0])

        shopList = "\n".join("{}: {} ({} gold)".format(*i)
                             for i in zip(item[::3], item[1::3], item[2::3]))

        await ctx.send("Items available in shop: (Item:  Amount (cost)) \n" + shopList)

    @potionshop.error
    async def potionshop_error(self, ctx, error):
        if isinstance(error, commands.PrivateMessageOnly):
            await ctx.send("The command !potionshop may only be used in PMs")
        else:
            raise error

    #!rewardgold <gold> <player> <reason> (If no reason, default to: "Not Specified")
    @commands.command()
    @commands.dm_only()
    async def rewardgold(self, ctx, gold, player, reason="Not Specified"):
        msg = ""
        charFolder = characters()
        stuffFolder = roomID()
        with open(charFolder + "playerDatabase.txt", 'r', encoding="utf-8") as file2:
            playerDatabase = json.loads(file2.read())
            file2.close()
        with open(roomID, + "token.txt", 'r', encoding="utf-8") as file:
            stuff = json.loads(file.read())
            file.close()
        try:
            gifted = ""
            for item in playerDatabase.items():
                if item[0].lower() == player.lower():
                    gifted = item[1]
            giftedFile = open(charFolder + gifted + ".txt", "r", encoding="utf-8")
            giftedData = json.load(giftedFile)
            giftedFile.close()
            giftedData['gold'] += int(gold)
            file = open(charFolder + gifted + ".txt", "w", encoding="utf-8")
            json.dump(giftedData, file, ensure_ascii=False, indent=2)
            file.close()
            gifted = int(gifted)
            user = ctx.bot.get_user(gifted)
            await user.send(player + " has been awarded  " + str(gold) +
                                      " gold. (Reason: " + reason + ")")
            gameMaster = stuff["gamemaster"]
            user = ctx.bot.get_user(gameMaster)
            await user.send(player + " has been awarded " + str(gold) +
                            " gold. (Reason: " + reason + ")")
        except FileNotFoundError:
            await ctx.send(player + " does not have a character.")


    @rewardgold.error
    async def rewardgold_error(self, ctx, error):
        if isinstance(error, commands.PrivateMessageOnly):
            await ctx.send("The command !rewardgold may only be used in PMs")
        else:
            raise error

    #!wholevel <level>
    @commands.command()
    @commands.dm_only()
    async def wholevel(self, ctx, level):
        msg = onPRIUtil.pri_9_wholevel(level)
        for msg_item in msg:
            await ctx.send(msg_item)

    @wholevel.error
    async def wholevel_error(self, ctx, error):
        if isinstance(error, commands.PrivateMessageOnly):
            await ctx.send("The command !wholevel may only be used in PMs")
        else:
            raise error

def setup(client):
    client.add_cog(Combat(client))
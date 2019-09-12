import os
import json
import random
import time
from pathlib import Path

import discord
from discord.ext import commands

from gamelogic import onMSGAccept, onMSGRoll, onMSGUtil, onPRIUtil, playerone_zero_current_hp, playertwo_zero_current_hp, Roll_not_strike, Roll_true_strike

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

class Combat(commands.Cog):

    def __init__(self, client):

        self.opponent = ""
        self.client = client
        # STRINGS
        self.opponent = ""
        self.playerOne = ""
        self.playerTwo = ""
        self.winner = ""
        self.quitter = ""
        # PLAYER INFO
        self.pOneInfo = {}
        self.pTwoInfo = {}
        # HP AND TURN COUNTERS
        # challenge = 0
        # reset = 0
        self.featToken = 0
        self.game = 0
        self.count = 0
        self.token = 0
        self.critical = 0
        self.bonusHurt = 0
        self.nerveDamage = 0
        self.totalDamage = 0
        self.pOneTotalHP = 0
        self.pTwoTotalHP = 0
        self.pOneCurrentHP = 0
        self.pTwoCurrentHP = 0
        # PLAYER ONE FEAT COUNTERS
        self.pOnepMod = 0
        self.pOnecMod = 0
        self.pOnedMod = 0
        self.pOnemMod = 0
        self.pOneEvade = 1
        self.pOneDeflect = 1
        self.pOneRiposte = 0
        self.pOneQuickDamage = 0
        self.pOneFeatInfo = None
        self.pOneSpentFeat = []
        # PLAYER TWO FEAT COUNTERS
        self.pTwopMod = 0
        self.pTwocMod = 0
        self.pTwodMod = 0
        self.pTwomMod = 0
        self.pTwoEvade = 1
        self.pTwoDeflect = 1
        self.pTwoRiposte = 0
        self.pTwoQuickDamage = 0
        self.pTwoFeatInfo = None
        self.pTwoSpentFeat = []
        # XP AND LEVEL COUNTERS
        self.pOneLevel = 0
        self.pTwoLevel = 0
        self.xp = 0
        self.currentPlayerXP = 0
        self.nextLevel = 0
        self.levelUp = 0
        self.iddqd = 0

        # Susanna added
        self.bEvasion = False
        self.bDeflect = False

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is Online")

#---------------------------------------------CHATROOM COMMANDS---------------------------------------------------------

    #!start
    @commands.command()
    @commands.guild_only()
    async def start(self, ctx):
        msg = onMSGUtil.message_6_start()
        await ctx.send(msg)

    @start.error
    async def start_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("The command !start may not be used in PMs!")
        raise error

    #!tutorial
    @commands.command()
    @commands.guild_only()
    async def tutorial(self, ctx):
        msg = onMSGUtil.message_10_tutortial()
        await ctx.send(msg)

    @tutorial.error
    async def tutorial_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("The command !tutorial may not be used in PMs!")
        raise error

    #!feats
    @commands.command()
    @commands.guild_only()
    async def feats(self, ctx):
        msg = onMSGUtil.message_6_feats()
        await ctx.send( msg)

    @feats.error
    async def feats_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("The command !feats may not be used in PMs!")
        raise error

    #!leaderboard
    @commands.command()
    @commands.guild_only()
    async def leaderboard(self, ctx, option):
        msg = onMSGUtil.message_12_leaderboard(option)
        # await ctx.send( "This is working.")
        for msg_item in msg:
            await ctx.send(msg_item)

    @leaderboard.error
    async def leaderboard_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("The command !leaderboard may not be used in PMs!")
        raise error

    #!level
    @commands.command()
    @commands.guild_only()
    async def level(self, ctx):
        msg = onMSGUtil.message_6_level()
        await ctx.send(msg)

    @level.error
    async def level_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("The command !level may not be used in PMs!")
        else:
            raise error

    # !name
    @commands.command()
    @commands.guild_only()
    async def name(self, ctx, name):

        name.capitalize()
        player = str(ctx.message.author.id)
        path = os.getcwd()
        charFolder = os.path.join(path + "/characters/")
        charFile = Path(charFolder + player + ".txt")

        # make sure that this command cannot be ran if a fight is taking place.
        msg = onMSGUtil.message_5_name(charFile, charFolder, name, player, self.game)
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
        path = os.getcwd()
        charFolder = os.path.join(path + "/characters/")
        charFile = Path(charFolder + player + ".txt")

        charSheet = open(charFolder + self.quitter + ".txt", "r", encoding="utf-8")
        pInfo = json.load(charSheet)
        charSheet.close()
        await ctx.send( "Are you sure you want to delete " + pInfo['name'] + "? (Type **!confirm**"
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
            await ctx.send( "You aren't the one asking for the erase, not cool.")

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
        plyer = str(ctx.message.author.id)
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

        if self.game == 1:
            self.opponent = ""
            self.playerOne = ""
            self.playerTwo = ""
            self.winner = ""
            self.loser = ""
            self.pOneUsername = None
            self.pTwoUsername = None
            # PLAYER INFO
            self.pOneInfo = {}
            self.pTwoInfo = {}
            # HP AND TURN COUNTERS
            self.gameTimer.cancel()
            self.gameTimer = 0
            self.count = 0
            self.base = 0
            self.token = 0
            self.game = 0
            self.critical = 0
            self.bonusHurt = 0
            self.nerveDamage = 0
            self.totalDamage = 0
            self.pOneTotalHP = 0
            self.pTwoTotalHP = 0
            self.pOneCurrentHP = 0
            self.pTwoCurrentHP = 0
            # PLAYER ONE FEAT COUNTERS
            self.pOnepMod = 0
            self.pOnecMod = 0
            self.pOnedMod = 0
            self.pOnemMod = 0
            self.pOneEvade = 1
            self.pTwoDeflect = 1
            self.pOneRiposte = 0
            self.pOneQuickDamage = 0
            self.pOneFeatInfo = None
            self.pOneSpentFeat = []
            # PLAYER TWO FEAT COUNTERS
            self.pTwopMod = 0
            self.pTwocMod = 0
            self.pTwodMod = 0
            self.pTwomMod = 0
            self.pTwoEvade = 1
            self.pTwoDeflect = 1
            self.pTwoRiposte = 0
            self.pTwoQuickDamage = 0
            self.pTwoFeatInfo = None
            self.pTwoSpentFeat = []
            # XP AND LEVEL COUNTERS
            self.pOneLevel = 0
            self.pTwoLevel = 0
            self.xp = 0
            self.currentPlayerXP = 0
            self.nextLevel = 0
            self.levelUp = 0
            await ctx.send("Show's over folks. Nothing to see here.")
        else:
            await ctx.send("There isn't a game to reset.")

    @commands.command()
    @commands.guild_only()
    async def player(self, ctx, player):
        msg = onMSGUtil.message_7_player(player)
        await ctx.send(msg)


        if total == 0:
            await ctx.send(player + " has 100% win ratio. Or 0%. However you want to rationalize not having a single "
                                    "fight under their belt.")
        else:
            ratio = int((int(wins) / total) * 100)

            await ctx.send(player + " has " + wins + " wins, and " + losses + " losses. (" + (str(ratio)) + "%)")

    @player.error
    async def player_error(self,ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("The command !player may not be used in PMs!")
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
        msg, opponentID, pOneInfo, new_game, bTimer, playerOne = onMSGUtil.message_10_challenge(challenger, opponent, charFolder,
                                                                                    self.game)
        if opponent is not "":
            self.opponent = opponentID
        if pOneInfo is not None:
            self.pOneInfo = pOneInfo
            self.pOneTotalHP = self.pOneInfo['thp']
            self.pOneCurrentHP = self.pOneInfo['thp']
            self.pOneLevel = self.pOneInfo['level']
        if new_game != 0:
            self.game = new_game
        if bTimer is True:
            timeout = 60
            self.timer = Timer(timeout, self.challengeTimeOut)
            self.timer.start()
        if playerOne is not "":
            self.playerOne = playerOne
        await ctx.send(msg)

    @challenge.error
    async def name_challenge(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("The command !challenge may not be used in PMs!")
        else:
            raise error

    #!accept
    @commands.command()
    @commands.guild_only()
    async def accept(self, ctx):
        accepted = str(ctx.message.author.id)
        path = os.getcwd()
        charFolder = os.path.join(path + "/characters/")
        msg, pTwoInfo, new_game, playerTwo, bTimer, bGameTimer, new_oppenent, token = onMSGAccept.message_accept(charFolder, accepted,
                                                                                                     self.game,
                                                                                                     self.opponentID,
                                                                                                     self.pOneInfo)
        if not charFile.is_file():
            await ctx.send("You don't even have a character made to fight.")
        else:
            if new_game is not None:
                self.game = new_game
            if pTwoInfo is not None:
                self.pTwoInfo = pTwoInfo
                self.pTwoTotalHP = self.pTwoInfo['thp']
                self.pTwoCurrentHP = self.pTwoInfo['thp']
                self.pTwoLevel = self.pTwoInfo['level']
            if bTimer:
                self.timer.cancel()
            if bGameTimer:
                gametimeout = 3600
                self.gameTimer = Timer(gametimeout, self.combatTimeOut)
                self.gameTimer.start()
            if new_oppenent is not None:
                self.opponent = new_oppenent
            if playerTwo is not None:
                self.playerTwo = playerTwo
            if token is not None:
                self.token = token
            for msg_item in msg:
                await ctx.send( msg_item)

    @accept.error
    async def name_accept(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("The command !accept may not be used in PMs!")
        else:
            raise error

    #!usefeat
    @commands.command()
    @commands.guild_only()
    async def usefeat(self, ctx, *, answer):
        user = str(cxt.message.author.id)
        msg, featToken_new, pOneSpentFeat, pOneFeatInfo, pTwoSpentFeat, pTwoFeatInfo = message_8_usefeat(answer, charFolder,
                                                                                                         user, self.game,
                                                                                                         self.playerOne, \
                                                                                                         self.playerTwo,
                                                                                                         self.token,
                                                                                                         self.featToken,
                                                                                                         self.pOneInfo,
                                                                                                         self.pOneSpentFeat,
                                                                                                         self.pTwoSpentFeat,
                                                                                                         self.pTwoInfo)
        for msg_item in msg:
            await ctx.send(msg_item)
        if featToken_new is not None:
            self.featToken = featToken_new
        if pOneSpentFeat is not None:
            self.pOneSpentFeat.append(pOneSpentFeat)
        if pOneFeatInfo is not None:
            self.pOneFeatInfo = pOneFeatInfo
        if pTwoSpentFeat is not None:
            self.pTwoSpentFeat.append(pTwoSpentFeat)
        if pTwoFeatInfo is not None:
            self.pTwoFeatInfo = pTwoFeatInfo

    @usefeat.error
    async def name_usefeat(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("The command !usefeat may not be used in PMs!")
        else:
            raise error

    #!roll
    @commands.command()
    @commands.guild_only()
    async def roll(self, ctx):
        user = str(ctx.message.author.id)
        try:
            self.gameTimer.cancel()
            msg, self.bEvasion, self.bDeflect, bGameTimer, self.opponent, self.playerOne, self.playerTwo, self.winner, \
            self.pOneInfo, self.pTwoInfo, self.featToken, self.game, self.count, self.token, self.critical, \
            self.bonusHurt, self.totalDamage, self.pOneTotalHP, self.pTwoTotalHP, self.pOneCurrentHP, self.pTwoCurrentHP,\
            self.pOnepMod, self.pOnecMod, self.pOnedMod, self.pOnemMod, self.pOneEvade, self.pOneDeflect, \
            self.pOneRiposte, self.pOneQuickDamage, self.pOneFeatInfo, self.pOneSpentFeat, self.pTwopMod, self.pTwocMod, self.pTwodMod, \
            self.pTwomMod, self.pTwoEvade, self.pTwoDeflect, self.pTwoRiposte, self.pTwoQuickDamage, self.pTwoFeatInfo, \
            self.pTwoSpentFeat, self.pOneLevel, self.pTwoLevel, self.xp, self.currentPlayerXP, self.nextLevel, \
            self.levelUp, self.iddqd = onMSGRoll.message_roll(user, charFolder,
                                                    self.opponent, self.playerOne, self.playerTwo, self.winner,
                                                    self.pOneInfo, self.pTwoInfo, self.featToken, self.game, \
                                                    self.count, self.token, self.critical, self.bonusHurt,
                                                    self.totalDamage, self.pOneTotalHP, self.pTwoTotalHP, self.pOneCurrentHP,
                                                    self.pTwoCurrentHP, self.pOnepMod, self.pOnecMod, self.pOnedMod,
                                                    self.pOnemMod, self.pOneEvade, self.pOneDeflect, self.pOneRiposte,
                                                    self.pOneQuickDamage, self.pOneFeatInfo, self.pOneSpentFeat, self.pTwopMod,
                                                    self.pTwocMod, self.pTwodMod, self.pTwomMod, self.pTwoEvade, self.pTwoDeflect,
                                                    self.pTwoRiposte, self.pTwoQuickDamage, self.pTwoFeatInfo, self.pTwoSpentFeat,
                                                    self.pOneLevel, self.pTwoLevel, self.xp, self.currentPlayerXP,
                                                    self.nextLevel, self.levelUp, self.iddqd)
            for msg_item in msg:
                await ctx.send(msg_item)
                if bGameTimer:
                   gametimeout = 3600
                   self.gameTimer = Timer(gametimeout, self.combatTimeOut)
                   self.gameTimer.start()
        except AttributeError:
            await ctx.send("Either a fight is not taking place, or it isn't your turn.")

                # # assign both player's feat selections to variables
                # pOneFeatUsed = self.pOneFeatInfo
                # pTwoFeatUsed = self.pTwoFeatInfo
                #
                # # If the feat used was 'true strike' forgo rolling to see if player hit opponent, and go
                # # straight to damage.
                # if pOneFeatUsed[0] == "true strike":
                #     await ctx.send( self.pOneInfo['name'] +
                #                 " used the feat 'True Strike.' And forgoes the need to determine if hit was success.")
                #
                #     # Obtain Player One's base damage and base modifier, and roll damage. Assign 'power attack' and 'combat defense'
                #     # modifiers to variables, and roll damage.
                #     pOneBaseDamage = self.pOneInfo['base damage']
                #     pOneModifier = self.pOneInfo['damage']
                #     pOneMinimum, pOneMaximum = pOneBaseDamage.split('d')
                #     pMod = self.pOnepMod
                #     cMod = self.pOnecMod
                #     damage = random.randint(int(pOneMinimum), int(pOneMaximum))
                #
                #     # if critical counter is a value of 1, double the damage done, then reset counter to 0.
                #     if self.critical == 1:
                #         damage = damage * 2
                #         self.critical = 0
                #     # if Player One used feat 'titan blow', apply 50% bonus damage.
                #     if pOneFeatUsed[0] == "titan blow":
                #         await ctx.send( self.pOneInfo['name'] + " used the feat 'titan blow'.")
                #         damage = damage * float(pOneFeatUsed[1])
                #     # if Player Two use 'staggering blow' half damage done.
                #     if pTwoFeatUsed[0] == "staggering blow":
                #         await ctx.send(
                #                     self.pTwoInfo['name'] + " used the feat 'staggering blow', halving " +
                #                     self.pOneInfo['name'] + "'s damage roll")
                #         damage = damage * float(pTwoFeatUsed[1])
                #
                #     # ensure that no matter what, raw damage can not fall below 1, then assign total damage to variable, and in turn
                #     # assign it to variable to be accessed for scoreboard.
                #     if damage < 1:
                #         damage = 1
                #     total = int(damage + pOneModifier + pMod - cMod)
                #
                #     # if Player Two used 'quick strike', 'improved quick strike', or 'greater quick strike', apply the return
                #     # damage here
                #     pTwoBaseDamage = self.pTwoInfo['base damage']
                #     pTwoModifier = self.pTwoInfo['damage']
                #     pTwoMinimum, pTwoMaximum = pTwoBaseDamage.split('d')
                #     pMod = self.pTwopMod
                #     cMod = self.pTwocMod
                #
                #     # apply the damage from 'quick strike', 'improved quick strike', or 'greater quick strike' if such feats were
                #     # used
                #     if pTwoFeatUsed[0] == "quick strike":
                #
                #         # Roll damage for Player One, and multiply it by desired amount.
                #         damage = random.randint(int(pTwoMinimum), int(pTwoMaximum))
                #         total = (damage + pTwoModifier + pMod - cMod)
                #         quickDamage = int(total * float(pTwoFeatUsed[1]))
                #
                #         # Ensure damage is always at least 1hp and print out result
                #         if quickDamage < 1:
                #             quickDamage = 1
                #         self.pTwoQuickDamage = quickDamage
                #         self.pOneCurrentHP = self.pOneCurrentHP - self.pTwoQuickDamage
                #         await ctx.send(self.pTwoInfo['name'] + " used 'quick strike,' managing to do an additional "
                #                        + str(self.pTwoQuickDamage) + "hp of damage.")
                #
                #     elif pTwoFeatUsed[0] == "improved quick strike":
                #         # Roll damage for Player one, and multiply it by desired amount.
                #         damage = random.randint(int(pTwoMinimum), int(pTwoMaximum))
                #         total = (damage + pTwoModifier + pMod - cMod)
                #         quickDamage = int(total * float(pTwoFeatUsed[1]))
                #         # Ensure damage is always at least 1hp and print out result
                #         if quickDamage < 1:
                #             quickDamage = 1
                #         self.pTwoQuickDamage = quickDamage
                #         self.pOneCurrentHP = self.pOneCurrentHP - self.pTwoQuickDamage
                #         await ctx.send(self.pTwoInfo['name'] + " used 'quick strike,' managing to do an additional "
                #                        + str(self.pTwoQuickDamage) + "hp of damage.")
                #
                #     elif pTwoFeatUsed[0] == "greater quick strike":
                #
                #         # roll damage for player One, and multiply it by desired amount
                #         damage = random.randint(int(pTwoMinimum), int(pTwoMaximum))
                #         total = (damage + pTwoModifier + pMod - cMod)
                #         quickDamage = int(total * float(pTwoFeatUsed[1]))
                #         # Ensure damage is always at least 1hp and print out result
                #         if quickDamage < 1:
                #             quickDamage = 1
                #         self.pTwoQuickDamage = quickDamage
                #         self.pOneCurrentHP = self.pOneCurrentHP - self.pTwoQuickDamage
                #         await ctx.send(self.pTwoInfo['name'] + " used 'quick strike,' managing to do an additional "
                #                        + str(self.pTwoQuickDamage) + "hp of damage.")
                #
                #     elif pTwoFeatUsed[0] == "riposte":
                #         # roll damage for player One, and multiply it by desired amount
                #         damage = random.randint(int(pTwoMinimum), int(pTwoMaximum))
                #         total = (damage + pTwoModifier + pMod - cMod)
                #         quickDamage = int(total * float(pTwoFeatUsed[1][0]))
                #         # Ensure damage is always at least 1hp and print out result
                #         if quickDamage < 1:
                #             quickDamage = 1
                #         self.pTwoQuickDamage = quickDamage
                #         self.pOneCurrentHP = self.pOneCurrentHP - self.pTwoQuickDamage
                #         await ctx.send(self.pTwoInfo['name'] + " used 'quick strike,' managing to do an additional "
                #                        + str(self.pTwoQuickDamage) + "hp of damage.")
                #         self.pTwoRiposte = 1
                #
                #     # If Player Two has Evasion, Improved Evasion, or Greater Evasion, give them the option to use it.
                #     for word in self.pTwoInfo['feats taken']:
                #         answer = ""
                #         if self.pTwoEvade == 1 and word == "evasion":
                #             while answer != "yes" and answer != "no":
                #                 answer = await ctx.send(
                #                     self.pTwoInfo['name'] + ", do you wish to evade? ").lower()
                #                 if answer == "yes" and character == self.pTwoUsername:
                #                     total = int(total * 0.75)
                #                     self.totalDamage = total
                #                     self.pTwoEvade = 0
                #                 elif answer == "no" and character == self.pTwoUsername:
                #                     pass
                #                 else:
                #                     await ctx.send("You aren't " + self.pTwoUsername )
                #     #     elif self.pTwoEvade == 1 and word == "improved evasion":
                #     #         while answer != "yes" and answer != "no":
                #     #             answer = await ctx.send(
                #     #                 self.pTwoInfo['name'] + ", do you wish to evade? ").lower()
                #     #             if answer == "yes":
                #     #                 total = int(total * 0.5)
                #     #                 self.totalDamage = total
                #     #                 self.pTwoEvade = 0
                #     #             elif answer == "no":
                #     #                 pass
                #     #             else:
                #     #                 await ctx.send("Answer 'yes' or 'no'")
                #     #     elif self.pTwoEvade == 1 and word == "greater evasion":
                #     #         while answer != "yes" and answer != "no":
                #     #             answer = await ctx.send(
                #     #                 self.pTwoInfo['name'] + ", do you wish to evade? ").lower()
                #     #             if answer == "yes":
                #     #                 total = 0
                #     #                 self.totalDamage = total
                #     #                 self.pTwoEvade = 0
                #     #             elif answer == "no":
                #     #                 pass
                #     #             else:
                #     #                 await ctx.send("Answer 'yes' or 'no'")
                #     # If Player Two used 'async deflect', 'improved async deflect', or 'greater async deflect', apply damage mitigation here
                #     if pTwoFeatUsed[0] == "deflect":
                #         await ctx.send( self.pTwoInfo['name'] + " used async deflect to lessen the blow.")
                #         total = int(total * float(pTwoFeatUsed[1]))
                #     elif pTwoFeatUsed[0] == "improved deflect":
                #         await ctx.send( self.pTwoInfo['name'] + " used async deflect to lessen the blow")
                #         total = int(total * float(pTwoFeatUsed[1]))
                #     elif pTwoFeatUsed[0] == "greater deflect":
                #         await ctx.send( self.pTwoInfo['name'] + " used deflect to lessen the blow")
                #         total = int(total * float(pTwoFeatUsed[1]))
                #     self.totalDamage = total
                #     # testing data to see that modifiers are carrying over correctly. Delete this when project is finished.
                #     await ctx.send("Roll: " + str(damage) + " Modifier: " + str(pOneModifier) + " PA: " + str(
                #                     pMod) + " CE: " + str(cMod))
                #     # display total damage done, and reset passive feat counters (power attack and combat defense)
                #     await ctx.send(self.pOneInfo['name'] + " did " + str(total) + " points of damage.")
                #     self.pOnepMod = 0
                #     self.pOnecMod = 0
                #     self.token = 2
                #
                # # Otherwise, continue on with the bulk of this method.
                # else:
                #     pOneToHit = self.pOneInfo['hit']
                #     pTwoAC = self.pTwoInfo['ac']
                #
                #     pMod = self.pOnepMod
                #     cMod = self.pOnecMod
                #     dMod = self.pOnedMod
                #     mMod = self.pOnemMod
                #     pTwodMod = self.pTwodMod
                #     pTwomMod = self.pTwomMod
                #
                #     hit = random.randint(1, 20)
                #
                #     # if the raw result is equal to 20, count the critical counter up to 1.
                #     if hit == 20:
                #         self.critical = 1
                #         await ctx.send( self.pOneInfo['name'] + " has critically hit.")
                #
                #     # If Player One has Hurt Me, Improved Hurt Me, and Greater Hurt Me, check hit points, and apply
                #     # bonuses.
                #     for word in self.pOneInfo['feats taken']:
                #         percentage = int((self.pOneCurrentHP / self.pOneTotalHP) * 100)
                #         if word == 'hurt me':
                #             if percentage < 66:
                #                 self.bonusHurt = 1
                #             elif percentage < 33:
                #                 self.bonusHurt = 2
                #         elif word == 'improved hurt me':
                #             if percentage < 66:
                #                 self.bonusHurt = 2
                #             elif percentage < 33:
                #                 self.bonusHurt = 3
                #         elif word == 'greater hurt me':
                #             if percentage < 66:
                #                 self.bonusHurt = 2
                #             elif percentage < 33:
                #                 self.bonusHurt = 4
                #         elif word == 'hurt me more':
                #             if percentage < 75:
                #                 self.bonusHurt = 2
                #             elif percentage < 50:
                #                 self.bonusHurt = 4
                #             elif percentage < 25:
                #                 self.bonusHurt = 6
                #
                #     # Notify that Player One is getting the hit benefit from 'riposte'
                #     if self.pOneRiposte == 5:
                #         await ctx.send( self.pOneInfo['name'] +
                #                     " benefits from +5 hit bonus effect from riposte.")
                #
                #     # calculate the total after modifiers
                #     total = int(hit + pOneToHit - pMod + cMod - dMod + mMod + self.pOneRiposte + self.bonusHurt)
                #
                #     # Ensures Player One benefits from hit bonus of Riposte only once.
                #     self.pOneRiposte = 0
                #
                #     # Reset Hurt Me bonuses, so it doesn't bleed over to player two.
                #     self.bonusHurt = 0
                #
                #     # if any version of crippling blow was used, tack on the penalty to the above total
                #     if pTwoFeatUsed[0] == "crippling blow" or pTwoFeatUsed[0] == "improved crippling blow" or \
                #             pTwoFeatUsed[0] == "greater crippling blow":
                #         await ctx.send(self.pTwoInfo['name'] + " Used " + str(pTwoFeatUsed[0]) + ", Giving "
                #                        + self.pOneInfo['name'] + " a " + str(pTwoFeatUsed[1]) + " To their attack.")
                #         total = total + pTwoFeatUsed[1]
                #
                #     # testing data to see that modifiers are carrying over correctly. Comment out
                #     # when project is finished.
                #     await ctx.send("Roll: " + str(hit) + " Base: " + str(pOneToHit) + " PA: "
                #                    + str(pMod) + " CE: " + str(cMod) + " DF: " + str(dMod) + " MC: "
                #                    + str(mMod) + " Riposte: " + str(self.pOneRiposte) + " Hurt Me: " + str(self.bonusHurt))
                #
                #     # find Player One's total AC
                #     totalAC = pTwoAC + pTwodMod - pTwomMod
                #
                #     # testing data to see that modifiers are carrying over correctly. Delete this when project is finished.
                #     await ctx.send("P2 AC: " + str(pTwoAC) + " DF: " + str(pTwodMod) + " MC: " + str(pTwomMod))
                #
                #     # determine if the total roll, after all modifiers have been included, is a successful hit or not. then
                #     # head to the appropriate method
                #     if total >= totalAC:
                #         await ctx.send(self.pOneInfo['name'] + " rolled a " + str(total) + " to hit an AC " + str(
                #                        totalAC) + " and was successful.")
                #         self.pTwodMod = 0
                #         self.pTwomMod = 0
                #         self.pTwoRiposte = 0
                #
                #         # Obtain Player One's base damage and base modifier, and roll damage. Assign 'power attack' and 'combat defense'
                #         # modifiers to variables, and roll damage.
                #         pOneBaseDamage = self.pOneInfo['base damage']
                #         pOneModifier = self.pOneInfo['damage']
                #         pOneMinimum, pOneMaximum = pOneBaseDamage.split('d')
                #         pMod = self.pOnepMod
                #         cMod = self.pOnecMod
                #         damage = random.randint(int(pOneMinimum), int(pOneMaximum))
                #         # if critical counter is a value of 1, double the damage done, then reset counter to 0.
                #         if self.critical == 1:
                #             damage = damage * 2
                #             self.critical = 0
                #         # if Player One used feat 'titan blow', apply 50% bonus damage.
                #         if pOneFeatUsed[0] == "titan blow":
                #             await ctx.send( self.pOneInfo['name'] + " used the feat 'titan blow'.")
                #             damage = damage * float(pOneFeatUsed[1])
                #         # if Player Two use 'staggering blow' half damage done.
                #         if pTwoFeatUsed[0] == "staggering blow":
                #             await ctx.send(self.pTwoInfo['name'] + " used the feat 'staggering blow', halving "
                #                            + self.pOneInfo['name'] + "'s damage roll")
                #             damage = damage * float(pTwoFeatUsed[1])
                #         # ensure that no matter what, raw damage can not fall below 1, then assign total damage to variable, and in turn
                #         # assign it to variable to be accessed for scoreboard.
                #         if damage < 1:
                #             damage = 1
                #         total = int(damage + pOneModifier + pMod - cMod)
                #         # if Player Two used 'quick strike', 'improved quick strike', or 'greater quick strike', apply the return
                #         # damage here
                #         pTwoBaseDamage = self.pTwoInfo['base damage']
                #         pTwoModifier = self.pTwoInfo['damage']
                #         pTwoMinimum, pTwoMaximum = pTwoBaseDamage.split('d')
                #         pMod = self.pTwopMod
                #         cMod = self.pTwocMod
                #         # apply the damage from 'quick strike', 'improved quick strike', or 'greater quick strike' if such feats were
                #         # used
                #         if pTwoFeatUsed[0] == "quick strike":
                #             # Roll damage for Player One, and multiply it by desired amount.
                #             damage = random.randint(int(pTwoMinimum), int(pTwoMaximum))
                #             total = (damage + pTwoModifier + pMod - cMod)
                #             quickDamage = int(total * float(pTwoFeatUsed[1]))
                #             # Ensure damage is always at least 1hp and print out result
                #             if quickDamage < 1:
                #                 quickDamage = 1
                #             self.pTwoQuickDamage = quickDamage
                #             self.pOneCurrentHP = self.pOneCurrentHP - self.pTwoQuickDamage
                #             await ctx.send(self.pTwoInfo['name'] + " used 'quick strike,' managing to do an additional "
                #                            + str(self.pTwoQuickDamage) + "hp of damage.")
                #         elif pTwoFeatUsed[0] == "improved quick strike":
                #             # Roll damage for Player one, and multiply it by desired amount.
                #             damage = random.randint(int(pTwoMinimum), int(pTwoMaximum))
                #             total = (damage + pTwoModifier + pMod - cMod)
                #             quickDamage = int(total * float(pTwoFeatUsed[1]))
                #             # Ensure damage is always at least 1hp and print out result
                #             if quickDamage < 1:
                #                 quickDamage = 1
                #             self.pTwoQuickDamage = quickDamage
                #             self.pOneCurrentHP = self.pOneCurrentHP - self.pTwoQuickDamage
                #             await ctx.send(self.pTwoInfo['name'] + " used 'quick strike,' managing to do an additional "
                #                            + str(self.pTwoQuickDamage) + "hp of damage.")
                #         elif pTwoFeatUsed[0] == "greater quick strike":
                #             # roll damage for player One, and multiply it by desired amount
                #             damage = random.randint(int(pTwoMinimum), int(pTwoMaximum))
                #             total = (damage + pTwoModifier + pMod - cMod)
                #             quickDamage = int(total * float(pTwoFeatUsed[1]))
                #             # Ensure damage is always at least 1hp and print out result
                #             if quickDamage < 1:
                #                 quickDamage = 1
                #             self.pTwoQuickDamage = quickDamage
                #             self.pOneCurrentHP = self.pOneCurrentHP - self.pTwoQuickDamage
                #             await ctx.send(self.pTwoInfo['name'] + " used 'quick strike,' managing to do an additional "
                #                            + str(self.pTwoQuickDamage) + "hp of damage.")
                #         elif pTwoFeatUsed[0] == "riposte":
                #             # roll damage for player One, and multiply it by desired amount
                #             damage = random.randint(int(pTwoMinimum), int(pTwoMaximum))
                #             total = (damage + pTwoModifier + pMod - cMod)
                #             quickDamage = int(total * float(pTwoFeatUsed[1][0]))
                #             # Ensure damage is always at least 1hp and print out result
                #             if quickDamage < 1:
                #                 quickDamage = 1
                #             self.pTwoQuickDamage = quickDamage
                #             self.pOneCurrentHP = self.pOneCurrentHP - self.pTwoQuickDamage
                #             await ctx.send(self.pTwoInfo['name'] + " used 'quick strike,' managing to do an additional "
                #                            + str(self.pTwoQuickDamage) + "hp of damage.")
                #         # # If Player Two has Evasion, Improved Evasion, or Greater Evasion, give them the option to use it.
                #
                #         for word in self.pTwoInfo['feats taken']:
                #
                #             answer = ""
                #             if self.pTwoEvade == 1 and word == "evasion":
                #                 while answer != "yes" and answer != "no":
                #                     answer = await ctx.send(
                #                         self.pTwoInfo['name'] + ", do you wish to evade? ").lower()
                #                     if answer == "yes" and character == self.pTwoUsername:
                #                         total = int(total * 0.75)
                #                         self.totalDamage = total
                #                         self.pTwoEvade = 0
                #                     elif answer == "no" and character == self.pTwoUsername:
                #                         pass
                #                     else:
                #                         await ctx.send("You aren't " + self.pTwoUsername)
                #         #     elif self.pTwoEvade == 1 and word == "improved evasion":
                #         #         while answer != "yes" and answer != "no":
                #         #             answer = await ctx.send(
                #         #                 self.pTwoInfo['name'] + ", do you wish to evade? ").lower()
                #         #             if answer == "yes":
                #         #                 total = int(total * 0.5)
                #         #                 self.totalDamage = total
                #         #                 self.pTwoEvade = 0
                #         #             elif answer == "no":
                #         #                 pass
                #         #             else:
                #         #                 await ctx.send("Answer 'yes' or 'no'")
                #         #     elif self.pTwoEvade == 1 and word == "greater evasion":
                #         #         while answer != "yes" and answer != "no":
                #         #             answer = await ctx.send(
                #         #                 self.pTwoInfo['name'] + ", do you wish to evade? ").lower()
                #         #             if answer == "yes":
                #         #                 total = 0
                #         #                 self.totalDamage = total
                #         #                 self.pTwoEvade = 0
                #         #             elif answer == "no":
                #         #                 pass
                #         #             else:
                #         #                 await ctx.send("Answer 'yes' or 'no'")
                #         # If Player Two used 'async deflect', 'improved async deflect', or 'greater async deflect', apply damage mitigation here
                #         if pTwoFeatUsed[0] == "deflect":
                #             await ctx.send( self.pTwoInfo['name'] + " used deflect to lessen the blow.")
                #             total = int(total * float(pTwoFeatUsed[1]))
                #         elif pTwoFeatUsed[0] == "improved deflect":
                #             await ctx.send( self.pTwoInfo['name'] + " used deflect to lessen the blow")
                #             total = int(total * float(pTwoFeatUsed[1]))
                #         elif pTwoFeatUsed[0] == "greater deflect":
                #             await ctx.send( self.pTwoInfo['name'] + " used deflect to lessen the blow")
                #             total = int(total * float(pTwoFeatUsed[1]))
                #         self.totalDamage = total
                #         # testing data to see that modifiers are carrying over correctly. Delete this when project is finished.
                #         await ctx.send("Roll: " + str(damage) + " Modifier: " + str(pOneModifier) + " PA: "
                #                        + str(pMod) + " CD: " + str(cMod))
                #         # display total damage done, and reset passive feat counters (power attack and combat defense)
                #         await ctx.send(self.pOneInfo['name'] + " did " + str(total) + " points of damage.")
                #         self.pOnepMod = 0
                #         self.pOnecMod = 0
                #         self.token = 2
                #     else:
                #         await ctx.send( self.pOneInfo['name'] + " rolled a " + str(total) + " to hit an AC " + str(
                #             totalAC) + " and missed.")
                #         self.pTwodMod = 0
                #         self.pTwomMod = 0
                #         self.token = 2
                #
                #         if pTwoFeatUsed[0] == "riposte":
                #             self.pTwoRiposte = 5
                #
                # # Determine HP at end of round.
                # if self.pTwoQuickDamage != 0:
                #     self.pTwoCurrentHP = self.pTwoCurrentHP - self.totalDamage - self.pOneQuickDamage
                #     self.pOneQuickDamage = 0
                #     self.count += 1
                # else:
                #     self.pTwoCurrentHP = self.pTwoCurrentHP - self.totalDamage
                #
                # # Print the scoreboard.
                # await ctx.send( self.pOneInfo['name'] + ": " + str(self.pOneCurrentHP) + "/" + str(
                #     self.pOneTotalHP) + "  ||  " + self.pTwoInfo['name'] + ": " + str(
                #     self.pTwoCurrentHP) + "/" + str(self.pTwoTotalHP) + " \n" +
                #             self.pTwoInfo['name'] + "'s turn. Type: !usefeat <feat> if you wish to use a feat.")
                #
                # # If Player Two is dead, state such, and how many rounds it took to win. Calculate and distribute xp.
                # # reset game and token counters back to 0.
                # if self.pTwoCurrentHP <= 0:
                #     self.game = 0
                #     self.token = 0
                #     await ctx.send( self.pOneInfo['name'] + " won in " + str(int(self.count / 2)) + " rounds")
                #     level = abs(self.pOneLevel - self.pTwoLevel)
                #     if level == 0:
                #         level = 1
                #     if level <= 3:
                #         levelDiff = level * self.pOneLevel
                #         differHP = abs(self.pOneCurrentHP - self.pTwoCurrentHP)
                #         self.xp = 10 * levelDiff + differHP
                #         await ctx.send(self.pOneInfo['name'] + " has earned: " + str(self.xp) + " experience points.")
                #     elif 3 > level < 6:
                #         levelDiff = level * self.pOneLevel
                #         differHP = abs(self.pOneCurrentHP - self.pTwoCurrentHP)
                #         self.xp = 7 * levelDiff + differHP
                #         await ctx.send(self.pOneInfo['name'] + " has earned: " + str(self.xp) + " experience points.")
                #     elif 7 > level < 10:
                #         levelDiff = level * self.pOneLevel
                #         differHP = abs(self.pOneCurrentHP - self.pTwoCurrentHP)
                #         self.xp = 5 * levelDiff + differHP
                #         await ctx.send(
                #                     self.pOneInfo['name'] + " has earned: " + str(self.xp) + " experience points.")
                #     else:
                #         await ctx.send( "As the level difference was greater than 10, no XP was awarded.")
                #     await ctx.send( self.pOneInfo['name'] + " has earned: " + str(self.xp) + " experience points.")
                #     self.currentPlayerXP = self.pOneInfo['currentxp'] + self.xp
                #     self.nextLevel = self.pOneInfo['nextlevel']
                #     self.winner = self.pOneUsername
                #     self.loser = self.pTwoUsername
                #     self.levelUp = self.pOneInfo['level']
                #     path = os.getcwd()
                #     charFolder = os.path.join(path + "/characters/")
                #
                #     with open(charFolder + self.winner + '.txt', 'r+') as file:
                #         charData = json.load(file)
                #         charData['currentxp'] = self.currentPlayerXP
                #         charData['wins'] += 1
                #         file.seek(0)
                #         file.write(json.dumps(charData, ensure_ascii=False, indent=2))
                #         file.truncate()
                #         file.close()
                #
                #     with open(charFolder + self.loser + '.txt', 'r+') as file:
                #         charData = json.load(file)
                #         charData['losses'] += 1
                #         file.seek(0)
                #         file.write(json.dumps(charData, ensure_ascii=False, indent=2))
                #         file.truncate()
                #         file.close()
                #     if self.currentPlayerXP >= self.nextLevel:
                #         newLevel = self.levelUp + 1
                #         newLevel = str(newLevel)
                #         await ctx.send( self.winner.capitalize() + " has reached level " + newLevel + "!")
                #         levelFile = open(charFolder + "levelchart.txt", "r", encoding="utf-8")
                #         levelDict = json.load(levelFile)
                #         levelFile.close()
                #         with open(charFolder + self.winner + '.txt', 'r+') as file:
                #             charData = json.load(file)
                #             charData['level'] = int(newLevel)
                #             charData['hitpoints'] = int(levelDict[newLevel][0])
                #             charData['base damage'] = str(levelDict[newLevel][1]) + "d" + str(
                #                 levelDict[newLevel][2])
                #             if charData['total feats'] == levelDict[newLevel][4]:
                #                 charData['total feats'] = levelDict[newLevel][4]
                #             else:
                #                 await ctx.send("You have a new feat slot to fill. Use the !feat command to select new feat.")
                #                 charData['total feats'] = levelDict[newLevel][4]
                #                 charData['remaining feats'] = 1
                #             if charData['total ap'] == levelDict[newLevel][3]:
                #                 charData['total ap'] = levelDict[newLevel][3]
                #             else:
                #                 await ctx.send("You have a new ability point to spend. the !add command.")
                #             charData['hit'] = int(levelDict[newLevel][5])
                #             charData['damage modifier'] = int(levelDict[newLevel][5])
                #             charData['ac'] = int(levelDict[newLevel][6])
                #             charData['currentxp'] = int(self.currentPlayerXP)
                #             charData['nextlevel'] = int(levelDict[newLevel][7])
                #             file.seek(0)
                #             file.write(json.dumps(charData, ensure_ascii=False, indent=2))
                #             file.truncate()
                #             file.close()
                #
                #     else:
                #         pass
            # ensures the command can only be used by player two, when it is their turn. To prevent trolls from
            # spamming commands.
                # # assign both player's feat selections to variables
                # pOneFeatUsed = self.pOneFeatInfo
                # pTwoFeatUsed = self.pTwoFeatInfo
                #
                # # If a feat wasn't used by a player, assign it async default values.
                # if pOneFeatUsed is None:
                #     pOneFeatUsed = ["none", 0]
                # if pTwoFeatUsed is None:
                #     pTwoFeatUsed = ["none", 0]
                #
                # # If the feat used was 'true strike' forgo rolling to see if player hit opponent, and go straight to damage.
                # if pTwoFeatUsed[0] == "true strike":
                #     await ctx.send( self.pTwoInfo['name'] +
                #                 " used the feat 'True Strike.' And forgoes the need to determine if hit was success.")
                #
                #     # Obtain Player Two's base damage and base modifier, and roll damage. Assign 'power attack' and 'combat defense'
                #     # modifiers to variables, and roll damage.
                #     pTwoBaseDamage = self.pTwoInfo['base damage']
                #     pTwoModifier = self.pTwoInfo['damage']
                #     pTwoMinimum, pTwoMaximum = pTwoBaseDamage.split('d')
                #     pMod = self.pTwopMod
                #     cMod = self.pTwocMod
                #     damage = random.randint(int(pTwoMinimum), int(pTwoMaximum))
                #     # if critical counter is a value of 1, double the damage done, then reset counter to 0.
                #     if self.critical == 1:
                #         damage = damage * 2
                #         self.critical = 0
                #     # if Player Two used feat 'titan blow', apply 50% bonus damage.
                #     if pTwoFeatUsed[0] == "titan blow":
                #         await ctx.send( self.pTwoInfo['name'] + " used the feat 'titan blow'.")
                #         damage = damage * float(pTwoFeatUsed[1])
                #     # if Player One use 'staggering blow' half damage done.
                #     if pOneFeatUsed[0] == "staggering blow":
                #         await ctx.send(
                #                     self.pOneInfo['name'] + " used the feat 'staggering blow', halving " +
                #                     self.pTwoInfo['name'] + "'s damage roll")
                #         damage = damage * float(pOneFeatUsed[1])
                #     # ensure that no matter what, raw damage can not fall below 1, then assign total damage to variable, and in turn
                #     # assign it to variable to be accessed for scoreboard.
                #     if damage < 1:
                #         damage = 1
                #     total = int(damage + pTwoModifier + pMod - cMod)
                #     # if Player One used 'quick strike', 'improved quick strike', or 'greater quick strike', apply the return
                #     # damage here
                #     pOneBaseDamage = self.pOneInfo['base damage']
                #     pOneModifier = self.pOneInfo['damage']
                #     pOneMinimum, pOneMaximum = pOneBaseDamage.split('d')
                #     pMod = self.pOnepMod
                #     cMod = self.pOnecMod
                #     # apply the damage from 'quick strike', 'improved quick strike', or 'greater quick strike' if such feats were
                #     # used
                #     if pOneFeatUsed[0] == "quick strike":
                #         # Roll damage for Player One, and multiply it by desired amount.
                #         damage = random.randint(int(pOneMinimum), int(pOneMaximum))
                #         total = (damage + pOneModifier + pMod - cMod)
                #         quickDamage = int(total * float(pOneFeatUsed[1]))
                #         # Ensure damage is always at least 1hp and print out result
                #         if quickDamage < 1:
                #             quickDamage = 1
                #         self.pOneQuickDamage = quickDamage
                #         self.pTwoCurrentHP = self.pTwoCurrentHP - self.pOneQuickDamage
                #         await ctx.send(
                #                     self.pOneInfo[
                #                         'name'] + " used 'quick strike,' managing to do an additional " + str(
                #                         self.pOneQuickDamage) + "hp of damage.")
                #     if pOneFeatUsed[0] == "improved quick strike":
                #         # Roll damage for Player one, and multiply it by desired amount.
                #         damage = random.randint(int(pOneMinimum), int(pOneMaximum))
                #         total = (damage + pOneModifier + pMod - cMod)
                #         quickDamage = int(total * float(pOneFeatUsed[1]))
                #         # Ensure damage is always at least 1hp and print out result
                #         if quickDamage < 1:
                #             quickDamage = 1
                #         self.pOneQuickDamage = quickDamage
                #         self.pTwoCurrentHP = self.pTwoCurrentHP - self.pOneQuickDamage
                #         await ctx.send(
                #                     self.pOneInfo[
                #                         'name'] + " used 'quick strike,' managing to do an additional " + str(
                #                         self.pOneQuickDamage) + "hp of damage.")
                #     if pOneFeatUsed[0] == "greater quick strike":
                #         # roll damage for player One, and multiply it by desired amount
                #         damage = random.randint(int(pOneMinimum), int(pOneMaximum))
                #         total = (damage + pOneModifier + pMod - cMod)
                #         quickDamage = int(total * float(pOneFeatUsed[1]))
                #         # Ensure damage is always at least 1hp and print out result
                #         self.pOneQuickDamage = quickDamage
                #         self.pTwoCurrentHP = self.pTwoCurrentHP - self.pOneQuickDamage
                #         await ctx.send(
                #                     self.pOneInfo[
                #                         'name'] + " used 'quick strike,' managing to do an additional " + str(
                #                         self.pOneQuickDamage) + "hp of damage.")
                #     elif pOneFeatUsed[0] == "riposte":
                #         # roll damage for player One, and multiply it by desired amount
                #         damage = random.randint(int(pOneMinimum), int(pOneMaximum))
                #         total = (damage + pOneModifier + pMod - cMod)
                #         quickDamage = int(total * float(pOneFeatUsed[1][0]))
                #         # Ensure damage is always at least 1hp and print out result
                #         if quickDamage < 1:
                #             quickDamage = 1
                #         self.pOneQuickDamage = quickDamage
                #         self.pTwoCurrentHP = self.pTwoCurrentHP - self.pTwoQuickDamage
                #         await ctx.send(
                #                     self.pOneInfo[
                #                         'name'] + " used 'quick strike,' managing to do an additional " + str(
                #                         self.pOneQuickDamage) + "hp of damage.")
                #         self.pOneRiposte = 1
                #     # If Player One has Evasion, Improved Evasion, or Greater Evasion, give them the option to use it.
                #     # for word in self.pOneInfo['feats taken']:
                #     #     answer = ""
                #     #     if self.pOneEvade == 1 and word == "evasion":
                #     #         while answer != "yes" and answer != "no":
                #     #             answer = await ctx.send(
                #     #                 self.pOneInfo['name'] + ", do you wish to evade? ").lower()
                #     #             if answer == "yes":
                #     #                 total = int(total * 0.5)
                #     #                 self.totalDamage = total
                #     #                 self.pTwoEvade = 0
                #     #             elif answer == "no":
                #     #                 pass
                #     #             else:
                #     #                 await ctx.send("Answer 'yes' or 'no'")
                #     #     elif self.pOneEvade == 1 and word == "improved evasion":
                #     #         while answer != "yes" and answer != "no":
                #     #             answer = await ctx.send(
                #     #                 self.pOneInfo['name'] + ", do you wish to evade? ").lower()
                #     #             if answer == "yes":
                #     #                 total = int(total * 0.5)
                #     #                 self.totalDamage = total
                #     #                 self.pTwoEvade = 0
                #     #             elif answer == "no":
                #     #                 pass
                #     #             else:
                #     #                 await ctx.send("Answer 'yes' or 'no'")
                #     #     elif self.pOneEvade == 1 and word == "greater evasion":
                #     #         while answer != "yes" and answer != "no":
                #     #             answer = await ctx.send(
                #     #                 self.pTwoInfo['name'] + ", do you wish to evade? ").lower()
                #     #             if answer == "yes":
                #     #                 total = int(total * 0.5)
                #     #                 self.totalDamage = total
                #     #                 self.pTwoEvade = 0
                #     #             elif answer == "no":
                #     #                 pass
                #     #             else:
                #     #                 await ctx.send("Answer 'yes' or 'no'")
                #     # If Player One used 'deflect', 'improved async deflect', or 'greater async deflect', apply damage mitigation here
                #     if pOneFeatUsed[0] == "deflect":
                #         await ctx.send( self.pOneInfo['name'] + " used async deflect to lessen the blow.")
                #         total = int(total * float(pOneFeatUsed[1]))
                #     elif pOneFeatUsed[0] == "improved deflect":
                #         await ctx.send( self.pOneInfo['name'] + " used async deflect to lessen the blow")
                #         total = int(total * float(pOneFeatUsed[1]))
                #     elif pOneFeatUsed[0] == "greater deflect":
                #         await ctx.send( self.pOneInfo['name'] + " used async deflect to lessen the blow")
                #         await ctx.send( pOneFeatUsed[1])
                #         await ctx.send( total)
                #         total = int(total * float(pOneFeatUsed[1]))
                #         await ctx.send( total)
                #     self.totalDamage = total
                #     # testing data to see that modifiers are carrying over correctly. Delete this when project is finished.
                #     await ctx.send(
                #                 "Roll: " + str(damage) + " Modifier: " + str(pTwoModifier) + " PA: " + str(
                #                     pMod) + " CD: " + str(cMod))
                #     # display total damage done, and reset passive feat counters (power attack and combat defense).
                #     await ctx.send( self.pTwoInfo['name'] + " did " + str(total) + " points of damage.")
                #     self.pTwopMod = 0
                #     self.pTwocMod = 0
                #     self.token = 1
                #
                # # Otherwise, continue on with the bulk of this method.
                # else:
                #     pTwoToHit = self.pTwoInfo['hit']
                #     pOneAC = self.pOneInfo['ac']
                #
                #     pMod = self.pTwopMod
                #     cMod = self.pTwocMod
                #     dMod = self.pTwodMod
                #     mMod = self.pTwomMod
                #     pOnedMod = self.pOnedMod
                #     pOnemMod = self.pOnemMod
                #
                #     # determine the roll of the 1d20.
                #     hit = random.randint(1, 20)
                #
                #
                #     # If Player Two has Hurt Me, Improved Hurt Me, and Greater Hurt Me, check hit points, and apply
                #     # bonuses.
                #     for word in self.pOneInfo['feats taken']:
                #         percentage = int((self.pTwoCurrentHP / self.pTwoTotalHP) * 100)
                #         if word == 'hurt me':
                #             if percentage < 66:
                #                 self.bonusHurt = 1
                #             elif percentage < 33:
                #                 self.bonusHurt = 2
                #         elif word == 'improved hurt me':
                #             if percentage < 66:
                #                 self.bonusHurt = 2
                #             elif percentage < 33:
                #                 self.bonusHurt = 3
                #         elif word == 'greater hurt me':
                #             if percentage < 66:
                #                 self.bonusHurt = 2
                #             elif percentage < 33:
                #                 self.bonusHurt = 4
                #         elif word == 'hurt me more':
                #             if percentage < 75:
                #                 self.bonusHurt = 2
                #             elif percentage < 50:
                #                 self.bonusHurt = 4
                #             elif percentage < 25:
                #                 self.bonusHurt = 6
                #
                #     # if the raw result is equal to 20, count the critical counter up to 1.
                #     if hit == 20:
                #         self.critical = 1
                #         await ctx.send( self.pTwoInfo['name'] + " has critically hit.")
                #
                #     if self.pTwoRiposte == 5:
                #         await ctx.send(
                #                     self.pTwoInfo['name'] + "Benefits from +5 hit bonus effect from riposte.")
                #
                #     # calculate the total after modifiers
                #     total = int(hit + pTwoToHit - pMod + cMod - dMod + mMod + self.pTwoRiposte + self.hurtBonus)
                #
                #     # Ensures Player Two benefits from hit bonus of Riposte only once.
                #     self.pTwoRiposte = 0
                #
                #     # Reset Hurt Me bonuses to ensure it doesn't bleed over to Player One.
                #     self.hurtBonus = 0
                #
                #     # if Player Two used riposte, and
                #     # if any version of crippling blow was used, tack on the penalty to the above total
                #     if pOneFeatUsed[0] == "crippling blow" or pOneFeatUsed[0] == "improved crippling blow" or \
                #             pOneFeatUsed[0] == "greater crippling blow":
                #         await ctx.send(
                #                     self.pOneInfo['name'] + " Used " + str(pOneFeatUsed[0]) + ", Giving " + self.pTwoInfo[
                #                         'name'] + " a " + str(pOneFeatUsed[1]) + " To their attack.")
                #         total = total + pOneFeatUsed[1]
                #
                #     # testing data to see that modifiers are carrying over correctly. Delete this when project is finished.
                #     await ctx.send(
                #                 "Roll: " + str(hit) + " Base: " + str(pTwoToHit) + " PA: " + str(pMod) + " CE: "
                #                 + str(cMod) + " DF: " + str(dMod) + " MC: " + str(mMod) +
                #                 " Riposte: " + str(self.pTwoRiposte) + " Hurt Me: " + str(self.bonusHurt))
                #
                #     # find Player One's total AC
                #     totalAC = int(pOneAC + pOnedMod - pOnemMod)
                #
                #     # testing data to see that modifiers are carrying over correctly. Delete this when project is finished.
                #     await ctx.send( " P1 AC: " + str(pOneAC) + " DF: " + str(pOnedMod) + " MC: " + str(pOnemMod))
                #
                #     # determine if the total roll, after all modifiers have been included, is a successful hit or not. then
                #     # head to the appropriate method
                #     if total >= pOneAC:
                #
                #         await ctx.send(
                #                     self.pTwoInfo['name'] + " rolled a " + str(total) + " to hit an AC " + str(
                #                         totalAC) + " and was successful.")
                #         self.pOnedMod = 0
                #         self.pOnemMod = 0
                #         self.pOneRiposte = 0
                #
                #         # Obtain Player Two's base damage and base modifier, and roll damage. Assign 'power attack' and 'combat defense'
                #         # modifiers to variables, and roll damage.
                #         pTwoBaseDamage = self.pTwoInfo['base damage']
                #         pTwoModifier = self.pTwoInfo['damage']
                #         pTwoMinimum, pTwoMaximum = pTwoBaseDamage.split('d')
                #         pMod = self.pTwopMod
                #         cMod = self.pTwocMod
                #         damage = random.randint(int(pTwoMinimum), int(pTwoMaximum))
                #         # if critical counter is a value of 1, double the damage done, then reset counter to 0.
                #         if self.critical == 1:
                #             damage = damage * 2
                #             self.critical = 0
                #         # if Player Two used feat 'titan blow', apply 50% bonus damage.
                #         if pTwoFeatUsed[0] == "titan blow":
                #             await ctx.send( self.pTwoInfo['name'] + " used the feat 'titan blow'.")
                #             damage = damage * float(pTwoFeatUsed[1])
                #         # if Player One use 'staggering blow' half damage done.
                #         if pOneFeatUsed[0] == "staggering blow":
                #             await ctx.send(
                #                         self.pOneInfo['name'] + " used the feat 'staggering blow', halving " +
                #                         self.pTwoInfo['name'] + "'s damage roll")
                #             damage = damage * float(pOneFeatUsed[1])
                #         # ensure that no matter what, raw damage can not fall below 1, then assign total damage to variable, and in turn
                #         # assign it to variable to be accessed for scoreboard.
                #         if damage < 1:
                #             damage = 1
                #         total = int(damage + pTwoModifier + pMod - cMod)
                #         # if Player One used 'quick strike', 'improved quick strike', or 'greater quick strike', apply the return
                #         # damage here
                #         pOneBaseDamage = self.pOneInfo['base damage']
                #         pOneModifier = self.pOneInfo['damage']
                #         pOneMinimum, pOneMaximum = pOneBaseDamage.split('d')
                #         pMod = self.pOnepMod
                #         cMod = self.pOnecMod
                #         # apply the damage from 'quick strike', 'improved quick strike', or 'greater quick strike' if such feats were
                #         # used
                #         if pOneFeatUsed[0] == "quick strike":
                #             # Roll damage for Player One, and multiply it by desired amount.
                #             damage = random.randint(int(pOneMinimum), int(pOneMaximum))
                #             total = (damage + pOneModifier + pMod - cMod)
                #             quickDamage = int(total * float(pOneFeatUsed[1]))
                #             # Ensure damage is always at least 1hp and print out result
                #             if quickDamage < 1:
                #                 quickDamage = 1
                #             self.pOneQuickDamage = quickDamage
                #             self.pTwoCurrentHP = self.pTwoCurrentHP - self.pOneQuickDamage
                #             await ctx.send(
                #                         self.pOneInfo['name'] + " used 'quick strike,' managing to do an additional " + str(
                #                             self.pOneQuickDamage) + "hp of damage.")
                #         if pOneFeatUsed[0] == "improved quick strike":
                #             # Roll damage for Player one, and multiply it by desired amount.
                #             damage = random.randint(int(pOneMinimum), int(pOneMaximum))
                #             total = (damage + pOneModifier + pMod - cMod)
                #             quickDamage = int(total * float(pOneFeatUsed[1]))
                #             # Ensure damage is always at least 1hp and print out result
                #             if quickDamage < 1:
                #                 quickDamage = 1
                #             self.pOneQuickDamage = quickDamage
                #             self.pTwoCurrentHP = self.pTwoCurrentHP - self.pOneQuickDamage
                #             await ctx.send(
                #                         self.pOneInfo['name'] + " used 'quick strike,' managing to do an additional " + str(
                #                             self.pOneQuickDamage) + "hp of damage.")
                #         if pOneFeatUsed[0] == "greater quick strike":
                #             # roll damage for player One, and multiply it by desired amount
                #             damage = random.randint(int(pOneMinimum), int(pOneMaximum))
                #             total = (damage + pOneModifier + pMod - cMod)
                #             quickDamage = int(total * float(pOneFeatUsed[1]))
                #             # Ensure damage is always at least 1hp and print out result
                #             self.pOneQuickDamage = quickDamage
                #             self.pTwoCurrentHP = self.pTwoCurrentHP - self.pOneQuickDamage
                #             await ctx.send(
                #                         self.pOneInfo['name'] + " used 'quick strike,' managing to do an additional " + str(
                #                             self.pOneQuickDamage) + "hp of damage.")
                #         if pOneFeatUsed[0] == "riposte":
                #             # roll damage for player One, and multiply it by desired amount
                #             damage = random.randint(int(pOneMinimum), int(pOneMaximum))
                #             total = (damage + pOneModifier + pMod - cMod)
                #             quickDamage = int(total * float(pOneFeatUsed[1][0]))
                #             # Ensure damage is always at least 1hp and print out result
                #             if quickDamage < 1:
                #                 quickDamage = 1
                #             self.pOneQuickDamage = quickDamage
                #             self.pTwoCurrentHP = self.pTwoCurrentHP - self.pTwoQuickDamage
                #             await ctx.send(
                #                         self.pOneInfo['name'] + " used 'quick strike,' managing to do an additional " + str(
                #                             self.pOneQuickDamage) + "hp of damage.")
                #             self.pOneRiposte = 1
                #         # If Player One has Evasion, Improved Evasion, or Greater Evasion, give them the option to use it.
                #         # for word in self.pOneInfo['feats taken']:
                #         #     answer = ""
                #         #     if self.pOneEvade == 1 and word == "evasion":
                #         #         while answer != "yes" and answer != "no":
                #         #             answer = await ctx.send(
                #         #                 self.pOneInfo['name'] + ", do you wish to evade? ").lower()
                #         #             if answer == "yes":
                #         #                 total = int(total * 0.5)
                #         #                 self.totalDamage = total
                #         #                 self.pTwoEvade = 0
                #         #             elif answer == "no":
                #         #                 pass
                #         #             else:
                #         #                 await ctx.send("Answer 'yes' or 'no'")
                #         #     elif self.pOneEvade == 1 and word == "improved evasion":
                #         #         while answer != "yes" and answer != "no":
                #         #             answer = await ctx.send(
                #         #                 self.pOneInfo['name'] + ", do you wish to evade? ").lower()
                #         #             if answer == "yes":
                #         #                 total = int(total * 0.5)
                #         #                 self.totalDamage = total
                #         #                 self.pTwoEvade = 0
                #         #             elif answer == "no":
                #         #                 pass
                #         #             else:
                #         #                 await ctx.send("Answer 'yes' or 'no'")
                #         #     elif self.pOneEvade == 1 and word == "greater evasion":
                #         #         while answer != "yes" and answer != "no":
                #         #             answer = await ctx.send(
                #         #                 self.pTwoInfo['name'] + ", do you wish to evade? ").lower()
                #         #             if answer == "yes":
                #         #                 total = int(total * 0.5)
                #         #                 self.totalDamage = total
                #         #                 self.pTwoEvade = 0
                #         #             elif answer == "no":
                #         #                 pass
                #         #             else:
                #         #                 await ctx.send("Answer 'yes' or 'no'")
                #         # If Player One used 'deflect', 'improved async deflect', or 'greater async deflect', apply damage mitigation here
                #         if pOneFeatUsed[0] == "deflect":
                #             await ctx.send( self.pOneInfo['name'] + " used async deflect to lessen the blow.")
                #             total = int(total * float(pOneFeatUsed[1]))
                #         elif pOneFeatUsed[0] == "improved deflect":
                #             await ctx.send( self.pOneInfo['name'] + " used async deflect to lessen the blow")
                #             total = int(total * float(pOneFeatUsed[1]))
                #         elif pOneFeatUsed[0] == "greater deflect":
                #             await ctx.send( self.pOneInfo['name'] + " used async deflect to lessen the blow")
                #             await ctx.send( pOneFeatUsed[1])
                #             await ctx.send( total)
                #             total = int(total * float(pOneFeatUsed[1]))
                #             await ctx.send( total)
                #         self.totalDamage = total
                #         # testing data to see that modifiers are carrying over correctly. Delete this when project is finished.
                #         await ctx.send(
                #                     "Roll: " + str(damage) + " Modifier: " + str(pTwoModifier) + " PA: " + str(
                #                         pMod) + " CD: " + str(cMod))
                #         # display total damage done, and reset passive feat counters (power attack and combat defense).
                #         await ctx.send( self.pTwoInfo['name'] + " did " + str(total) + " points of damage.")
                #         self.pTwopMod = 0
                #         self.pTwocMod = 0
                #         self.token = 1
                #     else:
                #         await ctx.send(
                #                     self.pTwoInfo['name'] + " rolled a " + str(total) + " to hit an AC " + str(
                #                         totalAC) + " and missed.")
                #         self.pOnedMod = 0
                #         self.pOnemMod = 0
                #         self.token = 1
                #         if pOneFeatUsed[0] == "riposte":
                #             self.pOneRiposte = 5
                #
                # # Determine HP at end of round.
                # if self.pOneQuickDamage != 0:
                #     self.pOneCurrentHP = self.pOneCurrentHP - self.totalDamage - self.pOneQuickDamage
                #     self.pOneQuickDamage = 0
                #     self.count += 1
                # else:
                #     self.pOneCurrentHP = self.pOneCurrentHP - self.totalDamage
                #
                # # Print the scoreboard
                # await ctx.send( self.pOneInfo['name'] + ": " + str(self.pOneCurrentHP) + "/" +
                #             str(self.pOneTotalHP) + "  ||  " + self.pTwoInfo['name'] + ": " +
                #             str(self.pTwoCurrentHP) + "/" + str(self.pTwoTotalHP) + " \n" +
                #             self.pOneInfo['name'] + "'s turn. Type: !usefeat <feat> if you wish to use a feat.")
                #
                # # If Player One is dead, state such, and how many rounds it took to win. Calculate and distribute xp.
                # # reset game and token counters back to 0.
                # if self.pOneCurrentHP <= 0:
                #     self.game = 0
                #     self.token = 0
                #     await ctx.send( self.pTwoInfo['name'] + " won in " + str(int(self.count / 2)) + " rounds")
                #     level = abs(self.pOneLevel - self.pTwoLevel)
                #     if level == 0:
                #         level = 1
                #     if level <= 3:
                #         levelDiff = level * self.pOneLevel
                #         differHP = abs(self.pOneCurrentHP - self.pTwoCurrentHP)
                #         self.xp = 10 * levelDiff + differHP
                #
                #     elif 3 > level < 6:
                #         levelDiff = level * self.pOneLevel
                #         differHP = abs(self.pOneCurrentHP - self.pTwoCurrentHP)
                #         self.xp = 7 * levelDiff + differHP
                #
                #     elif 7 > level < 10:
                #         levelDiff = level * self.pOneLevel
                #         differHP = abs(self.pOneCurrentHP - self.pTwoCurrentHP)
                #         self.xp = 5 * levelDiff + differHP
                #
                #     else:
                #         await ctx.send( "As the level difference was greater than 10, no XP was awarded.")
                #     await ctx.send( self.pTwoInfo['name'] + " has earned: " + str(self.xp) + " experience points.")
                #     self.currentPlayerXP = self.pTwoInfo['currentxp'] + self.xp
                #     self.nextLevel = self.pTwoInfo['nextlevel']
                #     self.winner = self.pTwoUsername
                #     self.loser = self.pOneUsername
                #     self.levelUp = self.pTwoInfo['level']
                #     path = os.getcwd()
                #     charFolder = os.path.join(path + "/characters/")
                #
                #     with open(charFolder + self.winner + '.txt', 'r+') as file:
                #         charData = json.load(file)
                #         charData['currentxp'] = self.currentPlayerXP
                #         charData['wins'] += 1
                #         file.seek(0)
                #         file.write(json.dumps(charData, ensure_ascii=False, indent=2))
                #         file.truncate()
                #         file.close()
                #
                #     with open(charFolder + self.loser + '.txt', 'r+') as file:
                #         charData = json.load(file)
                #         charData['losses'] += 1
                #         file.seek(0)
                #         file.write(json.dumps(charData, ensure_ascii=False, indent=2))
                #         file.truncate()
                #         file.close()
                #
                #     if self.currentPlayerXP >= self.nextLevel:
                #         newLevel = self.levelUp + 1
                #         newLevel = str(newLevel)
                #         await ctx.send( self.winner.capitalize() + " has reached level " + newLevel + "!")
                #         levelFile = open(charFolder + "levelchart.txt", "r", encoding="utf-8")
                #         levelDict = json.load(levelFile)
                #         levelFile.close()
                #         with open(charFolder + self.winner + '.txt', 'r+') as file:
                #             charData = json.load(file)
                #             charData['level'] = int(newLevel)
                #             charData['hitpoints'] = int(levelDict[newLevel][0])
                #             charData['base damage'] = str(levelDict[newLevel][1]) + "d" + str(
                #                 levelDict[newLevel][2])
                #             if charData['total feats'] == levelDict[newLevel][4]:
                #                 charData['total feats'] = levelDict[newLevel][4]
                #             else:
                #                 await ctx.send(
                #                     "You have a new feat slot to fill. Use the !feat command to select new feat.")
                #                 charData['total feats'] = levelDict[newLevel][4]
                #                 charData['remaining feats'] = 1
                #             if charData['total ap'] == levelDict[newLevel][3]:
                #                 charData['total ap'] = levelDict[newLevel][3]
                #             else:
                #                 await ctx.send("You have a new ability point to spend. the !add command.")
                #             charData['hit'] = int(levelDict[newLevel][5])
                #             charData['damage modifier'] = int(levelDict[newLevel][5])
                #             charData['ac'] = int(levelDict[newLevel][6])
                #             charData['currentxp'] = int(self.currentPlayerXP)
                #             charData['nextlevel'] = int(levelDict[newLevel][7])
                #             file.seek(0)
                #             file.write(json.dumps(charData, ensure_ascii=False, indent=2))
                #             file.truncate()
                #             file.close()
                #
                #     else:
                #         pass

    @roll.error
    async def name_roll(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("The command !roll may not be used in PMs!")
        else:
            raise error

    #!evasion
    @commands.command()
    @commands.guild_only()
    async def evasion(self, ctx):
        user = str(ctx.message.author.id)
        msg, bGameTimer, self.playerOne, self.playerTwo, self.pOneInfo, self.pTwoInfo, self.featToken, \
        self.count, self.token, self.totalDamage, self.pOneTotalHP, self.pTwoTotalHP, \
        self.pOneCurrentHP, self.pTwoCurrentHP, self.pOnepMod, self.pOnecMod, self.pOnedMod,\
        self.pOnemMod, self.pOneQuickDamage, self.pTwoQuickDamage, \
        self.pTwoEvade, self.pOneEvade, self.iddqd = onMSGUtil.message_8_evasion(user, self.playerOne, self.playerTwo,
                                                                       self.pOneInfo, self.pTwoInfo, self.featToken, \
                                                                       self.count, self.token, self.critical,
                                                                       self.bonusHurt, self.totalDamage,
                                                                       self.pOneTotalHP, self.pTwoTotalHP,
                                                                       self.pOneCurrentHP, self.pTwoCurrentHP,
                                                                       self.pOnepMod, self.pOnecMod, self.pOnedMod,
                                                                       self.pOnemMod, self.pOneQuickDamage,
                                                                       self.pTwoQuickDamage, self.pTwoEvade,
                                                                       self.pOneEvade, self.iddqd)
        for msg_item in msg:
            await ctx.send(msg_item)
        if bGameTimer:
            gametimeout = 3600
            self.gameTimer = Timer(gametimeout, self.combatTimeOut)
            self.gameTimer.start()
        if self.bEvasion is True:
            self.bEvasion = False
        if self.bDeflect is True:
            self.bDeflect = False
    
    @evasion.error
    async def name_evasion(self, ctx,error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("The command !evasion may not be used in PMs!")
        else:
            raise error

    #!deflect
    @commands.command()
    @commands.guild_only()
    async def deflect(self, ctx):
        user = str(ctx.message.author.id)
        msg, bGameTimer, self.playerOne, self.playerTwo, self.pOneInfo, self.pTwoInfo, self.featToken, \
        self.count, self.token, self.totalDamage, self.pOneTotalHP, self.pTwoTotalHP, \
        self.pOneCurrentHP, self.pTwoCurrentHP, self.pOnepMod, self.pOnecMod, self.pOnedMod,\
        self.pOnemMod, self.pOneQuickDamage, self.pTwoQuickDamage, \
        self.pTwoDeflect, self.pOneDeflect, self.iddqd = message_8_deflect(user, self.playerOne, self.playerTwo,
                                                                           self.pOneInfo, self.pTwoInfo, self.featToken, \
                                                                           self.count, self.token, self.critical,
                                                                           self.bonusHurt, self.totalDamage,
                                                                           self.pOneTotalHP, self.pTwoTotalHP,
                                                                           self.pOneCurrentHP, self.pTwoCurrentHP,
                                                                           self.pOnepMod, self.pOnecMod, self.pOnedMod,
                                                                           self.pOnemMod, self.pOneQuickDamage,
                                                                           self.pTwoQuickDamage, self.pTwoDeflect,
                                                                           self.pOneDeflect, self.iddqd)
        for msg_item in msg:
            await ctx.send(msg_item)
        if bGameTimer:
            gametimeout = 3600
            self.gameTimer = Timer(gametimeout, self.combatTimeOut)
            self.gameTimer.start()
        if self.bDeflect is True:
            self.bDeflect = False
        if self.bEvasion is True:
            self.bEvasion = False

    @evasion.error
    async def name_deflect(self, ctx,error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("The command !deflect may not be used in PMs!")
        else:
            raise error

    # !forfeit
    @commands.command()
    @commands.guild_only()
    async def forfeit(self, ctx):
        user = str(ctx.message.author.id)
        if self.game == 1:
            if user == self.playerOne or user == self.playerTwo:
                if character.lower() == self.playerOne:
                    await ctx.send(self.pOneInfo['name'] + " has forfeited the match.")
                    xpCap = self.pOneInfo['nextlevel'] - 10
                    if self.pOneInfo['currentxp'] < xpCap:
                        await ctx.send(self.pOneInfo['name'] + " has earned 10xp")
                        with open(charFolder + user + '.txt', 'r+') as file:
                            charData = json.load(file)
                            self.pOneInfo['currentxp'] = self.pOneInfo['currentxp'] + 10
                            file.seek(0)
                            file.write(json.dumps(charData, ensure_ascii=False, indent=2))
                            file.truncate()
                            file.close()
                    else:
                        await ctx.send(self.pOneInfo['name'] + " has earned 0xp")
                elif user == self.playerTwo:
                    await ctx.send(self.pOneInfo['name'] + " has forfeited the match.")
                    xpCap = self.pTwoInfo['nextlevel'] - 10
                    if self.pTwoInfo['currentxp'] < xpCap:
                        await ctx.send(self.pTwoInfo['name'] + " has earned 10xp")
                        with open(charFolder + user + '.txt', 'r+') as file:
                            charData = json.load(file)
                            self.pTwoInfo['currentxp'] = self.pTwoInfo['currentxp'] + 10
                            file.seek(0)
                            file.write(json.dumps(charData, ensure_ascii=False, indent=2))
                            file.truncate()
                            file.close()
                    else:
                        await ctx.send(self.pTwoInfo['name'] + " has earned 0xp")
                self.opponent = ""
                self.playerOne = ""
                self.playerTwo = ""
                self.winner = ""
                self.loser = ""
                self.pOneUsername = None
                self.pTwoUsername = None
                # PLAYER INFO
                self.pOneInfo = {}
                self.pTwoInfo = {}
                # HP AND TURN COUNTERS
                self.gameTimer.cancel()
                self.gameTimer = 0
                self.count = 0
                self.base = 0
                self.token = 0
                self.game = 0
                self.critical = 0
                self.bonusHurt = 0
                self.nerveDamage = 0
                self.totalDamage = 0
                self.pOneTotalHP = 0
                self.pTwoTotalHP = 0
                self.pOneCurrentHP = 0
                self.pTwoCurrentHP = 0
                # PLAYER ONE FEAT COUNTERS
                self.pOnepMod = 0
                self.pOnecMod = 0
                self.pOnedMod = 0
                self.pOnemMod = 0
                self.pOneEvade = 1
                self.pOneDeflect = 1
                self.pOneRiposte = 0
                self.pOneQuickDamage = 0
                self.pOneFeatInfo = None
                self.pOneSpentFeat = []
                # PLAYER TWO FEAT COUNTERS
                self.pTwopMod = 0
                self.pTwocMod = 0
                self.pTwodMod = 0
                self.pTwomMod = 0
                self.pTwoEvade = 1
                self.pTwoDeflect = 1
                self.pTwoRiposte = 0
                self.pTwoQuickDamage = 0
                self.pTwoFeatInfo = None
                self.pTwoSpentFeat = []
                # XP AND LEVEL COUNTERS
                self.pOneLevel = 0
                self.pTwoLevel = 0
                self.xp = 0
                self.currentPlayerXP = 0
                self.nextLevel = 0
                self.levelUp = 0
                await ctx.send("Well, that was a waste everyone's time. Show's over folks. (Resetting Match Status)")
            else:
                await ctx.send("You aren't even fighting, why you so afraid?")
        else:
            await ctx.send("There is no fight taking place. What are you running from?")

    @player.error
    async def player_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("The command !forfeit may not be used in PMs!")
        else:
            raise error

    #!pattack
    @commands.command()
    @commands.guild_only()
    async def pattack(self, ctx, *, points):
        user = str(cts.message.author.id)

        msg, self.game, self.playerOne, self.playerTwo, self.pOneInfo, self.pTwoInfo, self.token, \
        self.pOnepMod, self.pTwopMod, self.pOneLevel, self.pTwoLevel \
            = onMSGUtil.message_8_pattack(user, points, self.game, self.playerOne,
                                self.playerTwo, self.pOneInfo, self.pTwoInfo, self.token, self.pOnepMod, self.pTwopMod,
                                self.pOneLevel, self.pTwoLevel)
        for msg_item in msg:
            await ctx.send(msg_item)

    @pattack.error
    async def name_pattack(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("The command !pattack may not be used in PMs!")
        else:
            raise error

    #!dfight
    @commands.command()
    @commands.guild_only()
    async def dfight(self, ctx, *, points):
        user = str(ctx.message.author.id)
        msg, self.game, self.playerOne, self.playerTwo, self.pOneInfo, self.pTwoInfo, self.token, self.pOnedMod, \
        self.pTwodMod, self.pOneLevel, self.pTwoLevel \
            = message_8_dfight(user, points, self.game, self.playerOne,
                               self.playerTwo,
                               self.pOneInfo, self.pTwoInfo, self.token, self.pOnedMod, self.pTwodMod,
                               self.pOneLevel, self.pTwoLevel)
        for msg_item in msg:
            await ctx.send(msg_item)
        # Allows for the use of the 'defensive fighting' passive feat. Makes sure it applies correct bonuses for correct
        # levels.

    @dfight.error
    async def name_dfight(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("The command !dfight may not be used in PMs!")
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
    #                 await ctx.send( "You are not high enough level to invest that many points.")
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
    #                 await ctx.send( "You are not high enough level to invest that many points.")
    #
    #         else:
    #             await ctx.send( "Either it's not your turn, or you aren't even fighting. Either way, No.")
    #
    #     else:
    #         await ctx.send( "This command does nothing right now. No combat is taking place.")
    #
    # @cexpert.error
    # async def name_cexpert(self, ctx, error):
    #     if isinstance(error, commands.NoPrivateMessage):
    #         await ctx.send("The command !cexpert may not be used in PMs!")
    #     else:
    #         raise error

    #!masochist
    @commands.command()
    @commands.guild_only()
    async def masochist(self, ctx, *, points):
        character = ctx.author.send
        # make sure that this command cannot be ran if a fight is taking place.
        if self.game == 1:
            # ensures the command can only be used by player one, when it is their turn. To prevent trolls from
            # spamming commands.
            if character == self.pOneUsername and self.token == 1:
                mod = int(message)
                if self.pOneLevel <= 4 and mod == 1:
                    self.pOnemMod = 1
                elif 4 < self.pOneLevel <= 8 and mod == 2:
                    self.pOnemMod = 2
                elif 8 < self.pOneLevel <= 12 and mod == 3:
                    self.pOnemMod = 3
                elif 12 < self.pOneLevel <= 16 and mod == 4:
                    self.pOnemMod = 4
                elif 16 < self.pOneLevel <= 20 and mod == 5:
                    self.pOnemMod = 5
                else:
                    await ctx.send( "You are not high enough level to invest that many points.")
            # ensures the command can only be used by player two, when it is their turn. To prevent trolls from
            # spamming commands.
            elif character == self.pTwoUsername and self.token == 2:
                mod = int(message)
                if self.pTwoLevel <= 4 and mod == 1:
                    self.pTwomMod = 1
                elif 4 < self.pTwoLevel <= 8 and mod == 2:
                    self.pTwomMod = 2
                elif 8 < self.pTwoLevel <= 12 and mod == 3:
                    self.pTwomMod = 3
                elif 12 < self.pTwoLevel <= 16 and mod == 4:
                    self.pTwomMod = 4
                elif 16 < self.pTwoLevel <= 20 and mod == 5:
                    self.pTwomMod = 5
                else:
                    await ctx.send( "You are not high enough level to invest that many points.")

            else:
                await ctx.send( "Either it's not your turn, or you aren't even fighting. Either way, No.")
        else:
            await ctx.send( "This command does nothing right now. No combat is taking place.")

    @masochist.error
    async def name_masochist(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("The command !masochist may not be used in PMs!")
        else:
            raise error

#------------------------------------------PM COMMANDS------------------------------------------------------------------
   #!stats
    #!stats
    @commands.command()
    @commands.dm_only()
    async def stats(self, ctx, strength, dexterity, constitution):
        private = ctx.send
        player = str(ctx.message.author.id)
        path = os.getcwd()
        charFolder = os.path.join(path + "/characters/")
        charFile = Path(charFolder + player + ".txt")
        file = open(charFolder + player + ".txt", "r", encoding="utf-8")
        charData = json.load(file)
        file.close()
        reset = charData['reset']
        try:
            msg = onPRIUtil.pri_6_stats(charData, charFolder, charFile, player, strength, dexterity, constitution)
            for msg_item in msg:
                await ctx.send( msg_item)
        except IndexError:
            await ctx.send( "You need to use the command as instructed. !stat <str> <dex> <con>. Where "
                                   "<str> is your desired strength, <dex> is your desired dexterity, and "
                                   "<con> is your desired constitution. do **NOT** use commas, and place a "
                                   "space between each number. Example; !stats 10 5 0")
        except ValueError:
            await ctx.send( "You need to use the command as instructed. !stat <str> <dex> <con>. Where "
                                   "<str> is your desired strength, <dex> is your desired dexterity, and "
                                   "<con> is your desired constitution. do **NOT** use commas, and place a "

                                   "space between each number. Example: !stats 10 5 0")
        except UnboundLocalError:
            await ctx.send( "You don't even have a character created yet. Type !name <name> in the room. "
                                   "Where <name> is your character's actual name. (Example: !name Joe")

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
            await ctx.send( msg_item)

    @viewchar.error
    async def viewchar_error(self, ctx, error):
        if isinstance(error, commands.PrivateMessageOnly):
            await ctx.send("You're an idiot, now everyone knows. Why would you want to display your character sheet "
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
        await ctx.send( stringList + "\n Type: !feat help <feat name> to get a PM of feat info\n"
                                            "or just go "
                                            "https://docs.google.com/document/d/1CJjC0FxunXXi8zh1I9fZqRrWij9oJiIfIZoxrPJ7GYQ/edit?usp=sharing")

    @featlist.error
    async def name_featlist(self, ctx, error):
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

        if answer not in featList:
            await ctx.send( "Make sure you have spelled the feat correctly")
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
    async def name_feathelp(self, ctx, error):
        if isinstance(error, commands.PrivateMessageOnly):
            await ctx.send("I'm not gonna spam the arena with this list, man. PM me with !feathelp <feat> for assistance.")

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("I need the name of the feat you want help on. I can't read minds.")

        raise error

    #!featpick
    @commands.command()
    @commands.dm_only()
    async def featpick(self, ctx, *, answer):

        private = ctx.author.send
        player = str(ctx.message.author.id)

        featDictionary = featDict()[0]
        featList = featDict()[1]

        path = os.getcwd()
        charFolder = os.path.join(path + "/characters/")
        # charFile = Path(charFolder + player + ".txt")
        file = open(charFolder + player + ".txt", "r", encoding="utf-8")
        charData = json.load(file)
        file.close()

        msg = onPRIUtil.pri_10_feat_pick(answer, player, featList, featDictionary)
        for msg_item in msg:
            await ctx.send(msg_item)

    @feathelp.error
    async def name_featpick(self, ctx, error):
        if isinstance(error, commands.PrivateMessageOnly):
            await ctx.send(
                "Hey! Good work! You just told everyone what feat you are going to take! Now PM me with !feat <feat> to"
                " do it correctly.")
        else:
            raise error

def setup(client):
    client.add_cog(Combat(client))
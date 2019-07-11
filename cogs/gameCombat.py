import discord
from discord.ext import commands
import os
import json
import random
import time
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


class Combat(commands.Cog):

    def __init__(self, client):

        self.client = client
        # STRINGS
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
        self.count = 0
        self.token = 0
        self.game = 0
        self.critical = 0
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

    @commands.command()
    @commands.guild_only()
    @commands.has_role("Admin")
    async def reset(self, ctx):

        if self.token == 1:

            self.winner = self.pOneInfo["name"]
            self.loser = self.pTwoInfo["name"]
            ctx.send("Fight is being reset due to inactivity. ")
            ctx.send(self.winner + " wins by default.")
            self.xp = 50
            self.currentPlayerXP = self.pOneInfo['currentxp'] + self.xp
            self.nextLevel = self.pOneInfo['nextlevel']
            self.winner = self.pOneUsername
            self.loser = self.pTwoUsername
            self.levelUp = self.pOneInfo['level']
            path = os.getcwd()
            charFolder = os.path.join(path + "/characters/")

            with open(charFolder + self.winner + '.txt', 'r+') as file:
                charData = json.load(file)
                charData['currentxp'] = self.currentPlayerXP
                charData['wins'] += 1
                file.seek(0)
                file.write(json.dumps(charData, ensure_ascii=False, indent=2))
                file.truncate()
                file.close()

            with open(charFolder + self.loser + '.txt', 'r+') as file:
                charData = json.load(file)
                charData['losses'] += 1
                file.seek(0)
                file.write(json.dumps(charData, ensure_ascii=False, indent=2))
                file.truncate()
                file.close()
            if self.currentPlayerXP >= self.nextLevel:
                newLevel = self.levelUp + 1
                newLevel = str(newLevel)
                await ctx.send(self.winner.capitalize() + " has reached level " + newLevel + "!")
                levelFile = open(charFolder + "levelchart.txt", "r", encoding="utf-8")
                levelDict = json.load(levelFile)
                levelFile.close()
                with open(charFolder + self.winner + '.txt', 'r+') as file:
                    charData = json.load(file)
                    charData['level'] = int(newLevel)
                    charData['hitpoints'] = int(levelDict[newLevel][0])
                    charData['base damage'] = str(levelDict[newLevel][1]) + "d" + str(
                        levelDict[newLevel][2])
                    if charData['total feats'] == levelDict[newLevel][4]:
                        charData['total feats'] = levelDict[newLevel][4]
                    else:
                        await ctx.send("You have a new feat slot to fill. Use the !feat command to select new feat.")
                        charData['total feats'] = levelDict[newLevel][4]
                        charData['remaining feats'] = 1
                    if charData['total ap'] == levelDict[newLevel][3]:
                        charData['total ap'] = levelDict[newLevel][3]
                    else:
                        await ctx.send("You have a new ability point to spend. the !add command.")
                    charData['hit'] = int(levelDict[newLevel][5])
                    charData['damage modifier'] = int(levelDict[newLevel][5])
                    charData['ac'] = int(levelDict[newLevel][6])
                    charData['currentxp'] = int(self.currentPlayerXP)
                    charData['nextlevel'] = int(levelDict[newLevel][7])
                    file.seek(0)
                    file.write(json.dumps(charData, ensure_ascii=False, indent=2))
                    file.truncate()
                    file.close()
        elif self.token == 0:
            self.winner = self.pOneInfo["name"]
            self.loser = self.pTwoInfo["name"]
            ctx.send("Fight is being reset due to inactivity. ")
            ctx.send(self.winner + " wins by default.")
            self.xp = 50
            self.currentPlayerXP = self.pTwoInfo['currentxp'] + self.xp
            self.nextLevel = self.pTwoInfo['nextlevel']
            self.winner = self.pTwoUsername
            self.loser = self.pOneUsername
            self.levelUp = self.pTwoInfo['level']
            path = os.getcwd()
            charFolder = os.path.join(path + "/characters/")

            with open(charFolder + self.winner + '.txt', 'r+') as file:
                charData = json.load(file)
                charData['currentxp'] = self.currentPlayerXP
                charData['wins'] += 1
                file.seek(0)
                file.write(json.dumps(charData, ensure_ascii=False, indent=2))
                file.truncate()
                file.close()

            with open(charFolder + self.loser + '.txt', 'r+') as file:
                charData = json.load(file)
                charData['losses'] += 1
                file.seek(0)
                file.write(json.dumps(charData, ensure_ascii=False, indent=2))
                file.truncate()
                file.close()

            if self.currentPlayerXP >= self.nextLevel:
                newLevel = self.levelUp + 1
                newLevel = str(newLevel)
                await ctx.send(self.winner.capitalize() + " has reached level " + newLevel + "!")
                levelFile = open(charFolder + "levelchart.txt", "r", encoding="utf-8")
                levelDict = json.load(levelFile)
                levelFile.close()
                with open(charFolder + self.winner + '.txt', 'r+') as file:
                    charData = json.load(file)
                    charData['level'] = int(newLevel)
                    charData['hitpoints'] = int(levelDict[newLevel][0])
                    charData['base damage'] = str(levelDict[newLevel][1]) + "d" + str(
                        levelDict[newLevel][2])
                    if charData['total feats'] == levelDict[newLevel][4]:
                        charData['total feats'] = levelDict[newLevel][4]
                    else:
                        await ctx.send("You have a new feat slot to fill. Use the !feat command to select new feat.")
                        charData['total feats'] = levelDict[newLevel][4]
                        charData['remaining feats'] = 1
                    if charData['total ap'] == levelDict[newLevel][3]:
                        charData['total ap'] = levelDict[newLevel][3]
                    else:
                        await ctx.send("You have a new ability point to spend. the !add command.")
                    charData['hit'] = int(levelDict[newLevel][5])
                    charData['damage modifier'] = int(levelDict[newLevel][5])
                    charData['ac'] = int(levelDict[newLevel][6])
                    charData['currentxp'] = int(self.currentPlayerXP)
                    charData['nextlevel'] = int(levelDict[newLevel][7])
                    file.seek(0)
                    file.write(json.dumps(charData, ensure_ascii=False, indent=2))
                    file.truncate()
                    file.close()

        else:
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
            self.count = 0
            self.token = 0
            self.game = 0
            self.critical = 0
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
            ctx.send("The game has been reset.")

    @commands.command()
    @commands.guild_only()
    async def score(self, ctx, player):

        player = str(player.capitalize())

        path = os.getcwd()
        charFolder = os.path.join(path + "/characters/")
        with open(charFolder + "playerDatabase.txt", 'r', encoding="utf-8") as file:
            playerDatabase = json.loads(file.read())
        character = playerDatabase[player]
        with open(charFolder + character + ".txt", "r", encoding="utf-8") as file2:
            score = json.loads(file2.read())
            wins = str(score['wins'])
            losses = str(score['losses'])
        total = int(wins) + int(losses)


        if total == 0:
            await ctx.send(player + " has 100% win ratio. Or 0%. However you want to rationalize not having a single "
                                    "fight under their belt.")
        else:
            ratio = int((int(wins) / total) * 100)

            await ctx.send(player + " has " + wins + " wins, and " + losses + " losses. (" + (str(ratio)) + "%)")

    @commands.command()
    @commands.guild_only()
    async def challenge(self, ctx):
        # opens and loads in player one's character sheet. This is done in this method solely because I'm unsure if
        # loading json files in __init__ is actually a good idea. If I understand things correctly, things in a class's
        # __init__ is ran EVERY TIME a method is called within it. If so, then the json files would be opened, loaded,
        # and closed multiple times in a single run. Seems inefficient, and bad coding.
        if self.game == 0:
            player = str(ctx.message.author)
            path = os.getcwd()
            charFolder = os.path.join(path + "/characters/")
            charFile = Path(charFolder + player + ".txt")
            if not charFile.is_file():
                await ctx.send("You don't even have a character made to fight. What are you planning to do? Emoji the"
                               "opponent to death? Make a character, first.")
            elif self.game == 0.5:
                await ctx.send("A challenge has already been issued.")
            else:
                self.pOneUsername = ctx.message.author
                file = open(charFolder + player + ".txt", "r", encoding="utf-8")
                charStats = json.load(file)
                file.close()

                self.pOneInfo = charStats

                await ctx.send(self.pOneInfo['name'] + " has issued a challenge. Who accepts? (type !accept)")
                self.game = 0.5

                for seconds in range(0, 61):
                    time.sleep(1)
                    if seconds == 30:
                        await ctx.send("30 seconds to respond to challenge.")
                    elif seconds == 50:
                        await ctx.send("10 seconds to respond to challenge.")
                    elif seconds == 60:
                        await ctx.send("Challenge reset.")
                        self.game = 0

        else:
            await ctx.send("A Fight is already taking place. Wait your turn")

    @challenge.error
    async def name_challenge(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("The command !challenge may not be used in PMs!")
        else:
            raise error

    @commands.command()
    @commands.guild_only()
    async def accept(self, ctx):
        if self.game == 0.5:
            player = str(ctx.message.author)
            path = os.getcwd()
            charFolder = os.path.join(path + "/characters/")
            charFile = Path(charFolder + player + ".txt")
            if not charFile.is_file():
                await ctx.send("You don't even have a character made to fight. What are you planning to do? Emoji the "
                               "opponent to death? Make a character, first.")
            elif ctx.message.author == self.pOneUsername:
                await ctx.send("You can't fight yourself. This isn't Street Fighter.")
            else:
                self.game = 1
                self.pTwoUsername = ctx.message.author
                file = open(charFolder + player + ".txt", "r", encoding="utf-8")
                charStats = json.load(file)
                file.close()

                self.pTwoInfo = charStats

                self.pOneTotalHP = self.pOneInfo['hp']
                self.pTwoTotalHP = self.pTwoInfo['hp']
                self.pOneCurrentHP = self.pOneInfo['hp']
                self.pTwoCurrentHP = self.pTwoInfo['hp']
                self.pOneLevel = self.pOneInfo['level']
                self.pTwoLevel = self.pTwoInfo['level']

                await ctx.send("Rolling for Initiative (1d20 + (dexterity / 2). In result of tie, highest dex goes first. Should "
                               "that tie as well, coin toss. Player One has value of One.")

                playerOneInit = random.randint(1, 20)
                playerOneMod = int(self.pOneInfo['dexterity'] / 2)
                totalOne = playerOneInit + playerOneMod
                await ctx.send(self.pOneInfo['name'] + " rolled: " + str(playerOneInit) + " + " + str(
                    playerOneMod) + " and got " + str(totalOne))

                playerTwoInit = random.randint(1, 20)
                playerTwoMod = int(self.pTwoInfo['dexterity'] / 2)
                totalTwo = playerTwoInit + playerTwoMod
                await ctx.send(self.pTwoInfo['name'] + " rolled: " + str(playerTwoInit) + " + " + str(
                    playerTwoMod) + " and got " + str(totalTwo))

                if totalOne > totalTwo:
                    await ctx.send(self.pOneInfo['name'] + " Goes first")
                    token = 1
                    self.token = token
                    await ctx.send("If you wish to use one of your feats, type !usefeat <feat>. ")

                elif totalTwo > totalOne:
                    await ctx.send(self.pTwoInfo['name'] + " Goes first")
                    token = 2
                    self.token = token
                    await ctx.send("If you wish to use one of your feats, type !usefeat <feat>. ")

                elif totalOne == totalTwo:
                    await ctx.send("In result of tie, person with highest dexterity modifier goes first:")
                    await ctx.send(self.pOneInfo['name'] + "'s dexterity: " + str(playerOneMod))
                    await ctx.send(self.pTwoInfo['name'] + "'s dexterity: " + str(playerTwoMod))

                    if playerOneMod > playerTwoMod:
                        await ctx.send(self.pOneInfo['name'] + " Goes first")
                        token = 1
                        self.token = token
                        await ctx.send("If you wish to use one of your feats, type !usefeat <feat>. ")

                    elif playerOneMod < playerTwoMod:
                        await ctx.send(self.pTwoInfo['name'] + " Goes first")
                        token = 2
                        self.token = token
                        await ctx.send("If you wish to use one of your feats, type !usefeat <feat>. ")

                    else:
                        await ctx.send("As both dexterity values are equal as well. A coin flip. Value of one means " + self.pOneInfo['name'] + " goes first")
                        value = random.randint(1, 2)
                        await ctx.send(value)

                        if value == 1:
                            await ctx.send(self.pTwoInfo['name'] + " Goes first")
                            token = 1
                            self.token = token
                            await ctx.send("If you wish to use one of your feats, type !usefeat <feat>. ")

                        else:
                            await ctx.send(self.playerTwo + " Goes first")
                            token = 2
                            self.token = token
                            await ctx.send("If you wish to use one of your feats, type !usefeat <feat>. ")
        else:
                await ctx.send("A Fight is already taking place. Wait your turn")
            
    @accept.error
    async def name_accept(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("The command !accept may not be used in PMs!")
        else:
            raise error

    @commands.command()
    @commands.guild_only()
    async def usefeat(self, ctx, *, answer):
        if self.pOneUsername == ctx.message.author and self.token == 1:

            featDictionary = featDict()[0]
            if answer != "none":
                pOneLastFeat = answer
            else:
                pOneLastFeat = None

                if pOneLastFeat == 'none':
                    pOneLastFeat = None
                    self.pOneFeatInfo = pOneLastFeat

                elif pOneLastFeat in ('power attack', 'combat expertise', 'async defensive fighting', 'masochist', 'hurt me', 'improved hurt me',
                'greater hurt me', 'hurt me more', 'evasion', 'improved evasion', 'greater evasion'):
                    await ctx.send(pOneLastFeat + " will be determined after this phase.")

                elif pOneLastFeat in self.pOneSpentFeat:
                    await ctx.send("You have already used this feat. Please select another or type 'none.': ")

                elif pOneLastFeat in self.pOneInfo['feats taken']:
                    self.pOneSpentFeat.append(pOneLastFeat)
                    self.pOneFeatInfo = [pOneLastFeat, featDictionary[0][pOneLastFeat]['action']]

                elif pOneLastFeat not in self.pOneInfo['feats taken']:
                    await ctx.send("Either you do not have that feat, or you did not type it correctly")

        elif self.pTwoUsername == ctx.message.author and self.token == 2:

            featDictionary = featDict()[0]
            pTwoLastFeat = None

            if pTwoLastFeat == 'none':
                    pTwoLastFeat = None
                    self.pTwoFeatInfo = pTwoLastFeat

            elif pTwoLastFeat in (
                    'power attack', 'combat expertise', 'async defensive fighting', 'masochist', 'hurt me',
                    'improved hurt me',
                    'greater hurt me', 'hurt me more', 'evasion', 'improved evasion', 'greater evasion'):
                await ctx.send(pTwoLastFeat + " will be determined after this phase.")

            elif pTwoLastFeat in self.pTwoSpentFeat:
                await ctx.send("You have already used this feat. Please select another or type 'none.': ")

            elif pTwoLastFeat in self.pTwoInfo['feats taken']:
                self.pTwoSpentFeat.append(pTwoLastFeat)
                self.pTwoFeatInfo = [pTwoLastFeat, featDictionary[0][pTwoLastFeat]['action']]

            elif pTwoLastFeat not in self.pTwoInfo['feats taken']:
                await ctx.send("Either you do not have that feat, or you did not type it correctly")

        else:
            ctx.send("Either it is not your turn to select a feat, or you aren't even fighting. Either way, Stop.")

    @usefeat.error
    async def name_usefeat(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("The command !usefeat may not be used in PMs!")
        else:
            raise error

    @commands.command()
    @commands.guild_only()
    async def roll(self, ctx):
        character = ctx.author
        # ensures the command can only be used when combat is taking place. To prevent trolls from spamming commands
        if self.game == 1:
            # ensures the command can only be used by player one, when it is their turn. To prevent trolls from
            # spamming commands.
            if character == self.pOneUsername and self.token == 1:

                # assign both player's feat selections to variables
                pOneFeatUsed = self.pOneFeatInfo
                pTwoFeatUsed = self.pTwoFeatInfo

                # If a feat wasn't used by a player, assign it default values.
                if pOneFeatUsed is None:
                    pOneFeatUsed = ["none", 0]
                if pTwoFeatUsed is None:
                    pTwoFeatUsed = ["none", 0]

                # If the feat used was 'true strike' forgo rolling to see if player hit opponent, and go
                # straight to damage.
                if pOneFeatUsed[0] == "true strike":
                    await ctx.send( self.pOneInfo['name'] +
                                " used the feat 'True Strike.' And forgoes the need to determine if hit was success.")

                    # Obtain Player One's base damage and base modifier, and roll damage. Assign 'power attack' and 'combat defense'
                    # modifiers to variables, and roll damage.
                    pOneBaseDamage = self.pOneInfo['base damage']
                    pOneModifier = self.pOneInfo['damage']
                    pOneMinimum, pOneMaximum = pOneBaseDamage.split('d')
                    pMod = self.pOnepMod
                    cMod = self.pOnecMod
                    damage = random.randint(int(pOneMinimum), int(pOneMaximum))
                    # if critical counter is a value of 1, double the damage done, then reset counter to 0.
                    if self.critical == 1:
                        damage = damage * 2
                        self.critical = 0
                    # if Player One used feat 'titan blow', apply 50% bonus damage.
                    if pOneFeatUsed[0] == "titan blow":
                        await ctx.send( self.pOneInfo['name'] + " used the feat 'titan blow'.")
                        damage = damage * float(pOneFeatUsed[1])
                    # if Player Two use 'staggering blow' half damage done.
                    if pTwoFeatUsed[0] == "staggering blow":
                        await ctx.send(
                                    self.pTwoInfo['name'] + " used the feat 'staggering blow', halving " +
                                    self.pOneInfo['name'] + "'s damage roll")
                        damage = damage * float(pTwoFeatUsed[1])
                    # ensure that no matter what, raw damage can not fall below 1, then assign total damage to variable, and in turn
                    # assign it to variable to be accessed for scoreboard.
                    if damage < 1:
                        damage = 1
                    total = int(damage + pOneModifier + pMod - cMod)
                    # if Player Two used 'quick strike', 'improved quick strike', or 'greater quick strike', apply the return
                    # damage here
                    pTwoBaseDamage = self.pTwoInfo['base damage']
                    pTwoModifier = self.pTwoInfo['damage']
                    pTwoMinimum, pTwoMaximum = pTwoBaseDamage.split('d')
                    pMod = self.pTwopMod
                    cMod = self.pTwocMod
                    # apply the damage from 'quick strike', 'improved quick strike', or 'greater quick strike' if such feats were
                    # used
                    if pTwoFeatUsed[0] == "quick strike":
                        # Roll damage for Player One, and multiply it by desired amount.
                        damage = random.randint(int(pTwoMinimum), int(pTwoMaximum))
                        total = (damage + pTwoModifier + pMod - cMod)
                        quickDamage = int(total * float(pTwoFeatUsed[1]))
                        # Ensure damage is always at least 1hp and print out result
                        if quickDamage < 1:
                            quickDamage = 1
                        self.pTwoQuickDamage = quickDamage
                        self.pOneCurrentHP = self.pOneCurrentHP - self.pTwoQuickDamage
                        await ctx.send(self.pTwoInfo['name'] + " used 'quick strike,' managing to do an additional "
                                       + str(self.pTwoQuickDamage) + "hp of damage.")
                    elif pTwoFeatUsed[0] == "improved quick strike":
                        # Roll damage for Player one, and multiply it by desired amount.
                        damage = random.randint(int(pTwoMinimum), int(pTwoMaximum))
                        total = (damage + pTwoModifier + pMod - cMod)
                        quickDamage = int(total * float(pTwoFeatUsed[1]))
                        # Ensure damage is always at least 1hp and print out result
                        if quickDamage < 1:
                            quickDamage = 1
                        self.pTwoQuickDamage = quickDamage
                        self.pOneCurrentHP = self.pOneCurrentHP - self.pTwoQuickDamage
                        await ctx.send(self.pTwoInfo['name'] + " used 'quick strike,' managing to do an additional "
                                       + str(self.pTwoQuickDamage) + "hp of damage.")
                    elif pTwoFeatUsed[0] == "greater quick strike":
                        # roll damage for player One, and multiply it by desired amount
                        damage = random.randint(int(pTwoMinimum), int(pTwoMaximum))
                        total = (damage + pTwoModifier + pMod - cMod)
                        quickDamage = int(total * float(pTwoFeatUsed[1]))
                        # Ensure damage is always at least 1hp and print out result
                        if quickDamage < 1:
                            quickDamage = 1
                        self.pTwoQuickDamage = quickDamage
                        self.pOneCurrentHP = self.pOneCurrentHP - self.pTwoQuickDamage
                        await ctx.send(self.pTwoInfo['name'] + " used 'quick strike,' managing to do an additional "
                                       + str(self.pTwoQuickDamage) + "hp of damage.")
                    elif pTwoFeatUsed[0] == "riposte":
                        # roll damage for player One, and multiply it by desired amount
                        damage = random.randint(int(pTwoMinimum), int(pTwoMaximum))
                        total = (damage + pTwoModifier + pMod - cMod)
                        quickDamage = int(total * float(pTwoFeatUsed[1][0]))
                        # Ensure damage is always at least 1hp and print out result
                        if quickDamage < 1:
                            quickDamage = 1
                        self.pTwoQuickDamage = quickDamage
                        self.pOneCurrentHP = self.pOneCurrentHP - self.pTwoQuickDamage
                        await ctx.send(self.pTwoInfo['name'] + " used 'quick strike,' managing to do an additional "
                                       + str(self.pTwoQuickDamage) + "hp of damage.")
                        self.pTwoRiposte = 1
                    # # If Player Two has Evasion, Improved Evasion, or Greater Evasion, give them the option to use it.

                    for word in self.pTwoInfo['feats taken']:

                        answer = ""
                        if self.pTwoEvade == 1 and word == "evasion":
                            while answer != "yes" and answer != "no":
                                answer = await ctx.send(
                                    self.pTwoInfo['name'] + ", do you wish to evade? ").lower()
                                if answer == "yes" and character == self.pTwoUsername:
                                    total = int(total * 0.75)
                                    self.totalDamage = total
                                    self.pTwoEvade = 0
                                elif answer == "no" and character == self.pTwoUsername:
                                    pass
                                else:
                                    await ctx.send("You aren't " + self.pTwoUsername )
                    #     elif self.pTwoEvade == 1 and word == "improved evasion":
                    #         while answer != "yes" and answer != "no":
                    #             answer = await ctx.send(
                    #                 self.pTwoInfo['name'] + ", do you wish to evade? ").lower()
                    #             if answer == "yes":
                    #                 total = int(total * 0.5)
                    #                 self.totalDamage = total
                    #                 self.pTwoEvade = 0
                    #             elif answer == "no":
                    #                 pass
                    #             else:
                    #                 await ctx.send("Answer 'yes' or 'no'")
                    #     elif self.pTwoEvade == 1 and word == "greater evasion":
                    #         while answer != "yes" and answer != "no":
                    #             answer = await ctx.send(
                    #                 self.pTwoInfo['name'] + ", do you wish to evade? ").lower()
                    #             if answer == "yes":
                    #                 total = 0
                    #                 self.totalDamage = total
                    #                 self.pTwoEvade = 0
                    #             elif answer == "no":
                    #                 pass
                    #             else:
                    #                 await ctx.send("Answer 'yes' or 'no'")
                    # If Player Two used 'async deflect', 'improved async deflect', or 'greater async deflect', apply damage mitigation here
                    if pTwoFeatUsed[0] == "deflect":
                        await ctx.send( self.pTwoInfo['name'] + " used async deflect to lessen the blow.")
                        total = int(total * float(pTwoFeatUsed[1]))
                    elif pTwoFeatUsed[0] == "improved deflect":
                        await ctx.send( self.pTwoInfo['name'] + " used async deflect to lessen the blow")
                        total = int(total * float(pTwoFeatUsed[1]))
                    elif pTwoFeatUsed[0] == "greater deflect":
                        await ctx.send( self.pTwoInfo['name'] + " used deflect to lessen the blow")
                        total = int(total * float(pTwoFeatUsed[1]))
                    self.totalDamage = total
                    # testing data to see that modifiers are carrying over correctly. Delete this when project is finished.
                    await ctx.send("Roll: " + str(damage) + " Modifier: " + str(pOneModifier) + " PA: " + str(
                                    pMod) + " CE: " + str(cMod))
                    # display total damage done, and reset passive feat counters (power attack and combat defense)
                    await ctx.send(self.pOneInfo['name'] + " did " + str(total) + " points of damage.")
                    self.pOnepMod = 0
                    self.pOnecMod = 0
                    self.token = 2

                # Otherwise, continue on with the bulk of this method.
                else:
                    pOneToHit = self.pOneInfo['hit']
                    pTwoAC = self.pTwoInfo['ac']

                    pMod = self.pOnepMod
                    cMod = self.pOnecMod
                    dMod = self.pOnedMod
                    mMod = self.pOnemMod
                    pTwodMod = self.pTwodMod
                    pTwomMod = self.pTwomMod

                    hit = random.randint(1, 20)

                    # if the raw result is equal to 20, count the critical counter up to 1.
                    if hit == 20:
                        self.critical = 1
                        await ctx.send( self.pOneInfo['name'] + " has critically hit.")

                    # Notify that Player One is getting the hit benefit from 'riposte'
                    if self.pOneRiposte == 5:
                        await ctx.send( self.pOneInfo['name'] +
                                    " benefits from +5 hit bonus effect from riposte.")

                    # calculate the total after modifiers
                    total = int(hit + pOneToHit - pMod + cMod - dMod + mMod + self.pOneRiposte)

                    # Ensures Player One benefits from hit bonus of Riposte only once.
                    self.pOneRiposte = 0

                    # if any version of crippling blow was used, tack on the penalty to the above total
                    if pTwoFeatUsed[0] == "crippling blow" or pTwoFeatUsed[0] == "improved crippling blow" or \
                            pTwoFeatUsed[0] == "greater crippling blow":
                        await ctx.send(self.pTwoInfo['name'] + " Used " + str(pTwoFeatUsed[0]) + ", Giving "
                                       + self.pOneInfo['name'] + " a " + str(pTwoFeatUsed[1]) + " To their attack.")
                        total = total + pTwoFeatUsed[1]

                    # testing data to see that modifiers are carrying over correctly. Comment out
                    # when project is finished.
                    await ctx.send("Roll: " + str(hit) + " Base: " + str(pOneToHit) + " PA: "
                                    + str(pMod) + " CE: " + str(cMod) + " DF: " + str(dMod) + " MC: " + str(mMod))

                    # find Player One's total AC
                    totalAC = pTwoAC + pTwodMod - pTwomMod

                    # testing data to see that modifiers are carrying over correctly. Delete this when project is finished.
                    await ctx.send("P2 AC: " + str(pTwoAC) + " DF: " + str(pTwodMod) + " MC: " + str(pTwomMod))

                    # determine if the total roll, after all modifiers have been included, is a successful hit or not. then
                    # head to the appropriate method
                    if total >= totalAC:
                        await ctx.send(self.pOneInfo['name'] + " rolled a " + str(total) + " to hit an AC " + str(
                                       totalAC) + " and was successful.")
                        self.pTwodMod = 0
                        self.pTwomMod = 0
                        self.pTwoRiposte = 0

                        # Obtain Player One's base damage and base modifier, and roll damage. Assign 'power attack' and 'combat defense'
                        # modifiers to variables, and roll damage.
                        pOneBaseDamage = self.pOneInfo['base damage']
                        pOneModifier = self.pOneInfo['damage']
                        pOneMinimum, pOneMaximum = pOneBaseDamage.split('d')
                        pMod = self.pOnepMod
                        cMod = self.pOnecMod
                        damage = random.randint(int(pOneMinimum), int(pOneMaximum))
                        # if critical counter is a value of 1, double the damage done, then reset counter to 0.
                        if self.critical == 1:
                            damage = damage * 2
                            self.critical = 0
                        # if Player One used feat 'titan blow', apply 50% bonus damage.
                        if pOneFeatUsed[0] == "titan blow":
                            await ctx.send( self.pOneInfo['name'] + " used the feat 'titan blow'.")
                            damage = damage * float(pOneFeatUsed[1])
                        # if Player Two use 'staggering blow' half damage done.
                        if pTwoFeatUsed[0] == "staggering blow":
                            await ctx.send(self.pTwoInfo['name'] + " used the feat 'staggering blow', halving "
                                           + self.pOneInfo['name'] + "'s damage roll")
                            damage = damage * float(pTwoFeatUsed[1])
                        # ensure that no matter what, raw damage can not fall below 1, then assign total damage to variable, and in turn
                        # assign it to variable to be accessed for scoreboard.
                        if damage < 1:
                            damage = 1
                        total = int(damage + pOneModifier + pMod - cMod)
                        # if Player Two used 'quick strike', 'improved quick strike', or 'greater quick strike', apply the return
                        # damage here
                        pTwoBaseDamage = self.pTwoInfo['base damage']
                        pTwoModifier = self.pTwoInfo['damage']
                        pTwoMinimum, pTwoMaximum = pTwoBaseDamage.split('d')
                        pMod = self.pTwopMod
                        cMod = self.pTwocMod
                        # apply the damage from 'quick strike', 'improved quick strike', or 'greater quick strike' if such feats were
                        # used
                        if pTwoFeatUsed[0] == "quick strike":
                            # Roll damage for Player One, and multiply it by desired amount.
                            damage = random.randint(int(pTwoMinimum), int(pTwoMaximum))
                            total = (damage + pTwoModifier + pMod - cMod)
                            quickDamage = int(total * float(pTwoFeatUsed[1]))
                            # Ensure damage is always at least 1hp and print out result
                            if quickDamage < 1:
                                quickDamage = 1
                            self.pTwoQuickDamage = quickDamage
                            self.pOneCurrentHP = self.pOneCurrentHP - self.pTwoQuickDamage
                            await ctx.send(self.pTwoInfo['name'] + " used 'quick strike,' managing to do an additional "
                                           + str(self.pTwoQuickDamage) + "hp of damage.")
                        elif pTwoFeatUsed[0] == "improved quick strike":
                            # Roll damage for Player one, and multiply it by desired amount.
                            damage = random.randint(int(pTwoMinimum), int(pTwoMaximum))
                            total = (damage + pTwoModifier + pMod - cMod)
                            quickDamage = int(total * float(pTwoFeatUsed[1]))
                            # Ensure damage is always at least 1hp and print out result
                            if quickDamage < 1:
                                quickDamage = 1
                            self.pTwoQuickDamage = quickDamage
                            self.pOneCurrentHP = self.pOneCurrentHP - self.pTwoQuickDamage
                            await ctx.send(self.pTwoInfo['name'] + " used 'quick strike,' managing to do an additional "
                                           + str(self.pTwoQuickDamage) + "hp of damage.")
                        elif pTwoFeatUsed[0] == "greater quick strike":
                            # roll damage for player One, and multiply it by desired amount
                            damage = random.randint(int(pTwoMinimum), int(pTwoMaximum))
                            total = (damage + pTwoModifier + pMod - cMod)
                            quickDamage = int(total * float(pTwoFeatUsed[1]))
                            # Ensure damage is always at least 1hp and print out result
                            if quickDamage < 1:
                                quickDamage = 1
                            self.pTwoQuickDamage = quickDamage
                            self.pOneCurrentHP = self.pOneCurrentHP - self.pTwoQuickDamage
                            await ctx.send(self.pTwoInfo['name'] + " used 'quick strike,' managing to do an additional "
                                           + str(self.pTwoQuickDamage) + "hp of damage.")
                        elif pTwoFeatUsed[0] == "riposte":
                            # roll damage for player One, and multiply it by desired amount
                            damage = random.randint(int(pTwoMinimum), int(pTwoMaximum))
                            total = (damage + pTwoModifier + pMod - cMod)
                            quickDamage = int(total * float(pTwoFeatUsed[1][0]))
                            # Ensure damage is always at least 1hp and print out result
                            if quickDamage < 1:
                                quickDamage = 1
                            self.pTwoQuickDamage = quickDamage
                            self.pOneCurrentHP = self.pOneCurrentHP - self.pTwoQuickDamage
                            await ctx.send(self.pTwoInfo['name'] + " used 'quick strike,' managing to do an additional "
                                           + str(self.pTwoQuickDamage) + "hp of damage.")
                        # # If Player Two has Evasion, Improved Evasion, or Greater Evasion, give them the option to use it.

                        for word in self.pTwoInfo['feats taken']:

                            answer = ""
                            if self.pTwoEvade == 1 and word == "evasion":
                                while answer != "yes" and answer != "no":
                                    answer = await ctx.send(
                                        self.pTwoInfo['name'] + ", do you wish to evade? ").lower()
                                    if answer == "yes" and character == self.pTwoUsername:
                                        total = int(total * 0.75)
                                        self.totalDamage = total
                                        self.pTwoEvade = 0
                                    elif answer == "no" and character == self.pTwoUsername:
                                        pass
                                    else:
                                        await ctx.send("You aren't " + self.pTwoUsername)
                        #     elif self.pTwoEvade == 1 and word == "improved evasion":
                        #         while answer != "yes" and answer != "no":
                        #             answer = await ctx.send(
                        #                 self.pTwoInfo['name'] + ", do you wish to evade? ").lower()
                        #             if answer == "yes":
                        #                 total = int(total * 0.5)
                        #                 self.totalDamage = total
                        #                 self.pTwoEvade = 0
                        #             elif answer == "no":
                        #                 pass
                        #             else:
                        #                 await ctx.send("Answer 'yes' or 'no'")
                        #     elif self.pTwoEvade == 1 and word == "greater evasion":
                        #         while answer != "yes" and answer != "no":
                        #             answer = await ctx.send(
                        #                 self.pTwoInfo['name'] + ", do you wish to evade? ").lower()
                        #             if answer == "yes":
                        #                 total = 0
                        #                 self.totalDamage = total
                        #                 self.pTwoEvade = 0
                        #             elif answer == "no":
                        #                 pass
                        #             else:
                        #                 await ctx.send("Answer 'yes' or 'no'")
                        # If Player Two used 'async deflect', 'improved async deflect', or 'greater async deflect', apply damage mitigation here
                        if pTwoFeatUsed[0] == "deflect":
                            await ctx.send( self.pTwoInfo['name'] + " used deflect to lessen the blow.")
                            total = int(total * float(pTwoFeatUsed[1]))
                        elif pTwoFeatUsed[0] == "improved deflect":
                            await ctx.send( self.pTwoInfo['name'] + " used deflect to lessen the blow")
                            total = int(total * float(pTwoFeatUsed[1]))
                        elif pTwoFeatUsed[0] == "greater deflect":
                            await ctx.send( self.pTwoInfo['name'] + " used deflect to lessen the blow")
                            total = int(total * float(pTwoFeatUsed[1]))
                        self.totalDamage = total
                        # testing data to see that modifiers are carrying over correctly. Delete this when project is finished.
                        await ctx.send("Roll: " + str(damage) + " Modifier: " + str(pOneModifier) + " PA: "
                                       + str(pMod) + " CD: " + str(cMod))
                        # display total damage done, and reset passive feat counters (power attack and combat defense)
                        await ctx.send(self.pOneInfo['name'] + " did " + str(total) + " points of damage.")
                        self.pOnepMod = 0
                        self.pOnecMod = 0
                        self.token = 2
                    else:
                        await ctx.send( self.pOneInfo['name'] + " rolled a " + str(total) + " to hit an AC " + str(
                            totalAC) + " and missed.")
                        self.pTwodMod = 0
                        self.pTwomMod = 0
                        self.token = 2

                        if pTwoFeatUsed[0] == "riposte":
                            self.pTwoRiposte = 5

                # Determine HP at end of round.
                if self.pTwoQuickDamage != 0:
                    self.pTwoCurrentHP = self.pTwoCurrentHP - self.totalDamage - self.pOneQuickDamage
                    self.pOneQuickDamage = 0
                    self.count += 1
                else:
                    self.pTwoCurrentHP = self.pTwoCurrentHP - self.totalDamage

                # Print the scoreboard.
                await ctx.send( self.pOneInfo['name'] + ": " + str(self.pOneCurrentHP) + "/" + str(
                    self.pOneTotalHP) + "  ||  " + self.pTwoInfo['name'] + ": " + str(
                    self.pTwoCurrentHP) + "/" + str(self.pTwoTotalHP) + " \n" +
                            self.pTwoInfo['name'] + "'s turn. Type: !usefeat <feat> if you wish to use a feat.")

                # If Player Two is dead, state such, and how many rounds it took to win. Calculate and distribute xp.
                # reset game and token counters back to 0.
                if self.pTwoCurrentHP <= 0:
                    self.game = 0
                    self.token = 0
                    await ctx.send( self.pOneInfo['name'] + " won in " + str(int(self.count / 2)) + " rounds")
                    level = abs(self.pOneLevel - self.pTwoLevel)
                    if level == 0:
                        level = 1
                    if level <= 3:
                        levelDiff = level * self.pOneLevel
                        differHP = abs(self.pOneCurrentHP - self.pTwoCurrentHP)
                        self.xp = 10 * levelDiff + differHP
                        await ctx.send(self.pOneInfo['name'] + " has earned: " + str(self.xp) + " experience points.")
                    elif 3 > level < 6:
                        levelDiff = level * self.pOneLevel
                        differHP = abs(self.pOneCurrentHP - self.pTwoCurrentHP)
                        self.xp = 7 * levelDiff + differHP
                        await ctx.send(self.pOneInfo['name'] + " has earned: " + str(self.xp) + " experience points.")
                    elif 7 > level < 10:
                        levelDiff = level * self.pOneLevel
                        differHP = abs(self.pOneCurrentHP - self.pTwoCurrentHP)
                        self.xp = 5 * levelDiff + differHP
                        await ctx.send(
                                    self.pOneInfo['name'] + " has earned: " + str(self.xp) + " experience points.")
                    else:
                        await ctx.send( "As the level difference was greater than 10, no XP was awarded.")
                    await ctx.send( self.pOneInfo['name'] + " has earned: " + str(self.xp) + " experience points.")
                    self.currentPlayerXP = self.pOneInfo['currentxp'] + self.xp
                    self.nextLevel = self.pOneInfo['nextlevel']
                    self.winner = self.pOneUsername
                    self.loser = self.pTwoUsername
                    self.levelUp = self.pOneInfo['level']
                    path = os.getcwd()
                    charFolder = os.path.join(path + "/characters/")

                    with open(charFolder + self.winner + '.txt', 'r+') as file:
                        charData = json.load(file)
                        charData['currentxp'] = self.currentPlayerXP
                        charData['wins'] += 1
                        file.seek(0)
                        file.write(json.dumps(charData, ensure_ascii=False, indent=2))
                        file.truncate()
                        file.close()

                    with open(charFolder + self.loser + '.txt', 'r+') as file:
                        charData = json.load(file)
                        charData['losses'] += 1
                        file.seek(0)
                        file.write(json.dumps(charData, ensure_ascii=False, indent=2))
                        file.truncate()
                        file.close()
                    if self.currentPlayerXP >= self.nextLevel:
                        newLevel = self.levelUp + 1
                        newLevel = str(newLevel)
                        await ctx.send( self.winner.capitalize() + " has reached level " + newLevel + "!")
                        levelFile = open(charFolder + "levelchart.txt", "r", encoding="utf-8")
                        levelDict = json.load(levelFile)
                        levelFile.close()
                        with open(charFolder + self.winner + '.txt', 'r+') as file:
                            charData = json.load(file)
                            charData['level'] = int(newLevel)
                            charData['hitpoints'] = int(levelDict[newLevel][0])
                            charData['base damage'] = str(levelDict[newLevel][1]) + "d" + str(
                                levelDict[newLevel][2])
                            if charData['total feats'] == levelDict[newLevel][4]:
                                charData['total feats'] = levelDict[newLevel][4]
                            else:
                                await ctx.send("You have a new feat slot to fill. Use the !feat command to select new feat.")
                                charData['total feats'] = levelDict[newLevel][4]
                                charData['remaining feats'] = 1
                            if charData['total ap'] == levelDict[newLevel][3]:
                                charData['total ap'] = levelDict[newLevel][3]
                            else:
                                await ctx.send("You have a new ability point to spend. the !add command.")
                            charData['hit'] = int(levelDict[newLevel][5])
                            charData['damage modifier'] = int(levelDict[newLevel][5])
                            charData['ac'] = int(levelDict[newLevel][6])
                            charData['currentxp'] = int(self.currentPlayerXP)
                            charData['nextlevel'] = int(levelDict[newLevel][7])
                            file.seek(0)
                            file.write(json.dumps(charData, ensure_ascii=False, indent=2))
                            file.truncate()
                            file.close()

                    else:
                        pass
            # ensures the command can only be used by player two, when it is their turn. To prevent trolls from
            # spamming commands.
            elif character == self.pTwoUsername and self.token == 2:

                # assign both player's feat selections to variables
                pOneFeatUsed = self.pOneFeatInfo
                pTwoFeatUsed = self.pTwoFeatInfo

                # If a feat wasn't used by a player, assign it async default values.
                if pOneFeatUsed is None:
                    pOneFeatUsed = ["none", 0]
                if pTwoFeatUsed is None:
                    pTwoFeatUsed = ["none", 0]

                # If the feat used was 'true strike' forgo rolling to see if player hit opponent, and go straight to damage.
                if pTwoFeatUsed[0] == "true strike":
                    await ctx.send( self.pTwoInfo['name'] +
                                " used the feat 'True Strike.' And forgoes the need to determine if hit was success.")

                    # Obtain Player Two's base damage and base modifier, and roll damage. Assign 'power attack' and 'combat defense'
                    # modifiers to variables, and roll damage.
                    pTwoBaseDamage = self.pTwoInfo['base damage']
                    pTwoModifier = self.pTwoInfo['damage']
                    pTwoMinimum, pTwoMaximum = pTwoBaseDamage.split('d')
                    pMod = self.pTwopMod
                    cMod = self.pTwocMod
                    damage = random.randint(int(pTwoMinimum), int(pTwoMaximum))
                    # if critical counter is a value of 1, double the damage done, then reset counter to 0.
                    if self.critical == 1:
                        damage = damage * 2
                        self.critical = 0
                    # if Player Two used feat 'titan blow', apply 50% bonus damage.
                    if pTwoFeatUsed[0] == "titan blow":
                        await ctx.send( self.pTwoInfo['name'] + " used the feat 'titan blow'.")
                        damage = damage * float(pTwoFeatUsed[1])
                    # if Player One use 'staggering blow' half damage done.
                    if pOneFeatUsed[0] == "staggering blow":
                        await ctx.send(
                                    self.pOneInfo['name'] + " used the feat 'staggering blow', halving " +
                                    self.pTwoInfo['name'] + "'s damage roll")
                        damage = damage * float(pOneFeatUsed[1])
                    # ensure that no matter what, raw damage can not fall below 1, then assign total damage to variable, and in turn
                    # assign it to variable to be accessed for scoreboard.
                    if damage < 1:
                        damage = 1
                    total = int(damage + pTwoModifier + pMod - cMod)
                    # if Player One used 'quick strike', 'improved quick strike', or 'greater quick strike', apply the return
                    # damage here
                    pOneBaseDamage = self.pOneInfo['base damage']
                    pOneModifier = self.pOneInfo['damage']
                    pOneMinimum, pOneMaximum = pOneBaseDamage.split('d')
                    pMod = self.pOnepMod
                    cMod = self.pOnecMod
                    # apply the damage from 'quick strike', 'improved quick strike', or 'greater quick strike' if such feats were
                    # used
                    if pOneFeatUsed[0] == "quick strike":
                        # Roll damage for Player One, and multiply it by desired amount.
                        damage = random.randint(int(pOneMinimum), int(pOneMaximum))
                        total = (damage + pOneModifier + pMod - cMod)
                        quickDamage = int(total * float(pOneFeatUsed[1]))
                        # Ensure damage is always at least 1hp and print out result
                        if quickDamage < 1:
                            quickDamage = 1
                        self.pOneQuickDamage = quickDamage
                        self.pTwoCurrentHP = self.pTwoCurrentHP - self.pOneQuickDamage
                        await ctx.send(
                                    self.pOneInfo[
                                        'name'] + " used 'quick strike,' managing to do an additional " + str(
                                        self.pOneQuickDamage) + "hp of damage.")
                    if pOneFeatUsed[0] == "improved quick strike":
                        # Roll damage for Player one, and multiply it by desired amount.
                        damage = random.randint(int(pOneMinimum), int(pOneMaximum))
                        total = (damage + pOneModifier + pMod - cMod)
                        quickDamage = int(total * float(pOneFeatUsed[1]))
                        # Ensure damage is always at least 1hp and print out result
                        if quickDamage < 1:
                            quickDamage = 1
                        self.pOneQuickDamage = quickDamage
                        self.pTwoCurrentHP = self.pTwoCurrentHP - self.pOneQuickDamage
                        await ctx.send(
                                    self.pOneInfo[
                                        'name'] + " used 'quick strike,' managing to do an additional " + str(
                                        self.pOneQuickDamage) + "hp of damage.")
                    if pOneFeatUsed[0] == "greater quick strike":
                        # roll damage for player One, and multiply it by desired amount
                        damage = random.randint(int(pOneMinimum), int(pOneMaximum))
                        total = (damage + pOneModifier + pMod - cMod)
                        quickDamage = int(total * float(pOneFeatUsed[1]))
                        # Ensure damage is always at least 1hp and print out result
                        self.pOneQuickDamage = quickDamage
                        self.pTwoCurrentHP = self.pTwoCurrentHP - self.pOneQuickDamage
                        await ctx.send(
                                    self.pOneInfo[
                                        'name'] + " used 'quick strike,' managing to do an additional " + str(
                                        self.pOneQuickDamage) + "hp of damage.")
                    elif pOneFeatUsed[0] == "riposte":
                        # roll damage for player One, and multiply it by desired amount
                        damage = random.randint(int(pOneMinimum), int(pOneMaximum))
                        total = (damage + pOneModifier + pMod - cMod)
                        quickDamage = int(total * float(pOneFeatUsed[1][0]))
                        # Ensure damage is always at least 1hp and print out result
                        if quickDamage < 1:
                            quickDamage = 1
                        self.pOneQuickDamage = quickDamage
                        self.pTwoCurrentHP = self.pTwoCurrentHP - self.pTwoQuickDamage
                        await ctx.send(
                                    self.pOneInfo[
                                        'name'] + " used 'quick strike,' managing to do an additional " + str(
                                        self.pOneQuickDamage) + "hp of damage.")
                        self.pOneRiposte = 1
                    # If Player One has Evasion, Improved Evasion, or Greater Evasion, give them the option to use it.
                    # for word in self.pOneInfo['feats taken']:
                    #     answer = ""
                    #     if self.pOneEvade == 1 and word == "evasion":
                    #         while answer != "yes" and answer != "no":
                    #             answer = await ctx.send(
                    #                 self.pOneInfo['name'] + ", do you wish to evade? ").lower()
                    #             if answer == "yes":
                    #                 total = int(total * 0.5)
                    #                 self.totalDamage = total
                    #                 self.pTwoEvade = 0
                    #             elif answer == "no":
                    #                 pass
                    #             else:
                    #                 await ctx.send("Answer 'yes' or 'no'")
                    #     elif self.pOneEvade == 1 and word == "improved evasion":
                    #         while answer != "yes" and answer != "no":
                    #             answer = await ctx.send(
                    #                 self.pOneInfo['name'] + ", do you wish to evade? ").lower()
                    #             if answer == "yes":
                    #                 total = int(total * 0.5)
                    #                 self.totalDamage = total
                    #                 self.pTwoEvade = 0
                    #             elif answer == "no":
                    #                 pass
                    #             else:
                    #                 await ctx.send("Answer 'yes' or 'no'")
                    #     elif self.pOneEvade == 1 and word == "greater evasion":
                    #         while answer != "yes" and answer != "no":
                    #             answer = await ctx.send(
                    #                 self.pTwoInfo['name'] + ", do you wish to evade? ").lower()
                    #             if answer == "yes":
                    #                 total = int(total * 0.5)
                    #                 self.totalDamage = total
                    #                 self.pTwoEvade = 0
                    #             elif answer == "no":
                    #                 pass
                    #             else:
                    #                 await ctx.send("Answer 'yes' or 'no'")
                    # If Player One used 'deflect', 'improved async deflect', or 'greater async deflect', apply damage mitigation here
                    if pOneFeatUsed[0] == "deflect":
                        await ctx.send( self.pOneInfo['name'] + " used async deflect to lessen the blow.")
                        total = int(total * float(pOneFeatUsed[1]))
                    elif pOneFeatUsed[0] == "improved deflect":
                        await ctx.send( self.pOneInfo['name'] + " used async deflect to lessen the blow")
                        total = int(total * float(pOneFeatUsed[1]))
                    elif pOneFeatUsed[0] == "greater deflect":
                        await ctx.send( self.pOneInfo['name'] + " used async deflect to lessen the blow")
                        await ctx.send( pOneFeatUsed[1])
                        await ctx.send( total)
                        total = int(total * float(pOneFeatUsed[1]))
                        await ctx.send( total)
                    self.totalDamage = total
                    # testing data to see that modifiers are carrying over correctly. Delete this when project is finished.
                    await ctx.send(
                                "Roll: " + str(damage) + " Modifier: " + str(pTwoModifier) + " PA: " + str(
                                    pMod) + " CD: " + str(cMod))
                    # display total damage done, and reset passive feat counters (power attack and combat defense).
                    await ctx.send( self.pTwoInfo['name'] + " did " + str(total) + " points of damage.")
                    self.pTwopMod = 0
                    self.pTwocMod = 0
                    self.token = 1

                # Otherwise, continue on with the bulk of this method.
                else:
                    pTwoToHit = self.pTwoInfo['hit']
                    pOneAC = self.pOneInfo['ac']

                    pMod = self.pTwopMod
                    cMod = self.pTwocMod
                    dMod = self.pTwodMod
                    mMod = self.pTwomMod
                    pOnedMod = self.pOnedMod
                    pOnemMod = self.pOnemMod

                    # determine the roll of the 1d20.
                    hit = random.randint(1, 20)

                    # if the raw result is equal to 20, count the critical counter up to 1.
                    if hit == 20:
                        self.critical = 1
                        await ctx.send( self.pTwoInfo['name'] + " has critically hit.")

                    if self.pTwoRiposte == 5:
                        await ctx.send(
                                    self.pTwoInfo['name'] + "Benefits from +5 hit bonus effect from riposte.")

                    # calculate the total after modifiers
                    total = int(hit + pTwoToHit - pMod + cMod - dMod + mMod + self.pTwoRiposte)

                    # Ensures Player Two benefits from hit bonus of Riposte only once.
                    self.pTwoRiposte = 0

                    # if Player Two used riposte, and
                    # if any version of crippling blow was used, tack on the penalty to the above total
                    if pOneFeatUsed[0] == "crippling blow" or pOneFeatUsed[0] == "improved crippling blow" or \
                            pOneFeatUsed[0] == "greater crippling blow":
                        await ctx.send(
                                    self.pOneInfo['name'] + " Used " + str(pOneFeatUsed[0]) + ", Giving " + self.pTwoInfo[
                                        'name'] + " a " + str(pOneFeatUsed[1]) + " To their attack.")
                        total = total + pOneFeatUsed[1]

                    # testing data to see that modifiers are carrying over correctly. Delete this when project is finished.
                    await ctx.send(
                                "Roll: " + str(hit) + " Base: " + str(pTwoToHit) + " PA: " + str(pMod) + " CE: " + str(
                                    cMod) + " DF: " + str(dMod) + " MC: " + str(mMod))

                    # find Player One's total AC
                    totalAC = int(pOneAC + pOnedMod - pOnemMod)

                    # testing data to see that modifiers are carrying over correctly. Delete this when project is finished.
                    await ctx.send( " P1 AC: " + str(pOneAC) + " DF: " + str(pOnedMod) + " MC: " + str(pOnemMod))

                    # determine if the total roll, after all modifiers have been included, is a successful hit or not. then
                    # head to the appropriate method
                    if total >= pOneAC:

                        await ctx.send(
                                    self.pTwoInfo['name'] + " rolled a " + str(total) + " to hit an AC " + str(
                                        totalAC) + " and was successful.")
                        self.pOnedMod = 0
                        self.pOnemMod = 0
                        self.pOneRiposte = 0

                        # Obtain Player Two's base damage and base modifier, and roll damage. Assign 'power attack' and 'combat defense'
                        # modifiers to variables, and roll damage.
                        pTwoBaseDamage = self.pTwoInfo['base damage']
                        pTwoModifier = self.pTwoInfo['damage']
                        pTwoMinimum, pTwoMaximum = pTwoBaseDamage.split('d')
                        pMod = self.pTwopMod
                        cMod = self.pTwocMod
                        damage = random.randint(int(pTwoMinimum), int(pTwoMaximum))
                        # if critical counter is a value of 1, double the damage done, then reset counter to 0.
                        if self.critical == 1:
                            damage = damage * 2
                            self.critical = 0
                        # if Player Two used feat 'titan blow', apply 50% bonus damage.
                        if pTwoFeatUsed[0] == "titan blow":
                            await ctx.send( self.pTwoInfo['name'] + " used the feat 'titan blow'.")
                            damage = damage * float(pTwoFeatUsed[1])
                        # if Player One use 'staggering blow' half damage done.
                        if pOneFeatUsed[0] == "staggering blow":
                            await ctx.send(
                                        self.pOneInfo['name'] + " used the feat 'staggering blow', halving " +
                                        self.pTwoInfo['name'] + "'s damage roll")
                            damage = damage * float(pOneFeatUsed[1])
                        # ensure that no matter what, raw damage can not fall below 1, then assign total damage to variable, and in turn
                        # assign it to variable to be accessed for scoreboard.
                        if damage < 1:
                            damage = 1
                        total = int(damage + pTwoModifier + pMod - cMod)
                        # if Player One used 'quick strike', 'improved quick strike', or 'greater quick strike', apply the return
                        # damage here
                        pOneBaseDamage = self.pOneInfo['base damage']
                        pOneModifier = self.pOneInfo['damage']
                        pOneMinimum, pOneMaximum = pOneBaseDamage.split('d')
                        pMod = self.pOnepMod
                        cMod = self.pOnecMod
                        # apply the damage from 'quick strike', 'improved quick strike', or 'greater quick strike' if such feats were
                        # used
                        if pOneFeatUsed[0] == "quick strike":
                            # Roll damage for Player One, and multiply it by desired amount.
                            damage = random.randint(int(pOneMinimum), int(pOneMaximum))
                            total = (damage + pOneModifier + pMod - cMod)
                            quickDamage = int(total * float(pOneFeatUsed[1]))
                            # Ensure damage is always at least 1hp and print out result
                            if quickDamage < 1:
                                quickDamage = 1
                            self.pOneQuickDamage = quickDamage
                            self.pTwoCurrentHP = self.pTwoCurrentHP - self.pOneQuickDamage
                            await ctx.send(
                                        self.pOneInfo['name'] + " used 'quick strike,' managing to do an additional " + str(
                                            self.pOneQuickDamage) + "hp of damage.")
                        if pOneFeatUsed[0] == "improved quick strike":
                            # Roll damage for Player one, and multiply it by desired amount.
                            damage = random.randint(int(pOneMinimum), int(pOneMaximum))
                            total = (damage + pOneModifier + pMod - cMod)
                            quickDamage = int(total * float(pOneFeatUsed[1]))
                            # Ensure damage is always at least 1hp and print out result
                            if quickDamage < 1:
                                quickDamage = 1
                            self.pOneQuickDamage = quickDamage
                            self.pTwoCurrentHP = self.pTwoCurrentHP - self.pOneQuickDamage
                            await ctx.send(
                                        self.pOneInfo['name'] + " used 'quick strike,' managing to do an additional " + str(
                                            self.pOneQuickDamage) + "hp of damage.")
                        if pOneFeatUsed[0] == "greater quick strike":
                            # roll damage for player One, and multiply it by desired amount
                            damage = random.randint(int(pOneMinimum), int(pOneMaximum))
                            total = (damage + pOneModifier + pMod - cMod)
                            quickDamage = int(total * float(pOneFeatUsed[1]))
                            # Ensure damage is always at least 1hp and print out result
                            self.pOneQuickDamage = quickDamage
                            self.pTwoCurrentHP = self.pTwoCurrentHP - self.pOneQuickDamage
                            await ctx.send(
                                        self.pOneInfo['name'] + " used 'quick strike,' managing to do an additional " + str(
                                            self.pOneQuickDamage) + "hp of damage.")
                        if pOneFeatUsed[0] == "riposte":
                            # roll damage for player One, and multiply it by desired amount
                            damage = random.randint(int(pOneMinimum), int(pOneMaximum))
                            total = (damage + pOneModifier + pMod - cMod)
                            quickDamage = int(total * float(pOneFeatUsed[1][0]))
                            # Ensure damage is always at least 1hp and print out result
                            if quickDamage < 1:
                                quickDamage = 1
                            self.pOneQuickDamage = quickDamage
                            self.pTwoCurrentHP = self.pTwoCurrentHP - self.pTwoQuickDamage
                            await ctx.send(
                                        self.pOneInfo['name'] + " used 'quick strike,' managing to do an additional " + str(
                                            self.pOneQuickDamage) + "hp of damage.")
                            self.pOneRiposte = 1
                        # If Player One has Evasion, Improved Evasion, or Greater Evasion, give them the option to use it.
                        # for word in self.pOneInfo['feats taken']:
                        #     answer = ""
                        #     if self.pOneEvade == 1 and word == "evasion":
                        #         while answer != "yes" and answer != "no":
                        #             answer = await ctx.send(
                        #                 self.pOneInfo['name'] + ", do you wish to evade? ").lower()
                        #             if answer == "yes":
                        #                 total = int(total * 0.5)
                        #                 self.totalDamage = total
                        #                 self.pTwoEvade = 0
                        #             elif answer == "no":
                        #                 pass
                        #             else:
                        #                 await ctx.send("Answer 'yes' or 'no'")
                        #     elif self.pOneEvade == 1 and word == "improved evasion":
                        #         while answer != "yes" and answer != "no":
                        #             answer = await ctx.send(
                        #                 self.pOneInfo['name'] + ", do you wish to evade? ").lower()
                        #             if answer == "yes":
                        #                 total = int(total * 0.5)
                        #                 self.totalDamage = total
                        #                 self.pTwoEvade = 0
                        #             elif answer == "no":
                        #                 pass
                        #             else:
                        #                 await ctx.send("Answer 'yes' or 'no'")
                        #     elif self.pOneEvade == 1 and word == "greater evasion":
                        #         while answer != "yes" and answer != "no":
                        #             answer = await ctx.send(
                        #                 self.pTwoInfo['name'] + ", do you wish to evade? ").lower()
                        #             if answer == "yes":
                        #                 total = int(total * 0.5)
                        #                 self.totalDamage = total
                        #                 self.pTwoEvade = 0
                        #             elif answer == "no":
                        #                 pass
                        #             else:
                        #                 await ctx.send("Answer 'yes' or 'no'")
                        # If Player One used 'deflect', 'improved async deflect', or 'greater async deflect', apply damage mitigation here
                        if pOneFeatUsed[0] == "deflect":
                            await ctx.send( self.pOneInfo['name'] + " used async deflect to lessen the blow.")
                            total = int(total * float(pOneFeatUsed[1]))
                        elif pOneFeatUsed[0] == "improved deflect":
                            await ctx.send( self.pOneInfo['name'] + " used async deflect to lessen the blow")
                            total = int(total * float(pOneFeatUsed[1]))
                        elif pOneFeatUsed[0] == "greater deflect":
                            await ctx.send( self.pOneInfo['name'] + " used async deflect to lessen the blow")
                            await ctx.send( pOneFeatUsed[1])
                            await ctx.send( total)
                            total = int(total * float(pOneFeatUsed[1]))
                            await ctx.send( total)
                        self.totalDamage = total
                        # testing data to see that modifiers are carrying over correctly. Delete this when project is finished.
                        await ctx.send(
                                    "Roll: " + str(damage) + " Modifier: " + str(pTwoModifier) + " PA: " + str(
                                        pMod) + " CD: " + str(cMod))
                        # display total damage done, and reset passive feat counters (power attack and combat defense).
                        await ctx.send( self.pTwoInfo['name'] + " did " + str(total) + " points of damage.")
                        self.pTwopMod = 0
                        self.pTwocMod = 0
                        self.token = 1
                    else:
                        await ctx.send(
                                    self.pTwoInfo['name'] + " rolled a " + str(total) + " to hit an AC " + str(
                                        totalAC) + " and missed.")
                        self.pOnedMod = 0
                        self.pOnemMod = 0
                        self.token = 1
                        if pOneFeatUsed[0] == "riposte":
                            self.pOneRiposte = 5

                # Determine HP at end of round.
                if self.pOneQuickDamage != 0:
                    self.pOneCurrentHP = self.pOneCurrentHP - self.totalDamage - self.pOneQuickDamage
                    self.pOneQuickDamage = 0
                    self.count += 1
                else:
                    self.pOneCurrentHP = self.pOneCurrentHP - self.totalDamage

                # Print the scoreboard
                await ctx.send( self.pOneInfo['name'] + ": " + str(self.pOneCurrentHP) + "/" +
                            str(self.pOneTotalHP) + "  ||  " + self.pTwoInfo['name'] + ": " +
                            str(self.pTwoCurrentHP) + "/" + str(self.pTwoTotalHP) + " \n" +
                            self.pOneInfo['name'] + "'s turn. Type: !usefeat <feat> if you wish to use a feat.")

                # If Player One is dead, state such, and how many rounds it took to win. Calculate and distribute xp.
                # reset game and token counters back to 0.
                if self.pOneCurrentHP <= 0:
                    self.game = 0
                    self.token = 0
                    await ctx.send( self.pTwoInfo['name'] + " won in " + str(int(self.count / 2)) + " rounds")
                    level = abs(self.pOneLevel - self.pTwoLevel)
                    if level == 0:
                        level = 1
                    if level <= 3:
                        levelDiff = level * self.pOneLevel
                        differHP = abs(self.pOneCurrentHP - self.pTwoCurrentHP)
                        self.xp = 10 * levelDiff + differHP

                    elif 3 > level < 6:
                        levelDiff = level * self.pOneLevel
                        differHP = abs(self.pOneCurrentHP - self.pTwoCurrentHP)
                        self.xp = 7 * levelDiff + differHP

                    elif 7 > level < 10:
                        levelDiff = level * self.pOneLevel
                        differHP = abs(self.pOneCurrentHP - self.pTwoCurrentHP)
                        self.xp = 5 * levelDiff + differHP

                    else:
                        await ctx.send( "As the level difference was greater than 10, no XP was awarded.")
                    await ctx.send( self.pTwoInfo['name'] + " has earned: " + str(self.xp) + " experience points.")
                    self.currentPlayerXP = self.pTwoInfo['currentxp'] + self.xp
                    self.nextLevel = self.pTwoInfo['nextlevel']
                    self.winner = self.pTwoUsername
                    self.loser = self.pOneUsername
                    self.levelUp = self.pTwoInfo['level']
                    path = os.getcwd()
                    charFolder = os.path.join(path + "/characters/")

                    with open(charFolder + self.winner + '.txt', 'r+') as file:
                        charData = json.load(file)
                        charData['currentxp'] = self.currentPlayerXP
                        charData['wins'] += 1
                        file.seek(0)
                        file.write(json.dumps(charData, ensure_ascii=False, indent=2))
                        file.truncate()
                        file.close()

                    with open(charFolder + self.loser + '.txt', 'r+') as file:
                        charData = json.load(file)
                        charData['losses'] += 1
                        file.seek(0)
                        file.write(json.dumps(charData, ensure_ascii=False, indent=2))
                        file.truncate()
                        file.close()

                    if self.currentPlayerXP >= self.nextLevel:
                        newLevel = self.levelUp + 1
                        newLevel = str(newLevel)
                        await ctx.send( self.winner.capitalize() + " has reached level " + newLevel + "!")
                        levelFile = open(charFolder + "levelchart.txt", "r", encoding="utf-8")
                        levelDict = json.load(levelFile)
                        levelFile.close()
                        with open(charFolder + self.winner + '.txt', 'r+') as file:
                            charData = json.load(file)
                            charData['level'] = int(newLevel)
                            charData['hitpoints'] = int(levelDict[newLevel][0])
                            charData['base damage'] = str(levelDict[newLevel][1]) + "d" + str(
                                levelDict[newLevel][2])
                            if charData['total feats'] == levelDict[newLevel][4]:
                                charData['total feats'] = levelDict[newLevel][4]
                            else:
                                await ctx.send(
                                    "You have a new feat slot to fill. Use the !feat command to select new feat.")
                                charData['total feats'] = levelDict[newLevel][4]
                                charData['remaining feats'] = 1
                            if charData['total ap'] == levelDict[newLevel][3]:
                                charData['total ap'] = levelDict[newLevel][3]
                            else:
                                await ctx.send("You have a new ability point to spend. the !add command.")
                            charData['hit'] = int(levelDict[newLevel][5])
                            charData['damage modifier'] = int(levelDict[newLevel][5])
                            charData['ac'] = int(levelDict[newLevel][6])
                            charData['currentxp'] = int(self.currentPlayerXP)
                            charData['nextlevel'] = int(levelDict[newLevel][7])
                            file.seek(0)
                            file.write(json.dumps(charData, ensure_ascii=False, indent=2))
                            file.truncate()
                            file.close()

                    else:
                        pass

            else:
                await ctx.send( "Either it's not your turn, or you aren't even fighting. Either way, No.")

        else:
            await ctx.send( "This command does nothing right now. No combat is taking place.")

    @roll.error
    async def name_roll(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("The command !roll may not be used in PMs!")
        else:
            raise error

    @commands.command()
    @commands.guild_only()
    async def pattack(self, ctx, *, message):
        character = ctx.author.send
        # make sure that this command cannot be ran if a fight is taking place.
        if self.game == 1:
            # ensures the command can only be used by player one, when it is their turn. To prevent trolls from
            # spamming commands.
            if character == self.playerOne and self.token == 1:
                mod = int(message)
                if self.pOneLevel <= 4 and mod == 1:
                    self.pOnepMod = 1
                elif 4 < self.pOneLevel <= 8 and mod == 2:
                    self.pOnepMod = 2
                elif 8 < self.pOneLevel <= 12 and mod == 3:
                    self.pOnepMod = 3
                elif 12 < self.pOneLevel <= 16 and mod == 4:
                    self.pOnepMod = 4
                elif 16 < self.pOneLevel <= 20 and mod == 5:
                    self.pOnepMod = 5
                else:
                    await ctx.send( "You are not high enough level to invest that many points.")
            # ensures the command can only be used by player two, when it is their turn. To prevent trolls from
            # spamming commands.
            elif character == self.playerTwo and self.token == 2:
                mod = int(message)
                if self.pTwoLevel <= 4 and mod == 1:
                    self.pTwopMod = 1
                elif 4 < self.pTwoLevel <= 8 and mod == 2:
                    self.pTwopMod = 2
                elif 8 < self.pTwoLevel <= 12 and mod == 3:
                    self.pTwopMod = 3
                elif 12 < self.pTwoLevel <= 16 and mod == 4:
                    self.pTwopMod = 4
                elif 16 < self.pTwoLevel <= 20 and mod == 5:
                    self.pTwopMod = 5
                else:
                    await ctx.send( "You are not high enough level to invest that many points.")

            else:
                await ctx.send( "Either it's not your turn, or you aren't even fighting. Either way, No.")
        else:
            await ctx.send( "This command does nothing right now. No combat is taking place.")
        # Allows for the use of the 'defensive fighting' passive feat. Makes sure it applies correct bonuses for correct
        # levels.

    @pattack.error
    async def name_pattack(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("The command !pattack may not be used in PMs!")
        else:
            raise error

    @commands.command()
    @commands.guild_only()
    async def dfight(self, ctx, *, message):
        character = ctx.author.send
        # make sure that this command cannot be ran if a fight is taking place.
        if self.game == 1:
            # ensures the command can only be used by player one, when it is their turn. To prevent trolls from
            # spamming commands.
            if character == self.pOneUsername and self.token == 1:
                mod = int(message)
                if self.pOneLevel <= 4 and mod == 1:
                    self.pOnedMod = 1
                elif 4 < self.pOneLevel <= 8 and mod == 2:
                    self.pOnedMod = 2
                elif 8 < self.pOneLevel <= 12 and mod == 3:
                    self.pOnedMod = 3
                elif 12 < self.pOneLevel <= 16 and mod == 4:
                    self.pOnedMod = 4
                elif 16 < self.pOneLevel <= 20 and mod == 5:
                    self.pOnedMod = 5
                else:
                    await ctx.send( "You are not high enough level to invest that many points.")
            # ensures the command can only be used by player two, when it is their turn. To prevent trolls from
            # spamming commands.
            elif character == self.playerTwo and self.token == 2:
                mod = int(message)
                if self.pTwoLevel <= 4 and mod == 1:
                    self.pTwodMod = 1
                elif 4 < self.pTwoLevel <= 8 and mod == 2:
                    self.pTwodMod = 2
                elif 8 < self.pTwoLevel <= 12 and mod == 3:
                    self.pTwodMod = 3
                elif 12 < self.pTwoLevel <= 16 and mod == 4:
                    self.pTwodMod = 4
                elif 16 < self.pTwoLevel <= 20 and mod == 5:
                    self.pTwodMod = 5
                else:
                    await ctx.send( "You are not high enough level to invest that many points.")

            else:
                await ctx.send( "Either it's not your turn, or you aren't even fighting. Either way, No.")
        else:
            await ctx.send( "This command does nothing right now. No combat is taking place.")
        # Allows for the use of the 'defensive fighting' passive feat. Makes sure it applies correct bonuses for correct
        # levels.

    @dfight.error
    async def name_dfight(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("The command !dfight may not be used in PMs!")
        else:
            raise error

    @commands.command()
    @commands.guild_only()
    async def cexpert(self, ctx, *, message):
        character = ctx.author.send
    # make sure that this command cannot be ran if a fight is taking place.
        if self.game == 1:
            # ensures the command can only be used by player one, when it is their turn. To prevent trolls from
            # spamming commands.
            if character == self.pOneUsername and self.token == 1:
                mod = int(message)
                if self.pOneLevel <= 4 and mod == 1:
                    self.pOnecMod = 1
                elif 4 < self.pOneLevel <= 8 and mod == 2:
                    self.pOnecMod = 2
                elif 8 < self.pOneLevel <= 12 and mod == 3:
                    self.pOnecMod = 3
                elif 12 < self.pOneLevel <= 16 and mod == 4:
                    self.pOnecMod = 4
                elif 16 < self.pOneLevel <= 20 and mod == 5:
                    self.pOnecMod = 5
                else:
                    await ctx.send( "You are not high enough level to invest that many points.")
            # ensures the command can only be used by player two, when it is their turn. To prevent trolls from
            # spamming commands.
            elif character == self.pTwoUsername and self.token == 2:
                mod = int(message)
                if self.pTwoLevel <= 4 and mod == 1:
                    self.pTwocMod = 1
                elif 4 < self.pTwoLevel <= 8 and mod == 2:
                    self.pTwocMod = 2
                elif 8 < self.pTwoLevel <= 12 and mod == 3:
                    self.pTwocMod = 3
                elif 12 < self.pTwoLevel <= 16 and mod == 4:
                    self.pTwocMod = 4
                elif 16 < self.pTwoLevel <= 20 and mod == 5:
                    self.pTwocMod = 5
                else:
                    await ctx.send( "You are not high enough level to invest that many points.")

            else:
                await ctx.send( "Either it's not your turn, or you aren't even fighting. Either way, No.")

        else:
            await ctx.send( "This command does nothing right now. No combat is taking place.")

    @cexpert.error
    async def name_cexpert(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("The command !cexpert may not be used in PMs!")
        else:
            raise error

    @commands.command()
    @commands.guild_only()
    async def masochist(self, ctx, *, message):
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

def setup(client):
    client.add_cog(Combat(client))
import discord
from discord.ext import commands
import os
import json
import random
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
        self.pOneUsername = None
        self.pTwoUsername = None
        # PLAYER INFO
        self.pOneInfo = {}
        self.pTwoInfo = {}
        # HP AND TURN COUNTERS
        self.count = 0
        self.token = 0
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
    async def challenge(self, ctx):
        # opens and loads in player one's character sheet. This is done in this method solely because I'm unsure if
        # loading json files in __init__ is actually a good idea. If I understand things correctly, things in a class's
        # __init__ is ran EVERY TIME a method is called within it. If so, then the json files would be opened, loaded,
        # and closed multiple times in a single run. Seems inefficient, and bad coding.
        player = str(ctx.message.author)
        self.pOneUsername = ctx.message.author
        path = os.getcwd()
        charFolder = os.path.join(path + "/characters/")
        charFile = Path(charFolder + player + ".txt")
        file = open(charFolder + player + ".txt", "r", encoding="utf-8")
        charStats = json.load(file)
        file.close()

        self.pOneInfo = charStats

        await ctx.send(self.pOneInfo['name'] + " has issued a challenge. Who accepts? (type !accept)")

    @commands.command()
    @commands.guild_only()
    async def accept(self, ctx):
        player = str(ctx.message.author)
        self.pTwoUsername = ctx.message.author
        path = os.getcwd()
        charFolder = os.path.join(path + "/characters/")
        charFile = Path(charFolder + player + ".txt")
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
            await ctx.send("If you wish to use one of your feats, type !usefeat <feat>. Otherwise type '!usefeat none'")

        elif totalTwo > totalOne:
            await ctx.send(self.pTwoInfo['name'] + " Goes first")
            token = 2
            self.token = token
            await ctx.send("If you wish to use one of your feats, type !usefeat <feat>. Otherwise type '!usefeat none'")

        elif totalOne == totalTwo:
            await ctx.send("In result of tie, person with highest dexterity modifier goes first:")
            await ctx.send(self.pOneInfo['name'] + "'s dexterity: " + str(playerOneMod))
            await ctx.send(self.pTwoInfo['name'] + "'s dexterity: " + str(playerTwoMod))

            if playerOneMod > playerTwoMod:
                await ctx.send(self.pOneInfo['name'] + " Goes first")
                token = 1
                self.token = token
                await ctx.send("If you wish to use one of your feats, type !usefeat <feat>. Otherwise type '!usefeat none'")

            elif playerOneMod < playerTwoMod:
                await ctx.send(self.pTwoInfo['name'] + " Goes first")
                token = 2
                self.token = token
                await ctx.send("If you wish to use one of your feats, type !usefeat <feat>. Otherwise type '!usefeat none'")

            else:
                await ctx.send("As both dexterity values are equal as well. A coin flip. Value of one means " + self.pOneInfo['name'] + " goes first")
                value = random.randint(1, 2)
                await ctx.send(value)

                if value == 1:
                    await ctx.send(self.pTwoInfo['name'] + " Goes first")
                    token = 1
                    self.token = token
                    await ctx.send("If you wish to use one of your feats, type !usefeat <feat>. Otherwise type '!usefeat none'")

                else:
                    await ctx.send(self.playerTwo + " Goes first")
                    token = 2
                    self.token = token
                    await ctx.send("If you wish to use one of your feats, type !usefeat <feat>. Otherwise type '!usefeat none'")

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

    # Next two methods are created to see if a character hit the other character or not. Simulates rolling 1d20 (1-20)
    # then adding any modifiers to the result. If the total either meets or exceeds the other players AC, notify the
    # players that the hit was successful, then move on to the damage methods. If the total does not, notify player
    # that it was a miss, and move on to other player's turn.
    # Note: I want to add in a result that will double damage if the ROLL is a 20, not the total.

    @commands.command()
    @commands.guild_only()
    async def roll(self, ctx):
        print(str(ctx.message.author))
        print(self.pOneUsername)
        if self.pOneUsername == ctx.message.author and self.token == 1:

            # assign both player's feat selections to variables
            pOneFeatUsed = self.pOneFeatInfo
            pTwoFeatUsed = self.pTwoFeatInfo
    
            # If a feat wasn't used by a player, assign it default values.
            if pOneFeatUsed is None:
                pOneFeatUsed = ["none", 0]
            if pTwoFeatUsed is None:
                pTwoFeatUsed = ["none", 0]
    
            # If the feat used was 'true strike' forgo rolling to see if player hit opponent, and go straight to damage.
            if pOneFeatUsed[0] == "true strike":
                await ctx.send(
                    self.pOneInfo['name'] + " used the feat 'True Strike.' And forgoes the need to determine if hit was success.")
    
            # Otherwise, continue on with the bulk of this method
            else:
                pOneToHit = self.pOneInfo['hit']
                pTwoAC = self.pTwoInfo['ac']
    
                # If Player One has power attack, combat expertise, async defensive fighting, or masochist, go to those methods first
                # before continuing.
                # for word in self.pOneInfo["feats taken"]:
                #     if word == "power attack":
                #         #self.pOnepMod = self.pOnePowerAttack()
                #     if word == "combat expertise":
                #         #self.pOnecMod = self.pOneCombatExpertise()
                #     if word == "async defensive fighting":
                #         #self.pOnedMod = self.pOneDefensiveFighting()
                #     if word == "masochist":
                #         #self.pOnemMod = self.pOneMasochist()
                pMod = self.pOnepMod
                cMod = self.pOnecMod
                dMod = self.pOnedMod
                mMod = self.pOnemMod
                pTwodMod = self.pTwodMod
                pTwomMod = self.pTwomMod
    
                # determine the roll of the 1d20.
                hit = random.randint(1, 20)
    
                # if the raw result is equal to 20, count the critical counter up to 1.
                if hit == 20:
                    self.critical = 1
                    await ctx.send(self.pOneInfo['name'] + " has critically hit.")
    
                # Notify that Player One is getting the hit benefit from 'riposte'
                if self.pOneRiposte == 5:
                    await ctx.send(self.pOneInfo['name'] + " benefits from +5 hit bonus effect from riposte.")
    
                # calculate the total after modifiers
                total = int(hit + pOneToHit - pMod + cMod - dMod + mMod + self.pOneRiposte)
    
                # Ensures Player One benefits from hit bonus of Riposte only once.
                self.pOneRiposte = 0
    
                # if any version of crippling blow was used, tack on the penalty to the above total
                if pTwoFeatUsed[0] == "crippling blow" or pTwoFeatUsed[0] == "improved crippling blow" or pTwoFeatUsed[
                    0] == "greater crippling blow":
                    await ctx.send(self.playerTwo + " Used " + pTwoFeatUsed[0] + ", Giving " + self.playerOne + " a " + str(
                        pTwoFeatUsed[1]) + " To their attack.")
                    total = total + pTwoFeatUsed[1]
    
                # testing data to see that modifiers are carrying over correctly. Delete this when project is finished.
                await ctx.send("Roll: " + str(hit) + " Base: " + str(pOneToHit) + " PA: " + str(pMod) + " CE: " + str(
                    cMod) + " DF: " + str(dMod) + " MC: " + str(mMod))
    
                # find Player One's total AC
                totalAC = pTwoAC + pTwodMod - pTwomMod
    
                # testing data to see that modifiers are carrying over correctly. Delete this when project is finished.
                await ctx.send("P2 AC: " + str(pTwoAC) + " DF: " + str(pTwodMod) + " MC: " + str(pTwomMod))
    
                # determine if the total roll, after all modifiers have been included, is a successful hit or not. then
                # head to the appropriate method
                if total >= totalAC:
                    await ctx.send(self.playerOne + " rolled a " + str(total) + " to hit an AC " + str(
                        totalAC) + " and was successful.")
                    self.pTwodMod = 0
                    self.pTwomMod = 0
                    self.pTwoRiposte = 0
                else:
                    await ctx.send(self.playerOne + " rolled a " + str(total) + " to hit an AC " + str(totalAC) + " and missed.")
                    self.pTwodMod = 0
                    self.pTwomMod = 0
                    if pTwoFeatUsed[0] == "riposte":
                        self.pTwoRiposte = 5
        
        elif self.pTwoUsername == ctx.message.author and self.token == 2:        
            pOneFeatUsed = self.pOneFeatInfo
            pTwoFeatUsed = self.pTwoFeatInfo
    
            # If a feat wasn't used by a player, assign it async default values.
            if pOneFeatUsed is None:
                pOneFeatUsed = ["none", 0]
            if pTwoFeatUsed is None:
                pTwoFeatUsed = ["none", 0]
    
            # If the feat used was 'true strike' forgo rolling to see if player hit opponent, and go straight to damage.
            if pTwoFeatUsed[0] == "true strike":
                await ctx.send(
                    self.pTwoInfo['name'] + " used the feat 'True Strike.' And forgoes the need to determine if hit was success.")
    
            # Otherwise, continue on with the bulk of this method
            else:
                pTwoToHit = self.pTwoInfo['hit']
                pOneAC = self.pOneInfo['ac']
    
                # If Player Two has power attack, combat expertise, async defensive fighting, or masochist, go to those methods first
                # before continuing.
                # for word in self.pTwoInfo["feats taken"]:
                #     if word == "power attack":
                #         #self.pTwopMod = self.pTwoPowerAttack()
                #     if word == "combat expertise":
                #         #self.pTwocMod = self.pTwoCombatExpertise()
                #     if word == "async defensive fighting":
                #         #self.pTwodMod = self.pTwoDefensiveFighting()
                #     if word == "masochist":
                #         #self.pTwomMod = self.pTwoMasochist()
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
                    await ctx.send(self.pTwoInfo['name'] + " has critically hit.")
    
                if self.pTwoRiposte == 5:
                    await ctx.send(self.pTwoInfo['name'] + "Benefits from +5 hit bonus effect from riposte.")
    
                # calculate the total after modifiers
                total = int(hit + pTwoToHit - pMod + cMod - dMod + mMod + self.pTwoRiposte)
    
                # Ensures Player Two benefits from hit bonus of Riposte only once.
                self.pTwoRiposte = 0
    
                # if Player Two used riposte, and
                # if any version of crippling blow was used, tack on the penalty to the above total
                if pOneFeatUsed[0] == "crippling blow" or pOneFeatUsed[0] == "improved crippling blow" or pOneFeatUsed[0] == "greater crippling blow":
                    await ctx.send(self.pOneInfo['name'] + " Used " + pOneFeatUsed[0] + ", Giving " + self.pTwoInfo['name'] + " a " + str(OneFeatUsed[1]) + " To their attack.")
                    total = total + pOneFeatUsed[1]
    
                # testing data to see that modifiers are carrying over correctly. Delete this when project is finished.
                await ctx.send("Roll: " + str(hit) + " Base: " + str(pTwoToHit) + " PA: " + str(pMod) + " CE: " + str(
                    cMod) + " DF: " + str(dMod) + " MC: " + str(mMod))
    
                # find Player One's total AC
                totalAC = int(pOneAC + pOnedMod - pOnemMod)
    
                # testing data to see that modifiers are carrying over correctly. Delete this when project is finished.
                await ctx.send(" P1 AC: " + str(pOneAC) + " DF: " + str(pOnedMod) + " MC: " + str(pOnemMod))
    
                # determine if the total roll, after all modifiers have been included, is a successful hit or not. then
                # head to the appropriate method
                if total >= pOneAC:
                    await ctx.send(self.pTwoInfo['name'] + " rolled a " + str(total) + " to hit an AC " + str(
                        totalAC) + " and was successful.")
                    self.pOnedMod = 0
                    self.pOnemMod = 0
                    self.pOneRiposte = 0
                else:
                    await ctx.send(self.pTwoInfo['name'] + " rolled a " + str(total) + " to hit an AC " + str(
                        totalAC) + " and missed.")
                    self.pOnedMod = 0
                    self.pOnemMod = 0
                    if pOneFeatUsed[0] == "riposte":
                        self.pOneRiposte = 5

    # Next two methods will determine how much damage is done after a successful hit. It finds the value placed in the
    # 'base damage' key of the character's json, Parses it out to remove the 'd', and uses the first number as the
    # minimum range, and second for the maximum. After determining the random value, then adds any modifiers to the roll
    # and displays that as the damage.
'''
    async def determineDamagePOne(self, ctx):

        # assign both player's feat selections to variables.
        pOneFeatUsed = self.pOneFeatInfo
        pTwoFeatUsed = self.pTwoFeatInfo

        # If a feat wasn't used by a player, assign it async default values.
        if pOneFeatUsed is None:
            pOneFeatUsed = ["none", 0]
        if pTwoFeatUsed is None:
            pTwoFeatUsed = ["none", 0]

        # Obtain Player One's base damage and base modifier, and roll damage. Assign 'power attack' and 'combat async defense'
        # modifiers to variables, and roll damage.
        pOneBaseDamage = self.pOneInfo['base damage']
        pOneModifier = self.pOneInfo['damage modifier']
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
            await ctx.send(self.pOneInfo['name'] + " used the feat 'titan blow'.")
            damage = damage * float(pOneFeatUsed[1])

        # if Player Two use 'staggering blow' half damage done.
        if pTwoFeatUsed[0] == "staggering blow":
            await ctx.send(
                self.pTwoInfo['name'] + " used the feat 'staggering blow', halving " + self.pOneInfo['name'] + "'s damage roll")
            damage = damage * float(pTwoFeatUsed[1])

        # ensure that no matter what, raw damage can not fall below 1, then assign total damage to variable, and in turn
        # assign it to variable to be accessed for scoreboard.
        if damage < 1:
            damage = 1
        total = int(damage + pOneModifier + pMod - cMod)

        # if Player Two used 'quick strike', 'improved quick strike', or 'greater quick strike', apply the return
        # damage here
        pTwoBaseDamage = self.pTwoInfo['base damage']
        pTwoModifier = self.pTwoInfo['damage modifier']
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
            await ctx.send(self.pTwoInfo['name'] + " used 'quick strike,' managing to do an additional " + str(
                self.pTwoQuickDamage) + "hp of damage.")

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
            await ctx.send(self.pTwoInfo['name'] + " used 'quick strike,' managing to do an additional " + str(
                self.pTwoQuickDamage) + "hp of damage.")

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
            await ctx.send(self.pTwoInfo['name'] + " used 'quick strike,' managing to do an additional " + str(
                self.pTwoQuickDamage) + "hp of damage.")

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
            await ctx.send(self.pTwoInfo['name'] + " used 'quick strike,' managing to do an additional " + str(
                self.pTwoQuickDamage) + "hp of damage.")

        # If Player Two has Evasion, Improved Evasion, or Greater Evasion, give them the option to use it.
        for word in self.pTwoInfo['feats taken']:
            answer = ""
            if self.pTwoEvade == 1 and word == "evasion":
                while answer != "yes" and answer != "no":
                    answer = await ctx.send(self.pTwoInfo['name'] + ", do you wish to evade? ").lower()
                    if answer == "yes":
                        total = int(total * 0.75)
                        self.totalDamage = total
                        self.pTwoEvade = 0
                    elif answer == "no":
                        pass
                    else:
                        await ctx.send("Answer 'yes' or 'no'")
            elif self.pTwoEvade == 1 and word == "improved evasion":
                while answer != "yes" and answer != "no":
                    answer = await ctx.send(self.pTwoInfo['name'] + ", do you wish to evade? ").lower()
                    if answer == "yes":
                        total = int(total * 0.5)
                        self.totalDamage = total
                        self.pTwoEvade = 0
                    elif answer == "no":
                        pass
                    else:
                        await ctx.send("Answer 'yes' or 'no'")
            elif self.pTwoEvade == 1 and word == "greater evasion":
                while answer != "yes" and answer != "no":
                    answer = await ctx.send(self.pTwoInfo['name'] + ", do you wish to evade? ").lower()
                    if answer == "yes":
                        total = 0
                        self.totalDamage = total
                        self.pTwoEvade = 0
                    elif answer == "no":
                        pass
                    else:
                        await ctx.send("Answer 'yes' or 'no'")

        # If Player Two used 'async deflect', 'improved async deflect', or 'greater async deflect', apply damage mitigation here
        if pTwoFeatUsed[0] == "async deflect":
            await ctx.send(self.pTwoInfo['name'] + " used async deflect to lessen the blow.")
            total = int(total * float(pTwoFeatUsed[1]))
        elif pTwoFeatUsed[0] == "improved async deflect":
            await ctx.send(self.pTwoInfo['name'] + " used async deflect to lessen the blow")
            total = int(total * float(pTwoFeatUsed[1]))
        elif pTwoFeatUsed[0] == "greater async deflect":
            await ctx.send(self.pTwoInfo['name'] + " used async deflect to lessen the blow")
            total = int(total * float(pTwoFeatUsed[1]))
        self.totalDamage = total

        # testing data to see that modifiers are carrying over correctly. Delete this when project is finished.
        await ctx.send(
            "Roll: " + str(damage) + " Modifier: " + str(pOneModifier) + " PA: " + str(pMod) + " CD: " + str(cMod))

        # display total damage done, and reset passive feat counters (power attack and combat async defense)
        await ctx.send(self.pOneInfo['name'] + " did " + str(total) + " points of damage.")
        self.pOnepMod = 0
        self.pOnecMod = 0
        self.getHitPointsPTwo()

    async def determineDamagePTwo(self, ctx):

        # assign both player's feat selections to variables.
        pOneFeatUsed = self.pOneFeatInfo
        pTwoFeatUsed = self.pTwoFeatInfo

        # If a feat wasn't used by a player, assign it async default values.
        if pOneFeatUsed is None:
            pOneFeatUsed = ["none", 0]
        if pTwoFeatUsed is None:
            pTwoFeatUsed = ["none", 0]

        # Obtain Player Two's base damage and base modifier, and roll damage. Assign 'power attack' and 'combat async defense'
        # modifiers to variables, and roll damage.
        pTwoBaseDamage = self.pTwoInfo['base damage']
        pTwoModifier = self.pTwoInfo['damage modifier']
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
            await ctx.send(self.pTwoInfo['name'] + " used the feat 'titan blow'.")
            damage = damage * float(pTwoFeatUsed[1])

        # if Player One use 'staggering blow' half damage done.
        if pOneFeatUsed[0] == "staggering blow":
            await ctx.send(
                self.pOneInfo['name'] + " used the feat 'staggering blow', halving " + self.pTwoInfo['name'] + "'s damage roll")
            damage = damage * float(pOneFeatUsed[1])

        # ensure that no matter what, raw damage can not fall below 1, then assign total damage to variable, and in turn
        # assign it to variable to be accessed for scoreboard.
        if damage < 1:
            damage = 1
        total = int(damage + pTwoModifier + pMod - cMod)

        # if Player One used 'quick strike', 'improved quick strike', or 'greater quick strike', apply the return
        # damage here
        pOneBaseDamage = self.pOneInfo['base damage']
        pOneModifier = self.pOneInfo['damage modifier']
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
            await ctx.send(self.pOneInfo['name'] + " used 'quick strike,' managing to do an additional " + str(
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
            await ctx.send(self.pOneInfo['name'] + " used 'quick strike,' managing to do an additional " + str(
                self.pOneQuickDamage) + "hp of damage.")

        if pOneFeatUsed[0] == "greater quick strike":
            # roll damage for player One, and multiply it by desired amount
            damage = random.randint(int(pOneMinimum), int(pOneMaximum))
            total = (damage + pOneModifier + pMod - cMod)
            quickDamage = int(total * float(pOneFeatUsed[1]))

            # Ensure damage is always at least 1hp and print out result
            self.pOneQuickDamage = quickDamage
            self.pTwoCurrentHP = self.pTwoCurrentHP - self.pOneQuickDamage
            await ctx.send(self.pOneInfo['name'] + " used 'quick strike,' managing to do an additional " + str(
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
            await ctx.send(self.pOneInfo['name'] + " used 'quick strike,' managing to do an additional " + str(
                self.pOneQuickDamage) + "hp of damage.")
            self.pOneRiposte = 1

        # If Player One has Evasion, Improved Evasion, or Greater Evasion, give them the option to use it.
        for word in self.pOneInfo['feats taken']:
            answer = ""
            if self.pOneEvade == 1 and word == "evasion":
                while answer != "yes" and answer != "no":
                    answer = await ctx.send(self.pOneInfo['name'] + ", do you wish to evade? ").lower()
                    if answer == "yes":
                        total = int(total * 0.5)
                        self.totalDamage = total
                        self.pTwoEvade = 0
                    elif answer == "no":
                        pass
                    else:
                        await ctx.send("Answer 'yes' or 'no'")
            elif self.pOneEvade == 1 and word == "improved evasion":
                while answer != "yes" and answer != "no":
                    answer = await ctx.send(self.pOneInfo['name'] + ", do you wish to evade? ").lower()
                    if answer == "yes":
                        total = int(total * 0.5)
                        self.totalDamage = total
                        self.pTwoEvade = 0
                    elif answer == "no":
                        pass
                    else:
                        await ctx.send("Answer 'yes' or 'no'")
            elif self.pOneEvade == 1 and word == "greater evasion":
                while answer != "yes" and answer != "no":
                    answer = await ctx.send(self.pTwoInfo['name'] + ", do you wish to evade? ").lower()
                    if answer == "yes":
                        total = int(total * 0.5)
                        self.totalDamage = total
                        self.pTwoEvade = 0
                    elif answer == "no":
                        pass
                    else:
                        await ctx.send("Answer 'yes' or 'no'")

        # If Player One used 'async deflect', 'improved async deflect', or 'greater async deflect', apply damage mitigation here
        if pOneFeatUsed[0] == "async deflect":
            await ctx.send(self.pOneInfo['name'] + " used async deflect to lessen the blow.")
            total = int(total * float(pOneFeatUsed[1]))
        elif pOneFeatUsed[0] == "improved async deflect":
            await ctx.send(self.pOneInfo['name'] + " used async deflect to lessen the blow")
            total = int(total * float(pOneFeatUsed[1]))
        elif pOneFeatUsed[0] == "greater async deflect":
            await ctx.send(self.pOneInfo['name'] + " used async deflect to lessen the blow")
            await ctx.send(pOneFeatUsed[1])
            await ctx.send(total)
            total = int(total * float(pOneFeatUsed[1]))
            await ctx.send(total)

        self.totalDamage = total
        # testing data to see that modifiers are carrying over correctly. Delete this when project is finished.
        await ctx.send(
            "Roll: " + str(damage) + " Modifier: " + str(pTwoModifier) + " PA: " + str(pMod) + " CD: " + str(cMod))

        # display total damage done, and reset passive feat counters (power attack and combat async defense).
        await ctx.send(self.pTwoInfo['name'] + " did " + str(total) + " points of damage.")
        self.pTwopMod = 0
        self.pTwocMod = 0
        self.getHitPointsPOne()

    # Two methods to update hit points as the fight progresses along.

    def getHitPointsPOne(self):
        if self.pTwoQuickDamage != 0:
            self.pOneCurrentHP = self.pOneCurrentHP - self.totalDamage - self.pTwoQuickDamage
            self.pTwoQuickDamage = 0
        else:
            self.pOneCurrentHP = self.pOneCurrentHP - self.totalDamage
        self.token = 2
        self.scoreboard()

    def getHitPointsPTwo(self):
        if self.pOneQuickDamage != 0:
            self.pTwoCurrentHP = self.pTwoCurrentHP - self.totalDamage - self.pOneQuickDamage
            self.pOneQuickDamage = 0
        else:
            self.pTwoCurrentHP = self.pTwoCurrentHP - self.totalDamage
        self.token = 1
        self.scoreboard()

    # Creates the scoreboard to display to players after every turn. The if statement is placed here as a break, to
    # not allow the program to run test runs in one fluid motion. However, I believe this will be the place to obtain
    # player input on if they want to use any special feats they have - such as evasion to halve damage taken, and so on
    # Believe that each feat requiring extra variables will require methods of their own. Unsure of how to go about that yet.

    async def scoreboard(self, ctx):
        await ctx.send(self.pOneInfo['name'] + ": " + str(self.pOneCurrentHP) + "/" + str(
            self.pOneTotalHP) + "  ||  " + self.pTwoInfo['name'] + ": " + str(self.pTwoCurrentHP) + "/" + str(
            self.pTwoTotalHP))
        self.combatRounds()

    # the 'meat and potatoes' of combat. This method will keep track of whose turn it is via a token variable I
    # initiated back in the Initiative method. This method will also watch to see if any opponent drops to 0 or below
    # hit points, and when that happens, end combat.

    def combatRounds(self):
        if self.pOneCurrentHP > 0 and self.pTwoCurrentHP > 0:
            if self.token == 1:
                self.count += 1
                self.token += 1
            elif self.token == 2:
                self.count += 1
                self.token -= 1
        else:
            self.setXP()

    # Determines xp for the victor. Formula is: 10 * Difference in opponent's HP + (difference in level * 50), where
    # difference in level will never equal 0. Added a small 'if' statement to ensure that level never equals 0, which
    # can only happen if both player character's are of the same level.
    async def setXP(self, ctx):
        if self.pOneCurrentHP <= 0:
            await ctx.send(self.pTwoInfo['name'] + " won in " + str(int(self.count / 2)) + " rounds")
            level = abs(self.pOneLevel - self.pTwoLevel)
            if level == 0:
                level = 1
            if level <= 3:
                levelDiff = level * self.pOneLevel
                differHP = abs(self.pOneCurrentHP - self.pTwoCurrentHP)
                self.xp = 10 * levelDiff + differHP
                await ctx.send(self.pTwoInfo['name'] + " has earned: " + str(self.xp) + " experience points.")
            elif 3 > level < 6:
                levelDiff = level * self.pOneLevel
                differHP = abs(self.pOneCurrentHP - self.pTwoCurrentHP)
                self.xp = 7 * levelDiff + differHP
            elif 7 > level < 10:
                levelDiff = level * self.pOneLevel
                differHP = abs(self.pOneCurrentHP - self.pTwoCurrentHP)
                self.xp = 5 * levelDiff + differHP
            else:
                await ctx.send("As the level difference was greater than 10, no XP was awarded.")
            await ctx.send(self.pTwoInfo['name'] + " has earned: " + str(self.xp) + " experience points.")
            self.currentPlayerXP = self.pTwoInfo['currentxp'] + self.xp
            self.nextLevel = self.pTwoInfo['nextlevel']
            self.winner = self.playerTwo
            self.levelUp = self.pTwoInfo['level']
            self.checkLevel()

        elif self.pTwoCurrentHP <= 0:
            await ctx.send(self.pOneInfo['name'] + " won in " + str(int(self.count / 2)) + " rounds")
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
                await ctx.send(self.pOneInfo['name'] + " has earned: " + str(self.xp) + " experience points.")
            else:
                await ctx.send("As the level difference was greater than 10, no XP was awarded.")
            await ctx.send(self.pOneInfo['name'] + " has earned: " + str(self.xp) + " experience points.")
            self.currentPlayerXP = self.pOneInfo['currentxp'] + self.xp
            self.nextLevel = self.pOneInfo['nextlevel']
            self.winner = self.playerOne
            self.levelUp = self.pOneInfo['level']
            self.checkLevel()

    # Method to check the value of 'currentxp' on a character's json file. If it exceeds the 'nextlevel' value, notify
    # the winning player that they have leveled up. Then proceed to write all the new values for that level to the
    # json file.
    # this Method opens up levelchart.txt, a json that contains a dictionary containing values for levels 1 through 20.
    async def checkLevel(self, ctx):

        with open(self.winner + '.txt', 'r+') as file:
            charData = json.load(file)
            charData['currentxp'] = self.currentPlayerXP
            file.seek(0)
            file.write(json.dumps(charData, ensure_ascii=False, indent=2))
            file.truncate()
            file.close()

        if self.currentPlayerXP >= self.nextLevel:
            newLevel = self.levelUp + 1
            newLevel = str(newLevel)
            await ctx.send(self.winner.capitalize() + " has reached level " + newLevel + "!")
            levelFile = open("levelchart.txt", "r", encoding="utf-8")
            levelDict = json.load(levelFile)
            levelFile.close()

            with open(self.winner + '.txt', 'r+') as file:
                charData = json.load(file)
                charData['level'] = int(newLevel)
                charData['hitpoints'] = int(levelDict[newLevel][0])
                charData['base damage'] = str(levelDict[newLevel][1]) + "d" + str(levelDict[newLevel][2])
                charData['total feats'] = levelDict[newLevel][4]
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

    # ----------------------------------------------- FEAT METHODS ------------------------------------------------------
    def pOnePowerAttack(self):
        mod = 0
        if self.pOneLevel <= 4:
            mod = "1"
        elif 4 < self.pOneLevel <= 8:
            mod = "2"
        elif 8 < self.pOneLevel <= 12:
            mod = "3"
        elif 12 < self.pOneLevel <= 16:
            mod = "4"
        elif 16 < self.pOneLevel <= 20:
            mod = "5"
        pMod = 6
        while pMod > int(mod):
            try:
                pMod = int(await ctx.send("Select point allocation for Power Attack (0-" + mod + "): "))
            except ValueError:
                await ctx.send("Please select a number between 0 and " + mod + ": ")
        return int(pMod)

    def pTwoPowerAttack(self):
        mod = 0
        await ctx.send(type(self.pTwoLevel))
        if self.pTwoLevel <= 4:
            mod = "1"
        elif 4 < self.pTwoLevel <= 8:
            mod = "2"
        elif 8 < self.pTwoLevel <= 12:
            mod = "3"
        elif 12 < self.pTwoLevel <= 16:
            mod = "4"
        elif 16 < self.pTwoLevel <= 20:
            mod = "5"
        pMod = 6
        while pMod > int(mod):
            try:
                pMod = int(await ctx.send("Select point allocation for Power Attack (0-" + mod + "): "))
            except ValueError:
                await ctx.send("Please select a number between 0 and " + mod + ": ")
        return int(pMod)

    def pOneCombatExpertise(self):
        mod = 0
        if self.pTwoLevel <= 4:
            mod = "1"
        elif 4 < self.pOneLevel <= 8:
            mod = "2"
        elif 8 < self.pOneLevel <= 12:
            mod = "3"
        elif 12 < self.pOneLevel <= 16:
            mod = "4"
        elif 16 < self.pOneLevel <= 20:
            mod = "5"
        cMod = 6
        while cMod > int(mod):
            try:
                cMod = int(await ctx.send("Select point allocation for Combat Expertise (0-" + mod + "): "))
            except ValueError:
                await ctx.send("Please select a number between 0 and " + mod + ": ")
        return int(cMod)

    def pTwoCombatExpertise(self):
        mod = 0
        if self.pTwoLevel <= 4:
            mod = "1"
        elif 4 < self.pTwoLevel <= 8:
            mod = "2"
        elif 8 < self.pTwoLevel <= 12:
            mod = "3"
        elif 12 < self.pTwoLevel <= 16:
            mod = "4"
        elif 16 < self.pTwoLevel <= 20:
            mod = "5"
        cMod = 6
        while cMod > int(mod):
            try:
                cMod = int(await ctx.send("Select point allocation for Combat Expertise (0- " + mod + "): "))
            except ValueError:
                await ctx.send("Please select a number between 0 and " + mod + ": ")
        return int(cMod)

    def pOneDefensiveFighting(self):
        mod = 0
        if self.pTwoLevel <= 4:
            mod = "1"
        elif 4 < self.pOneLevel <= 8:
            mod = "2"
        elif 8 < self.pOneLevel <= 12:
            mod = "3"
        elif 12 < self.pOneLevel <= 16:
            mod = "4"
        elif 16 < self.pOneLevel <= 20:
            mod = "5"
        dMod = 6
        while dMod > int(mod):
            try:
                dMod = int(await ctx.send("Select point allocation for async defensive Fighting (0-" + mod + "): "))
            except ValueError:
                await ctx.send("Please select a number between 0 and " + mod + ": ")
        return int(dMod)

    def pTwoDefensiveFighting(self):
        mod = 0
        if self.pTwoLevel <= 4:
            mod = "1"
        elif 4 < self.pTwoLevel <= 8:
            mod = "2"
        elif 8 < self.pTwoLevel <= 12:
            mod = "3"
        elif 12 < self.pTwoLevel <= 16:
            mod = "4"
        elif 16 < self.pTwoLevel <= 20:
            mod = "5"
        dMod = 6
        while dMod > int(mod):
            try:
                dMod = int(await ctx.send("Select point allocation for async defensive Fighting (0-" + mod + "): "))
            except ValueError:
                await ctx.send("Please select a number between 0 and " + mod + ": ")
        return int(dMod)

    def pOneMasochist(self):
        mod = 0
        if self.pTwoLevel <= 4:
            mod = "1"
        elif 4 < self.pOneLevel <= 8:
            mod = "2"
        elif 8 < self.pOneLevel <= 12:
            mod = "3"
        elif 12 < self.pOneLevel <= 16:
            mod = "4"
        elif 16 < self.pOneLevel <= 20:
            mod = "5"
        mMod = 6
        while mMod > int(mod):
            try:
                mMod = int(await ctx.send("Select point allocation for Masochist (0-" + mod + "): "))
            except ValueError:
                await ctx.send("Please select a number between 0 and " + mod + ": ")
        return int(mMod)

    def pTwoMasochist(self):
        mod = 0
        if self.pTwoLevel <= 4:
            mod = "1"
        elif 4 < self.pTwoLevel <= 8:
            mod = "2"
        elif 8 < self.pTwoLevel <= 12:
            mod = "3"
        elif 12 < self.pTwoLevel <= 16:
            mod = "4"
        elif 16 < self.pTwoLevel <= 20:
            mod = "5"
        mMod = 6
        while mMod > int(mod):
            try:
                mMod = int(await ctx.send("Select point allocation for Masochist (0-" + mod + "): "))
            except ValueError:
                await ctx.send("Please select a number between 0 and " + mod + ": ")

    return int(mMod)
'''
def setup(client):
    client.add_cog(Combat(client))
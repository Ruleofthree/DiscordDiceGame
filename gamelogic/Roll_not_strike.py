import os
import json
import random
import time
import discord

from discord.ext import commands
from pathlib import Path
from threading import Timer

class Damage(commands.Cog):

    def __init__(self, client):
        self.client = client

    def Not_True_Strike(self, msg, pOneInfo, pTwoInfo, pOnepMod, pTwopMod, pOnecMod, pTwocMod, pOnedMod, pTwodMod, pOnemMod,
                        pTwomMod,
                        pOneRiposte, pTwoRiposte, pOneFeatUsed, pTwoFeatUsed, pOneFeatInfo, pTwoFeatInfo, pOneCurrentHP,
                        pTwoCurrentHP,
                        pOneTotalHP, pTwoTotalHP, pOneEvade, pTwoEvade, pOneDeflect, pTwoDeflect, pOneQuickDamage, pTwoQuickDamage, iddqd, critical,
                        count, featToken, bGameTimer,
                        token, totalDamage, new_token):
        pOneToHit = pOneInfo['thit']
        pTwoAC = pTwoInfo['tac']

        pMod = pOnepMod
        cMod = pOnecMod
        dMod = pOnedMod
        mMod = pOnemMod
        bonusHurt = 0
        nerveDamage = 0

        # Susanna Added , for ask prompt !evation or !pass
        bEvasion = False
        bDeflect = False

        # determine the roll of the 1d20.
        if iddqd != 0:
            hit = iddqd
        else:
            hit = random.randint(1, 20)

        # if the raw result is equal to 20, count the critical counter up to 1.
        if hit == 20:
            critical = 1
            msg.append(pOneInfo['name'] + " has [color=red][b]critically hit.[/b][/color]")
        elif hit == 1:
            msg.append(pOneInfo['name'] + " has [color=red][b]critically missed.[/b][/color]")

        # Notify that Player One is getting the hit benefit from 'riposte'
        if pOneRiposte == 1:
            msg.append(pOneInfo['name'] +
                       " benefits from [color=red]+5[/color] hit bonus effect from "
                       "[color=yellow]riposte.[/color]")

        # calculate the total after modifiers
        total = int(hit + pOneToHit - pMod + cMod - dMod + mMod + pOneRiposte)
        # Ensures Player One benefits from hit bonus of Riposte only once.
        pOneRiposte = 0

        # if any version of crippling blow was used, tack on the penalty to the above total
        if pTwoFeatUsed[0] == "crippling blow" or pTwoFeatUsed[0] == "improved crippling blow" or \
                pTwoFeatUsed[0] == "greater crippling blow":
            msg.append(pTwoInfo['name'] + " Used [color=yellow]'" + str(pTwoFeatUsed[0])
                       + "'[/color], Giving " + pOneInfo['name'] +
                       " a [color=red]" + str(pTwoFeatUsed[1]) + "[/color] To their attack.")
            total = total + pTwoFeatUsed[1]

        # # testing data to see that modifiers are carrying over correctly. Comment out
        # # when project is finished.
        # msg.append("Roll: " + str(hit) + " Base: " + str(pOneToHit) + " PA: " +
        #             str(pMod) + " CE: " + str(cMod) + " DF: " + str(dMod) + " MC: " +
        #             str(mMod) + " Riposte: " + str(pOneRiposte) + " Hurt Me: " + str(bonusHurt) +)

        # find Player Two's total AC
        totalAC = pTwoAC + pTwodMod - pTwomMod
        # # testing data to see that modifiers are carrying over correctly. Delete this when project is finished.
        # msg.append("P2 AC: " + str(pTwoAC) + " DF: " + str(pTwodMod) + " MC: " + str(pTwomMod))

        # determine if the total roll, after all modifiers have been included, is a successful hit or not. then
        # head to the appropriate method
        if total < totalAC or hit == 1:
            msg.append(pOneInfo['name'] + " rolled a [color=red]" + str(total) + "[/color] "
                                                                                 "to hit an AC [color=green]" + str(
                totalAC) + "[/color] and missed."
                           "(Base Roll: [color=blue]" + str(hit) + "[/color] \n" +
                       pTwoInfo['name'] + "'s turn. Type: [color=pink]!usefeat <feat>[/color] "
                                          "if you wish to use a feat.")

            if pTwoFeatUsed[0] == "riposte":
                pTwoRiposte = 1
            pTwodMod = 0
            pTwomMod = 0
            token = new_token
            iddqd = 0
            count += 1
            featToken = 0
            bGameTimer = True
            pTwoFeatInfo = None

        elif total >= totalAC or hit == 20:
            msg.append(pOneInfo['name'] + " rolled a [color=red]" + str(total) +
                       "[/color] to hit an AC [color=green]" + str(totalAC) + "[/color] and was "
                                                                              "successful. (Base Roll: [color=blue]" + str(
                hit) + "[/color]")
            pTwodMod = 0
            pTwomMod = 0
            pTwoRiposte = 0
            iddqd = 0

            # ------------------------------------PLAYER ONE DAMAGE--------------------------------------
            # Obtain Player One's base damage and base modifier, and roll damage. Assign 'power attack' and 'combat defense'
            # modifiers to variables, and roll damage.
            pOneBaseDamage = pOneInfo['base damage']
            pOneModifier = pOneInfo['tdamage']
            pOneMinimum, pOneMaximum = pOneBaseDamage.split('d')
            pMod = pOnepMod
            cMod = pOnecMod
            damage = random.randint(int(pOneMinimum), int(pOneMaximum))
            base = damage
            # if critical counter is a value of 1, double the damage done, then reset counter to 0.
            if critical == 1:
                damage = damage * 2
                critical = 0
            # if Player One used feat 'titan blow', apply 50% bonus damage.
            if pOneFeatUsed[0] == "titan blow":
                msg.append(pOneInfo['name'] + " used the feat "
                                              "[color=yellow]'titan blow'[/color]. Applying a "
                                              "[color=red]50%[/color] bonus to damage rolled.")
                damage = damage * float(pOneFeatUsed[1])

            # if Player Two use 'staggering blow' half damage done.
            if pTwoFeatUsed[0] == "staggering blow":
                msg.append(pTwoInfo['name'] + " used the feat "
                                              "[color=yellow]'staggering blow'[/color], halving " +
                           pOneInfo['name'] + "'s damage roll")
                damage = damage * float(pTwoFeatUsed[1])

            # ensure that no matter what, raw damage can not fall below 1, then assign total damage to variable, and in turn
            # assign it to variable to be accessed for scoreboard.
            if damage < 1:
                damage = 1
            # If Player One has Nerve Strike, Improved Nerve Strike, Greater Nerve Strike, or Never Damage
            # apply damage bonuses.
            if 'nerve strike' in pOneInfo['feats taken']:
                if total >= (totalAC + 3) or hit == 20:
                    nerveDamage = random.randint(1, 6)
                    msg.append(pOneInfo['name'] + " managed to strike a nerve, doing an additional [color=red]" +
                               str(nerveDamage) + "[/color] to their opponent.")
            if 'improved nerve strike' in pOneInfo['feats taken']:
                if total >= (totalAC + 3) or hit == 20:
                    nerveDamage = random.randint(2, 12)
                    msg.append(pOneInfo['name'] + " managed to strike a nerve, doing an additional [color=red]" +
                               str(nerveDamage) + "[/color] to their opponent.")
            if 'greater nerve strike' in pOneInfo['feats taken']:
                if total >= (totalAC + 3) or hit == 20:
                    nerveDamage = random.randint(3, 18)
                    msg.append(pOneInfo['name'] + " managed to strike a nerve, doing an additional [color=red]" +
                               str(nerveDamage) + "[/color] to their opponent.")
            if 'nerve damage' in pOneInfo['feats taken']:
                if total >= (totalAC + 3) or hit == 20:
                    nerveDamage = random.randint(3, 24)
                    msg.append(pOneInfo['name'] + " managed to strike a nerve, doing an additional [color=red]" +
                               str(nerveDamage) + "[/color] to their opponent.")

            # If Player One has Hurt Me, Improved Hurt Me, and Greater Hurt Me, check hit points, and apply
            # bonuses.
            number = (pOneCurrentHP / pOneTotalHP) * 100
            percentage = int(number)
            if 'hurt me' in pOneInfo['feats taken']:
                if 33 < percentage <= 66:
                    bonusHurt = 1
                    msg.append(pOneInfo['name'] + " has become enraged because of [color=yellow]"
                                                  "'hurt me'[/color], and are getting a [color=red]+" + str(bonusHurt) +
                               " [/color] bonus to their damage.")
                elif percentage <= 33:
                    bonusHurt = 2
                    msg.append(pOneInfo['name'] + " has become further enraged because of [color=yellow]"
                                                  "'hurt me',[/color] and are getting a [color=red]+" + str(bonusHurt) +
                               " [/color] bonus to their damage.")
            elif 'improved hurt me' in pOneInfo['feats taken']:
                if 33 < percentage <= 66:
                    bonusHurt = 2
                    msg.append(pOneInfo['name'] + " has become enraged because of [color=yellow]"
                                                  "'hurt me'[/color], and are getting a [color=red]+" + str(bonusHurt) +
                               " [/color] bonus to their damage.")
                elif percentage <= 33:
                    bonusHurt = 3
                    msg.append(pOneInfo['name'] + " has become enraged because of [color=yellow]"
                                                  "'hurt me'[/color], and are getting a [color=red]+" + str(bonusHurt) +
                               " [/color] bonus to their damage.")
            elif 'greater hurt me' in pOneInfo['feats taken']:
                if 33 < percentage <= 66:
                    bonusHurt = 2
                    msg.append(pOneInfo['name'] + " has become enraged because of [color=yellow]"
                                                  "'hurt me'[/color], and are getting a [color=red]+" + str(bonusHurt) +
                               " [/color] bonus to their damage.")
                elif percentage <= 33:
                    bonusHurt = 4
                    msg.append(pOneInfo['name'] + " has become further enraged because of [color=yellow]"
                                                  "'hurt me',[/color] and are getting a [color=red]+" + str(bonusHurt) +
                               " [/color] bonus to their damage.")
            elif 'hurt me more' in pOneInfo['feats taken']:
                if 50 < percentage <= 75:
                    bonusHurt = 2
                    msg.append(pOneInfo['name'] + " has become enraged because of [color=yellow]"
                                                  "'hurt me'[/color], and are getting a [color=red]+" + str(bonusHurt) +
                               " [/color] bonus to their damage.")
                elif 25 < percentage <= 50:
                    bonusHurt = 4
                    msg.append(pOneInfo['name'] + " has become further enraged because of [color=yellow]"
                                                  "'hurt me',[/color] and are getting a [color=red]+" + str(bonusHurt) +
                               " [/color] bonus to their damage.")
                elif percentage <= 25:
                    bonusHurt = 6
                    msg.append(pOneInfo['name'] + " has become further enraged because of [color=yellow]"
                                                  "'hurt me',[/color] and are getting a [color=red]+" + str(bonusHurt) +
                               " [/color] bonus to their damage.")

            total = int(damage + pOneModifier + pMod - cMod - pTwoInfo['dr'] + bonusHurt + nerveDamage)
            if pTwoInfo['dr'] != 0:
                msg.append(pTwoInfo['name'] + " has [color=yellow]thick skin[/color], and has aborbed " +
                           str(pTwoInfo['dr']) + " hp of damage from opponent's roll.")
            # if Plaer One has 'reckless abandon' apply bonus damage
            if pOneFeatUsed[0] == "reckless abandon":
                damageToPTwo = random.randint(1, 4)
                damageToPOne = random.randint(1, 2)
                pOneCurrentHP = pOneCurrentHP - damageToPOne
                total = total + damageToPTwo
                msg.append(pOneInfo['name'] + " did [color=red]" + str(damageToPOne) + "[/color]"
                                                                                       " damage to themself, to deal an additional [color=red]" + str(
                    damageToPTwo) +
                           "[/color] damage to their opponent.")

            elif pOneFeatUsed[0] == "improved reckless abandon":
                damageToPTwo = random.randint(1, 8)
                damageToPOne = random.randint(1, 4)
                pOneCurrentHP = pOneCurrentHP - damageToPOne
                total = total + damageToPTwo
                msg.append(pOneInfo['name'] + " did [color=red]" + str(damageToPOne) + "[/color]"
                                                                                       " damage to themself, to deal an additional [color=red]" + str(
                    damageToPTwo) +
                           "[/color] damage to their opponent.")

            elif pOneFeatUsed[0] == "greater reckless abandon":
                damageToPTwo = random.randint(1, 6)
                damageToPOne = random.randint(1, 12)
                pOneCurrentHP = pOneCurrentHP - damageToPOne
                total = total + damageToPTwo
                msg.append(pOneInfo['name'] + " did [color=red]" + str(damageToPOne) + "[/color]"
                                                                                       " damage to themself, to deal an additional [color=red]" + str(
                    damageToPTwo) +
                           "[/color] damage to their opponent.")
            # if Player Two used 'quick strike', 'improved quick strike', or 'greater quick strike', apply the return
            # damage here
            pTwoBaseDamage = pTwoInfo['base damage']
            pTwoModifier = pTwoInfo['tdamage']
            pTwoMinimum, pTwoMaximum = pTwoBaseDamage.split('d')

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
                pTwoQuickDamage = quickDamage
                pOneCurrentHP = pOneCurrentHP - pTwoQuickDamage
                msg.append(pTwoInfo['name'] + " used [color=yellow]'quick strike,'[/color]"
                                              " managing to do an additional [color=red]"
                           + str(pTwoQuickDamage) + "[/color] hp of damage.")

            elif pTwoFeatUsed[0] == "improved quick strike":
                # Roll damage for Player one, and multiply it by desired amount.
                damage = random.randint(int(pTwoMinimum), int(pTwoMaximum))
                total = (damage + pTwoModifier + pMod - cMod)
                quickDamage = int(total * float(pTwoFeatUsed[1]))
                # Ensure damage is always at least 1hp and print out result
                if quickDamage < 1:
                    quickDamage = 1
                pTwoQuickDamage = quickDamage
                pOneCurrentHP = pOneCurrentHP - pTwoQuickDamage
                msg.append(pTwoInfo['name'] + " used [color=yellow]'quick strike,'[/color]"
                           " managing to do an additional [color=red]" + str(pTwoQuickDamage) + "[/color] hp of damage.")

            elif pTwoFeatUsed[0] == "greater quick strike":
                # roll damage for player One, and multiply it by desired amount
                damage = random.randint(int(pTwoMinimum), int(pTwoMaximum))
                total = (damage + pTwoModifier + pMod - cMod)
                quickDamage = int(total * float(pTwoFeatUsed[1]))
                # Ensure damage is always at least 1hp and print out result
                if quickDamage < 1:
                    quickDamage = 1
                pTwoQuickDamage = quickDamage
                pOneCurrentHP = pOneCurrentHP - pTwoQuickDamage
                msg.append(pTwoInfo['name'] + " used [color=yellow]'quick strike,'[/color]"
                                              " managing to do an additional [color=red]"
                           + str(pTwoQuickDamage) + "[/color] hp of damage.")

            elif pTwoFeatUsed[0] == "riposte":
                # roll damage for player One, and multiply it by desired amount
                damage = random.randint(int(pTwoMinimum), int(pTwoMaximum))
                total = (damage + pTwoModifier + pMod - cMod)
                quickDamage = int(total * float(pTwoFeatUsed[1][0]))
                # Ensure damage is always at least 1hp and print out result
                if quickDamage < 1:
                    quickDamage = 1
                pTwoQuickDamage = quickDamage
                pOneCurrentHP = pOneCurrentHP - pTwoQuickDamage
                msg.append(pTwoInfo['name'] + " used [color=yellow]'riposte,'[/color]"
                                              " managing to do an additional [color=red]"
                           + str(pTwoQuickDamage) + "[/color] hp of damage.")
                pTwoRiposte = 1

            if total < 1:
                total = 1
            totalDamage = total
            # # testing data to see that modifiers are carrying over correctly. Delete this when project is finished.
            # msg.append("Roll: " + str(base) + " Modifier: " + str(pOneModifier) + " PA: " + str(
            #             pMod) + " CD: " + str(cMod))
            # display total damage done, and reset passive feat counters (power attack and combat defense)
            msg.append(pOneInfo['name'] + " did [color=red]" + str(total) + "[/color]"
                      " points of damage." + " (Base Roll: [color=blue]" + str(base) + ")[/color]")
            pOnepMod = 0
            pOnecMod = 0
            # check to see if player has evasion.
            if "evasion" in pTwoInfo['feats taken'] and pTwoEvade == 1:
                bEvasion = True
                msg.append(pTwoInfo['name'] + " has an evasion available for use. Type [color=pink]!evasion[/color] to "
                                              "use, or type [color=pink]!pass[/color]")
            elif "improved evasion" in pTwoInfo['feats taken'] and pTwoEvade == 1:
                bEvasion = True
                msg.append(pTwoInfo['name'] + " has an evasion available for use. Type [color=pink]!evasion[/color] to "
                                              "use, or type [color=pink]!pass[/color]")
            elif "greater evasion" in pTwoInfo['feats taken'] and pTwoEvade == 1:
                bEvasion = True
                msg.append(pTwoInfo['name'] + " has an evasion available for use. Type [color=pink]!evasion[/color] to "
                                              "use, or type [color=pink]!pass[/color]")

            # check to see if player has deflect.
            if "deflect" in pTwoInfo['feats taken'] and pTwoDeflect == 1:
                bDeflect = True
                msg.append(pTwoInfo['name'] + " has deflect available for use. Type [color=pink]!deflect[/color] to "
                                              "use, or type [color=pink]!pass[/color]")
            elif "improved deflect" in pTwoInfo['feats taken'] and pTwoDeflect == 1:
                bDeflect = True
                msg.append(pTwoInfo['name'] + " has deflect available for use. Type [color=pink]!deflect[/color] to "
                                              "use, or type [color=pink]!pass[/color]")
            elif "greater deflect" in pTwoInfo['feats taken'] and pTwoDeflect == 1:
                bDeflect = True
                msg.append(pTwoInfo['name'] + " has deflect available for use. Type [color=pink]!deflect[/color] to "
                                              "use, or type [color=pink]!pass[/color]")

            if bEvasion is False:
                if bDeflect is False:
                    # Determine if Quick Strike was used by Player Two and apply damage
                    if pTwoQuickDamage != 0:
                        pOneCurrentHP = pOneCurrentHP - totalDamage - pTwoQuickDamage
                        pTwoQuickDamage = 0
                    else:
                        pTwoCurrentHP = pTwoCurrentHP - totalDamage

                    # Print the scoreboard
                    msg.append(pOneInfo['name'] + ": [color=red]" + str(pOneCurrentHP) + "[/color]/" +
                               str(pOneTotalHP) + "  ||  " + pTwoInfo['name'] + ": [color=red]" +
                               str(pTwoCurrentHP) + "[/color]/" + str(pTwoTotalHP) + " \n" +
                               pTwoInfo['name'] + "'s turn. Type: [color=pink]!usefeat <feat>[/color]"
                                                  " if you wish to use a feat.")

                    if pTwoFeatUsed[0] == "riposte":
                        pTwoRiposte = 5

                    pOnepMod = 0
                    pOnecMod = 0
                    token = new_token
                    iddqd = 0
                    count += 1
                    featToken = 0
                    bGameTimer = True
                    pTwoFeatInfo = None

        return msg, bEvasion, bDeflect, pOneInfo, pTwoInfo, pOnepMod, pTwopMod, pOnecMod, pTwocMod, pOnedMod, pTwodMod, pOnemMod, pTwomMod, \
               pOneRiposte, pTwoRiposte, pOneFeatUsed, pTwoFeatUsed, pOneFeatInfo, pTwoFeatInfo, pOneCurrentHP, pTwoCurrentHP, \
               pOneTotalHP, pTwoTotalHP, pOneEvade, pTwoEvade, pOneDeflect, pTwoDeflect, pOneQuickDamage, pTwoQuickDamage, iddqd,\
               critical, count, featToken, bGameTimer, token, totalDamage

def setup(client):
    client.add_cog(Damage(client))
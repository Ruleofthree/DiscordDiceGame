import os
import json
import random
import time

from discord.ext import commands
from pathlib import Path
from threading import Timer

class Damage(commands.Cog):

    def True_Strike(self, msg, pOneInfo, pTwoInfo, pOnepMod, pTwopMod, pOnecMod, pTwocMod, pOnedMod, pTwodMod, pOnemMod, pTwomMod,
        pOneRiposte, pTwoRiposte, pOneFeatUsed, pTwoFeatUsed, pOneFeatInfo, pTwoFeatInfo, pOneCurrentHP, pTwoCurrentHP,
        pOneTotalHP, pTwoTotalHP, pOneEvade, pTwoEvade, pOneDeflect, pTwoDeflect, pOneQuickDamage, pTwoQuickDamage, iddqd, critical, count, featToken, bGameTimer,
         token, totalDamage, new_token ):
        msg.append(pOneInfo['name'] +
                    " used the feat [color=yellow]'True Strike.'[/color] And forgoes the need to determine if hit was success.")

        # Susanna Added , for ask prompt !evation or !pass
        bEvasion = False
        bDeflect = False


        #--------------------------------PLAYER ONE TRUE STRIKE DAMAGE----------------------------------------------
        # Obtain Player One's base damage and base modifier, and roll damage. Assign 'power attack' and 'combat defense'
        # modifiers to variables, and roll damage.
        pOneBaseDamage = pOneInfo['base damage']
        pOneModifier = pOneInfo['tdamage']
        pOneMinimum, pOneMaximum = pOneBaseDamage.split('d')
        pMod = pOnepMod
        cMod = pOnecMod
        damage = random.randint(int(pOneMinimum), int(pOneMaximum))
        base = damage
        bonusHurt = 0
        nerveDamage = 0
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
        # ensure that no matter what, raw damage can not fall below 1, then assign total damage to variable, and in turn
        # assign it to variable to be accessed for scoreboard.
        if damage < 1:
            damage = 1
        total = int(damage + pOneModifier + pMod - cMod - pTwoInfo['dr'] + bonusHurt)
        if pTwoInfo['dr'] != 0:
            msg.append(pTwoInfo['name'] + " has [color=yellow]thick skin[/color], and has aborbed " +
                       str(pTwoInfo['dr']) + " hp of damage from opponent's roll.")

        # if Player One has 'reckless abandon' apply bonus damage
        if pOneFeatUsed[0] == "reckless abandon":
            damageToPTwo = random.randint(1, 4)
            damageToPOne = random.randint(1, 2)
            pOneCurrentHP = pOneCurrentHP - damageToPOne
            total = total + damageToPTwo
            msg.append(pOneInfo['name'] + " did [color=red]" + str(damageToPOne) + "[/color]"
                       " damage to themself, to deal an additional [color=red]" + str(damageToPTwo) +
                       "[/color] damage to their opponent.")

        elif pOneFeatUsed[0] == "improved reckless abandon":
            damageToPTwo = random.randint(1, 8)
            damageToPOne = random.randint(1, 4)
            pOneCurrentHP = pOneCurrentHP - damageToPOne
            total = total + damageToPTwo
            msg.append(pOneInfo['name'] + " did [color=red]" + str(damageToPOne) + "[/color]"
                       " damage to themself, to deal an additional [color=red]" + str(damageToPTwo) +
                       "[/color] damage to their opponent.")

        elif pOneFeatUsed[0] == "greater reckless abandon":
            damageToPTwo = random.randint(1, 6)
            damageToPOne = random.randint(1, 12)
            pOneCurrentHP = pOneCurrentHP - damageToPOne
            total = total + damageToPTwo
            msg.append(pOneInfo['name'] + " did [color=red]" + str(damageToPOne) + "[/color]"
                       " damage to themself, to deal an additional [color=red]" + str(damageToPTwo) +
                       "[/color] damage to their opponent.")

        # if Player Two used 'quick strike', 'improved quick strike', or 'greater quick strike', apply the return
        # damage here
        pTwoBaseDamage = pTwoInfo['base damage']
        pTwoModifier = pTwoInfo['tdamage']
        pTwoMinimum, pTwoMaximum = pTwoBaseDamage.split('d')
        pMod = pTwopMod
        cMod = pTwocMod
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
                                 " managing to do an additional [color=red]"
                                 + str(pTwoQuickDamage) + "[/color] hp of damage.")

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
        # msg.append("Roll: " + str(base) + " Modifier: " + str(pOneModifier) + " PA: " + str(pMod) + " CE: " + str(cMod))
        # # display total damage done, and reset passive feat counters (power attack and combat defense)
        msg.append(pOneInfo['name'] + " did [color=red]" + str(total) + "[/color]"
                   " points of damage." + "(Base Roll: [color=blue]" + str(base) + ")[/color]")

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
        elif "greater evasion" in pTwoInfo['feats taken'] and pTwoDeflect == 1:
            bDeflect = True
            msg.append(pTwoInfo['name'] + " has deflect available for use. Type [color=pink]!deflect[/color] to "
                       "use, or type [color=pink]!pass[/color]")

        if bEvasion and bDeflect is False:
            # Determine if Quick Strike was used by Player Two and apply damage
            if pTwoQuickDamage != 0:
                pOneCurrentHP = pOneCurrentHP - totalDamage - pTwoQuickDamage
                pOneQuickDamage = 0
            else:
                pTwoCurrentHP = pTwoCurrentHP - totalDamage

            # Print the scoreboard
            msg.append(pOneInfo['name'] + ": [color=red]" + str(pOneCurrentHP) + "[/color]/" +
                        str(pOneTotalHP) + "  ||  " + pTwoInfo['name'] + ": [color=red]" +
                        str(pTwoCurrentHP) + "[/color]/" + str(pTwoTotalHP) + " \n" +
                        pTwoInfo['name'] + "'s turn. Type: [color=pink]!usefeat <feat>[/color]"
                        " if you wish to use a feat.")
            count += 1
            featToken = 0
            pOnepMod = 0
            pOnecMod = 0
            token = 2
            iddqd = 0
            bGameTimer = True
            pTwoFeatInfo = None

        return msg, bEvasion, bDeflect, pOneInfo, pTwoInfo, pOnepMod, pTwopMod, pOnecMod, pTwocMod, pOnedMod, pTwodMod, pOnemMod, pTwomMod,\
        pOneRiposte, pTwoRiposte, pOneFeatUsed, pTwoFeatUsed, pOneFeatInfo, pTwoFeatInfo, pOneCurrentHP, pTwoCurrentHP,\
        pOneTotalHP, pTwoTotalHP, pOneEvade, pTwoEvade, pOneDeflect, pTwoDeflect, pOneQuickDamage, pTwoQuickDamage, iddqd, \
        critical, count, featToken, bGameTimer, token, totalDamage

def setup(client):
    client.add_cog(Damage(client))
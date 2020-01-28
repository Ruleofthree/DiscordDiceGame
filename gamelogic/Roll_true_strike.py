import os
import json
import random
import time

from discord.ext import commands
from pathlib import Path
from threading import Timer

def True_Strike(msg, pOneInfo, pTwoInfo, pOnepMod, pTwopMod, pOnecMod, pTwocMod, pOnedMod, pTwodMod, pOnemMod,
                pTwomMod, pOneRiposte, pTwoRiposte, pOneFeatUsed, pTwoFeatUsed, pOneFeatInfo, pTwoFeatInfo,
                pOneCurrentHP, pTwoCurrentHP, pOneTotalHP, pTwoTotalHP, pOneEvade, pTwoEvade, pOneDeflect, pTwoDeflect,
                pOneQuickDamage, pTwoQuickDamage, critical, count, featToken, bGameTimer, token,
                totalDamage, pOneDeathsDoor, pTwoDeathsDoor, new_token):
    msg.append(pOneInfo['name'] + " used the feat 'True Strike.' And forgoes the need to"
               " determine if hit was success.")

    # Susanna Added , for ask prompt !evasion or !pass
    bEvasion = False
    bDeflect = False

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
        msg.append(pOneInfo['name'] + " used the feat 'titan blow'. Applying a "
                   "50% bonus to damage rolled.")
        damage = damage * float(pOneFeatUsed[1])

    # if Player Two use 'staggering blow' half damage done.
    if pTwoFeatUsed[0] == "staggering blow":
        msg.append(pTwoInfo['name'] + " used the feat 'staggering blow', halving " +
                   pOneInfo['name'] + "'s damage roll")
        damage = damage * float(pTwoFeatUsed[1])

    # If Player One has Hurt Me, Improved Hurt Me, and Greater Hurt Me, check hit points, and apply
    # bonuses.
    number = (pOneCurrentHP / pOneTotalHP) * 100
    percentage = int(number)
    if 'hurt me' in pOneInfo['feats taken']:
        if 33 < percentage <= 66:
            bonusHurt = 1
            msg.append(pOneInfo['name'] + " has become enraged because of 'hurt me', "
                       "and are getting a +" + str(bonusHurt) + "  bonus to their damage.")
        elif percentage <= 33:
            bonusHurt = 2
            msg.append(pOneInfo['name'] + " has become further enraged because of 'hurt me',, "
                       " and are getting a +" + str(bonusHurt) + "  bonus to their damage.")
    elif 'improved hurt me' in pOneInfo['feats taken']:
        if 33 < percentage <= 66:
            bonusHurt = 2
            msg.append(pOneInfo['name'] + " has become enraged because of 'hurt me', "
                       "and are getting a +" + str(bonusHurt) + "  bonus to their damage.")
        elif percentage <= 33:
            bonusHurt = 3
            msg.append(pOneInfo['name'] + " has become enraged because of 'hurt me', "
                       " and are getting a +" + str(bonusHurt) + "  bonus to their damage.")
    elif 'greater hurt me' in pOneInfo['feats taken']:
        if 33 < percentage <= 66:
            bonusHurt = 2
            msg.append(pOneInfo['name'] + " has become enraged because of 'hurt me', "
                       "and are getting a +" + str(bonusHurt) + "  bonus to their damage.")
        elif percentage <= 33:
            bonusHurt = 4
            msg.append(pOneInfo['name'] + " has become further enraged because of 'hurt me', "
                       "and are getting a +" + str(bonusHurt) + "  bonus to their damage.")
    elif 'hurt me more' in pOneInfo['feats taken']:
        if 50 < percentage <= 75:
            bonusHurt = 2
            msg.append(pOneInfo['name'] + " has become enraged because of 'hurt me', "
                       "and are getting a +" + str(bonusHurt) + "  bonus to their damage.")
        elif 25 < percentage <= 50:
            bonusHurt = 4
            msg.append(pOneInfo['name'] + " has become further enraged because of 'hurt me', "
                       "and are getting a +" + str(bonusHurt) + "  bonus to their damage.")
        elif percentage <= 25:
            bonusHurt = 6
            msg.append(pOneInfo['name'] + " has become further enraged because of 'hurt me', "
                       " and are getting a +" + str(bonusHurt) + "  bonus to their damage.")
    # ensure that no matter what, raw damage can not fall below 1, then assign total damage to variable, and in turn
    # assign it to variable to be accessed for scoreboard.
    if damage < 1:
        damage = 1
    total = int(damage + pOneModifier + pMod - cMod - pTwoInfo['tdr'] + bonusHurt + pOneInfo['potiondamage'])
    if pTwoInfo['tdr'] != 0:
        msg.append(pTwoInfo['name'] + " has thick skin, and has absorbed " +
                   str(pTwoInfo['tdr']) + " hp of damage from opponent's roll.")

    # if Player One has 'reckless abandon' apply bonus damage
    if pOneFeatUsed[0] == "reckless abandon":
        damageToPTwo = random.randint(1, 4)
        damageToPOne = random.randint(1, 2)
        pOneCurrentHP = pOneCurrentHP - damageToPOne
        total = total + damageToPTwo
        msg.append(pOneInfo['name'] + " did " + str(damageToPOne) + 
                   " damage to themself, to deal an additional " + str(damageToPTwo) +
                   " damage to their opponent.")

    elif pOneFeatUsed[0] == "improved reckless abandon":
        damageToPTwo = random.randint(1, 8)
        damageToPOne = random.randint(1, 4)
        pOneCurrentHP = pOneCurrentHP - damageToPOne
        total = total + damageToPTwo
        msg.append(pOneInfo['name'] + " did " + str(damageToPOne) + 
                   " damage to themself, to deal an additional " + str(damageToPTwo) +
                   " damage to their opponent.")

    elif pOneFeatUsed[0] == "greater reckless abandon":
        damageToPTwo = random.randint(1, 6)
        damageToPOne = random.randint(1, 12)
        pOneCurrentHP = pOneCurrentHP - damageToPOne
        total = total + damageToPTwo
        msg.append(pOneInfo['name'] + " did " + str(damageToPOne) + 
                   " damage to themself, to deal an additional " + str(damageToPTwo) +
                   " damage to their opponent.")

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
        msg.append(pTwoInfo['name'] + " used 'quick strike,' managing to do an additional "
                    + str(pTwoQuickDamage) + " hp of damage.")

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
        msg.append(pTwoInfo['name'] + " used 'quick strike,' managing to do an additional "
                    + str(pTwoQuickDamage) + " hp of damage.")

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
        msg.append(pTwoInfo['name'] + " used 'quick strike,' managing to do an additional "
                    + str(pTwoQuickDamage) + " hp of damage.")

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
        msg.append(pTwoInfo['name'] + " used 'riposte,' managing to do an additional "
                   + str(pTwoQuickDamage) + " hp of damage.")
        pTwoRiposte = 1

    if total < 1:
        total = 1
    totalDamage = total - pTwoInfo['tdr']
    if totalDamage < 1:
        totalDamage = 1
    # # testing data to see that modifiers are carrying over correctly. Delete this when project is finished.
    # msg.append("Roll: " + str(base) + " Modifier: " + str(pOneModifier) + " PA: " + str(pMod) + " CE: " + str(cMod))
    # # display total damage done, and reset passive feat counters (power attack and combat defense)
    msg.append(pOneInfo['name'] + " did " + str(totalDamage) +
               " points of damage." + "(Base Roll: " + str(base) + ")")

    # check to see if player has evasion.
    if "evasion" in pTwoInfo['feats taken'] and pTwoEvade == 1:
        bEvasion = True
        msg.append(pTwoInfo['name'] + " has an evasion available for use. Type !evasion to "
                   "use, or type !pass")
    elif "improved evasion" in pTwoInfo['feats taken'] and pTwoEvade == 1:
        bEvasion = True
        msg.append(pTwoInfo['name'] + " has an evasion available for use. Type !evasion to "
                   "use, or type !pass")
    elif "greater evasion" in pTwoInfo['feats taken'] and pTwoEvade == 1:
        bEvasion = True
        msg.append(pTwoInfo['name'] + " has an evasion available for use. Type !evasion to "
                   "use, or type !pass")

    # check to see if player has deflect.
    if "deflect" in pTwoInfo['feats taken'] and pTwoDeflect == 1:
        bDeflect = True
        msg.append(pTwoInfo['name'] + " has deflect available for use. Type !deflect to "
                   "use, or type !pass")
    elif "improved deflect" in pTwoInfo['feats taken'] and pTwoDeflect == 1:
        bDeflect = True
        msg.append(pTwoInfo['name'] + " has deflect available for use. Type !deflect to "
                   "use, or type !pass")
    elif "greater evasion" in pTwoInfo['feats taken'] and pTwoDeflect == 1:
        bDeflect = True
        msg.append(pTwoInfo['name'] + " has deflect available for use. Type !deflect to "
                   "use, or type !pass")

    if bEvasion and bDeflect is False:
        # Determine if Quick Strike was used by Player Two and apply damage
        if pTwoQuickDamage != 0:
            pOneCurrentHP = pOneCurrentHP - totalDamage - pTwoQuickDamage
            pOneQuickDamage = 0
        else:
            pTwoCurrentHP = pTwoCurrentHP - totalDamage

        # Check to see if Player has the feat 'death's door', and if it has been triggered already.
        revive = random.randint(1, 100)
        if "deaths door" in pTwoInfo['feats taken'] and pTwoCurrentHP <= 0 \
                and revive <= 50 and pTwoDeathsDoor == 0:
            returnHeal = random.randint(5, 10) + int(pTwoInfo['constitution'] / 2)
            pTwoCurrentHP += returnHeal
            pTwoDeathsDoor = 1
            msg.append(
                pTwoInfo['name'] + " has returned from death's door, regaining " + str(returnHeal) +
                " hit points.")
        elif "improved deaths door" in pTwoInfo['feats taken'] and pTwoCurrentHP <= 0 \
                and revive <= 75 and pTwoDeathsDoor == 0:
            returnHeal = random.randint(5, 15) + int(pTwoInfo['constitution'] / 2)
            pTwoCurrentHP += returnHeal
            pTwoDeathsDoor = 1
            msg.append(
                pTwoInfo['name'] + " has returned from death's door, regaining " + str(returnHeal) +
                " hit points.")
        elif "greater deaths door" in pTwoInfo['feats taken'] and pTwoCurrentHP <= 0 \
                and revive <= 100 and pTwoDeathsDoor == 1:
            returnHeal = random.randint(5, 20) + int(pTwoInfo['constitution'] / 2)
            pTwoCurrentHP += returnHeal
            pTwoDeathsDoor = 0
            msg.append(
                pTwoInfo['name'] + " has returned from death's door, regaining " + str(returnHeal) +
                " hit points.")

        # If it is the end of Player One's turn, and they have regeneration:
        if token == 1 and pOneInfo['regeneration'] != 0 and pOneCurrentHP < pOneTotalHP:
            msg.append(pOneInfo['name'] + " has regenerated " + str(pOneInfo['regeneration']) + " hp.")
            pOneCurrentHP += pOneInfo['regeneration']

        # If it is the end of Player Two's turn, and they have regeneration:
        elif token == 2 and pOneInfo['regeneration'] != 0 and pOneCurrentHP < pOneTotalHP:
            msg.append(pOneInfo['name'] + " has regenerated " + str(pOneInfo['regeneration']) + " hp.")
            pOneCurrentHP += pOneInfo['regeneration']

        # Print the scoreboard
        msg.append(pOneInfo['name'] + ": " + str(pOneCurrentHP) + "/" +
                   str(pOneTotalHP) + "  ||  " + pTwoInfo['name'] + ": " +
                   str(pTwoCurrentHP) + "/" + str(pTwoTotalHP) + " \n" +
                   pTwoInfo['name'] + "'s turn. Type: !usefeat <feat>"
                   " if you wish to use a feat.")
        count += 1
        featToken = 0
        pOnepMod = 0
        pOnecMod = 0
        token = 2

        bGameTimer = True
        pTwoFeatInfo = None

    return msg, bEvasion, bDeflect, pOneInfo, pTwoInfo, pOnepMod, pTwopMod, pOnecMod, pTwocMod, pOnedMod, pTwodMod,\
        pOnemMod, pTwomMod, pOneRiposte, pTwoRiposte, pOneFeatUsed, pTwoFeatUsed, pOneFeatInfo, pTwoFeatInfo,\
        pOneCurrentHP, pTwoCurrentHP, pOneTotalHP, pTwoTotalHP, pOneEvade, pTwoEvade, pOneDeflect, pTwoDeflect,\
        pOneQuickDamage, pTwoQuickDamage, critical, count, featToken, bGameTimer, token, totalDamage,\
        pOneDeathsDoor, pTwoDeathsDoor

import os
import json
import random
import time
from pathlib import Path
from threading import Timer

from gamelogic import Roll_not_strike
from gamelogic import Roll_true_strike
from gamelogic import playerone_zero_current_hp
from gamelogic import playertwo_zero_current_hp


def evasionTimer(self):
    pass


def message_roll(character, message, channel, unspoiledArena, charFolder, opponent, playerOne, playerTwo,
                 winner, pOneInfo, pTwoInfo, featToken, game, count, token, critical, bonusHurt, totalDamage,
                 pOneTotalHP, pTwoTotalHP, pOneCurrentHP, pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod, pOnemMod,
                 pOneEvade, pOneDeflect, pOneRiposte, pOneQuickDamage, pOneFeatInfo, pOneSpentFeat, pTwopMod,
                 pTwocMod, pTwodMod, pTwomMod, pTwoEvade, pTwoDeflect, pTwoRiposte, pTwoQuickDamage, pTwoFeatInfo,
                 pTwoSpentFeat, pOneLevel, pTwoLevel, xp, currentPlayerXP, nextLevel, levelUp, pOneDeathsDoor,
                 pTwoDeathsDoor, pOneTempDR, pTwoTempDR):
    msg = []
    bGameTimer = False
    bTimer = True

    # Susanna Added , for ask prompt !evasion or !pass
    bEvasion = False
    bDeflect = False
    # ensures the command can only be used when combat is taking place. To prevent trolls from spamming commands
    if game == 1:
        # assign both player's feat selections to variables
        pOneFeatUsed = pOneFeatInfo
        pTwoFeatUsed = pTwoFeatInfo

        # If a feat wasn't used by a player, assign it default values.
        if pOneFeatUsed is None:
            pOneFeatUsed = ["none", 0]
        if pTwoFeatUsed is None:
            pTwoFeatUsed = ["none", 0]
        nerveDamage = 0
        base = 0

        # ensures the command can only be used by player one, when it is their turn. To prevent trolls from
        # spamming commands.
        if character.lower() == playerOne and token == 1:
            # If the feat used was 'true strike' forgo rolling to see if player hit opponent, and go
            # straight to damage.
            if pOneFeatUsed[0] == "true strike":
                msg, bEvasion, bDeflect, pOneInfo, pTwoInfo, pOnepMod, pTwopMod, pOnecMod, pTwocMod, pOnedMod,\
                    pTwodMod, pOnemMod, pTwomMod, pOneRiposte, pTwoRiposte, pOneFeatUsed, pTwoFeatUsed,\
                    pOneFeatInfo, pTwoFeatInfo, pOneCurrentHP, pTwoCurrentHP, pOneTotalHP, pTwoTotalHP, pOneEvade,\
                    pTwoEvade, pOneDeflect, pTwoDeflect, pOneQuickDamage, pTwoQuickDamage, critical, count,\
                    featToken, bGameTimer, token, totalDamage, pOneDeathsDoor, pTwoDeathsDoor =\
                    Roll_True_Strike(msg, pOneInfo, pTwoInfo, pOnepMod, pTwopMod, pOnecMod, pTwocMod, pOnedMod, pTwodMod,
                                pOnemMod, pTwomMod, pOneRiposte, pTwoRiposte, pOneFeatUsed, pTwoFeatUsed,
                                pOneFeatInfo, pTwoFeatInfo, pOneCurrentHP, pTwoCurrentHP, pOneTotalHP, pTwoTotalHP,
                                pOneEvade, pTwoEvade, pOneDeflect, pTwoDeflect, pOneQuickDamage, pTwoQuickDamage,
                                critical, count, featToken, bGameTimer, token, totalDamage, pOneDeathsDoor,
                                pTwoDeathsDoor, 2)

            # Otherwise, continue on with the bulk of this method.
            else:
                msg, bEvasion, bDeflect, pOneInfo, pTwoInfo, pOnepMod, pTwopMod, pOnecMod, pTwocMod, pOnedMod,\
                    pTwodMod, pOnemMod, pTwomMod, pOneRiposte, pTwoRiposte, pOneFeatUsed, pTwoFeatUsed,\
                    pOneFeatInfo, pTwoFeatInfo, pOneCurrentHP, pTwoCurrentHP, pOneTotalHP, pTwoTotalHP, pOneEvade,\
                    pTwoEvade, pOneDeflect, pTwoDeflect, pOneQuickDamage, pTwoQuickDamage, critical, count,\
                    featToken, bGameTimer, token, totalDamage, pOneDeathsDoor, pTwoDeathsDoor,\
                    pOneTempDR, pTwoTempDR =\
                    Not_True_Strike(msg, pOneInfo, pTwoInfo, pOnepMod, pTwopMod, pOnecMod, pTwocMod, pOnedMod,
                                    pTwodMod, pOnemMod, pTwomMod, pOneRiposte, pTwoRiposte, pOneFeatUsed,
                                    pTwoFeatUsed, pOneFeatInfo, pTwoFeatInfo, pOneCurrentHP, pTwoCurrentHP,
                                    pOneTotalHP, pTwoTotalHP, pOneEvade, pTwoEvade, pOneDeflect, pTwoDeflect,
                                    pOneQuickDamage, pTwoQuickDamage, critical, count, featToken,
                                    bGameTimer, token, totalDamage, pOneDeathsDoor, pTwoDeathsDoor,
                                    pOneTempDR, pTwoTempDR, 2)
            # If Player Two is dead, state such, and how many rounds it took to win. Calculate and distribute xp.
            # reset game and token counters back to 0.
            if pTwoCurrentHP <= 0:
                pTwoSpentFeat = []
                pOneSpentFeat = []
                game = 0
                token = 0
                rounds = int(count / 2)
                bGameTimer = False
                count = 0
                msg, pOneInfo, pTwoInfo, pOneDeathsDoor, pTwoDeathsDoor =\
                    playertwo_currentHP_less_zero(msg, pOneInfo, pTwoInfo, playerOne, playerTwo, pOneCurrentHP,
                                                  pTwoCurrentHP, pOneLevel, pTwoLevel, charFolder, rounds,
                                                  pOneDeathsDoor, pTwoDeathsDoor)
        # ensures the command can only be used by player two, when it is their turn. To prevent trolls from
        # spamming commands.
        elif character.lower() == playerTwo and token == 2:
            # If the feat used was 'true strike' forgo rolling to see if player hit opponent, and go
            # straight to damage.
            if pTwoFeatUsed[0] == "true strike":
                msg, bEvasion, bDeflect, pTwoInfo, pOneInfo, pTwopMod, pOnepMod, pTwocMod, pOnecMod, pTwodMod,\
                    pOnedMod, pTwomMod, pOnemMod, pTwoRiposte, pOneRiposte, pTwoFeatUsed, pOneFeatUsed,\
                    pTwoFeatInfo, pOneFeatInfo, pTwoCurrentHP, pOneCurrentHP, pTwoTotalHP, pOneTotalHP,\
                    pTwoEvade, pOneEvade, pTwoDeflect, pOneDeflect, pTwoQuickDamage, pOneQuickDamage,\
                    critical, count, featToken, bGameTimer, token, totalDamage, pTwoDeathsDoor, pOneDeathsDoor =\
                    Roll_True_Strike(msg, pTwoInfo, pOneInfo, pTwopMod, pOnepMod, pTwocMod, pOnecMod, pTwodMod,
                                    pOnedMod, pTwomMod, pOnemMod, pTwoRiposte, pOneRiposte, pTwoFeatUsed,
                                    pOneFeatUsed, pTwoFeatInfo, pOneFeatInfo, pTwoCurrentHP, pOneCurrentHP,
                                    pTwoTotalHP, pOneTotalHP, pTwoEvade, pOneEvade, pTwoDeflect, pOneDeflect,
                                    pTwoQuickDamage, pOneQuickDamage, critical, count, featToken,
                                    bGameTimer, token, totalDamage, pTwoDeathsDoor, pOneDeathsDoor, 1)

            # Otherwise, continue on with the bulk of this method.
            else:
                msg, bEvasion, bDeflect, pTwoInfo, pOneInfo, pTwopMod, pOnepMod, pTwocMod, pOnecMod, pTwodMod,\
                    pOnedMod, pTwomMod, pOnemMod, pTwoRiposte, pOneRiposte, pTwoFeatUsed, pOneFeatUsed,\
                    pTwoFeatInfo, pOneFeatInfo, pTwoCurrentHP, pOneCurrentHP, pTwoTotalHP, pOneTotalHP, pTwoEvade,\
                    pOneEvade, pTwoDeflect, pOneDeflect, pTwoQuickDamage, pOneQuickDamage, critical, count,\
                    featToken, bGameTimer, token, totalDamage, pTwoDeathsDoor, pOneDeathsDoor, pTwoTempDR,\
                    pOneTempDR =\
                    Not_True_Strike(msg, pTwoInfo, pOneInfo, pTwopMod, pOnepMod, pTwocMod, pOnecMod, pTwodMod,
                                    pOnedMod, pTwomMod, pOnemMod, pTwoRiposte, pOneRiposte, pTwoFeatUsed,
                                    pOneFeatUsed, pTwoFeatInfo, pOneFeatInfo, pTwoCurrentHP, pOneCurrentHP,
                                    pTwoTotalHP, pOneTotalHP, pTwoEvade, pOneEvade, pTwoDeflect, pOneDeflect,
                                    pTwoQuickDamage, pOneQuickDamage, critical, count, featToken,
                                    bGameTimer, token, totalDamage, pTwoDeathsDoor, pOneDeathsDoor,
                                    pTwoTempDR, pOneTempDR, 1)

            # If Player One is dead, state such, and how many rounds it took to win. Calculate and distribute xp.
            # reset game and token counters back to 0.
            if pOneCurrentHP <= 0:
                pTwoSpentFeat = []
                pOneSpentFeat = []
                game = 0
                token = 0
                rounds = int(count / 2)
                bGameTimer = False
                count = 0
                msg, pTwoInfo, pOneInfo, pOneDeathsDoor, pTwoDeathsDoor =\
                    playerone_currentHP_less_zero(msg, pOneInfo, pTwoInfo, playerOne, playerTwo, pOneCurrentHP,
                                                  pTwoCurrentHP, pOneLevel, pTwoLevel, charFolder, rounds,
                                                  pOneDeathsDoor, pTwoDeathsDoor)
        else:
            msg.append("Either it's not your turn, or you aren't even fighting. Either way, No.")
    else:
        msg.append("This command does nothing right now. No combat is taking place.")

    return msg, bEvasion, bDeflect, bGameTimer, opponent, playerOne, playerTwo, winner, pOneInfo, pTwoInfo,\
        featToken, game, count, token, critical, bonusHurt, totalDamage, pOneTotalHP, pTwoTotalHP, \
        pOneCurrentHP, pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod, pOnemMod, pOneEvade, pOneDeflect, \
        pOneRiposte, pOneQuickDamage, pOneFeatInfo, pOneSpentFeat, pTwopMod, pTwocMod, pTwodMod, \
        pTwomMod, pTwoEvade, pTwoDeflect, pTwoRiposte, pTwoQuickDamage, pTwoFeatInfo, pTwoSpentFeat, pOneLevel,\
        pTwoLevel, xp, currentPlayerXP, nextLevel, levelUp, pOneDeathsDoor, pTwoDeathsDoor, pOneTempDR,\
        pTwoTempDR
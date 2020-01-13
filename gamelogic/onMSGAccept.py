import os
import json
import random
import time
from pathlib import Path
from threading import Timer


def message_accept(charFolder, accepted, game, opponentID, pOneInfo):
    msg = []
    print(opponentID)
    print(accepted)
    pTwoInfo = None
    new_game = None
    bTimer = False
    bGameTimer = False
    new_oppenent = None
    token = None
    playerTwo = accepted
    if game == 0.5:

        if opponentID == accepted:

            # since challenge is being accepted, set game counter to 1.
            bTimer = True

            new_game = 1
            new_opponent = ""
            charSheet = open(charFolder + opponentID + ".txt", "r", encoding="utf-8")
            pTwoInfo = json.load(charSheet)
            charSheet.close()

            # since if a person !accepts a challenge, that mights a fight is about to take place. Just go
            # straight into combat by starting initiative. Depending on who wins, token is set to 1 or 2. Tokens
            # will be used to determine whose turn it is during the fight, and lock out anyone using fight commands
            # but the player whose turn it is.
            msg.append("Rolling Initiative to see who goes first. In result of tie, person with "
                       "highest dexterity modifier goes first. Should that tie as well, then fuck "
                       "it, coin flip. " + pOneInfo['name'] + " wins on a One.")

            playerOneInit = random.randint(1, 20)
            playerOneMod = int(pOneInfo['dexterity'] / 2)
            totalOne = playerOneInit + playerOneMod

            playerTwoInit = random.randint(1, 20)
            playerTwoMod = int(pTwoInfo['dexterity'] / 2)
            totalTwo = playerTwoInit + playerTwoMod

            msg.append("\n" + pOneInfo['name'] + " rolled: " + str(playerOneInit) + " + " +
                       str(playerOneMod) + " and got " + str(totalOne) + "\n" + pTwoInfo[
                           'name'] +
                       " rolled: " + str(playerTwoInit) + " + " + str(playerTwoMod) +
                       " and got " + str(totalTwo) + "")

            if totalOne > totalTwo:
                msg.append(pOneInfo['name'] + " Goes first")
                token = 1
                msg.append("Type !usefeat <feat> to use a feat, or spend points for your passiv a passive, such as !pattack."
                           "(use !feathelp in DM with Fight Bot for more help)")

            elif totalTwo > totalOne:
                msg.append(pTwoInfo['name'] + " Goes first")
                token = 2
                msg.append("Type !usefeat <feat> to use a feat, or spend points for your passiv a passive, such as !pattack."
                           "(use !feathelp in DM with Fight Bot for more help)")

            elif totalOne == totalTwo:
                msg.append(pOneInfo['name'] + "'s dexterity: " + str(playerOneMod) +
                           "\n" + pTwoInfo['name'] + "'s dexterity: " + str(playerTwoMod) +
                           "")

                if playerOneMod > playerTwoMod:
                    msg.append(pOneInfo['name'] + "Type !usefeat <feat> to use a feat, or spend points for your a passive,"
                               " such as !pattack. (use !feathelp in DM with Fight Bot for more help)")
                    token = 1


                elif playerOneMod < playerTwoMod:
                    msg.append(pTwoInfo['name'] + "Type !usefeat <feat> to use a feat, or spend points for your a passive,"
                               " such as !pattack. (use !feathelp in DM with Fight Bot for more help)")
                    token = 2


                else:
                    value = random.randint(1, 2)

                    if value == 1:
                        msg.append(
                            pOneInfo['name'] + "Type !usefeat <feat> to use a feat, or spend points for your a passive,"
                                               " such as !pattack. (use !feathelp in DM with Fight Bot for more help)")
                        token = 1


                    else:
                        msg.append(
                            pTwoInfo['name'] + "Type !usefeat <feat> to use a feat, or spend points for your a passive,"
                                               " such as !pattack. (use !feathelp in DM with Fight Bot for more help)")
                        token = 2
            bGameTimer = True

        else:
            msg.append("I may be a bot, but I'm pretty sure you aren't " + opponent + ". A for"
                       " effort, though.")
    else:
        msg.append("A fight is already taking place. Wait your turn.")

    return msg, pTwoInfo, new_game, playerTwo, bTimer, bGameTimer, new_oppenent, token
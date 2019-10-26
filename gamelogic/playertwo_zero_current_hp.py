import os
import json
import random
import time

from discord.ext import commands
from pathlib import Path
from threading import Timer


def playertwo_currentHP_less_zero(msg, pTwoInfo, pOneInfo, playerTwo, playerOne, pOneCurrentHP, pTwoCurrentHP,
                                  pOneLevel, pTwoLevel, charFolder, rounds):

    msg.append(pTwoInfo['name'] + " won in "
               + str(int(rounds)) + " rounds")
    level = abs(pOneLevel - pTwoLevel)
    rounds = int(rounds / 2)
    base = 20
    if level == 0:
        level = 1
    if level <= 3:
        differHP = abs(pOneCurrentHP - pTwoCurrentHP)
        xp = int((20 * level) + (differHP * rounds))
        gold = int((((base * level) ** 1.06) + ((rounds * 2) + base)))
    elif 3 > level <= 6:
        msg.append("As the level difference between opponents is between 3 and 6, total xp is reduced by half.")
        differHP = abs(pOneCurrentHP - pTwoCurrentHP)
        xp = int((20 * level) + (differHP * rounds) / 2)
        gold = int((((base * level) ** 1.06) + ((rounds * 2) + base)) / 2)
    elif 7 > level < 10:
        msg.append("As the level difference between opponents is between 7 and 9, total xp is divided by four.")
        differHP = abs(pOneCurrentHP - pTwoCurrentHP)
        xp = int(((20 * level) + (differHP * rounds)) / 4)
        gold = int((((base * level) ** 1.06) + ((rounds * 2) + base)) / 4)
    else:
        msg.append("As the level difference was greater than 10, no XP was awarded.")

    msg.append(pTwoInfo['name'] + " has earned: " + str(xp) + " experience points and" +
               str(gold) + " gold.\n " + pOneInfo['name'] + " has earned: " + str(int(xp / 2)) + "")
    pTwoXP = int(pTwoInfo['currentxp'] + xp)
    pTwoGold = int(pTwoInfo['gold'] + gold)
    pOneXP = int(pOneInfo['currentxp'] + (xp / 2))
    nextLevel = pTwoInfo['nextlevel']
    winner = playerTwo
    loser = playerOne
    levelUp = pTwoInfo['level']

    # Record xp gained and win
    with open(charFolder + winner + '.txt', 'r+') as file:
        pTwoInfo = json.load(file)
        pTwoInfo['currentxp'] = pTwoXP
        pTwoInfo['gold'] = pTwoGold
        pTwoInfo['wins'] += 1
        file.seek(0)
        file.write(json.dumps(pTwoInfo, ensure_ascii=False, indent=2))
        file.truncate()
        file.close()

    # Record loss
    with open(charFolder + loser + '.txt', 'r+') as file:
        pOneInfo = json.load(file)
        pOneInfo['currentxp'] = pOneXP
        pOneInfo['losses'] += 1
        file.seek(0)
        file.write(json.dumps(pOneInfo, ensure_ascii=False, indent=2))
        file.truncate()
        file.close()

    if pTwoInfo['currentxp'] >= nextLevel:
        newLevel = levelUp + 1
        levels = [5, 10, 15, 20]
        newLevel = str(newLevel)
        msg.append("" + pTwoInfo['name'].capitalize() + " has reached level "
                   + newLevel + "!")
        levelFile = open(charFolder + "levelchart.txt", "r", encoding="utf-8")
        levelDict = json.load(levelFile)
        levelFile.close()
        with open(charFolder + winner + '.txt', 'r+') as file:
            charData = json.load(file)
            charData['level'] = int(newLevel)
            if charData['level'] in levels:
                if charData['trait'] == 'regeneration':
                    charData['regeneration'] += 2
                elif charData['trait'] == 'brawler':
                    charData['strength'] += 1
                elif charData['trait'] == 'hearty':
                    charData['constitution'] += 1
                elif charData['trait'] == 'nimble':
                    charData['dexterity'] += 1
                elif charData['trait'] == 'thickskinned':
                    charData['dr'] += 1
            charData['hp'] = int(levelDict[newLevel][0])
            charData['base damage'] = str(levelDict[newLevel][1]) + "d" + str(
                levelDict[newLevel][2])
            if charData['total feats'] == levelDict[newLevel][4]:
                charData['total feats'] = levelDict[newLevel][4]
            else:
                msg.append(pTwoInfo['name'] + " has a new feat slot to fill. Use the "
                                              "!feat command to select new feat.")
                charData['total feats'] = levelDict[newLevel][4]
                charData['remaining feats'] = 1
            if charData['ap'] == levelDict[newLevel][3]:
                charData['ap'] = levelDict[newLevel][3]
            else:
                msg.append(pTwoInfo['name'] + " has a new ability point to spend. "
                                              "PM the !add command to Unspoiled "
                                              "Desire, to spend it.")
                charData['ap'] = levelDict[newLevel][3]
            charData['hit'] = int(levelDict[newLevel][5])
            charData['damage'] = int(levelDict[newLevel][5])
            charData['ac'] = int(levelDict[newLevel][6])
            charData['currentxp'] = pTwoXP
            charData['gold'] = pTwoGold
            charData['nextlevel'] = int(levelDict[newLevel][7])
            file.seek(0)
            file.write(json.dumps(charData, ensure_ascii=False, indent=2))
            file.truncate()
            file.close()

    if pOneInfo['currentxp'] >= pOneInfo['nextlevel']:
        pOneInfo['level'] = pOneInfo['level'] + 1
        newLevel = str(pOneInfo['level'])
        msg.append("" + pOneInfo['name'].capitalize() + " has reached level "
                   + newLevel + "!")
        levelFile = open(charFolder + "levelchart.txt", "r", encoding="utf-8")
        levelDict = json.load(levelFile)
        levelFile.close()
        with open(charFolder + loser + ".txt", "r+", encoding="utf-8") as file:
            charData = json.load(file)
            charData['level'] = int(newLevel)
            charData['hp'] = int(levelDict[newLevel][0])
            charData['base damage'] = str(levelDict[newLevel][1]) + "d" + str(
                levelDict[newLevel][2])
            if charData['total feats'] == levelDict[newLevel][4]:
                charData['total feats'] = levelDict[newLevel][4]
            else:
                msg.append(pOneInfo['name'] + " has a new feat slot to fill. Use the "
                                              "!feat command to select new feat.")
                charData['total feats'] = levelDict[newLevel][4]
                charData['remaining feats'] = 1
            if charData['ap'] == levelDict[newLevel][3]:
                charData['ap'] = levelDict[newLevel][3]
            else:
                msg.append(pOneInfo['name'] + " has a new ability point to spend. "
                                              "PM the !add command to Unspoiled "
                                              "Desire, to spend it.")
                charData['ap'] = levelDict[newLevel][3]
            charData['hit'] = int(levelDict[newLevel][5])
            charData['damage'] = int(levelDict[newLevel][5])
            charData['ac'] = int(levelDict[newLevel][6])
            charData['currentxp'] = pTwoXP
            charData['nextlevel'] = int(levelDict[newLevel][7])
            file.seek(0)
            file.write(json.dumps(charData, ensure_ascii=False, indent=2))
            file.truncate()
            file.close()
    return msg, pOneInfo, pTwoInfo
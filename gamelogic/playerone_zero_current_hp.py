import os
import json
import random
import time

from discord.ext import commands
from pathlib import Path
from threading import Timer

def playerone_currentHP_less_zero(msg, pOneInfo, pTwoInfo, playerOne, playerTwo, pOneCurrentHP, pTwoCurrentHP,
                                  pOneLevel, pTwoLevel, charFolder, rounds, pOneDeathsDoor, pTwoDeathsDoor):
    pOneDeathsDoor = 0
    ptwoDeathsDoor = 0
    msg.append(pTwoInfo['name'] + " won in "
               + str(int(rounds)) + " rounds")
    level = abs(pOneLevel - pTwoLevel)
    base = 100
    if level == 0:
        level = 1
    if level <= 5:
        differHP = abs(pOneCurrentHP - pTwoCurrentHP)
        if differHP > 20:
            differHP = 20
        xp = int((base * level) + (differHP * rounds))
        gold = int((((base * level) ** 1.06) + ((rounds * 2) + base)))

    elif 5 > level <= 10:
        msg.append("As the level difference between opponents is between 5 and 10, total reward is reduced by half.")
        differHP = abs(pOneCurrentHP - pTwoCurrentHP)
        if differHP > 20:
            differHP = 20
        xp = int((base * level) + (differHP * rounds) / 2)
        gold = int((((base * level) ** 1.06) + ((rounds * 2) + base)) / 2)

    elif 10 > level:
        msg.append("As the level difference between opponents is is between 11 and 15, total reward is divided by "
                   "four.")
        differHP = abs(pOneCurrentHP - pTwoCurrentHP)
        if differHP > 20:
            differHP = 20
        xp = int(((base * level) + (differHP * rounds)) / 4)
        gold = int((((base * level) ** 1.06) + ((rounds * 2) + base)) / 4)

    msg.append(pTwoInfo['name'] + " has earned: " + str(xp) +
               " experience points and  " + str(gold) + " gold.\n" +
               pOneInfo['name'] + " has earned: " + str(int(xp / 2)) +
               " experience points and  " +
               str(int(gold / 2)) + " gold.")
    pTwoXP = int(pTwoInfo['currentxp'] + xp)
    pTwoRenown = int(pTwoInfo['gold'] + gold)
    pOneXP = int(pOneInfo['currentxp'] + (xp / 2))
    pOneRenown = int(pOneInfo['gold'] + (gold / 2))
    nextLevel = pTwoInfo['nextlevel']
    winner = playerTwo
    loser = playerOne
    levelUp = pTwoInfo['level']

    # Record xp gained and win
    with open(charFolder + winner + '.txt', 'r+') as file:
        pTwoInfo = json.load(file)
        pTwoInfo['currentxp'] = pTwoXP
        pTwoInfo['gold'] = pTwoRenown
        pTwoInfo['wins'] += 1
        pTwoInfo["potioneffect"] = ""
        pTwoInfo["potionhit"] = 0
        pTwoInfo["potiondamage"] = 0
        pTwoInfo["potionac"] = 0
        pTwoInfo["potionhp"] = 0
        pTwoInfo["potiondr"] = 0
        pTwoInfo["potioninitiative"] = 0
        file.seek(0)
        file.write(json.dumps(pTwoInfo, ensure_ascii=False, indent=2))
        file.truncate()
        file.close()

    # Record loss
    with open(charFolder + loser + '.txt', 'r+') as file:
        pOneInfo = json.load(file)
        pOneInfo['currentxp'] = pOneXP
        pOneInfo['gold'] = pOneRenown
        pOneInfo['losses'] += 1
        pOneInfo["potioneffect"] = ""
        pOneInfo["potionhit"] = 0
        pOneInfo["potiondamage"] = 0
        pOneInfo["potionac"] = 0
        pOneInfo["potionhp"] = 0
        pOneInfo["potionblur"] = 0
        pOneInfo["potioninitiative"] = 0
        file.seek(0)
        file.write(json.dumps(pOneInfo, ensure_ascii=False, indent=2))
        file.truncate()
        file.close()

    if pTwoInfo['currentxp'] >= nextLevel:
        newLevel = levelUp + 1
        newLevel = str(newLevel)
        levels = [5, 10, 15, 20]
        msg.append("[b]" + pTwoInfo['name'].capitalize() + " has reached level "
                   + newLevel + "![/b]")
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
            charData['gold'] = pTwoRenown
            charData['nextlevel'] = int(levelDict[newLevel][7])
            file.seek(0)
            file.write(json.dumps(charData, ensure_ascii=False, indent=2))
            file.truncate()
            file.close()

    if pOneInfo['currentxp'] >= pOneInfo['nextlevel']:
        pOneInfo['level'] = pOneInfo['level'] + 1
        newLevel = str(pOneInfo['level'])
        levels = [5, 10, 15, 20]
        msg.append("[b]" + pOneInfo['name'].capitalize() + " has reached level " + newLevel +
                   "![/b]")
        levelFile = open(charFolder + "levelchart.txt", "r", encoding="utf-8")
        levelDict = json.load(levelFile)
        levelFile.close()
        with open(charFolder + loser + ".txt", "r+", encoding="utf-8") as file:
            charData = json.load(file)
            charData['level'] = int(newLevel)
            if charData['level'] in levels:
                if charData['trait'] == 'regeneration':
                    charData['regeneration'] += 2
                elif charData['trait'] == 'brawler':
                    charData['traithit'] += 1
                elif charData['trait'] == 'thug':
                    charData['traitdamage'] += 1
                elif charData['trait'] == 'hearty':
                    charData['traithp'] += 5
                elif charData['trait'] == 'nimble':
                    charData['traitac'] += 1
                elif charData['trait'] == 'thickskinned':
                    charData['traitdr'] += 1
                elif charData['trait'] == 'opportunist':
                    charData['opportunist'] += 1
                elif charData['trait'] == 'nebulous':
                    charData['blur'] += 1
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
            charData['currentxp'] = pOneXP
            charData['gold'] = pOneRenown
            charData['nextlevel'] = int(levelDict[newLevel][7])
            file.seek(0)
            file.write(json.dumps(charData, ensure_ascii=False, indent=2))
            file.truncate()
            file.close()
    return msg, pOneInfo, pTwoInfo, pOneDeathsDoor, pTwoDeathsDoor

def setup(client):
    client.add_cog(POneXP(client))
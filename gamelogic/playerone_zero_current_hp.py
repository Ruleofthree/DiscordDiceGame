import os
import json
import random
import time

from discord.ext import commands
from pathlib import Path
from threading import Timer

class POneXP(commands.Cog):
    def __init__(self, client):
        self.client = client

    def playerone_currentHP_less_zero(self, msg, pOneInfo, pTwoInfo, playerOne, playerTwo, pOneCurrentHP, pTwoCurrentHP,
                                      pOneLevel,
                                      pTwoLevel, charFolder, rounds):
        # charSheet = open(charFolder + playerOne.lower() + ".txt", "r", encoding="utf-8")
        # pOneInfo = json.load(charSheet)
        # charSheet = open(charFolder + playerTwo.lower() + ".txt", "r", encoding="utf-8")
        # pTwoInfo = json.load(charSheet)
        msg.append(pOneInfo['name'] + " won in [color=red]"
                   + str(int(rounds)) + "[/color] rounds")
        level = abs(pOneLevel - pTwoLevel)
        rounds = int(rounds / 2)
        if level == 0:
            level = 1
        if level <= 3:
            differHP = abs(pOneCurrentHP - pTwoCurrentHP)
            xp = int((20 * level) + (differHP * rounds))

        elif 3 > level <= 6:
            msg.append("As the level difference between opponents is between 3 and 6, total xp is reduced by half.")
            differHP = abs(pOneCurrentHP - pTwoCurrentHP)
            xp = int((20 * level) + (differHP * rounds) / 2)

        elif 7 > level < 10:
            msg.append("As the level difference between opponents is between 7 and 9, total xp is divied by four.")
            differHP = abs(pOneCurrentHP - pTwoCurrentHP)
            xp = int(((20 * level) + (differHP * rounds)) / 4)
        else:
            msg.append("As the level difference was greater than 10, no XP was awarded.")

        msg.append(pOneInfo['name'] + " has earned: [color=red]" +
                   str(xp) + "[/color] experience points.\n " +
                   pTwoInfo['name'] + " has earned: [color=red]"
                   + str(int(xp / 2)) + "[/color]")
        pOneXP = int(pOneInfo['currentxp'] + xp)
        pTwoXP = int(pTwoInfo['currentxp'] + (xp / 2))
        nextLevel = pOneInfo['nextlevel']
        winner = playerOne
        loser = playerTwo
        levelUp = pOneInfo['level']

        # Record xp gained and win
        with open(charFolder + winner + '.txt', 'r+') as file:
            pOneInfo = json.load(file)
            pOneInfo['currentxp'] = pOneXP
            pOneInfo['wins'] += 1
            file.seek(0)
            file.write(json.dumps(pOneInfo, ensure_ascii=False, indent=2))
            file.truncate()
            file.close()

        # Record loss
        with open(charFolder + loser + '.txt', 'r+') as file:
            pTwoInfo = json.load(file)
            pTwoInfo['currentxp'] = pTwoXP
            pTwoInfo['losses'] += 1
            file.seek(0)
            file.write(json.dumps(pTwoInfo, ensure_ascii=False, indent=2))
            file.truncate()
            file.close()

        if pOneInfo['currentxp'] >= nextLevel:
            newLevel = levelUp + 1
            newLevel = str(newLevel)
            msg.append("[color=red][b]" + pOneInfo['name'].capitalize() + " has reached level "
                       + newLevel + "![/b][/color]")
            levelFile = open(charFolder + "levelchart.txt", "r", encoding="utf-8")
            levelDict = json.load(levelFile)
            levelFile.close()
            with open(charFolder + winner + '.txt', 'r+') as file:
                charData = json.load(file)
                charData['level'] = int(newLevel)
                charData['hp'] = int(levelDict[newLevel][0])
                charData['base damage'] = str(levelDict[newLevel][1]) + "d" + str(
                    levelDict[newLevel][2])
                if charData['total feats'] == levelDict[newLevel][4]:
                    charData['total feats'] = levelDict[newLevel][4]
                else:
                    msg.append(pOneInfo['name'] + " has a new feat slot to fill. Use the "
                                                  "[color=pink]!feat[/color] command to select new feat.")
                    charData['total feats'] = levelDict[newLevel][4]
                    charData['remaining feats'] = 1
                if charData['ap'] == levelDict[newLevel][3]:
                    charData['ap'] = levelDict[newLevel][3]
                else:
                    msg.append(pOneInfo['name'] + " has a new ability point to spend. "
                                                  "PM the [color=pink]!add[/color] command to Unspoiled "
                                                  "Desire, to spend it.")
                    charData['ap'] = levelDict[newLevel][3]
                charData['hit'] = int(levelDict[newLevel][5])
                charData['damage'] = int(levelDict[newLevel][5])
                charData['ac'] = int(levelDict[newLevel][6])
                charData['currentxp'] = pOneXP
                charData['nextlevel'] = int(levelDict[newLevel][7])
                file.seek(0)
                file.write(json.dumps(charData, ensure_ascii=False, indent=2))
                file.truncate()
                file.close()

        if pTwoInfo['currentxp'] >= pTwoInfo['nextlevel']:
            pTwoInfo['level'] = pTwoInfo['level'] + 1
            newLevel = str(pTwoInfo['level'])
            msg.append("[color=red][b]" + pTwoInfo['name'].capitalize() + " has reached level "
                       + newLevel + "![/b][/color]")
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
                    msg.append(pTwoInfo['name'] + " has a new feat slot to fill. Use the "
                                                  "[color=pink]!feat[/color] command to select new feat.")
                    charData['total feats'] = levelDict[newLevel][4]
                    charData['remaining feats'] = 1
                if charData['ap'] == levelDict[newLevel][3]:
                    charData['ap'] = levelDict[newLevel][3]
                else:
                    msg.append(pTwoInfo['name'] + " has a new ability point to spend. "
                                                  "PM the [color=pink]!add[/color] command to Unspoiled "
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

def setup(client):
    client.add_cog(POneXP(client))


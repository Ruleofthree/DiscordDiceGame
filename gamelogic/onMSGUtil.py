
import os
import json
import random
import time
from pathlib import Path
from threading import Timer


def featDict():
    # Open up the json object containing the list of feats.
    featFile = open("feats.txt", "r", encoding="utf-8")
    featDictionary = json.load(featFile)
    featFile.close()

    # place all keys within a list for comparison later
    featList = []
    for keys in featDictionary[0]:
        featList.append(keys)
    return featDictionary, featList

def message_10_tutortial():
    msg = "https://docs.google.com/document/d/1_icTTM7xBZ-i_rynFFpbW6TT23x4GZS9NwT6t5N6U6k/edit?usp=sharing"
    return msg

def message_6_feats():
    msg = "https://docs.google.com/document/d/1CJjC0FxunXXi8zh1I9fZqRrWij9oJiIfIZoxrPJ7GYQ/edit?usp=sharing"
    return msg

def message_6_level():
    msg = "https://docs.google.com/document/d/102oueUxrlJtmdTf58CgpHpc1QlJQ1vCnsgrRilqPpfs/edit?usp=sharing"
    return msg

def message_6_start():
    msg = "Type, in this room, !name <name> where <name> is your characters's Name. Couldn't be simplier."
    return msg

def message_12_leaderboard(option):
    path = os.getcwd()
    charFolder = os.path.join(path + "/characters/")

    msg = []
    profile = []
    with open(charFolder + "playerDatabase.txt", 'r', encoding="utf-8") as file2:
        playerDatabase = json.loads(file2.read())
        file2.close()
    for item in playerDatabase.items():
        name = item[1]
        profile.append(name)
    ratio = {}

    num = 1
    for player in profile:
        with open(charFolder + player + ".txt", "r+", encoding="utf-8") as file:
            charData = json.load(file)
            file.close()
        name = charData['name']
        wins = charData['wins']
        lose = charData['losses']
        level = charData['level']
        total = wins + lose
        try:
            percent = (wins / total) * 100
            charData['percent'] = int(percent)
        except ZeroDivisionError:
            percent = 0
            charData['percent'] = percent
        ratio[num] = [player, name, wins, lose, percent, level]
        num += 1

    if option == "win":
        indexSearch = 1
    elif option == "loss":
        indexSearch = 2
    elif option == "percent":
        indexSearch = 3
    else:
        indexSearch = 1
    indices = sorted(ratio, key=lambda d: ratio[d][indexSearch], reverse=True)
    sortedDict = {}
    index = 1
    for i in indices:
        sortedDict[index] = ratio[i]
        index += 1
    num = 5
    stringDict = []
    for num in range(1, num + 1):
        total = sortedDict[num][2] + sortedDict[num][3]
        stringDict.append("\n" + sortedDict[num][1] + " (" + sortedDict[num][0] + ", Level: [color=green]" +
                          str(sortedDict[num][5]) + "[/color]): [color=pink]" + str(sortedDict[num][2]) +
                          "[/color] wins/[color=yellow]" + str(sortedDict[num][3]) + "[/color] losses. [color=red]("
                          + str(sortedDict[num][4]) + "%)[/color]")
    seperator = " "
    completeMessage = seperator.join(stringDict)
    msg.append(completeMessage)
    return msg

def message_4_who(channel, charFolder, unspoiledBar, message):
    path = os.getcwd()
    charFolder = os.path.join(path + "/characters/")

    msg = ""
    if channel == unspoiledBar:
        profile = message[5:].lower()
        with open(charFolder + "playerDatabase.txt", 'r', encoding="utf-8") as file2:
            playerDatabase = json.loads(file2.read())
            file2.close()

        name = ""

        for item in playerDatabase.items():

            if item[1] == profile:
                name = item[0]
        try:
            with open(charFolder + profile + ".txt", "r+", encoding="utf-8") as file:
                charData = json.load(file)
                file.close()
            msg = profile + "'s character name is: " + name + \
                  ", and they are level: " + str(charData['level'])
        except FileNotFoundError:
            msg = profile + " isn't a valid name for a character sheet. You are just typing " \
                            "in their profile name. example: !who their perfect doll"
    else:
        msg = "This command is only available in the Bar."

    return msg

def message_7_player(player):
    msg = ""
    path = os.getcwd()
    charFolder = os.path.join(path + "/characters/")
    with open(charFolder + "playerDatabase.txt", 'r', encoding="utf-8") as file:
        playerDatabase = json.loads(file.read())
        file.close()

    playerID = 0

    for item in playerDatabase.items():
        if item[0].lower() == player.lower():
            playerID = item[1]
        else:
            msg = player + " isn't a character name."
    charFile = Path(charFolder + playerID + ".txt")
    if not charFile.is_file():
        msg = "Either they don't have a character, or you fucked up typing. (type: !player <character name>)" \

    else:
        charSheet = open(charFolder + playerID + ".txt", "r", encoding="utf-8")
        score = json.load(charSheet)
        charSheet.close()
        name = score['name']
        wins = score['wins']
        losses = score['losses']
        total = wins + losses
        try:
            ratio = int((wins / total) * 100)
            msg = player + "'s current win/loss score is: " + str(wins) + "/" + str(losses) + " (" + str(ratio) + "%)"
        except ZeroDivisionError:
            msg = "Either " + player + " has a 0% win/loss ratio, or 100%. It all depends " \
                  "on how you justify a person that has never entered combat yet."
    return msg

def message_5_name(charFile, charFolder, name, player, game):
    msg = []
    if charFile.is_file():
        msg.append("You've already created a character.")
    else:
        msg.append("Your character name is: " + name)
        msg.append("Your character sheet has been created.")

        levelFile = open(charFolder + "levelchart.txt", "r", encoding="utf-8")
        levelDict = json.load(levelFile)

        # store character data in to dictonary (characterFile), then dump it into a .json file.
        # .json file is named after the F-chat profile name, NOT the character name stored in the variable 'name'.
        # This is to prevent people from making multiple characters on one profile name.
        characterFile = {}
        level = 1
        xp = 0
        characterFile["name"] = name
        characterFile["level"] = level
        hp = levelDict["1"][0]
        characterFile["hp"] = hp
        tFeats = levelDict["1"][4]
        characterFile["total feats"] = tFeats
        numberOfDice = levelDict["1"][1]
        numberOfSides = levelDict["1"][2]
        characterFile["base damage"] = str(numberOfDice) + "d" + str(numberOfSides)
        characterFile["hit"] = levelDict["1"][5]
        characterFile["damage"] = levelDict["1"][5]
        characterFile["ac"] = levelDict["1"][6]
        characterFile["currentxp"] = xp
        nextLevel = levelDict["1"][7]
        characterFile["nextlevel"] = nextLevel
        characterFile["strength"] = 0
        characterFile["dexterity"] = 0
        characterFile["constitution"] = 0
        characterFile["remaining feats"] = 2
        ap = levelDict["1"][3]
        characterFile["ap"] = ap
        characterFile["dr"] = 0
        characterFile["feats taken"] = []
        characterFile["hfeats taken"] = []
        characterFile["reset"] = 3
        characterFile["wins"] = 0
        characterFile["losses"] = 0
        characterFile["abhp"] = 0
        characterFile["abhit"] = 0
        characterFile["abdamage"] = 0
        characterFile["abac"] = 0
        characterFile["feathp"] = 0
        characterFile["feathit"] = 0
        characterFile["featdamage"] = 0
        characterFile["featac"] = 0
        characterFile["thp"] = 0
        characterFile["tac"] = 0
        characterFile["thit"] = 0
        characterFile["tdamage"] = 0
        characterFile["dexfighter"] = 0
        file = open(charFolder + player + ".txt", "w", encoding="utf-8")
        json.dump(characterFile, file, ensure_ascii=False, indent=2)

        with open(charFolder + "playerDatabase.txt", 'r', encoding="utf-8") as file2:
            playerDatabase = json.loads(file2.read())
            file2.close()
        playerDatabase[name] = player
        with open(charFolder + "playerDatabase.txt", 'w') as file2:
            file2.write(json.dumps(playerDatabase, sort_keys=True, indent=2))
            file2.close()

        msg.append("PM me with '!stats <str> <dex> <con>' to set your abilities. Wouldn't want everyone "
                   "to see your secrets, would we?")
    return msg

def message_7_erase(player):
    msg = ""
    path = os.getcwd()
    charFolder = os.path.join(path + "/characters/")
    charFile = Path(charFolder + player + ".txt")

    with open(charFolder + "playerDatabase.txt", 'r', encoding="utf-8") as file:
        playerDatabase = json.loads(file.read())
        file.close()

    name = ""

    for item in playerDatabase.items():

        if item[1] == player:
            name = item[0]

    playerDatabase.pop(name, None)

    with open(charFolder + "playerDatabase.txt", "w", encoding="utf-8") as file:
        json.dump(playerDatabase, file, sort_keys=True, indent=2)
        file.close()

    try:
        os.remove(charFile)
        msg = name + " has been erased."
    except FileNotFoundError:
        msg = "You don't have a character to delete."
    return msg

def message_10_challenge(challenger, oppenent, charFolder, game):
    msg = ""
    pOneInfo = None
    bTimer = False
    new_game = 0
    playerOne = ""

    if game == 0:
        charFile = Path(charFolder + challenger + ".txt")
        # make sure the only people that can issue a challenge, is a person that has a character made.
        if not charFile.is_file():
            msg = "You don't even have a character made to fight."
        else:
            # find opponent's .json file, if one exists.
            with open(charFolder + "playerDatabase.txt", 'r', encoding="utf-8") as file:
                playerDatabase = json.loads(file.read())
                file.close()

            opponentID = 0

            for item in playerDatabase.items():
                if item[0].lower() == opponent.lower():
                    opponentID = item[1]
                else:
                    msg = opponent + " doesn't have a character made for you to fight."
            charFile = Path(charFolder + opponentID + ".txt")
            if opponentID == challenger:
                msg = "You can't fight yourself. No one is that special."
            else:
                # load in challenger's .json file, refered to from here on as 'pOneInfo'
                charSheet = open(charFolder + challenger + ".txt", "r", encoding="utf-8")
                pOneInfo = json.load(charSheet)
                charSheet.close()

                playerOne = challenger
                msg = pOneInfo['name'] + " is challenging " + opponent + " (Type '!accept') "
                new_game = 0.5
                timeout = 60
                bTimer = True
    else:
            msg = "A fight is already taking place. Wait your turn."

    return msg, opponentID, pOneInfo, new_game, bTimer, playerOne

def message_8_usefeat(answer, charFolder, user, game, playerOne, playerTwo, token, featToken, pOneInfo, pOneSpentFeat,
                      pTwoSpentFeat, pTwoInfo):
    msg = []
    featToken_new = None
    # pOneSpentFeat = None
    pOneFeatInfo = None
    # pTwoSpentFeat = None
    pTwoFeatInfo = None

    if game == 1:
        # ensures the command can only be used by player one, when it is their turn. To prevent trolls from
        # spamming commands.
        if user == playerOne and token == 1:

            # pull in the feat dictionary from the gameFeats definition.
            featDictionary = featDict()[0]

            if answer != "none":
                pOneLastFeat = answer
            else:
                pOneLastFeat = None

            # if the feat is one of the listed below. Tell the player that those feats are used with a different
            # command
            if featToken == 0:
                if pOneLastFeat in ('power attack', 'defensive fighting', 'masochist', 'nerve strike', 'improved nerve strike',
                'greater nerve strike', 'nerve damage', 'evasion', 'improved evasion', 'greater evasion', 'hurt me',
                'improved hurt me', 'greater hurt me', 'hurt me more', 'deflect', 'improved deflect', 'greater deflect'):
                    msg.append(pOneLastFeat + " will be determined elsewhere.")

                elif pOneLastFeat in ('crushing blow', 'improved crushing blow', 'greater crushing blow', 'precision strike',
                'improved precision strike', 'greater precision strike', 'lightning reflexes',
                'improved lightning reflexes', 'greater lightning reflexes'):
                    msg.append(pOneLastFeat + " is already factored into your attack/defense.")

                # make sure that a player can't reuse a feat already used.
                elif pOneLastFeat in pOneSpentFeat:
                    msg.append("You have already used this feat.")

                # if a feat chosen is on their character sheet, used the feat Dictionary load in the required
                # information to provide benefits/debuffs.
                elif pOneLastFeat in pOneInfo['feats taken']:
                    featToken_new = 1
                    pOneSpentFeat = pOneLastFeat
                    pOneFeatInfo = [pOneLastFeat, featDictionary[0][pOneLastFeat]['action']]
                    msg.append(pOneInfo['name'] + " has used [color=yellow] " + pOneSpentFeat +
                               "[/color]")

                # If the player doesn't have the feat, he can't use it.
                elif pOneLastFeat not in pOneInfo['feats taken']:
                    msg.append("Either you do not have that feat, or you did not type it correctly")
            else:
                msg.append("You've already used a feat for this round.")
            # ensures the command can only be used by player two, when it is their turn. To prevent trolls from
            # spamming commands.
        elif user == playerTwo and token == 2:

            # pull in the feat dictionary from the gameFeats definition.
            featDictionary = featDict()[0]

            if message[9:] != 'none':
                pTwoLastFeat = message[9:]
            else:
                pTwoLastFeat = "none"

            if featToken == 0:
                # if the feat is one of the listed below. Tell the player that those feats are used with a different
                # command
                if pTwoLastFeat in (
                'power attack', 'combat expertise', 'defensive fighting', 'masochist', 'hurt me',
                'improved hurt me', 'greater hurt me', 'hurt me more', 'evasion', 'improved evasion',
                'greater evasion'):
                    msg.append(pTwoLastFeat + " will be determined elsewhere.")

                elif pTwoLastFeat in (
                'crushing blow', 'improved crushing blow', 'greater crushing blow', 'precision strike',
                'improved precision strike', 'greater precision strike', 'lightning reflexes',
                'improved lightning reflexes',
                'greater lightning reflexes'):
                    msg.append(pTwoLastFeat + " is already factored into your attack/defense.")
                # make sure that a player can't reuse a feat already used.
                elif pTwoLastFeat in pTwoSpentFeat:
                    msg.append("You have already used this feat.")

                # if a feat chosen is on their character sheet, used the feat Dictionary load in the required
                # information to provide benefits/debuffs.
                elif pTwoLastFeat in pTwoInfo['feats taken']:
                    featToken_new = 1
                    pTwoSpentFeat = pTwoLastFeat
                    pTwoFeatInfo = [pTwoLastFeat, featDictionary[0][pTwoLastFeat]['action']]
                    msg.append(pTwoInfo['name'] + " has used [color=yellow]" + pTwoLastFeat +
                               "[/color]")

                # If the player doesn't have the feat, he can't use it.
                elif pTwoLastFeat not in pTwoInfo['feats taken']:
                    msg.append("Either you do not have that feat, or you did not type it correctly")
            else:
                msg.append("You've already used a feat this round.")
        else:
            msg.append("Either it is not your turn, or you aren't even fighting. Either way, No.")
    else:
        msg.append("This command does nothing right now. No combat is taking place.")

    return msg, featToken_new, pOneSpentFeat, pOneFeatInfo, pTwoSpentFeat, pTwoFeatInfo

def message_5_pass(character, channel, unspoiledArena, playerOne, playerTwo, pOneInfo, pTwoInfo, featToken,
                   count, token, critical, bonusHurt, totalDamage, pOneTotalHP, pTwoTotalHP,
                   pOneCurrentHP, pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod, pOnemMod, pOneQuickDamage,
                   pTwoQuickDamage, iddqd):
    msg = []
    bGameTimer = False
    if channel == unspoiledArena:
        if token == 2 and character.lower() == playerOne:
            msg.append(pOneInfo['name'] + " has chosen not to prevent this attack.")
            pOneCurrentHP = pOneCurrentHP - totalDamage

            # Print the scoreboard
            msg.append(pOneInfo['name'] + ": [color=red]"
                       + str(pOneCurrentHP) + "[/color]/" +
                       str(pOneTotalHP) + "  ||  " + pTwoInfo['name'] + ": [color=red]" +
                       str(pTwoCurrentHP) + "[/color]/" + str(pTwoTotalHP) + " \n" +
                       pOneInfo['name'] + "'s turn. Type: [color=pink]!usefeat <feat>[/color]"
                                          " if you wish to use a feat.")
            count += 1
            featToken = 0
            token = 1
            pOnedMod = 0
            pOnemMod = 0
            iddqd = 0
            bGameTimer = True
            pOneFeatInfo = None

        elif token == 1 and character.lower() == playerTwo:
            msg.append(pTwoInfo['name'] + " has chosen not to evade this attack.")
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
        else:
            msg.append(
                "You are either not in the fight, or it's not your turn. Either way, Don't do it again.")
    else:
        msg.append("This command is only available in the Arena.")
    return msg, bGameTimer, playerOne, playerTwo, pOneInfo, pTwoInfo, featToken, \
           count, token, critical, bonusHurt, totalDamage, pOneTotalHP, pTwoTotalHP, \
           pOneCurrentHP, pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod, pOnemMod, pOneQuickDamage, pTwoQuickDamage, iddqd

def message_8_evasion(user, playerOne, playerTwo, pOneInfo, pTwoInfo, featToken,
                      count, token, critical, bonusHurt, totalDamage, pOneTotalHP, pTwoTotalHP,
                      pOneCurrentHP, pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod, pOnemMod, pOneQuickDamage,
                      pTwoQuickDamage, pTwoEvade, pOneEvade, iddqd):
    msg = []
    bGameTimer = False

    if channel == unspoiledArena:
        if token == 2 and user == playerOne:
            for word in pOneInfo['feats taken']:
                if pOneEvade == 1 and word == "evasion":
                    totalDamage = int(totalDamage * 0.5)
                    pOneEvade = 0
                    msg.append(playerOne + " used [color=yellow]'" + word + "'[/color],"
                                           " reducing damage taken to [color=red]" + str(totalDamage) + "[/color]. \n")
                elif pOneEvade == 1 and word == "improved evasion":
                    totalDamage = int(totalDamage * 0.25)
                    pOneEvade = 0
                    msg.append(playerOne + " used [color=yellow]'" + word + "'[/color],"
                                                                            " reducing damage taken to [color=red]" + str(
                        totalDamage) + "[/color]. \n")
                elif pOneEvade == 1 and word == "greater evasion":
                    totalDamage = 0
                    pTwoEvade = 0
                    msg.append(playerOne + " used [color=yellow]'" + word + "'[/color],"
                                                                            " reducing damage taken to [color=red]" + str(
                        totalDamage) + "[/color]. \n")

            # Determine if Quick Strike was used by Player One and apply damage
            if pOneQuickDamage != 0:
                pTwoCurrentHP = pTwoCurrentHP - totalDamage - pOneQuickDamage
                pOneQuickDamage = 0
            else:
                pOneCurrentHP = pOneCurrentHP - totalDamage

            # Print the scoreboard
            msg.append(pOneInfo['name'] + ": [color=red]" + str(pOneCurrentHP) + "[/color]/" +
                       str(pOneTotalHP) + "  ||  " + pTwoInfo['name'] + ": [color=red]" +
                       str(pTwoCurrentHP) + "[/color]/" + str(pTwoTotalHP) + " \n" +
                       pOneInfo['name'] + "'s turn. Type: [color=pink]!usefeat <feat>[/color]"
                                          " if you wish to use a feat.")
            count += 1
            featToken = 0
            token = 1
            pOnedMod = 0
            pOnemMod = 0
            iddqd = 0
            bGameTimer = True


        elif token == 1 and user == playerTwo:
            for word in pTwoInfo['feats taken']:
                if pTwoEvade == 1 and word == "evasion":
                    totalDamage = int(totalDamage * 0.75)
                    pTwoEvade = 0
                    msg.append(playerTwo + " used [color=yellow]'" + word + "'[/color],"
                                                                            " reducing damage taken to [color=red]" + str(
                        totalDamage) + "[/color]. \n")
                elif pTwoEvade == 1 and word == "improved evasion":
                    totalDamage = int(totalDamage * 0.5)
                    pTwoEvade = 0
                    msg.append(playerTwo + " used [color=yellow]'" + str(totalDamage) + "'[/color],"
                                                                                        " reducing damage taken to [color=red]" + str(
                        total) + "[/color]. \n")
                elif pTwoEvade == 1 and word == "greater evasion":
                    totalDamage = 0
                    pTwoEvade = 0
                    msg.append(playerTwo + " used [color=yellow]'" + word + "'[/color],"
                                                                            " reducing damage taken to [color=red]" + str(
                        totalDamage) + "[/color]. \n")

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
        else:
            msg.append(
                "You are either not in the fight, or it's not your turn. Either way, Don't do it again.")
    else:
        msg.append("This command is only available in the Arena.")
    return msg, bGameTimer, playerOne, playerTwo, pOneInfo, pTwoInfo, featToken, \
           count, token, totalDamage, pOneTotalHP, pTwoTotalHP, pOneCurrentHP, pTwoCurrentHP, pOnepMod, pOnecMod, \
           pOnedMod, pOnemMod, pOneQuickDamage, pTwoQuickDamage, pTwoEvade, pOneEvade, iddqd

def message_8_deflect(user, playerOne, playerTwo, pOneInfo, pTwoInfo, featToken,
                      count, token, critical, bonusHurt, totalDamage, pOneTotalHP, pTwoTotalHP,
                      pOneCurrentHP, pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod, pOnemMod, pOneQuickDamage,
                      pTwoQuickDamage, pTwoDeflect, pOneDeflect, iddqd):
    msg = []
    bGameTimer = False

    if token == 2 and user == playerOne:
        for word in pOneInfo['feats taken']:
            if word == "deflect" and pOneDeflect == 1:
                pOneDeflect = 0
                oldDamage = totalDamage
                totalDamage = int(totalDamage - int(pOneInfo['abac']))
                if totalDamage < 1:
                    totalDamage = 1
                msg.append(pOneInfo['name'] + " used [color=yellow]'deflect'[/color] "
                           "to lessen the blow from [color=red]" + str(oldDamage) +
                           "[/color] to [color=red]" + str(int(totalDamage)) + "[/color]")

            elif word == "improved deflect" and pOneDeflect == 1:
                pOneDeflect = 0
                oldDamage = totalDamage
                totalDamage = int(totalDamage - int(pOneInfo['abac'] * 1.5))
                if totalDamage < 1:
                    totalDamage = 1
                msg.append(pOneInfo['name'] + " used [color=yellow]'deflect'[/color] "
                                              "to lessen the blow from [color=red]" + str(oldDamage) +
                           "[/color] to [color=red]" + str(int(totalDamage)) + "[/color]")

            elif word == "greater deflect" and pOneDeflect == 1:
                pOneDeflect = 0
                oldDamage = totalDamage
                totalDamage = int(totalDamage - int(pOneInfo['abac'] * 2))
                if totalDamage < 1:
                    totalDamage = 1
                msg.append(pOneInfo['name'] + " used [color=yellow]'deflect'[/color] "
                           "to lessen the blow from [color=red]" + str(oldDamage) +
                           "[/color] to [color=red]" + str(int(totalDamage)) + "[/color]")

        # Determine if Quick Strike was used by Player One and apply damage
        if pOneQuickDamage != 0:
            pTwoCurrentHP = pTwoCurrentHP - totalDamage - pOneQuickDamage
            pOneQuickDamage = 0
        else:
            pOneCurrentHP = pOneCurrentHP - totalDamage

        # Print the scoreboard
        msg.append(pOneInfo['name'] + ": [color=red]" + str(pOneCurrentHP) + "[/color]/" +
                   str(pOneTotalHP) + "  ||  " + pTwoInfo['name'] + ": [color=red]" +
                   str(pTwoCurrentHP) + "[/color]/" + str(pTwoTotalHP) + " \n" +
                   pOneInfo['name'] + "'s turn. Type: [color=pink]!usefeat <feat>[/color]"
                                      " if you wish to use a feat.")
        count += 1
        featToken = 0
        token = 1
        pOnedMod = 0
        pOnemMod = 0
        iddqd = 0
        bGameTimer = True


    elif token == 1 and user == playerTwo:
        for word in pTwoInfo['feats taken']:
            if word == "deflect" and pTwoDeflect == 1:
                pTwoDeflect = 0
                oldDamage = totalDamage
                totalDamage = int(totalDamage - int(pTwoInfo['abac']))
                if totalDamage < 1:
                    totalDamage = 1
                msg.append(pTwoInfo['name'] + " used [color=yellow]'deflect'[/color] "
                           "to lessen the blow from [color=red]" + str(oldDamage) + "[/color] to [color=red]" +
                           str(int(totalDamage)) + "[/color]")

            elif word == "improved deflect" and pTwoDeflect == 1:
                pTwoDeflect = 0
                oldDamage = totalDamage
                totalDamage = int(totalDamage - int(pTwoInfo['abac'] * 1.5))
                if totalDamage < 1:
                    totalDamage = 1
                msg.append(pTwoInfo['name'] + " used [color=yellow]'deflect'[/color] "
                          "to lessen the blow from [color=red]" + str(oldDamage) +
                           "[/color] to [color=red]" + str(int(totalDamage)) + "[/color]")

            elif word == "greater deflect" and pTwoDeflect == 1:
                pTwoDeflect = 0
                oldDamage = totalDamage
                totalDamage = int(totalDamage - int(pTwoInfo['abac'] * 2))
                if totalDamage < 1:
                    totalDamage = 1
                msg.append(pTwoInfo['name'] + " used [color=yellow]'deflect'[/color] "
                           "to lessen the blow from [color=red]" + str(oldDamage) +
                           "[/color] to [color=red]" + str(int(totalDamage)) + "[/color]")

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
    else:
        msg.append(
            "You are either not in the fight, or it's not your turn. Either way, Don't do it again.")

    msg.append("This command is only available in the Arena.")
    return msg, bGameTimer, playerOne, playerTwo, pOneInfo, pTwoInfo, featToken, \
           count, token, totalDamage, pOneTotalHP, pTwoTotalHP, pOneCurrentHP, pTwoCurrentHP, pOnepMod, pOnecMod, \
           pOnedMod, pOnemMod, pOneQuickDamage, pTwoQuickDamage, pTwoDeflect, pOneDeflect, iddqd

def message_8_pattack(user, points, game, playerOne, playerTwo, pOneInfo, pTwoInfo, token, pOnepMod, pTwopMod, pOneLevel, pTwoLevel):
    msg = []

    # make sure that this command cannot be ran if a fight is taking place.
    try:
        if game == 1:
            # ensures the command can only be used by player one, when it is their turn. To prevent trolls from
            # spamming commands.
            if user == playerOne and token == 1:
                if 'power attack' in pOneInfo['feats taken']:
                    mod = int(message[9:])
                    if pOneLevel <= 4 and mod == 1:
                        pOnepMod = 1
                        msg.append(pOneInfo['name'] + " invested [color=red]"
                                   + str(mod) + "[/color] points in [color=yellow]'power attack'[/color]")
                    elif 4 < pOneLevel <= 8 and mod == 2:
                        pOnepMod = 2
                        msg.append(pOneInfo['name'] + " invested [color=red]"
                                   + str(mod) + "[/color] points in [color=yellow]'power attack'[/color]")
                    elif 8 < pOneLevel <= 12 and mod == 3:
                        pOnepMod = 3
                        msg.append(pOneInfo['name'] + " invested [color=red]"
                                   + str(mod) + "[/color] points in [color=yellow]'power attack'[/color]")
                    elif 12 < pOneLevel <= 16 and mod == 4:
                        pOnepMod = 4
                        msg.append(pOneInfo['name'] + " invested [color=red]"
                                   + str(mod) + "[/color] points in [color=yellow]'power attack'[/color]")
                    elif 16 < pOneLevel <= 20 and mod == 5:
                        pOnepMod = 5
                        msg.append(pOneInfo['name'] + " invested [color=red]"
                                   + str(mod) + "[/color] points in [color=yellow]'power attack'[/color]")
                    else:
                        msg.append("You are not high enough level to invest that many points.")
                else:
                    msg.append("You have not taken this feat.")
            # ensures the command can only be used by player two, when it is their turn. To prevent trolls from
            # spamming commands.
            elif user == playerTwo and token == 2:
                if 'power attack' in pTwoInfo['feats taken']:
                    if pTwoLevel <= 4 and points == 1:
                        pTwopMod = 1
                        msg.append(pTwoInfo['name'] + " invested [color=red]"
                                   + str(points) + "[/color] points in [color=yellow]'power attack'[/color]")
                    elif 4 < pTwoLevel <= 8 and points == 2:
                        pTwopMod = 2
                        msg.append(pTwoInfo['name'] + " invested [color=red]"
                                   + str(points) + "[/color] points in [color=yellow]'power attack'[/color]")
                    elif 8 < pTwoLevel <= 12 and points == 3:
                        pTwopMod = 3
                        msg.append(pTwoInfo['name'] + " invested [color=red]"
                                   + str(points) + "[/color] points in [color=yellow]'power attack'[/color]")
                    elif 12 < pTwoLevel <= 16 and points == 4:
                        pTwopMod = 4
                        msg.append(pTwoInfo['name'] + " invested [color=red]"
                                   + str(points) + "[/color] points in [color=yellow]'power attack'[/color]")
                    elif 16 < pTwoLevel <= 20 and points == 5:
                        pTwopMod = 5
                        msg.append(pTwoInfo['name'] + " invested [color=red]"
                                   + str(points) + "[/color] points in [color=yellow]'power attack'[/color]")
                    else:
                        msg.append("You are not high enough level to invest that many points.")
                else:
                    msg.append("You have not taken this feat.")
            else:
                msg.append("Either it's not your turn, or you aren't even fighting. Either way, No.")
        else:
            msg.append("This command does nothing right now. No combat is taking place.")
    except ValueError:
        msg.append("Please allocate points to use this ability.")
    return msg, game, playerOne, playerTwo, pOneInfo, pTwoInfo, token, pOnepMod, pTwopMod, pOneLevel, pTwoLevel

def message_8_dfight(user, points, game, playerOne, playerTwo, pOneInfo, pTwoInfo, token, pOnedMod, pTwodMod, pOneLevel, pTwoLevel):
    msg = []
    # make sure that this command cannot be ran if a fight is taking place.
    try:
        if game == 1:
            # ensures the command can only be used by player one, when it is their turn. To prevent trolls from
            # spamming commands.
            if character.lower() == playerOne and token == 1:
                if 'defensive fighting' in pOneInfo['feats taken']:
                    if pOneLevel <= 4 and points == 1:
                        pOnedMod = 1
                        msg.append(pOneInfo['name'] + " invested [color=red]"
                                   + str(points) + "[/color] points in [color=yellow]'defensive fighting'[/color]")
                    elif 4 < pOneLevel <= 8 and points == 2:
                        pOnedMod = 2
                        msg.append(pOneInfo['name'] + " invested [color=red]"
                                   + str(points) + "[/color] points in [color=yellow]'defensive fighting'[/color]")
                    elif 8 < pOneLevel <= 12 and points == 3:
                        pOnedMod = 3
                        msg.append(pOneInfo['name'] + " invested [color=red]"
                                   + str(points) + "[/color] points in [color=yellow]'defensive fighting'[/color]")
                    elif 12 < pOneLevel <= 16 and points == 4:
                        pOnedMod = 4
                        msg.append(pOneInfo['name'] + " invested [color=red]"
                                   + str(points) + "[/color] points in [color=yellow]'defensive fighting'[/color]")
                    elif 16 < pOneLevel <= 20 and points == 5:
                        pOnedMod = 5
                        msg.append(pOneInfo['name'] + " invested [color=red]"
                                   + str(points) + "[/color] points in [color=yellow]'defensive fighting'[/color]")
                    else:
                        msg.append("You are not high enough level to invest that many points.")
                else:
                    msg.append("You do not have this feat.")
            # ensures the command can only be used by player two, when it is their turn. To prevent trolls from
            # spamming commands.
            elif character.lower() == playerTwo and token == 2:
                if 'defensive fighting' in pTwoInfo['feats taken']:
                    if pTwoLevel <= 4 and points == 1:
                        pTwodMod = 1
                        msg.append(pTwoInfo['name'] + " invested [color=red]"
                                   + str(points) + "[/color] points in [color=yellow]'defensive fighting'[/color]")
                    elif 4 < pTwoLevel <= 8 and points == 2:
                        pTwodMod = 2
                        msg.append(pTwoInfo['name'] + " invested [color=red]"
                                   + str(points) + "[/color] points in [color=yellow]'defensive fighting'[/color]")
                    elif 8 < pTwoLevel <= 12 and points == 3:
                        pTwodMod = 3
                        msg.append(pTwoInfo['name'] + " invested [color=red]"
                                   + str(points) + "[/color] points in [color=yellow]'defensive fighting'[/color]")
                    elif 12 < pTwoLevel <= 16 and points == 4:
                        pTwodMod = 4
                        msg.append(pTwoInfo['name'] + " invested [color=red]"
                                   + str(points) + "[/color] points in [color=yellow]'defensive fighting'[/color]")
                    elif 16 < pTwoLevel <= 20 and points == 5:
                        pTwodMod = 5
                        msg.append(pTwoInfo['name'] + " invested [color=red]"
                                   + str(points) + "[/color] points in [color=yellow]'defensive fighting'[/color]")
                    else:
                        msg.append("You are not high enough level to invest that many points.")
                else:
                    msg.append("You did not take that feat.")
            else:
                msg.append("Either it's not your turn, or you aren't even fighting. Either way, No.")
        else:
            msg.append("This command does nothing right now. No combat is taking place.")
    except ValueError:
        msg.append("Please allocate points to use this ability.")
    return msg, game, playerOne, playerTwo, pOneInfo, pTwoInfo, token, pOnedMod, pTwodMod, pOneLevel, pTwoLevel

# def message_8_cexpert(character, channel, unspoiledArena, message, game, playerOne, playerTwo,  pOneInfo, pTwoInfo,
#     token, pOnecMod, pTwocMod, pOneLevel, pTwoLevel):
#     msg = []
#     if channel == unspoiledArena:
#        # make sure that this command cannot be ran if a fight is taking place.
#        try:
#                if game == 1:
#                    # ensures the command can only be used by player one, when it is their turn. To prevent trolls from
#                    # spamming commands.
#                    if character.lower() == playerOne and token == 1:
#                        mod = int(message[9:])
#                        if pOneLevel <= 4 and mod == 1:
#                            pOnecMod = 1
#                            msg.append(pOneInfo['name'] + " invested [color=red]"
#                                        + str(mod) + "[/color] points in [color=yellow]'combat expertise'[/color]")
#                        elif 4 < pOneLevel <= 8 and mod == 2:
#                            pOnecMod = 2
#                            msg.append(pOneInfo['name'] + " invested [color=red]"
#                                        + str(mod) + "[/color] points in [color=yellow]'combat expertise'[/color]")
#                        elif 8 < pOneLevel <= 12 and mod == 3:
#                            pOnecMod = 3
#                            msg.append(pOneInfo['name'] + " invested [color=red]"
#                                        + str(mod) + "[/color] points in [color=yellow]'combat expertise'[/color]")
#                        elif 12 < pOneLevel <= 16 and mod == 4:
#                            pOnecMod = 4
#                            msg.append(pOneInfo['name'] + " invested [color=red]"
#                                        + str(mod) + "[/color] points in [color=yellow]'combat expertise'[/color]")
#                        elif 16 < pOneLevel <= 20 and mod == 5:
#                            pOnecMod = 5
#                            msg.append(pOneInfo['name'] + " invested [color=red]"
#                                        + str(mod) + "[/color] points in [color=yellow]'combat expertise'[/color]")
#                        else:
#                            msg.append("You are not high enough level to invest that many points.")
#                    # ensures the command can only be used by player two, when it is their turn. To prevent trolls from
#                    # spamming commands.
#                    elif character.lower() == playerTwo and token == 2:
#                        mod = int(message[9:])
#                        if pTwoLevel <= 4 and mod == 1:
#                            pTwocMod = 1
#                            msg.append(pTwoInfo['name'] + " invested [color=red]"
#                                        + str(mod) + "[/color] points in [color=yellow]'combat expertise'[/color]")
#                        elif 4 < pTwoLevel <= 8 and mod == 2:
#                            pTwocMod = 2
#                            msg.append(pTwoInfo['name'] + " invested [color=red]"
#                                        + str(mod) + "[/color] points in [color=yellow]'combat expertise'[/color]")
#                        elif 8 < pTwoLevel <= 12 and mod == 3:
#                            pTwocMod = 3
#                            msg.append(pTwoInfo['name'] + " invested [color=red]"
#                                        + str(mod) + "[/color] points in [color=yellow]'combat expertise'[/color]")
#                        elif 12 < pTwoLevel <= 16 and mod == 4:
#                            pTwocMod = 4
#                            msg.append(pTwoInfo['name'] + " invested [color=red]"
#                                        + str(mod) + "[/color] points in [color=yellow]'combat expertise'[/color]")
#                        elif 16 < pTwoLevel <= 20 and mod == 5:
#                            pTwocMod = 5
#                            msg.append(pTwoInfo['name'] + " invested [color=red]"
#                                        + str(mod) + "[/color] points in [color=yellow]'combat expertise'[/color]")
#                        else:
#                            msg.append("You are not high enough level to invest that many points.")
#
#                    else:
#                        msg.append("Either it's not your turn, or you aren't even fighting. Either way, No.")
#                else:
#                    msg.append("This command does nothing right now. No combat is taking place.")
#            except ValueError:
#                msg.append("Please allocate points to use this ability.")
#        else:
#            msg.append("This command is only available in the Arena.")
#        return msg, game, playerOne, playerTwo,  pOneInfo, pTwoInfo, token, pOnecMod, pTwocMod, pOneLevel, pTwoLevel

def message_10_masochist(user, points, game, playerOne, playerTwo, pOneInfo, pTwoInfo, token, pOnemMod, pTwomMod, pOneLevel, pTwoLevel):
    msg = []

    # make sure that this command cannot be ran if a fight is taking place.
    try:
        if game == 1:
            # ensures the command can only be used by player one, when it is their turn. To prevent trolls from
            # spamming commands.
            if character.lower() == playerOne and token == 1:
                if 'masochist' in pOneInfo['feats taken']:
                    if pOneLevel <= 4 and points == 1:

                        pOnemMod = 1
                        msg.append(pOneInfo['name'] + " invested [color=red]"
                                   + str(points) + "[/color] points in [color=yellow]'masochist'[/color]")
                    elif 4 < pOneLevel <= 8 and points == 2:
                        pOnemMod = 2
                        msg.append(pOneInfo['name'] + " invested [color=red]"
                                   + str(points) + "[/color] points in [color=yellow]'masochist'[/color]")
                    elif 8 < pOneLevel <= 12 and points == 3:
                        pOnemMod = 3
                        msg.append(pOneInfo['name'] + " invested [color=red]"
                                   + str(points) + "[/color] points in [color=yellow]'masochist'[/color]")
                    elif 12 < pOneLevel <= 16 and points == 4:
                        pOnemMod = 4
                        msg.append(pOneInfo['name'] + " invested [color=red]"
                                   + str(points) + "[/color] points in [color=yellow]'masochist'[/color]")
                    elif 16 < pOneLevel <= 20 and points == 5:
                        pOnemMod = 5
                        msg.append(pOneInfo['name'] + " invested [color=red]"
                                   + str(points) + "[/color] points in [color=yellow]'masochist'[/color]")
                    else:
                        msg.append("You are not high enough level to invest that many points.")
                else:
                    msg.append("You do not have this feat.")
            # ensures the command can only be used by player two, when it is their turn. To prevent trolls from
            # spamming commands.
            elif character.lower() == playerTwo and token == 2:
                if 'masochist' in pTwoInfo['feats taken']:
                    if pTwoLevel <= 4 and points == 1:

                        pTwomMod = 1
                        msg.append(pTwoInfo['name'] + " invested [color=red]"
                                   + str(points) + "[/color] points in [color=yellow]'masochist'[/color]")
                    elif 4 < pTwoLevel <= 8 and points == 2:
                        pTwomMod = 2
                        msg.append(pTwoInfo['name'] + " invested [color=red]"
                                   + str(points) + "[/color] points in [color=yellow]'masochist'[/color]")
                    elif 8 < pTwoLevel <= 12 and points == 3:
                        pTwomMod = 3
                        msg.append(pTwoInfo['name'] + " invested [color=red]"
                                   + str(points) + "[/color] points in [color=yellow]'masochist'[/color]")
                    elif 12 < pTwoLevel <= 16 and points == 4:
                        pTwomMod = 4
                        msg.append(pTwoInfo['name'] + " invested [color=red]"
                                   + str(points) + "[/color] points in [color=yellow]'masochist'[/color]")
                    elif 16 < pTwoLevel <= 20 and points == 5:
                        pTwomMod = 5
                        msg.append(pTwoInfo['name'] + " invested [color=red]"
                                   + str(points) + "[/color] points in [color=yellow]'masochist'[/color]")
                    else:
                        msg.append("You are not high enough level to invest that many points.")
                else:
                    msg.append("You do not have this feat.")

            else:
                msg.append("Either it's not your turn, or you aren't even fighting. Either way, No.")
        else:
            msg.append("This command does nothing right now. No combat is taking place.")
    except ValueError:
        msg.append("Please allocate points to use this ability.")
    return msg, game, playerOne, playerTwo, pOneInfo, pTwoInfo, token, pOnemMod, pTwomMod, pOneLevel, pTwoLevel
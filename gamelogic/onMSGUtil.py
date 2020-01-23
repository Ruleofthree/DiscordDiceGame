import os
import json
import random
import time
from pathlib import Path
from threading import Timer

# a script to handle all messages sent into a channel that is listening for said commands.

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


def traitDict():
    # Open up a json object containing the list of traits.
    path = os.getcwd()
    traitFolder = os.path.join(path + "/cogs/")
    traitFile = open(traitFolder + "trait.txt", "r", encoding="utf-8")
    traitDictonary = json.load(traitFile)
    traitfile.close()

    # place all keys within a list for comparison later
    traitList = []
    for keys in traitDictonary[0]:
        traitList.append(keys)
    return traitDictonary, traitList

# display top 5 in standings according to the following catagories: Wins, losses, percentage.
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

    indices = sorted(ratio, key=lambda d: ratio[d][indexSearch], reverse=False)
    sortedDict = {}
    index = 1
    for i in indices:
        sortedDict[index] = ratio[i]
        index += 1
    print(sortedDict)
    num = 2
    stringDict = []
    for num in range(1, num + 1):
        total = sortedDict[num][2] + sortedDict[num][3]
        stringDict.append("\n" + sortedDict[num][1] + " (Level: " +
                          str(sortedDict[num][5]) + "): " + str(sortedDict[num][2]) +
                          " wins/" + str(sortedDict[num][3]) + " losses. ("
                          + str(sortedDict[num][4]) + "%)")
    seperator = " "
    completeMessage = seperator.join(stringDict)
    msg.append(completeMessage)
    return msg

# display character and their current level.
def message_4_who(player):
    path = os.getcwd()
    charFolder = os.path.join(path + "/characters/")

    msg = ""
    with open(charFolder + "playerDatabase.txt", 'r', encoding="utf-8") as file2:
        playerDatabase = json.loads(file2.read())
        file2.close()

    playerID = ""

    for item in playerDatabase.items():
        if item[0].lower() == player.lower():
            playerID = item[1]
        else:
            msg = player + " isn't a character name."

    charFile = Path(charFolder + playerID + ".txt")

    if not charFile.is_file():
        msg = "Either they don't have a character, or you fucked up typing. (type: !player <character name>)"
    try:
        with open(charFolder + playerID + ".txt", "r+", encoding="utf-8") as file:
            charData = json.load(file)
            file.close()
        msg = player + ", is level: " + str(charData['level'])
    except FileNotFoundError:
        msg = player + " isn't a valid name for a character sheet. You are just typing " \
                        "in their profile name. example: !who RuleofThree"

    return msg

# display character and their current win/loss ratio
def message_7_player(player):
    msg = ""
    path = os.getcwd()
    charFolder = os.path.join(path + "/characters/")
    with open(charFolder + "playerDatabase.txt", 'r', encoding="utf-8") as file:
        playerDatabase = json.loads(file.read())
        file.close()

    playerID = ""

    for item in playerDatabase.items():
        if item[0].lower() == player.lower():
            playerID = item[1]
        else:
            msg = player + " isn't a character name."

    charFile = Path(charFolder + playerID + ".txt")

    if not charFile.is_file():
        msg = "Either they don't have a character, or you mistyped. (type: !player <character name>)"
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

# go through the process of creating a character
def message_5_name(charFile, charFolder, name, player):
    msg = []
    if charFile.is_file():
        msg.append("You've already created a character.")
    else:
        msg.append("**NOTE:** This bot is very much still in it's infancy. Bugs are probably everywhere. If you see"
                   " one, please tell one of the moderators. If the bot crashes, have patience. As of right now"
                   " there is only *one* developer, and they will get the bot online ASAP.")
        msg.append("Your character name is: " + name)
        msg.append("Your character sheet has been created.")

        levelFile = open(charFolder + "levelchart.txt", "r", encoding="utf-8")
        levelDict = json.load(levelFile)
        numberOfDice = levelDict["1"][1]
        numberOfSides = levelDict["1"][2]

        # store character data in to dictonary (characterFile), then dump it into a .json file.
        # .json file is named after the F-chat profile name, NOT the character name stored in the variable 'name'.
        # This is to prevent people from making multiple characters on one profile name.
        characterFile = {}
        level = 1
        xp = 0
        characterFile["name"] = name
        characterFile["level"] = level
        characterFile["trait"] = ""
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
        characterFile["regeneration"] = 0
        characterFile["feats taken"] = []
        characterFile["armor"] = {"armor1": "n/a", "armor2": "n/a", "armor3": "n/a",}
        characterFile["equip"] = ""
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
        characterFile["tdr"] = 0
        characterFile["dexfighter"] = 0
        characterFile["gold"] = 0
        characterFile["initiative"] = 0
        characterFile["potions"] = []
        characterFile["potioneffect"] = ""
        characterFile["potionhit"] = 0
        characterFile["potiondamage"] = 0
        characterFile["potionac"] = 0
        characterFile["potionhp"] = 0
        characterFile["potionblur"] = 0
        characterFile["potioninitiative"] = 0
        characterFile["pstrength"] = 0
        characterFile["pdexterity"] = 0
        characterFile["pconstitution"] = 0
        characterFile["armorhit"] = 0
        characterFile["armordamage"] = 0
        characterFile["armorac"] = 0
        characterFile["armorhp"] = 0
        characterFile["armordr"] = 0
        characterFile["armorstrength"] = 0
        characterFile["armordexterity"] = 0
        characterFile["armorconstitution"] = 0
        characterFile["armorblur"] = 0
        characterFile["armorinitiative"] = 0
        characterFile["blur"] = 0
        characterFile['traithit'] = 0
        characterFile['traitdamage'] = 0
        characterFile['traitac'] = 0
        characterFile['traitdr'] = 0
        characterFile['traithp'] = 0
        file = open(charFolder + player + ".txt", "w", encoding="utf-8")
        json.dump(characterFile, file, ensure_ascii=False, indent=2)
        file.close()

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

# resets a game if it has been idle for more than 60 minutes
def soft_reset(gameFolder,vwhichRoom):
    with open(gameFolder + whichRoom + '.txt', 'r+') as file:
        gameData = json.load(file)
        gameData["playerOneID"] = ""
        gameData["playerTwoID"] = ""
        gameData["winner"] = ""
        gameData["quitter"] = ""
        gameData["pOneInfo"] = {}
        gameData["pTwoInfo"] = {}
        gameData["featToken"] = 0
        gameData["game"] = 0
        gameData["count"] = 0
        gameData["token"] = 0
        gameData["critical"] = 0
        gameData["bonusHurt"] = 0
        gameData["nerveDamage"] = 0
        gameData["totalDamage"] = 0
        gameData["pOneTotalHP"] = 0
        gameData["pTwoTotalHP"] = 0
        gameData["pOneCurrentHP"] = 0
        gameData["pTwoCurrentHP"] = 0
        gameData["pOnepMod"] = 0
        gameData["pOnecMod"] = 0
        gameData["pOnedMod"] = 0
        gameData["pOnemMod"] = 0
        gameData["pOneEvade"] = 1
        gameData["pOneDeflect"] = 1
        gameData["pOneRiposte"] = 0
        gameData["pOneQuickDamage"] = 0
        gameData["pOneFeatInfo"] = None
        gameData["pOneSpentFeat"] = []
        gameData["pTwopMod"] = 0
        gameData["pTwocMod"] = 0
        gameData["pTwodMod"] = 0
        gameData["pTwomMod"] = 0
        gameData["pTwoEvade"] = 1
        gameData["pTwoDeflect"] = 1
        gameData["pTwoRiposte"] = 0
        gameData["pTwoQuickDamage"] = 0
        gameData["pTwoFeatInfo"] = None
        gameData["pTwoSpentFeat"] = []
        gameData["pOneLevel"] = 0
        gameData["pTwoLevel"] = 0
        gameData["xp"] = 0
        gameData["currentPlayerXP"] = 0
        gameData["nextLevel"] = 0
        gameData["levelUp"] = 0
        gameData["iddqd"] = 0
        file.seek(0)
        file.write(json.dumps(gameData, ensure_ascii=False, indent=2))
        file.truncate()
        file.close()

# resets a game if an administrator as used the !reset command
def message_6_reset(gameFolder, whichRoom):
    whichRoom = str(whichRoom)
    with open(gameFolder + whichRoom + '.txt', 'r+') as file:
        gameData = json.load(file)
        if gameData["game"] == 1:
            gameData["playerOneID"] = ""
            gameData["playerTwoID"] = ""
            gameData["winner"] = ""
            gameData["quitter"] = ""
            gameData["pOneInfo"] = {}
            gameData["pTwoInfo"] = {}
            gameData["featToken"] = 0
            gameData["game"] = 0
            gameData["count"] = 0
            gameData["token"] = 0
            gameData["critical"] = 0
            gameData["bonusHurt"] = 0
            gameData["nerveDamage"] = 0
            gameData["totalDamage"] = 0
            gameData["pOneTotalHP"] = 0
            gameData["pTwoTotalHP"] = 0
            gameData["pOneCurrentHP"] = 0
            gameData["pTwoCurrentHP"] = 0
            gameData["pOnepMod"] = 0
            gameData["pOnecMod"] = 0
            gameData["pOnedMod"] = 0
            gameData["pOnemMod"] = 0
            gameData["pOneEvade"] = 1
            gameData["pOneDeflect"] = 1
            gameData["pOneRiposte"] = 0
            gameData["pOneQuickDamage"] = 0
            gameData["pOneFeatInfo"] = None
            gameData["pOneSpentFeat"] = []
            gameData["pTwopMod"] = 0
            gameData["pTwocMod"] = 0
            gameData["pTwodMod"] = 0
            gameData["pTwomMod"] = 0
            gameData["pTwoEvade"] = 1
            gameData["pTwoDeflect"] = 1
            gameData["pTwoRiposte"] = 0
            gameData["pTwoQuickDamage"] = 0
            gameData["pTwoFeatInfo"] = None
            gameData["pTwoSpentFeat"] = []
            gameData["pOneLevel"] = 0
            gameData["pTwoLevel"] = 0
            gameData["xp"] = 0
            gameData["currentPlayerXP"] = 0
            gameData["nextLevel"] = 0
            gameData["levelUp"] = 0
            gameData["iddqd"] = 0
            file.seek(0)
            file.write(json.dumps(gameData, ensure_ascii=False, indent=2))
            file.truncate()
            file.close()
            msg = "Show's over folks. Nothing to see here."
        else:
            msg = "There isn't a game to reset."
    return msg

# gives the option to erase a player's character
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

# issues a challenge to another player
def message_10_challenge(challenger, opponent, charFolder, game):
    msg = ""
    pOneInfo = None
    bTimer = False
    new_game = 0
    playerOne = ""

    charFile = Path(charFolder + challenger + ".txt")
    # make sure the only people that can issue a challenge, is a person that has a character made.
    if not charFile.is_file():
        msg = "You don't even have a character made to fight."
    else:
        # find opponent's .json file, if one exists.
        with open(charFolder + "playerDatabase.txt", 'r', encoding="utf-8") as file:
            playerDatabase = json.loads(file.read())
            file.close()

        opponentID = ""

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

            playerOne = pOneInfo['name']
            msg = pOneInfo['name'] + " is challenging " + opponent + " (Type '!accept') "
            new_game = 0.5
            timeout = 60
            bTimer = True

    return msg, opponentID, pOneInfo, new_game, bTimer, playerOne, opponent

# allows a player to use a feat while in combat
def message_8_usefeat(answer, charFolder, user, game, playerOne, playerTwo, token, featToken, pOneInfo, pOneSpentFeat,
                      pTwoSpentFeat, pTwoInfo):
    msg = []
    passiveFeats = ['power attack', 'pattack', 'defensive fighting', 'dfight', 'masochist', 'nerve strike', 'improved nerve strike',
                    'greater nerve strike', 'nerve damage', 'evasion', 'improved evasion', 'greater evasion', 'hurt me',
                    'improved hurt me', 'greater hurt me', 'hurt me more', 'deflect', 'improved deflect', 'greater deflect', 'cat grace',
                    'improved cat grace', 'greater cat grace', 'bear endurance', 'improved bear endurance', 'greater bear endurance']
    passiveStats = ['crushing blow', 'improved crushing blow', 'greater crushing blow', 'precision strike',
                    'improved precision strike', 'greater precision strike', 'lightning reflexes',
                    'improved lightning reflexes', 'greater lightning reflexes']
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
                if pOneLastFeat in passiveFeats:
                    msg.append(pOneLastFeat + " will be determined elsewhere.")

                elif pOneLastFeat in passiveStats:
                    msg.append(pOneLastFeat + " is already factored into your attack/defense.")
                # make sure that a player can't reuse a feat already used.
                elif pOneLastFeat in pOneSpentFeat:
                    msg.append("You have already used this feat.")

                # if a feat chosen is on their character sheet, used the feat Dictionary load in the required
                # information to provide benefits/debuffs.
                elif pOneLastFeat in pOneInfo['feats taken']:
                    featToken_new = 1
                    pOneSpentFeat.append(pOneLastFeat)
                    pOneFeatInfo = [pOneLastFeat, featDictionary[0][pOneLastFeat]['action']]
                    msg.append(pOneInfo['name'] + " has used  " + pOneSpentFeat +
                               "")

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

            if answer != 'none':
                pTwoLastFeat = answer
            else:
                pTwoLastFeat = "none"

            if featToken == 0:
                # if the feat is one of the listed below. Tell the player that those feats are used with a different
                # command
                if pTwoLastFeat in ('power attack', 'pattack', 'defensive fighting', 'dfight', 'masochist', 'nerve strike', 'improved nerve strike',
                'greater nerve strike', 'nerve damage', 'evasion', 'improved evasion', 'greater evasion', 'hurt me',
                'improved hurt me', 'greater hurt me', 'hurt me more', 'deflect', 'improved deflect', 'greater deflect'):
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
                    pTwoSpentFeat.append(pTwoLastFeat)
                    pTwoFeatInfo = [pTwoLastFeat, featDictionary[0][pTwoLastFeat]['action']]
                    msg.append(pTwoInfo['name'] + " has used " + pTwoLastFeat +
                               "")

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

# gives the player an option to not use Evasion/Deflect for an attack
def message_7_permit(user, playerOneID, playerTwoID, pOneInfo, pTwoInfo, featToken, count,
                     token, critical, bonusHurt, totalDamage, pOneTotalHP, pTwoTotalHP,
                     pOneCurrentHP,  pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod, pOnemMod,
                     pOneQuickDamage, pTwoQuickDamage, pOneDeathsDoor,\
                     pTwoDeathsDoor, iddqd):
    msg = []
    bGameTimer = False

    if token == 2 and user == playerOne:
        msg.append(pOneInfo['name'] + " has chosen not to prevent this attack.")
        pOneCurrentHP = pOneCurrentHP - totalDamage

        if pOneInfo['regeneration'] != 0 and pOneCurrentHP < pOneTotalHP and pOneCurrentHP > 0:
            msg.append(pOneInfo['name'] + " has regenerated " + str(pOneInfo['regeneration']) +" hp.")
            pOneCurrentHP += pOneInfo['regeneration']

        # Check to see if Player has the feat 'death's door', and if it has been triggered already.
        revive = random.randint(1, 100)
        if "deaths door" in pOneInfo['feats taken'] and pOneCurrentHP <= 0 \
                and revive <= 50 and pOneDeathsDoor == 0:
            returnHeal = random.randint(5, 10) + int(pOneInfo['constitution'] / 2)
            pOneCurrentHP += returnHeal
            pOneDeathsDoor = 1
            msg.append(pOneInfo['name'] + " has returned from death's door, regaining " + str(returnHeal) +
                       " hit points.")
        elif "improved deaths door" in pOneInfo['feats taken'] and pOneCurrentHP <= 0 \
                and revive <= 75 and pOneDeathsDoor == 0:
            returnHeal = random.randint(5, 15) + int(pOneInfo['constitution'] / 2)
            pOneCurrentHP += returnHeal
            pOneDeathsDoor = 1
            msg.append(pOneInfo['name'] + " has returned from death's door, regaining " + str(returnHeal) +
                       " hit points.")
        elif "greater deaths door" in pOneInfo['feats taken'] and pOneCurrentHP <= 0 \
                and revive <= 100 and pOneDeathsDoor == 0:
            returnHeal = random.randint(5, 20) + int(pOneInfo['constitution'] / 2)
            pOneCurrentHP += returnHeal
            pOneDeathsDoor = 1
            msg.append(pOneInfo['name'] + " has returned from death's door, regaining " + str(returnHeal) +
                       " hit points.")
        # Print the scoreboard
        msg.append(pOneInfo['name'] + ": "
                   + str(pOneCurrentHP) + "/" +
                   str(pOneTotalHP) + "  ||  " + pTwoInfo['name'] + ": " +
                   str(pTwoCurrentHP) + "/" + str(pTwoTotalHP) + " \n" +
                   pOneInfo['name'] + "'s turn. Type: !usefeat <feat>"
                                      " if you wish to use a feat.")

        count += 1
        featToken = 0
        token = 1
        pOnedMod = 0
        pOnemMod = 0
        iddqd = 0
        bGameTimer = True
        pOneFeatInfo = None

    elif token == 1 and user == playerTwo:
        msg.append(pTwoInfo['name'] + " has chosen not to evade this attack.")
        # Determine if Quick Strike was used by Player Two and apply damage
        if pTwoQuickDamage != 0:
            pOneCurrentHP = pOneCurrentHP - totalDamage - pTwoQuickDamage
            pOneQuickDamage = 0
        else:
            pTwoCurrentHP = pTwoCurrentHP - totalDamage

        if pTwoInfo['regeneration'] != 0 and pTwoCurrentHP < pTwoTotalHP and pTwoCurrentHP > 0:
            msg.append(pTwoInfo['name'] + " has regenerated " + str(pTwoInfo['regeneration']) +" hp.")
            pTwoCurrentHP += pTwoInfo['regeneration']

        # Check to see if Player has the feat 'death's door', and if it has been triggered already.
        revive = random.randint(1, 100)
        if "deaths door" in pTwoInfo['feats taken'] and pTwoCurrentHP <= 0 \
                and revive <= 50 and pTwoDeathsDoor == 0:
            returnHeal = random.randint(5, 10) + int(pTwoInfo['constitution'] / 2)
            pTwoCurrentHP += returnHeal
            pTwoDeathsDoor = 1
            msg.append(pTwoInfo['name'] + " has returned from death's door, regaining " + str(returnHeal) +
                       " hit points.")
        elif "improved deaths door" in pTwoInfo['feats taken'] and pTwoCurrentHP <= 0 \
                and revive <= 75 and pTwoDeathsDoor == 0:
            returnHeal = random.randint(5, 15) + int(pTwoInfo['constitution'] / 2)
            pTwoCurrentHP += returnHeal
            pTwoDeathsDoor = 1
            msg.append(pTwoInfo['name'] + " has returned from death's door, regaining " + str(returnHeal) +
                       " hit points.")
        elif "greater deaths door" in pTwoInfo['feats taken'] and pTwoCurrentHP <= 0 \
                and revive <= 100 and pTwoDeathsDoor == 0:
            returnHeal = random.randint(5, 20) + int(pTwoInfo['constitution'] / 2)
            pTwoCurrentHP += returnHeal
            pTwoDeathsDoor = 1
            msg.append(pTwoInfo['name'] + " has returned from death's door, regaining " + str(returnHeal) +
                       " hit points.")
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
        iddqd = 0
        bGameTimer = True
    else:
        msg.append("You are either not in the fight, or it's not your turn. Either way, Don't do it again.")

    return msg, bGameTimer, playerOne, playerTwo, pOneInfo, pTwoInfo, featToken, \
           count, token, critical, bonusHurt, totalDamage, pOneTotalHP, pTwoTotalHP, \
           pOneCurrentHP, pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod, pOnemMod, pOneQuickDamage, pTwoQuickDamage,\
           pOneDeathsDoor, pTwoDeathsDoor, iddqd

# gives the player an option to use evasion for an attack
def message_8_evasion(user, playerOneID, playerTwoID, pOneInfo, pTwoInfo, featToken, count,
                      token, critical, bonusHurt, totalDamage, pOneTotalHP, pTwoTotalHP,
                      pOneCurrentHP,  pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod, pOnemMod,
                      pOneQuickDamage, pTwoQuickDamage, iddqd):
    msg = []
    bGameTimer = False

    if token == 2 and user == playerOne:
        for word in pOneInfo['feats taken']:
            if pOneEvade == 1 and word == "evasion":
                totalDamage = int(totalDamage * 0.5)
                pOneEvade = 0
                msg.append(pOneInfo['name'] + " used '" + word + "',"
                           " reducing damage taken to " + str(totalDamage) + ". \n")
            elif pOneEvade == 1 and word == "improved evasion":
                totalDamage = int(totalDamage * 0.25)
                pOneEvade = 0
                msg.append(pOneInfo['name'] + " used '" + word + "', reducing damage taken to " +
                           str(totalDamage) + ". \n")
            elif pOneEvade == 1 and word == "greater evasion":
                totalDamage = 0
                pTwoEvade = 0
                msg.append(pOneInfo['name'] + " used '" + word + "', reducing damage taken to " + str(totalDamage) +
                           ". \n")

        # Determine if Quick Strike was used by Player One and apply damage
        if pOneQuickDamage != 0:
            pTwoCurrentHP = pTwoCurrentHP - totalDamage - pOneQuickDamage
            pOneQuickDamage = 0
        else:
            pOneCurrentHP = pOneCurrentHP - totalDamage

        if pOneInfo['regeneration'] != 0 and pOneCurrentHP < pOneTotalHP and pOneCurrentHP > 0:
            msg.append(pOneInfo['name'] + " has regenerated " + str(pOneInfo['regeneration']) +" hp.")
            pOneCurrentHP += pOneInfo['regeneration']

        # Print the scoreboard
        msg.append(pOneInfo['name'] + ": " + str(pOneCurrentHP) + "/" +
                   str(pOneTotalHP) + "  ||  " + pTwoInfo['name'] + ": " +
                   str(pTwoCurrentHP) + "/" + str(pTwoTotalHP) + " \n" +
                   pOneInfo['name'] + "'s turn. Type: !usefeat <feat>"
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
                msg.append(pTwoInfo['name'] + " used '" + word + "', reducing damage taken to " + str(totalDamage) +
                           ". \n")
            elif pTwoEvade == 1 and word == "improved evasion":
                totalDamage = int(totalDamage * 0.5)
                pTwoEvade = 0
                msg.append(pTwoInfo['name'] + " used '" + str(totalDamage) + "', reducing damage taken to " +
                           str(totalDamage) + ". \n")
            elif pTwoEvade == 1 and word == "greater evasion":
                totalDamage = 0
                pTwoEvade = 0
                msg.append(pTwoInfo['name'] + " used '" + word + "', reducing damage taken to " + str(totalDamage) +
                           ". \n")

        # Determine if Quick Strike was used by Player Two and apply damage
        if pTwoQuickDamage != 0:
            pOneCurrentHP = pOneCurrentHP - totalDamage - pTwoQuickDamage
            pOneQuickDamage = 0
        else:
            pTwoCurrentHP = pTwoCurrentHP - totalDamage

        if pTwoInfo['regeneration'] != 0 and pTwoCurrentHP < pTwoTotalHP and pTwoCurrentHP > 0:
            msg.append(pTwoInfo['name'] + " has regenerated " + str(pTwoeInfo['regeneration']) +" hp.")
            pTwoCurrentHP += pTwoInfo['regeneration']

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
        iddqd = 0
        bGameTimer = True
    else:
        msg.append("You are either not in the fight, or it's not your turn. Either way, Don't do it again.")

    return msg, bGameTimer, playerOne, playerTwo, pOneInfo, pTwoInfo, featToken, \
           count, token, totalDamage, pOneTotalHP, pTwoTotalHP, pOneCurrentHP, pTwoCurrentHP, pOnepMod, pOnecMod, \
           pOnedMod, pOnemMod, pOneQuickDamage, pTwoQuickDamage, iddqd

# gives the player an option to use deflect for an attack
def message_8_deflect(user, playerOne, playerTwo, pOneInfo, pTwoInfo, featToken,
                      count, token, critical, bonusHurt, totalDamage, pOneTotalHP, pTwoTotalHP,
                      pOneCurrentHP, pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod, pOnemMod, pOneQuickDamage,
                      pTwoQuickDamage, pTwoDeflect, pOneDeflect, pOneDeathsDoor, pTwoDeathsDoor, iddqd):
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
                msg.append(pOneInfo['name'] + " used 'deflect' to lessen the blow from " + str(oldDamage) +
                           " to " + str(int(totalDamage)) + "")

            elif word == "improved deflect" and pOneDeflect == 1:
                pOneDeflect = 0
                oldDamage = totalDamage
                totalDamage = int(totalDamage - int(pOneInfo['abac'] * 1.5))
                if totalDamage < 1:
                    totalDamage = 1
                msg.append(pOneInfo['name'] + " used 'deflect' to lessen the blow from " + str(oldDamage) +
                           " to " + str(int(totalDamage)) + "")

            elif word == "greater deflect" and pOneDeflect == 1:
                pOneDeflect = 0
                oldDamage = totalDamage
                totalDamage = int(totalDamage - int(pOneInfo['abac'] * 2))
                if totalDamage < 1:
                    totalDamage = 1
                msg.append(pOneInfo['name'] + " used 'deflect' to lessen the blow from " + str(oldDamage) +
                           " to " + str(int(totalDamage)) + "")

        # Determine if Quick Strike was used by Player One and apply damage
        if pOneQuickDamage != 0:
            pTwoCurrentHP = pTwoCurrentHP - totalDamage - pOneQuickDamage
            pOneQuickDamage = 0
        else:
            pOneCurrentHP = pOneCurrentHP - totalDamage

        if pOneInfo['regeneration'] != 0 and pOneCurrentHP < pOneTotalHP and pOneCurrentHP > 0:
            msg.append(pOneInfo['name'] + " has regenerated " + str(pOneInfo['regeneration']) +" hp.")
            pOneCurrentHP += pOneInfo['regeneration']

            # Check to see if Player has the feat 'death's door', and if it has been triggered already.
        revive = random.randint(1, 100)
        if "deaths door" in pOneInfo['feats taken'] and pOneCurrentHP <= 0 \
                and revive <= 50 and pOneDeathsDoor == 0:
            returnHeal = random.randint(5, 10) + int(pOneInfo['constitution'] / 2)
            pOneCurrentHP += returnHeal
            pOneDeathsDoor = 1
            msg.append(pOneInfo['name'] + " has returned from death's door, regaining " + str(returnHeal) +
                       " hit points.")
        elif "improved deaths door" in pOneInfo['feats taken'] and pOneCurrentHP <= 0 \
                and revive <= 75 and pOneDeathsDoor == 0:
            returnHeal = random.randint(5, 15) + int(pOneInfo['constitution'] / 2)
            pOneCurrentHP += returnHeal
            pOneDeathsDoor = 1
            msg.append(pOneInfo['name'] + " has returned from death's door, regaining " + str(returnHeal) +
                       " hit points.")
        elif "greater deaths door" in pOneInfo['feats taken'] and pOneCurrentHP <= 0 \
                and revive <= 100 and pOneDeathsDoor == 0:
            returnHeal = random.randint(5, 20) + int(pOneInfo['constitution'] / 2)
            pOneCurrentHP += returnHeal
            pOneDeathsDoor = 1
            msg.append(pOneInfo['name'] + " has returned from death's door, regaining " + str(returnHeal) +
                       " hit points.")

        # Print the scoreboard
        msg.append(pOneInfo['name'] + ": " + str(pOneCurrentHP) + "/" +
                   str(pOneTotalHP) + "  ||  " + pTwoInfo['name'] + ": " +
                   str(pTwoCurrentHP) + "/" + str(pTwoTotalHP) + " \n" +
                   pOneInfo['name'] + "'s turn. Type: !usefeat <feat>"
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
                msg.append(pTwoInfo['name'] + " used 'deflect' to lessen the blow from " + str(oldDamage) + " to " +
                           str(int(totalDamage)) + "")

            elif word == "improved deflect" and pTwoDeflect == 1:
                pTwoDeflect = 0
                oldDamage = totalDamage
                totalDamage = int(totalDamage - int(pTwoInfo['abac'] * 1.5))
                if totalDamage < 1:
                    totalDamage = 1
                msg.append(pTwoInfo['name'] + " used 'deflect' to lessen the blow from " + str(oldDamage) +
                           " to " + str(int(totalDamage)) + "")

            elif word == "greater deflect" and pTwoDeflect == 1:
                pTwoDeflect = 0
                oldDamage = totalDamage
                totalDamage = int(totalDamage - int(pTwoInfo['abac'] * 2))
                if totalDamage < 1:
                    totalDamage = 1
                msg.append(pTwoInfo['name'] + " used 'deflect' to lessen the blow from " + str(oldDamage) +
                           " to " + str(int(totalDamage)) + "")

        # Determine if Quick Strike was used by Player Two and apply damage
        if pTwoQuickDamage != 0:
            pOneCurrentHP = pOneCurrentHP - totalDamage - pTwoQuickDamage
            pOneQuickDamage = 0
        else:
            pTwoCurrentHP = pTwoCurrentHP - totalDamage

        if pTwoInfo['regeneration'] != 0 and pTwoCurrentHP < pTwoTotalHP and pTwoCurrentHP > 0:
            msg.append(pTwoInfo['name'] + " has regenerated " + str(pTwoInfo['regeneration']) +" hp.")
            pTwoCurrentHP += pTwoInfo['regeneration']

        # Check to see if Player has the feat 'death's door', and if it has been triggered already.
        revive = random.randint(1, 100)
        if "deaths door" in pTwoInfo['feats taken'] and pTwoCurrentHP <= 0 \
                and revive <= 50 and pTwoDeathsDoor == 0:
            returnHeal = random.randint(5, 10) + int(pTwoInfo['constitution'] / 2)
            pTwoCurrentHP += returnHeal
            pTwoDeathsDoor = 1
            msg.append(pTwoInfo['name'] + " has returned from death's door, regaining " + str(returnHeal) +
                       " hit points.")
        elif "improved deaths door" in pTwoInfo['feats taken'] and pTwoCurrentHP <= 0 \
                and revive <= 75 and pTwoDeathsDoor == 0:
            returnHeal = random.randint(5, 15) + int(pTwoInfo['constitution'] / 2)
            pTwoCurrentHP += returnHeal
            pTwoDeathsDoor = 1
            msg.append(pTwoInfo['name'] + " has returned from death's door, regaining " + str(returnHeal) +
                       " hit points.")
        elif "greater deaths door" in pTwoInfo['feats taken'] and pTwoCurrentHP <= 0 \
                and revive <= 100 and pTwoDeathsDoor == 0:
            returnHeal = random.randint(5, 20) + int(pTwoInfo['constitution'] / 2)
            pTwoCurrentHP += returnHeal
            pTwoDeathsDoor = 1
            msg.append(pTwoInfo['name'] + " has returned from death's door, regaining " + str(returnHeal) +
                       " hit points.")
            
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
        iddqd = 0
        bGameTimer = True
    else:
        msg.append("You are either not in the fight, or it's not your turn. Either way, Don't do it again.")

    return msg, bGameTimer, playerOne, playerTwo, pOneInfo, pTwoInfo, featToken, \
           count, token, totalDamage, pOneTotalHP, pTwoTotalHP, pOneCurrentHP, pTwoCurrentHP, pOnepMod, pOnecMod, \
           pOnedMod, pOnemMod, pOneQuickDamage, pTwoQuickDamage, pTwoDeflect, pOneDeflect, iddqd

# allocates points used for power attack
def message_8_pattack(user, points, game, playerOne, playerTwo, pOneInfo, pTwoInfo, token, pOnepMod, pTwopMod,
                      pOneLevel, pTwoLevel):
    msg = []
    points = int(points)
    # make sure that this command cannot be ran if a fight is taking place.
    try:
        if game == 1:
            # ensures the command can only be used by player one, when it is their turn. To prevent trolls from
            # spamming commands.
            if user == playerOne and token == 1:
                if 'power attack' in pOneInfo['feats taken']:
                    if pOneLevel <= 4 and points == 1:
                        pOnepMod = 1
                        msg.append(pOneInfo['name'] + " invested " + str(points) + " points in 'power attack'")
                    elif 4 < pOneLevel <= 8 and points == 2:
                        pOnepMod = 2
                        msg.append(pOneInfo['name'] + " invested " + str(points) + " points in 'power attack'")
                    elif 8 < pOneLevel <= 12 and points == 3:
                        pOnepMod = 3
                        msg.append(pOneInfo['name'] + " invested " + str(points) + " points in 'power attack'")
                    elif 12 < pOneLevel <= 16 and points == 4:
                        pOnepMod = 4
                        msg.append(pOneInfo['name'] + " invested " + str(points) + " points in 'power attack'")
                    elif 16 < pOneLevel <= 20 and points == 5:
                        pOnepMod = 5
                        msg.append(pOneInfo['name'] + " invested " + str(points) + " points in 'power attack'")
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
                        msg.append(pTwoInfo['name'] + " invested " + str(points) + " points in 'power attack'")
                    elif 4 < pTwoLevel <= 8 and points == 2:
                        pTwopMod = 2
                        msg.append(pTwoInfo['name'] + " invested " + str(points) + " points in 'power attack'")
                    elif 8 < pTwoLevel <= 12 and points == 3:
                        pTwopMod = 3
                        msg.append(pTwoInfo['name'] + " invested " + str(points) + " points in 'power attack'")
                    elif 12 < pTwoLevel <= 16 and points == 4:
                        pTwopMod = 4
                        msg.append(pTwoInfo['name'] + " invested " + str(points) + " points in 'power attack'")
                    elif 16 < pTwoLevel <= 20 and points == 5:
                        pTwopMod = 5
                        msg.append(pTwoInfo['name'] + " invested " + str(points) + " points in 'power attack'")
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

# allocates points used for defensive fighting
def message_8_dfight(user, points, game, playerOne, playerTwo, pOneInfo, pTwoInfo, token, pOnedMod, pTwodMod,
                     pOneLevel, pTwoLevel):
    msg = []
    points = int(points)
    # make sure that this command cannot be ran if a fight is taking place.
    try:
        if game == 1:
            # ensures the command can only be used by player one, when it is their turn. To prevent trolls from
            # spamming commands.
            if user == playerOne and token == 1:
                if 'defensive fighting' in pOneInfo['feats taken']:
                    if pOneLevel <= 4 and points == 1:
                        pOnedMod = 1
                        msg.append(pOneInfo['name'] + " invested " + str(points) + " points in 'defensive fighting'")
                    elif 4 < pOneLevel <= 8 and points == 2:
                        pOnedMod = 2
                        msg.append(pOneInfo['name'] + " invested " + str(points) + " points in 'defensive fighting'")
                    elif 8 < pOneLevel <= 12 and points == 3:
                        pOnedMod = 3
                        msg.append(pOneInfo['name'] + " invested " + str(points) + " points in 'defensive fighting'")
                    elif 12 < pOneLevel <= 16 and points == 4:
                        pOnedMod = 4
                        msg.append(pOneInfo['name'] + " invested " + str(points) + " points in 'defensive fighting'")
                    elif 16 < pOneLevel <= 20 and points == 5:
                        pOnedMod = 5
                        msg.append(pOneInfo['name'] + " invested " + str(points) + " points in 'defensive fighting'")
                    else:
                        msg.append("You are not high enough level to invest that many points.")
                else:
                    msg.append("You do not have this feat.")
            # ensures the command can only be used by player two, when it is their turn. To prevent trolls from
            # spamming commands.
            elif user == playerTwo and token == 2:
                if 'defensive fighting' in pTwoInfo['feats taken']:
                    if pTwoLevel <= 4 and points == 1:
                        pTwodMod = 1
                        msg.append(pTwoInfo['name'] + " invested " + str(points) + " points in 'defensive fighting'")
                    elif 4 < pTwoLevel <= 8 and points == 2:
                        pTwodMod = 2
                        msg.append(pTwoInfo['name'] + " invested " + str(points) + " points in 'defensive fighting'")
                    elif 8 < pTwoLevel <= 12 and points == 3:
                        pTwodMod = 3
                        msg.append(pTwoInfo['name'] + " invested " + str(points) + " points in 'defensive fighting'")
                    elif 12 < pTwoLevel <= 16 and points == 4:
                        pTwodMod = 4
                        msg.append(pTwoInfo['name'] + " invested " + str(points) + " points in 'defensive fighting'")
                    elif 16 < pTwoLevel <= 20 and points == 5:
                        pTwodMod = 5
                        msg.append(pTwoInfo['name'] + " invested " + str(points) + " points in 'defensive fighting'")
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
#                    if user == playerOne and token == 1:
#                        mod = int(message[9:])
#                        if pOneLevel <= 4 and points == 1:
#                            pOnecMod = 1
#                            msg.append(pOneInfo['name'] + " invested "
#                                        + str(points) + " points in 'combat expertise'")
#                        elif 4 < pOneLevel <= 8 and points == 2:
#                            pOnecMod = 2
#                            msg.append(pOneInfo['name'] + " invested "
#                                        + str(points) + " points in 'combat expertise'")
#                        elif 8 < pOneLevel <= 12 and points == 3:
#                            pOnecMod = 3
#                            msg.append(pOneInfo['name'] + " invested "
#                                        + str(points) + " points in 'combat expertise'")
#                        elif 12 < pOneLevel <= 16 and points == 4:
#                            pOnecMod = 4
#                            msg.append(pOneInfo['name'] + " invested "
#                                        + str(points) + " points in 'combat expertise'")
#                        elif 16 < pOneLevel <= 20 and points == 5:
#                            pOnecMod = 5
#                            msg.append(pOneInfo['name'] + " invested "
#                                        + str(points) + " points in 'combat expertise'")
#                        else:
#                            msg.append("You are not high enough level to invest that many points.")
#                    # ensures the command can only be used by player two, when it is their turn. To prevent trolls from
#                    # spamming commands.
#                    elif user == playerTwo and token == 2:
#                        mod = int(message[9:])
#                        if pTwoLevel <= 4 and points == 1:
#                            pTwocMod = 1
#                            msg.append(pTwoInfo['name'] + " invested "
#                                        + str(points) + " points in 'combat expertise'")
#                        elif 4 < pTwoLevel <= 8 and points == 2:
#                            pTwocMod = 2
#                            msg.append(pTwoInfo['name'] + " invested "
#                                        + str(points) + " points in 'combat expertise'")
#                        elif 8 < pTwoLevel <= 12 and points == 3:
#                            pTwocMod = 3
#                            msg.append(pTwoInfo['name'] + " invested "
#                                        + str(points) + " points in 'combat expertise'")
#                        elif 12 < pTwoLevel <= 16 and points == 4:
#                            pTwocMod = 4
#                            msg.append(pTwoInfo['name'] + " invested "
#                                        + str(points) + " points in 'combat expertise'")
#                        elif 16 < pTwoLevel <= 20 and points == 5:
#                            pTwocMod = 5
#                            msg.append(pTwoInfo['name'] + " invested "
#                                        + str(points) + " points in 'combat expertise'")
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


def message_10_masochist(user, points, game, playerOne, playerTwo, pOneInfo, pTwoInfo, token, pOnemMod,
                         pTwomMod, pOneLevel, pTwoLevel):
# allocates points used for masochist
    msg = []
    points = int(points)
    # make sure that this command cannot be ran if a fight is taking place.
    try:
        if game == 1:
            # ensures the command can only be used by player one, when it is their turn. To prevent trolls from
            # spamming commands.
            if user == playerOne and token == 1:
                if 'masochist' in pOneInfo['feats taken']:
                    if pOneLevel <= 4 and points == 1:

                        pOnemMod = 1
                        msg.append(pOneInfo['name'] + " invested " + str(points) + " points in 'masochist'")
                    elif 4 < pOneLevel <= 8 and points == 2:
                        pOnemMod = 2
                        msg.append(pOneInfo['name'] + " invested " + str(points) + " points in 'masochist'")
                    elif 8 < pOneLevel <= 12 and points == 3:
                        pOnemMod = 3
                        msg.append(pOneInfo['name'] + " invested " + str(points) + " points in 'masochist'")
                    elif 12 < pOneLevel <= 16 and points == 4:
                        pOnemMod = 4
                        msg.append(pOneInfo['name'] + " invested " + str(points) + " points in 'masochist'")
                    elif 16 < pOneLevel <= 20 and points == 5:
                        pOnemMod = 5
                        msg.append(pOneInfo['name'] + " invested " + str(points) + " points in 'masochist'")
                    else:
                        msg.append("You are not high enough level to invest that many points.")
                else:
                    msg.append("You do not have this feat.")
            # ensures the command can only be used by player two, when it is their turn. To prevent trolls from
            # spamming commands.
            elif user == playerTwo and token == 2:
                if 'masochist' in pTwoInfo['feats taken']:
                    if pTwoLevel <= 4 and points == 1:

                        pTwomMod = 1
                        msg.append(pTwoInfo['name'] + " invested " + str(points) + " points in 'masochist'")
                    elif 4 < pTwoLevel <= 8 and points == 2:
                        pTwomMod = 2
                        msg.append(pTwoInfo['name'] + " invested " + str(points) + " points in 'masochist'")
                    elif 8 < pTwoLevel <= 12 and points == 3:
                        pTwomMod = 3
                        msg.append(pTwoInfo['name'] + " invested " + str(points) + " points in 'masochist'")
                    elif 12 < pTwoLevel <= 16 and points == 4:
                        pTwomMod = 4
                        msg.append(pTwoInfo['name'] + " invested " + str(points) + " points in 'masochist'")
                    elif 16 < pTwoLevel <= 20 and points == 5:
                        pTwomMod = 5
                        msg.append(pTwoInfo['name'] + " invested " + str(points) + " points in 'masochist'")
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

# allows player to buy armor from market
def message_9_buyarmor(player, armorslot, charFolder, itemFolder):
    armorFile = open("armor.txt", "r", encoding="utf-8")
    armorData = json.load(armorFile)
    armorFile.close()
    try:
        charFile = open(charFolder + player.lower() + ".txt", "r", encoding="utf-8")
        charSheet = json.load(charFile)
        charFile.close()
        isCharacter = Path(charFolder + player.lower() + ".txt")
    except FileNotFoundError:
        msg = "You don't have a character made to use this function."
        return msg

    if armor not in armorData[0]['armorlist']:
        msg = "Please make sure you typed in your desired choice correctly."
    else:
        choice = armorData[0]['armorlist'][armor]
        if choice == "sold":
            msg = "This armor has already been sold."
            return msg
        armorString = ", ".join(choice)
        price = 0
        if isCharacter.is_file():
            for word in choice:
                if word in armorData[0]["cat1"]["common"]:
                    price += armorData[0]["cat1"]["common"][word][0]
                elif word in armorData[0]["cat1"]['uncommon']:
                    price += armorData[0]["cat1"]['uncommon'][word][0]
                elif word in armorData[0]["cat1"]['rare']:
                    price += armorData[0]["cat1"]['rare'][word][0]
                if word in armorData[0]["cat2"]["common"]:
                    price += armorData[0]["cat2"]["common"][word][0]
                elif word in armorData[0]["cat2"]["uncommon"]:
                    price += armorData[0]["cat2"]["uncommon"][word][0]
                elif word in armorData[0]["cat2"]["rare"]:
                    price += armorData[0]["cat2"]["rare"][word][0]
                if word in armorData[0]["cat3"]["common"]:
                    price += armorData[0]["cat3"]["common"][word][0]
                elif word in armorData[0]["cat3"]["uncommon"]:
                    price += armorData[0]["cat3"]["uncommon"][word][0]
                elif word in armorData[0]["cat3"]["rare"]:
                    price += armorData[0]["cat3"]["common"][word][0]
                else:
                    msg = "Select an armor that is listed (Example: !buyarmor armor4)"
        invList = []
        for keys in charSheet['armor']:
            invList.append(keys)
        armor1 = invList[0]
        armor2 = invList[1]
        armor3 = invList[2]
        if price <= charSheet['gold']:
            if charSheet['armor'][armor1] != "n/a" \
                    and charSheet['armor'][armor2] != "n/a"\
                    and charSheet['armor'][armor3] != "n/a":
                msg = "You do not have enough inventory space to own more armor."
            else:
                charSheet['gold'] -= price
                armorData[0]["armorlist"][armor] = "sold"
                if charSheet['armor'][armor1] == "n/a":
                    charSheet['armor'][armor1] = choice
                    charSheet['armor'][armor1].append(price)
                elif charSheet['armor'][armor2] == "n/a":
                    charSheet['armor'][armor2] = choice
                    charSheet['armor'][armor2].append(price)
                elif charSheet['armor'][armor3] == "n/a":
                    charSheet['armor'][armor3] = choice
                    charSheet['armor'][armor3].append(price)
                msg = "You have puchased an armor of " + armorString + "."
        else:
            msg = "You do not have enough gold to purchase this."

        file = open(charFolder + player + ".txt", "w", encoding="utf-8")
        json.dump(charSheet, file, ensure_ascii=False, indent=2)
        file.close()

        file = open("armor.txt", "w", encoding="utf-8")
        json.dump(armorData, file, ensure_ascii=False, indent=2)
        file.close()
    return msg

# allows player to sell armor for half cost
def message_10_sellarmor(player, armorname, charFolder, itemFolder):
    armorFile = open(itemFolder + "armor.txt", "r", encoding="utf-8")
    armorDictionary = json.load(armorFile)
    armorFile.close()

    try:
        sellerFile = open(charFolder + player + ".txt", "r", encoding="utf-8")
        sellerData = json.load(sellerFile)
        sellerFile.close()
    # isCharacter = Path(charFolder + player + ".txt")
    except FileNotFoundError:
        msg = player + " does not have a character to use this command."
        return msg
    if armor in sellerData['armor']:
        if armor in sellerData['equip']:
            msg = "You can't sell armor that is currently equipped."
        else:
            price = int(sellerData['armor'][armor][-1] / 2)
            sellerData['gold'] += price
            sellerData['armor'][armor] = "n/a"
            if 'armor1' not in sellerData['armor']:
                sellerData["armor"]['armor1'] = sellerData['armor'].pop(armor)
            elif 'armor2' not in sellerData['armor']:
                sellerData["armor"]['armor2'] = sellerData['armor'].pop(armor)
            elif 'armor3' not in sellerData['armor']:
                sellerData["armor"]['armor3'] = sellerData['armor'].pop(armor)
            msg = player + " sold some armor for  " + str(price) + " gold"
    else:
        msg = "You do not have that armor to sell."

    file = open(charFolder + player + ".txt", "w", encoding="utf-8")
    json.dump(sellerData, file, ensure_ascii=False, indent=2)
    file.close()
    return msg

# allows player to name their armor
def message_10_namearmor(player, oldName, newName, charFolder):
    try:
        charFile = open(charFolder + player + ".txt", "r", encoding="utf-8")
        charSheet = json.load(charFile)
        charFile.close()
    except FileNotFoundError:
        msg = "You don't have a character made to use this function."
        return msg

    if armorRemove not in charSheet['armor'].keys():
        msg = armorRemove + " is not within your inventory to rename"
    elif armorName in charSheet['armor'].keys():
        msg = "You already have a piece of armor named " + armorName
    elif charSheet['armor'][armorRemove]  != []:
        charSheet['armor'][armorName] = charSheet['armor'].pop(armorRemove)
        msg = charSheet['name'] + " renamed " + armorRemove + " to " + armorName + "."
    else:
        msg = "There is no armor in that slot to rename."
    file = open(charFolder + player + ".txt", "w", encoding="utf-8")
    json.dump(charSheet, file, ensure_ascii=False, indent=2)
    file.close()

    return msg

# allows player to equip their armor
def message_6_equip(armor, player, charFolder):
    try:
        charFile = open(charFolder + player + ".txt", "r", encoding="utf-8")
        charSheet = json.load(charFile)
        charFile.close()
        isCharacter = Path(charFolder + player + ".txt")
    except FileNotFoundError:
        msg = "You don't have a character made to use this command."
        return msg

    armorFile = open("armor.txt", "r", encoding="utf-8")
    armorDictionary = json.load(armorFile)
    armorFile.close()

    charSheet["armorhit"] = 0
    charSheet["armordamage"] = 0
    charSheet["armorac"] = 0
    charSheet["armorhp"] = 0
    charSheet["armordr"] = 0
    charSheet["armorinitiative"] = 0
    charSheet["armorstrength"] = 0
    charSheet["armordexterity"] = 0
    charSheet["armorconstitution"] = 0
    charSheet["armorblur"] = 0
    if armor in charSheet['armor']:
        charSheet['equip'] = armor
        msg = charSheet['name'] + " has equipped " + armor
        if len(charSheet['armor'][armor]) == 2:
            statOne = charSheet['armor'][armor][0]
            statTwo = ""
            statThree = ""
        elif len(charSheet['armor'][armor]) == 3:
            statOne = charSheet['armor'][armor][0]
            statTwo = charSheet['armor'][armor][1]
            statThree = ""
        elif len(charSheet['armor'][armor]) == 4:
            statOne = charSheet['armor'][armor][0]
            statTwo = charSheet['armor'][armor][1]
            statThree = charSheet['armor'][armor][2]
        if statOne != "":
            if statOne in armorDictionary[0]["cat1"]["common"]:
                statOneValue = armorDictionary[0]["cat1"]["common"][statOne][1]
            elif statOne in armorDictionary[0]["cat1"]["uncommon"]:
                statOneValue = armorDictionary[0]["cat1"]["uncommon"][statOne][1]
            elif statOne in armorDictionary[0]["cat1"]["rare"]:
                statOneValue = armorDictionary[0]["cat1"]["rare"][statOne][1]
        if statTwo != "":
            if statTwo in armorDictionary[0]["cat2"]["common"]:
                statTwoValue = armorDictionary[0]["cat2"]["common"][statTwo][1]
            elif statTwo in armorDictionary[0]["cat2"]["uncommon"]:
                statTwoValue = armorDictionary[0]["cat2"]["uncommon"][statTwo][1]
            elif statTwo in armorDictionary[0]["cat2"]["rare"]:
                statTwoValue = armorDictionary[0]["cat2"]["rare"][statTwo][1]
        if statThree != "":
            if statThree in armorDictionary[0]["cat3"]["common"]:
                statThreeValue = armorDictionary[0]["cat3"]["common"][statThree][1]
            elif statThree in armorDictionary[0]["cat3"]["uncommon"]:
                statThreeValue = armorDictionary[0]["cat3"]["uncommon"][statThree][1]
            elif statThree in armorDictionary[0]["cat3"]["rare"]:
                statThreeValue = armorDictionary[0]["cat3"]["rare"][statThree][1]
        if statOne[:2] == "st":
            charSheet["armorstrength"] = statOneValue
        elif statOne[:2] == "de":
            charSheet["armordexterity"] = statOneValue
        elif statOne[:2] == "co":
            charSheet["armorconstitution"] = statOneValue
        if statTwo[:2] == "da":
            charSheet["armordamage"] = statTwoValue
        elif statTwo[:2] == "hi":
            charSheet["armorhit"] = statTwoValue
        elif statTwo[:2] == "in":
            charSheet["armorinitiative"] = statTwoValue
        if statThree[:2] == "dr":
            charSheet["armordr"] = statThreeValue
        elif statThree[:2] == "ac":
            charSheet["armorac"] = statThreeValue
        elif statThree[:2] == "bl":
            charSheet["armorblur"] += statThreeValue
    else:
        msg = armor + " doesn't exist in your inventory."

    file = open(charFolder + player + ".txt", "w", encoding="utf-8")
    json.dump(charSheet, file, ensure_ascii=False, indent=2)
    file.close()
    return msg

# allows player to unequip their armor
def message_8_unequip(armor, player, charFolder):
    try:
        charFile = open(charFolder + player + ".txt", "r", encoding="utf-8")
        charSheet = json.load(charFile)
        charFile.close()
        isCharacter = Path(charFolder + player + ".txt")
    except FileNotFoundError:
        msg = "You don't have a character made to use this function."
        return msg

    charSheet['equip'] = ""
    msg = charSheet['name'] + " has unequipped " + armor
    charSheet["armorhit"] = 0
    charSheet["armordamage"] = 0
    charSheet["armorac"] = 0
    charSheet["armorhp"] = 0
    charSheet["armordr"] = 0
    charSheet["armorinitiative"] = 0
    charSheet["armorstrength"] = 0
    charSheet["armordexterity"] = 0
    charSheet["armorconstitution"] = 0
    charSheet["armorblur"] = 0

    file = open(charFolder + player + ".txt", "w", encoding="utf-8")
    json.dump(charSheet, file, ensure_ascii=False, indent=2)
    file.close()
    return msg

# allows player to buy potions from the market
def message_10_buypotion(player, potion, charFolder, itemFolder):
    try:
        charFile = open(charFolder + player + ".txt", "r", encoding="utf-8")
        charSheet = json.load(charFile)
        charFile.close()
        isCharacter = Path(charFolder + player + ".txt")
    except FileNotFoundError:
        msg = "You don't have a character made to use this function."

    potionList = potionData[0]['shoplist']
    if isCharacter.is_file():
        if potion in potionList:
            if potion in potionData[0]['common']:
                price = potionData[0]['common'][potion][0]
            elif potion in potionData[0]['uncommon']:
                price = potionData[0]['uncommon'][potion][0]
            elif potion in potionData[0]['rare']:
                price = potionData[0]['rare'][potion][0]
            elif potion in potionData[0]['vrare']:
                price = potionData[0]['vrare'][potion][0]
            elif potion in potionData[0]['relic']:
                price = potionData[0]['relic'][potion][0]
            else:
                msg = "That potion is not being sold right now."
        if price <= charSheet['gold']:
            if len(charSheet['potions']) >= 5:
                msg = "You do not have enough inventory space to own more potions."
            else:
                charSheet['gold'] -= price
                potionData[0]['shoplist'].remove(potion)
                charSheet['potions'].append(potion)
                msg = "You have puchased a potion of " + potion + "."
        else:
            msg = "You do not have enough gold to purchase this."

    file = open(charFolder + player + ".txt", "w", encoding="utf-8")
    json.dump(charSheet, file, ensure_ascii=False, indent=2)
    file.close()

    file = open("potions.txt", "w", encoding="utf-8")
    json.dump(potionData, file, ensure_ascii=False, indent=2)
    file.close()
    return msg

# allows player to give a potion to another player
def message_11_givepotion(potion, gifter,  gifted, charFolder):
    msg = ""
    with open(charFolder + "playerDatabase.txt", 'r', encoding="utf-8") as file2:
        playerDatabase = json.loads(file2.read())
        file2.close()

    for item in playerDatabase.items():
        if item[0].lower() == gifted.lower():
            gifted = item[1]
        else:
            msg = gifted + " isn't a character name."

    file = open(charFolder + gifter + ".txt", "r", encoding="utf-8")
    gifterData = json.load(file)
    file.close()

    file = open(charFolder + gifted + ".txt", "r", encoding="utf-8")
    giftedData = json.load(file)
    file.close()

    if potion.lower() not in gifterData['potions']:
        msg = "You do not have this item to give."
    elif potion.lower() in gifterData['potions'] and len(giftedData['potions']) <= 3:
        gifterData['potions'].remove(item.lower())
        giftedData['potions'].append(item.lower())
        msg = gifterData['name'] + " has given " + giftedData['name'] + " a potion of " + potion.lower()
    else:
        msg = giftedData['name'] + " has no space in their inventory to take this item."
    #     else:
    #         msg = gifted + " does not have a character to use this command."
    # else:
    #
    file = open(charFolder + gifter + ".txt", "w", encoding="utf-8")
    json.dump(gifterData, file, ensure_ascii=False, indent=2)
    file.close()

    file = open(charFolder + gifted + ".txt", "w", encoding="utf-8")
    json.dump(giftedData, file, ensure_ascii=False, indent=2)
    file.close()

    return msg

# allows player to sell a potion for half cost
def message_11_sellpotion(player, potion, charFolder):
    potionFile = open("potions.txt", "r", encoding="utf-8")
    potionDictionary = json.load(potionFile)
    potionFile.close()

    try:
        sellerFile = open(charFolder + player + ".txt", "r", encoding="utf-8")
        sellerData = json.load(sellerFile)
        sellerFile.close()
    # isCharacter = Path(charFolder + player + ".txt")
    except FileNotFoundError:
        msg = player + " does not have a character to use this command."

    if potion in sellerData['potions']:
        if potion in potionDictionary[0]['common']:
            price = potionDictionary[0]['common'][potion][0]
            halfPrice = price / 2
            sellerData['gold'] += halfPrice
            sellerData['potions'].remove(potion)
            msg = sellerData['name'] + "has sold a " + potion + " for  " +\
                str(halfPrice) + "gold ."
        elif potion in potionDictionary[0]['uncommon']:
            price = potionDictionary[0]['uncommon'][potion][0]
            halfPrice = price / 2
            sellerData['gold'] += halfPrice
            sellerData['potions'].remove(potion)
            msg = sellerData['name'] + "has sold a " + potion + " for  " + \
                str(halfPrice) + "gold ."
        elif potion in potionDictionary[0]['rare']:
            price = potionDictionary[0]['rare'][potion][0]
            halfPrice = price / 2
            sellerData['gold'] += halfPrice
            sellerData['potions'].remove(potion)
            msg = sellerData['name'] + "has sold a " + potion + " for  " +\
                str(halfPrice) + "gold ."
        elif potion in potionDictionary[0]['vrare']:
            price = potionDictionary[0]['vrare'][potion][0]
            halfPrice = price / 2
            sellerData['gold'] += halfPrice
            sellerData['potions'].remove(potion)
            msg = sellerData['name'] + "has sold a " + potion + " for  " + \
                str(halfPrice) + "gold ."
        elif potion in potionDictionary[0]['relic']:
            price = potionDictionary[0]['relic'][potion][0]
            halfPrice = price / 2
            sellerData['gold'] += halfPrice
            sellerData['potions'].remove(potion)
            msg = sellerData['name'] + "has sold a " + potion + " for  " + \
                str(halfPrice) + "gold ."
        else:
            msg = "You do not have that potion to sell."
    file = open(charFolder + player + ".txt", "w", encoding="utf-8")
    json.dump(sellerData, file, ensure_ascii=False, indent=2)
    file.close()
    return msg

# allows a player to use a potion before combat
def message_10_usepotion(potion, player, commonList, uncommonList, rareList, vrareList, relicList, charFolder):
        potionFile = open(charFolder + "potions.txt", "r", encoding="utf-8")
        potionData = json.load(potionFile)
        potionFile.close()
        try:
            charFile = open(charFolder + player + ".txt", "r", encoding="utf-8")
            charSheet = json.load(charFile)
            charFile.close()
            isCharacter = Path(charFolder + player + ".txt")
        except FileNotFoundError:
            msg = "You don't have a character made to use these potions."
            return msg

        potionList = commonList + uncommonList + rareList + vrareList + relicList
        if potion in potionList:
            if potion in commonList:
                potionEffect = potionData[0]['common'][potion][2]
                potionDescription = potionData[0]['common'][potion][1]
            elif potion in uncommonList:
                potionEffect = potionData[0]['uncommon'][potion][2]
                potionDescription = potionData[0]['uncommon'][potion][1]
            elif potion in rareList:
                potionEffect = potionData[0]['rare'][potion][2]
                potionDescription = potionData[0]['rare'][potion][1]
            elif potion in vrareList:
                potionEffect = potionData[0]['vrare'][potion][2]
                potionDescription = potionData[0]['vrare'][potion][1]
            elif potion in relicList:
                potionEffect = potionData[0]['relic'][potion][2]
                potionDescription = potionData[0]['relic'][potion][1]
            if potion == "str1" and charSheet['pstrength'] == 0:
                charSheet['pstrength'] = 1
                msg = charSheet['name'] + " drank a " + potion + \
                    " potion, obtaining a permanent  +1 to strength"
                charSheet['potions'].remove(potion)
            elif potion == "dex1" and charSheet['pdexterity'] == 0:
                charSheet['pdexterity'] = 1
                msg = charSheet['name'] + " drank a " + potion +\
                    " potion, obtaining a permanent  +1 to dexterity"
                charSheet['potions'].remove(potion)
            elif potion == "con1" and charSheet['pconstitution'] == 0:
                charSheet['pconstitution'] = 1
                msg = charSheet['name'] + " drank a " + potion +\
                    " potion, obtaining a permanent  +1 to constitution"
                charSheet['potions'].remove(potion)
            elif potion == "str2" and charSheet['pstrength'] == 1:
                charSheet['pstrength'] = 2
                msg = charSheet['name'] + " drank a " + potion +\
                    " potion, obtaining a permanent  +1 to strength"
                charSheet['potions'].remove(potion)
            elif potion == "dex2" and charSheet['pdexterity'] == 1:
                charSheet['pdexterity'] = 2
                msg = charSheet['name'] + " drank a " + potion +\
                    " potion, obtaining a permanent  +1 to dexterity"
                charSheet['potions'].remove(potion)
            elif potion == "con2" and charSheet['pconstitution'] == 1:
                charSheet['pconstitution'] = 2
                msg = charSheet['name'] + " drank a " + potion +\
                    " potion, obtaining a permanent  +1 to constitution"
                charSheet['potions'].remove(potion)
            elif potion == "str3" and charSheet['pstrength'] == 2:
                charSheet['pstrength'] = 3
                msg = charSheet['name'] + " drank a " + potion +\
                    " potion, obtaining a permanent  +1 to strength"
                charSheet['potions'].remove(potion)
            elif potion == "dex3" and charSheet['pdexterity'] == 2:
                charSheet['pdexterity'] = 3
                msg = charSheet['name'] + " drank a " + potion +\
                    " potion, obtaining a permanent  +1 to dexterity"
                charSheet['potions'].remove(potion)
            elif potion == "con3" and charSheet['pconstitution'] == 2:
                charSheet['pconstitution'] = 3
                msg = charSheet['name'] + " drank a " + potion +\
                    " potion, obtaining a permanent  +1 to constitution"
                charSheet['potions'].remove(potion)
            elif potion == "str4" and charSheet['pstrength'] == 3:
                charSheet['pstrength'] = 4
                msg = charSheet['name'] + " drank a " + potion +\
                    " potion, obtaining a permanent  +1 to strength"
                charSheet['potions'].remove(potion)
            elif potion == "dex4" and charSheet['pdexterity'] == 3:
                charSheet['pdexterity'] = 4
                msg = charSheet['name'] + " drank a " + potion +\
                    " potion, obtaining a permanent  +1 to dexterity"
                charSheet['potions'].remove(potion)
            elif potion == "con4" and charSheet['pconstitution'] == 3:
                charSheet['pconstitution'] = 4
                msg = charSheet['name'] + " drank a " + potion +\
                    " potion, obtaining a permanent  +1 to constitution"
                charSheet['potions'].remove(potion)
            elif potion == "str5" and charSheet['pstrength'] == 4:
                charSheet['pstrength'] = 5
                msg = charSheet['name'] + " drank a " + potion +\
                    " potion, obtaining a permanent  +1 to strength"
                charSheet['potions'].remove(potion)
            elif potion == "dex5" and charSheet['pdexterity'] == 4:
                charSheet['pdexterity'] = 5
                msg = charSheet['name'] + " drank a " + potion +\
                    " potion, obtaining a permanent  +1 to dexterity"
                charSheet['potions'].remove(potion)
            elif potion == "con5" and charSheet['pconstitution'] == 4:
                charSheet['pconstitution'] = 5
                msg = charSheet['name'] + " drank a " + potion +\
                    " potion, obtaining a permanent  +1 to constitution"
                charSheet['potions'].remove(potion)
            else:
                msg = "This potion is either too powerful or too weak to use right now."
            if potion == "respec":
                charSheet['reset'] += 1
                msg = charSheet['name'] + " drank a " + potion + " potion. Allowing them a chance to change their " \
                    "feats, traits, and stat points."
                charSheet['potions'].remove(potion)
            elif potion == "stimulant":
                charSheet['remaining feats'] += 1
                charSheet['total feats'] += 1
                msg = charSheet['name'] + " drank a " + potion + " potion. Allowing them to learn a new feat they " \
                    "qualify for."
                charSheet['potions'].remove(potion)
            elif charSheet['potioneffect'] == "":
                if potion[:3] == "hit":
                    charSheet['potionhit'] = potionEffect
                    charSheet['potioneffect'] = potionDescription
                    msg = charSheet['name'] + " drank a " + potion + " potion, " +\
                        potionDescription + " for next match."
                    charSheet['potions'].remove(potion)
                elif potion[:6] == "damage":
                    charSheet['potiondamage'] = potionEffect
                    charSheet['potioneffect'] = potionDescription
                    msg = charSheet['name'] + "drank a " + potion + " potion, " + potionDescription +\
                        " for next match."
                    charSheet['potions'].remove(potion)
                elif potion[:2] == "ac":
                    charSheet['potionac'] = potionEffect
                    charSheet['potioneffect'] = potionDescription
                    msg = charSheet['name'] + " drank a " + potion + " potion, " + potionDescription +\
                        " for next match."
                    charSheet['potions'].remove(potion)
                elif potion[:4] == "init":
                    charSheet['potioninitiative'] = potionEffect
                    charSheet['potioneffect'] = potionDescription
                    msg = charSheet['name'] + " drank a " + potion + " potion, " +\
                        potionDescription + " for next match."
                    charSheet['potions'].remove(potion)
                elif potion[:2] == "hp":
                    charSheet['potionhp'] = potionEffect
                    charSheet['potioneffect'] = potionDescription
                    msg = charSheet['name'] + " drank a " + potion + " potion, " +\
                        potionDescription + " for next match."
                    charSheet['potions'].remove(potion)
                elif potion[:2] == "bl":
                    charSheet['potionblur'] += potionEffect
                    charSheet['potioneffect'] = potionDescription
                    msg = charSheet['name'] + " drank a " + potion + " potion, " + \
                          potionDescription + " for next match."
                    charSheet['potions'].remove(potion)
            else:
                msg = "You already have a potion in effect."
        else:
            msg = "You do not have a potion of " + potion

        file = open(charFolder + player + ".txt", "w", encoding="utf-8")
        json.dump(charSheet, file, ensure_ascii=False, indent=2)
        file.close()

        return msg

# allows a player to give gold to another player
def message_11_givegold(amount, gifter, gifted, charFolder):
    msg = ""
    with open(charFolder + "playerDatabase.txt", 'r', encoding="utf-8") as file2:
        playerDatabase = json.loads(file2.read())
        file2.close()

    for item in playerDatabase.items():
        if item[0].lower() == gifted.lower():
            gifted = item[1]
        else:
            msg = gifted + " isn't a character name."

    file = open(charFolder + gifter + ".txt", "r", encoding="utf-8")
    gifterData = json.load(file)
    file.close()

    file = open(charFolder + gifted + ".txt", "r", encoding="utf-8")
    giftedData = json.load(file)
    file.close()
    # if isCharacter.is_file():
    #     if isAlsoCharacter.is_file():
    if gold > gifterData['gold']:
        msg = "You do not have this much to give."
    else:
        gifterData['gold'] -= gold
        giftedData['gold'] += gold
        msg = gifterData['name'] + " has given " + giftedData['name'] + " " + str(gold) +\
            " gold"

    file = open(charFolder + gifter + ".txt", "w", encoding="utf-8")
    json.dump(gifterData, file, ensure_ascii=False, indent=2)
    file.close()

    file = open(charFolder + gifted + ".txt", "w", encoding="utf-8")
    json.dump(giftedData, file, ensure_ascii=False, indent=2)
    file.close()
    return msg
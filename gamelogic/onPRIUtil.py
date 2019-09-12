import os
import json
import random
import time
from pathlib import Path
from threading import Timer


def pri_6_stats(charData, charFolder, charFile, player, strength, dexterity, constitution):
    msg = []
    strength = int(strength)
    dexterity = int(dexterity)
    constitution = int(constitution)
    ap = charData["ap"]
    reset = charData["reset"]
    total = strength + dexterity + constitution
    # Find out if player even has a character created yet. If not. Tell them they are an idiot.
    if not charFile.is_file():
        msg.append("You don't even have a character created yet. Type !name <name> in the room. "
                   "Where <name> is your character's actual name. (Example: !name Joe")
    # Find out if player has reset points to use. If not. Tell them they are an idiot.
    elif charData['strength'] != 0 and charData['dexterity'] != 0 and charData['constitution'] != 0:
        msg.append("You have already set up your character's stats. If you want to change them, you will "
                   "need to appeal to a moderator for them to reset it.")

    # If it turns out, they aren't an idiot, and are using the command correctly. Record information and place
    # it in .json.
    else:
        total = strength + dexterity + constitution
        if total > ap or total < ap:
            msg.append("You've allocated more points than you have. Make sure total points used is less than" + str(
                ap) + ".")
        elif strength > 10 or dexterity > 10 or constitution > 10:
            msg.append("No one stat can be above 10 at this point in time. Please try again.")
        else:
            strMod = int(int(strength) / 2)
            dexMod = int(int(dexterity) / 2)
            conMod = int(int(constitution) / 2) * 5
            msg.append("Allocating the following: \n\n"
                       "Strength: " + str(strength) + "   (+" + str(strMod) +
                       " bonus to hit and damage.)\n"
                       "Dexterity: " + str(dexterity) +
                       "   (+" + str(dexMod) + " bonus to armor class.)\n"
                                               "Constitution: " + str(constitution) + "   "
                                                                                      "(+" + str(
                conMod) + " bonus to hit points.)\n")
            msg.append("The above points have been placed on your character sheet. Please "
                       "type !viewchar to see your character sheet. "
                       "You need to chose two feats as well. Type !feat list "
                       "to see a list of feats. Type !feat help <feat name>, "
                       "to get help on a specific feat, or type "
                       "!feat pick <feat name> to choose that feat.")

            # load the new data in the character's .json file.
            with open(charFolder + player + ".txt", "r+", encoding="utf-8") as file:
                charData = json.load(file)
                charData["strength"] = int(strength)
                charData["dexterity"] = int(dexterity)
                charData["constitution"] = int(constitution)
                charData["abhit"] = strMod
                charData["abdamage"] = strMod
                charData["abac"] = dexMod
                charData["abhp"] = conMod
                file.seek(0)
                file.write(json.dumps(charData, ensure_ascii=False, indent=2))
                file.truncate()
                file.close()
    return msg

def pri_4_add(player, ability):
    msg = []
    answer = ["str", "strength", "dex", "dexterity", "con", "constitution"]
    if ability not in answer:
        msg.append("You need to specify the ability you want to point the point to. I couldn't have made it "
                   "any more simple for you. Type '!add str' or '!add strength' for strength, and so on."
                   " I don't even need a number, just follow the instructions, and I'll do the rest.")
    else:
        with open(charFolder + player + ".txt", "r+", encoding="utf-8") as file:
            charData = json.load(file)
            strength = charData['strength']
            dexterity = charData['dexterity']
            constitution = charData['constitution']
            total = strength + dexterity + constitution
            if total < charData['ap']:
                if ability == "strength" or ability == "str":
                    charData['strength'] += 1
                    charData['abhit'] = int(charData['strength'] / 2)
                    charData['abdamage'] = int(charData['strength'] / 2)
                    file.seek(0)
                    file.write(json.dumps(charData, ensure_ascii=False, indent=2))
                    file.truncate()
                    msg.append("You have added an ability point to Strength. Please use !viewchar to ensure changes are correct.")
                if ability == "dexterity" or ability == "dex":
                    charData['dexterity'] += 1
                    charData['abac'] = int(charData['dexterity'])
                    file.seek(0)
                    file.write(json.dumps(charData, ensure_ascii=False, indent=2))
                    file.truncate()
                    msg.append("You have added an ability point to Dexterity. Please use !viewchar to ensure changes are correct.")
                if ability == "constitution" or ability == "con":
                    charData['constitution'] += 1
                    charData['abhp'] = int(charData['constitution'])
                    file.seek(0)
                    file.write(json.dumps(charData, ensure_ascii=False, indent=2))
                    file.truncate()
                    msg.append("You have added an ability point to Constitution. Please use !viewchar to ensure changes are correct.")
                file.close()
            else:
                msg.append("You do not have any more ability points to spend.")
    return msg

def pri_viewchar(player):
    msg = []
    path = os.getcwd()
    charFolder = os.path.join(path + "/characters/")
    charFile = Path(charFolder + player + ".txt")

    if not charFile.is_file():
        msg.append("You don't even have a character created yet. Type !name <name> in the room. "
                   "Where <name> is your character's actual name. (Example: !name Joe")
    # If it turns out the are not an idiot, and are using the command correctly. Display the character shit
    # as nicely as you can in F-list...which isn't nice at all.
    else:
        try:
            charSheet = open(charFolder + player + ".txt", "r+", encoding="utf-8")
            charData = json.load(charSheet)
            charSheet.close()
            name = charData['name']
            level = charData['level']
            hp = charData['hp']
            tFeats = charData['total feats']
            baseDamage = charData['base damage']
            hit = charData['hit']
            damage = charData['damage']
            ac = charData['ac']
            xp = charData['currentxp']
            nextLevel = charData['nextlevel']
            strength = charData['strength']
            dexterity = charData['dexterity']
            constitution = charData['constitution']
            remainingFeats = charData['remaining feats']
            hasTaken = charData['feats taken']
            hiddenTaken = charData['hfeats taken']
            dr = charData['dr']
            ap = charData['ap']
            reset = charData['reset']
            wins = charData['wins']
            losses = charData['losses']
            abhp = charData["abhp"]
            abhit = charData["abhit"]
            abdamage = charData["abdamage"]
            abac = charData["abac"]
            feathp = charData["feathp"]
            feathit = charData["feathit"]
            featdamage = charData["featdamage"]
            featac = charData["featac"]
            dexfighter = charData["dexfigher"]
            thp = charData["thp"]
            tac = charData["tac"]
            thit = charData["thit"]
            tdamage = charData["tdamage"]
        except:
            pass

        thp = hp + abhp + feathp
        tdamage = damage + abdamage + featdamage
        tac = ac + abac + featac
        hasTakenList = ", ".join(hasTaken)
        thit = hit + abhit + feathit
        for feat in hasTaken:
            if feat == 'dexterous fighter':
                thit = hit + abac + feathit

        msg.append("```\n"
                   "Character Name:                " + name + "\n"
                   "Strength:                      " + str(strength) + "          Level:                         " + str(level) + "\n"
                   "Dexterity:                     " + str(dexterity) + "          Hit Points:                    " + str(thp) + "\n"
                   "Constitution:                  " + str(constitution) + "          To Hit Modifier:               " + str(thit) + "\n"
                   "Armor Class:                   " + str(tac) + "         Damage Modifier:               " + str(tdamage) + "\n"
                   "Reset:                         " + str(reset) + "          Total Feats:                   " + str(tFeats) + "\n"
                   "Wins:                          " + str(wins) + "          Base Damage:                   " + str(baseDamage) + "\n"
                   "Losses:                        " + str(losses) + "          Damage Reduction:              " + str(dr) +
                   "\nTotal Ability Points:          " + str(ap) +
                   "\nCurrent XP:                    " + str(xp) +
                   "\nXP needed to level:            " + str(nextLevel) +
                   "\nAvailable Feats:               " + str(remainingFeats) +
                   "\nFeats Taken:                   " + hasTakenList + "\n```")
        with open(charFolder + player + ".txt", "r+", encoding="utf-8") as file:
            charData = json.load(file)
            charData["thp"] = thp
            charData["tac"] = tac
            charData["thit"] = thit
            charData["tdamage"] = tdamage
            file.seek(0)
            file.write(json.dumps(charData, ensure_ascii=False, indent=2))
            file.truncate()
            file.close()
    return msg

def pri_10_feat_pick(answer, player, featList, featDictionary):
    msg = []
    path = os.getcwd()
    charFolder = os.path.join(path + "/characters/")
    charFile = Path(charFolder + player + ".txt")
    try:
        charSheet = open(charFolder + player + ".txt", "r", encoding="utf-8")
        charData = json.load(charSheet)
        charSheet.close()
        name = charData['name']
        level = charData['level']
        hp = charData['hp']
        tFeats = charData['total feats']
        baseDamage = charData['base damage']
        hit = charData['hit']
        damage = charData['damage']
        ac = charData['ac']
        xp = charData['currentxp']
        nextLevel = charData['nextlevel']
        strength = charData['strength']
        dexterity = charData['dexterity']
        constitution = charData['constitution']
        remainingFeats = charData['remaining feats']
        hasTaken = charData['feats taken']
        hiddenTaken = charData['hfeats taken']
        ap = charData['ap']
        reset = charData['reset']
        wins = charData['wins']
        losses = charData['losses']
        abhp = charData["abhp"]
        abhit = charData["abhit"]
        abdamage = charData["abdamage"]
        abac = charData["abac"]
        feathp = charData["feathp"]
        feathit = charData["feathit"]
        featdamage = charData["featdamage"]
        featac = charData["featac"]
        dexfighter = charData["dexfigher"]
        thp = charData["thp"]
        tac = charData["tac"]
        thit = charData["thit"]
        tdamage = charData["tdamage"]
    except:
        pass

    # Check to see if they even have an open feat slot to fill. If not, they are an idiot.
    if charData["remaining feats"] == 0:
        msg.append("You have no feat slots left to select a new feat")
        # Check to see if they are not taking a feat that is weaker than the one they already have.
        # if it is, they are an idiot.
    elif answer in hiddenTaken:
        msg.append("Why are you trying to take a weaker feat than the one you already have? No.")
    # Check to see if the feat they want is even spelled correctly, or is a feat at all. If not, they are an
    # idiot.
    elif answer not in featList:
        msg.append("Make sure you have spelled the feat correctly")
    # If they do have a slot available, and they spelled it right. Congratulations, not an idiot.
    else:
        reqLevel = featDictionary[0][answer]['requirements'][0]
        reqStr = featDictionary[0][answer]['requirements'][1]
        reqDex = featDictionary[0][answer]['requirements'][2]
        reqCon = featDictionary[0][answer]['requirements'][3]
        reqFeats = featDictionary[0][answer]['requirements'][4]
        # Check to see if they meet the required level for chosen feat. If not, they are an idiot.
        if reqLevel > level:
            msg.append("You are not the required level for this feat.")
        # Check to see if they meet the required strength for chosen feat. If not, they are an idiot.
        elif reqStr > strength:
            msg.append("You do not have the required strength for this feat.")
        # Check to see if they meet the required dexterity for chosen feat. If not, they are an idiot.
        elif reqDex > dexterity:
            msg.append("You do not have the required dexterity for this feat.")
        # Check to see if they meet the required constitution for chosen feat. If not, they are an idiot.
        elif reqCon > constitution:
            msg.append("You do not have the required constitution for this feat.")
        # Check to see if they meet the required prerequisites for chosen feat. If not, they are an idiot.
        elif reqFeats not in hasTaken and reqFeats != "none":
            msg.append("You do hot have the required prerequisites to take this feat.")
        # If they passed all the above checks: Congratulations, not an idiot.
        elif answer not in hasTaken:
            msg.append(answer + " has been added to your character sheet.")
            msg.append("Make sure you use !viewchar to ensure you are "
                       "obtaining proper bonuses during fights.")
            remainingFeats -= 1
            hiddenTaken.append(answer)
            hasTaken.append(answer)

            # Since there are a lot of passive feats. Let's just apply those permanent bonuses here, and be done
            # with it. Feats that are a part of a 'feat tree' (Example: crushing blow, improved crushing blow,
            # and greater crushing blow) do NOT stack. So this ensures previous feat is 'popped out' of list
            # of feats taken, and replaced with upgraded feat.

            with open(charFolder + player + ".txt", "r+", encoding="utf-8") as file:
                charData = json.load(file)
                switchHit = 0
                acMod = 0
                damageMod = 0
                hitMod = 0
                hpMod = 0
                dr = 0

                if answer == "bull strength":
                    charData['strength'] = charData['strength'] + 2
                    charData['abhit'] = int(charData['strength'] / 2)
                    charData['abdamage'] = int(charData['strength'] / 2)
                if answer == "improved bull strength":
                    charData['strength'] = charData['strength'] + 4
                    charData['abhit'] = int(charData['strength'] / 2)
                    charData['abdamage'] = int(charData['strength'] / 2)
                if answer == "greater bull strength":
                    charData['strength'] = charData['strength'] + 6
                    charData['abhit'] = int(charData['strength'] / 2)
                    charData['abdamage'] = int(charData['strength'] / 2)

                if answer == "cat grace":
                    charData['dexterity'] = charData['dexterity'] + 2
                    charData['abac'] = int(charData['dexterity'] / 2)
                if answer == "improved cat grace":
                    charData['dexterity'] = charData['dexterity'] + 4
                    charData['abac'] = int(charData['dexterity'] / 2)
                if answer == "greater cat grace":
                    charData['dexterity'] = charData['dexterity'] + 6
                    charData['abac'] = int(charData['dexterity'] / 2)

                if answer == "bear endurance":
                    charData['constitution'] = charData['constitution'] + 2
                    charData['abhp'] = charData['abhp'] + 5
                if answer == "improved bear endurance":
                    charData['constitution'] = charData['constitution'] + 4
                    charData['abhp'] = charData['abhp'] + 10
                if answer == "greater bear endurance":
                    charData['constitution'] = charData['constitution'] + 6
                    charData['abhp'] = charData['abhp'] + 15

                if answer == "dexterous fighter":
                    dexMod = int(dexterity / 2)
                    strMod = int(strength / 2)
                    switchHit = hit + dexMod - strMod
                    charData["dexfighter"] = switchHit

                if answer == "crushing blow":
                    damageMod = 1
                    charData["featdamage"] = damageMod
                if answer == "improved crushing blow":
                    damageMod = 3
                    charData["featdamage"] = damageMod
                    index = hasTaken.index("crushing blow")
                    hasTaken.pop(index)

                if answer == "greater crushing blow":
                    damageMod = 5
                    charData["featdamage"] = damageMod
                    index = hasTaken.index("improved crushing blow")
                    hasTaken.pop(index)

                if answer == "precision strike":
                    hitMod = 1
                    charData["feathit"] = hitMod
                if answer == "improved precision strike":
                    hitMod = 3
                    charData["feathit"] = hitMod
                    index = hasTaken.index("precision strike")
                    hasTaken.pop(index)
                if answer == "greater precision strike":
                    hitMod = 5
                    charData["feathit"] = hitMod
                    index = hasTaken.index("improved precision strike")
                    hasTaken.pop(index)

                if answer == "lightning reflexes":
                    acMod = 1
                    charData["featac"] = acMod
                if answer == "improved lightning reflexes":
                    acMod = 3
                    charData["featac"] = acMod
                    index = hasTaken.index("lightning reflexes")
                    hasTaken.pop(index)
                if answer == "greater lightning reflexes":
                    acMod = 5
                    charData["featac"] = acMod
                    index = hasTaken.index("improved lightning reflexes")
                    hasTaken.pop(index)

                if answer == "endurance":
                    hpMod = 5
                    charData["feathp"] = hpMod
                if answer == "improved endurance":
                    hpMod = 15
                    charData["feathp"] = hpMod
                    index = hasTaken.index("endurance")
                    hasTaken.pop(index)
                if answer == "greater endurance":
                    hpMod = 30
                    charData["feathp"] = hpMod
                    index = hasTaken.index("improved endurance")
                    hasTaken.pop(index)

                if answer == "thick skin":
                    dr = 1
                    charData["dr"] = dr
                if answer == "improved thick skin":
                    dr = 2
                    charData["dr"] = dr
                    index = hasTaken.index("thick skin")
                    hasTaken.pop(index)
                if answer == "greater thick skin":
                    dr = 3
                    charData["dr"] = dr
                    index = hasTaken.index("thick skin")
                    hasTaken.pop(index)

                if answer == "improved crippling blow":
                    index = hasTaken.index("crippling blow")
                    hasTaken.pop(index)
                if answer == "greater crippling blow":
                    index = hasTaken.index("improved crippling blow")
                    hasTaken.pop(index)
                if answer == "staggering blow":
                    index = hasTaken.index("greater crippling blow")
                    hasTaken.pop(index)

                if answer == "improved evasion":
                    index = hasTaken.index("evasion")
                    hasTaken.pop(index)
                if answer == "greater evasion":
                    index = hasTaken.index("improved evasion")
                    hasTaken.pop(index)

                if answer == "improved quick strike":
                    index = hasTaken.index("quick strike")
                    hasTaken.pop(index)
                if answer == "greater quick strike":
                    index = hasTaken.index("improved quick strike")
                    hasTaken.pop(index)
                if answer == "riposte":
                    index = hasTaken.index("greater quick strike")
                    hasTaken.pop(index)

                if answer == "improved deflect":
                    index = hasTaken.index("deflect")
                    hasTaken.pop(index)
                if answer == "greater deflect":
                    index = hasTaken.index("improved deflect")
                    hasTaken.pop(index)

                if answer == "improved hurt me":
                    index = hasTaken.index("hurt me")
                    hasTaken.pop(index)
                if answer == "greater hurt me":
                    index = hasTaken.index("improved hurt me")
                    hasTaken.pop(index)
                if answer == "hurt me more":
                    index = hasTaken.index("greater hurt me")
                    hasTaken.pop(index)

                if answer == "improved reckless abandon":
                    index = hasTaken.index("reckless abandon")
                    hasTaken.pop(index)
                if answer == "greater reckless abandon":
                    index = hasTaken.index("improved reckless abandon")
                    hasTaken.pop(index)
                charData["feats taken"] = hasTaken
                charData["hfeats taken"] = hiddenTaken
                charData["remaining feats"] = remainingFeats
                file.seek(0)
                file.write(json.dumps(charData, ensure_ascii=False, indent=2))
                file.truncate()
                file.close()

    return msg
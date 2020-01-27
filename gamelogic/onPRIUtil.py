import os
import json
import random
import time
from pathlib import Path
from threading import Timer

# allows a player to reallocate points to their stats, pick a new trait, and select new feats
def pri_7_respec(charFiles, player):
    file = open(charFiles + player.lower() + ".txt", "r", encoding="utf-8")
    charData = json.load(file)
    file.close()
    reset = charData['reset']
    tFeats = charData['total feats']

    if reset != 0:
        reset -= 1
        with open(charFiles + player.lower() + ".txt", "r+", encoding="utf-8") as file:
            charData = json.load(file)
            charData['strength'] = 0
            charData['dexterity'] = 0
            charData['constitution'] = 0
            charData['regeneration'] = 0
            charData['traithit'] = 0
            charData['traitdamage'] = 0
            charData['traitac'] = 0
            charData['traitdr'] = 0
            charData['traithp'] = 0
            charData['initiative'] = 0
            charData['feats taken'] = []
            charData['hfeats taken'] = []
            charData["feathp"] = 0
            charData["feathit"] = 0
            charData["featdamage"] = 0
            charData["featac"] = 0
            charData["dexfighter"] = 0
            charData['remaining feats'] = tFeats
            charData['reset'] = reset
            charData['trait'] = ""
            file.seek(0)
            file.write(json.dumps(charData, ensure_ascii=False, indent=2))
            file.truncate()
            file.close()
        msg = "your characters abilities, trait, and feats have been reset, please use the !stats command to select" \
              " new stats, the !traitpick command to pick a new trait, and the !featpick command to select new feats." \
              " (you have " + str(reset) + " points remaining.)"
    else:
        msg = "You currently have no more reset points to use."
    return msg

# sets up players beginning stats once creating a character
def pri_6_stats(charFiles, gameFiles, player, strength, dexterity, constitution):
    file = open(charFiles + player + ".txt", "r", encoding="utf-8")
    charData = json.load(file)
    file.close()
    charFile = Path(charFiles + player + ".txt")
    strength = int(strength)
    dexterity = int(dexterity)
    constitution = int(constitution)
    msg = []
    ap = charData["ap"]
    total = strength + dexterity + constitution
    # Find out if player even has a character created yet. If not. Tell them they are an idiot.
    if not charFile.is_file():
        msg.append("You don't even have a character created yet. Type !name <name> in the room. "
                   "Where <name> is your character's actual name. (Example: !name Joe")
    # Find out if player has reset points to use. If not. Tell them they are an idiot.
    elif charData['strength'] != 0 and charData['dexterity'] != 0 and charData['constitution'] != 0:
        msg.append("You have already set up your character's stats. If you want to change them, you will "
                   "need to use the !respec command.")

    # If it turns out, they aren't an idiot, and are using the command correctly. Record information and place
    # it in .json.
    else:
        total = strength + dexterity + constitution
        # if total > ap or total < ap:
        #     msg.append("Make sure total points used is no more or less than" +
        #                str(ap) + ".")
        # elif strength > 10 or dexterity > 10 or constitution > 10:
        #     msg.append("No one stat can be above 10 at this point in time. Please try again.")
        if strength < 0 or dexterity < 0 or constitution < 0:
            msg.append("Why would you even try to pick a negative stat? Please try again.")
        else:
            strMod = int(int(strength) / 2)
            dexMod = int(int(dexterity) / 2)
            conMod = int(int(constitution) / 2) * 5
            msg.append("Allocating the following: \n\n"
                       "Strength: " + str(strength) + "   (+" + str(strMod) + " bonus to hit and damage.)\n"
                       "Dexterity: " + str(dexterity) + "   (+" + str(dexMod) + " bonus to armor class.)\n"
                       "Constitution: " + str(constitution) + "   (+" + str(conMod) + " bonus to hit points.)\n")
            msg.append("The above points have been placed on your character sheet. Please "
                       "type !viewchar to see your character sheet. "
                       "You need to chose two feats, and a trait as well. Type !featlist "
                       "to see a list of feats. Type !feathelp <feat name>, "
                       "to get help on a specific feat, or type "
                       "!featpick <feat name> to choose that feat. To see a list of traits, "
                       "use !traitlist, use !traithelp <trait name> for its"
                       "description and use !traitpick <trait name> to select that trait.")

            # load the new data in the character's .json file.
            with open(charFiles + player.lower() + ".txt", "r+", encoding="utf-8") as file:
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

# allows a player to allocate a point to a stat at levels 5, 10, 15 and 20
def pri_4_add(player, ability, charFiles):
    msg = []
    ability.lower()
    answer = ["str", "strength", "dex", "dexterity", "con", "constitution"]
    if ability not in answer:
        msg.append("You need to specify the ability you want to point the point to. "
                   "Type '!add str' or '!add strength' for strength, and so on.")
    else:
        player = player.lower()

        with open(charFiles + player + ".txt", "r+", encoding="utf-8") as file:
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
                    msg.append("You have added an ability point to Strength.")
                if ability == "dexterity" or ability == "dex":
                    charData['dexterity'] += 1
                    charData['abac'] = int(charData['dexterity'])
                    file.seek(0)
                    file.write(json.dumps(charData, ensure_ascii=False, indent=2))
                    file.truncate()
                    msg.append("You have added an ability point to Dexterity.")
                if ability == "constitution" or ability == "con":
                    charData['constitution'] += 1
                    charData['abhp'] = int(charData['constitution'])
                    file.seek(0)
                    file.write(json.dumps(charData, ensure_ascii=False, indent=2))
                    file.truncate()
                    msg.append("You have added an ability point to Constitution")
                file.close()
            else:
                msg.append("You do not have any more ability points to spend.")
    return msg

# allows a player to see their character sheet
def pri_viewchar(player, gameFiles, charFiles):
    msg = []
    charFile = Path(charFiles + player + ".txt")
    if not charFile.is_file():
        msg.append("You don't even have a character created yet. Type !name <name> in the room. "
                   "Where <name> is your character's actual name. (Example: !name Joe)")
    # If it turns out the are not an idiot, and are using the command correctly. Display the character shit
    # as nicely as you can in F-list...which isn't nice at all.
    else:
        # try:
        charSheet = open(charFiles + player.lower() + ".txt", "r+", encoding="utf-8")
        charData = json.load(charSheet)
        charSheet.close()
        keyDict = []
        for key in charData['armor']:
            keyDict.append(key)
        armorOne = keyDict[0]
        armorTwo = keyDict[1]
        armorThree = keyDict[2]
        armorInvOne = "n/a"
        armorInvTwo = "n/a"
        armorInvThree = "n/a"
        if charData['armor'][armorOne] != "n/a":
            del charData['armor'][armorOne][-1]
            armorInvOne = ", ".join(charData['armor'][armorOne])
        if charData['armor'][armorTwo] != "n/a":
            del charData['armor'][armorTwo][-1]
            armorInvTwo = ", ".join(charData['armor'][armorTwo])
        if charData['armor'][armorThree] != "n/a":
            del charData['armor'][armorThree][-1]
            armorInvThree = ", ".join(charData['armor'][armorThree])
        equip = charData['equip']
        name = charData['name']
        trait = charData['trait']
        level = charData['level']
        hp = charData['hp']
        tFeats = charData['total feats']
        baseDamage = charData['base damage']
        hit = charData['hit']
        damage = charData['damage']
        ac = charData['ac']
        gold = charData['gold']
        xp = charData['currentxp']
        nextLevel = charData['nextlevel']
        baseStrength = charData['strength']
        baseDexterity = charData['dexterity']
        baseConstitution = charData['constitution']
        remainingFeats = charData['remaining feats']
        hasTaken = charData['feats taken']
        hiddenTaken = charData['hfeats taken']
        ap = charData['ap']
        reset = charData['reset']
        wins = charData['wins']
        losses = charData['losses']
        # Ability Bonuses
        abhp = charData["abhp"]
        abhit = charData["abhit"]
        abdamage = charData["abdamage"]
        abac = charData["abac"]
        # Feat Bonuses
        feathp = charData["feathp"]
        feathit = charData["feathit"]
        featdamage = charData["featdamage"]
        featac = charData["featac"]
        dexfighter = charData["dexfighter"]
        # Potion Bonuses
        potionEffect = charData["potioneffect"]
        potionInventory = charData["potions"]
        potioninitiative = charData["potioninitiative"]
        pstrength = charData["pstrength"]
        pdexterity = charData["pdexterity"]
        pconstitution = charData["pconstitution"]
        potionblur = charData["potionblur"]
        # Armor Bonuses
        armorhit = charData["armorhit"]
        armordamage = charData["armordamage"]
        armorac = charData["armorac"]
        armorhp = charData["armorhp"]
        armordr = charData["armordr"]
        armorstrength = charData["armorstrength"]
        armordexterity = charData["armordexterity"]
        armorconstitution = charData["armorconstitution"]
        armorblur = charData["armorblur"]
        armorinitiative = charData["armorinitiative"]
        # Trait Bonuses
        nblur = charData['blur']
        traitHit = charData['traithit']
        traitDamage = charData['traitdamage']
        traitAC = charData['traitac']
        traitDR = charData['traitdr']
        traitHP = charData['traithp']
        regeneration = charData['regeneration']
        ninitiative = charData["initiative"]
        # Total bonuses
        thp = charData["thp"] + charData['potionhp']
        tac = charData["tac"]
        tdr = charData["tdr"]
        thit = charData["thit"]
        tdamage = charData["tdamage"]
        centeredfeat = 0
        # except:
        #     print("Something above doesn't exist")

        # Calculate total Strength
        strength = baseStrength + pstrength + armorstrength
        # Calculate total Dexterity
        dexterity = baseDexterity + pdexterity + armordexterity
        # Calculate total Constitution
        constitution = baseConstitution + pconstitution + armorconstitution
        # Calulcate total hit points
        thp = hp + feathp + armorhp + traitHP + int(int(constitution / 2) * 5)
        # Determind if player has feat 'centered self'
        for feat in hasTaken:
            if feat == "centered self":
                centeredfeat = int(constitution / 2 * 0.2)
            elif feat == "improved centered self":
                centeredfeat = int(constitution / 2 * 0.4)
            elif feat == "greater centered self":
                centeredfeat = int(constitution / 2 * 0.6)
        # Calculate total bonus to hit
        thit = hit + feathit + armorhit + traitHit + centeredfeat +  int(strength / 2)
        # Calculate total bonus to damage
        tdamage = damage + featdamage + armordamage + traitDamage + centeredfeat + int(strength / 2)
        # Calulate total bonus to armor class
        tac = ac + featac + armorac + traitAC + int(dexterity / 2)
        # Calculate total Damage Reduction
        tdr = armordr + traitDR
        # List feats taken
        hasTakenList = ", ".join(hasTaken)
        # List potion inventory
        potionInventoryList = ", ".join(potionInventory)
        # Calulate blur percentage
        blur = potionblur + armorblur + nblur
        # Calculate initiative bonus
        initiative = ninitiative + potioninitiative + armorinitiative
        for feat in hasTaken:
            if feat == 'dexterous fighter':
                thit = hit + abac + feathit

        msg.append("```" + name + "'s Character Sheet:\n"
                   "Character Name:          " + name + "\n"
                   "Strength:                " + str(strength) + "          "
                   "Level:                   " + str(level) + "\n"
                   "Dexterity:               " + str(dexterity) + "          "
                   "Armor Class:             " + str(tac) + "\n"
                   "Constitution:            " + str(constitution) + "          "
                   "Hit Points:              " + str(thp) + "\n"
                   "To Hit Modifier:         " + str(thit) + "          "
                   "Ability Points:          " + str(ap) + "\n"
                   "Damage Modifier:         " + str(tdamage) + "          "
                   "Base Damage:             " + str(baseDamage) + "\n"
                   "Regeneration:            " + str(regeneration) + "          "
                   "Damage Reduction:        " + str(tdr) + "\n"
                   "Reset:                   " + str(reset) + "          "
                   "Total Feats:             " + str(tFeats) + "\n"
                   "Wins:                    " + str(wins) + "          "
                   "Gold:                    " + str(gold) + "\n"
                   "Losses:                  " + str(losses) + "          "
                   "Trait:                   " + str(trait) + "\n"
                   "Blur:                    " + str(blur) + "%\n"
                   "Initiative Bonus:        " + str(initiative) + "\n"
                   "Current XP:              " + str(xp) + "\n"
                   "Next Level:              " + str(nextLevel) + "\n"
                   "Potion Inventory:        " + str(potionInventoryList) + "\n"
                   "Potion Effect:           " + str(potionEffect) + "\n"
                   "Permanent Bonuses (Str, Dex, Con):                           " + str(pstrength) + ", " +
                   str(pdexterity) + ", " + str(pconstitution) + "\n"
                   "Total Feats:             " + str(remainingFeats) + "\n"
                   "Feats Taken:             " + hasTakenList + "\n"
                   "Armor Inventory:         " + armorOne + ": (" + armorInvOne + "), " +
                   armorTwo + ": (" + armorInvTwo + "), " + armorThree + ": (" + armorInvThree + ")\n"
                   "Armor Equipped:          " + equip + "```")
        with open(charFiles + player.lower() + ".txt", "r+", encoding="utf-8") as file:
            charData = json.load(file)
            charData["thp"] = thp
            charData["tac"] = tac
            charData["tdr"] = tdr
            charData["thit"] = thit
            charData["tdamage"] = tdamage
            file.seek(0)
            file.write(json.dumps(charData, ensure_ascii=False, indent=2))
            file.truncate()
            file.close()
    return msg

# gives the player a list of people at the level given
def pri_9_wholevel(level, gameFiles, charFiles):
    profile = []
    response = []
    msg = []
    with open(gameFiles + "playerDatabase.txt", 'r', encoding="utf-8") as file2:
        playerDatabase = json.loads(file2.read())
        file2.close()

    for item in playerDatabase.items():
        name = item[1]
        profile.append(name)
    levelList = {}
    for player in profile:
        with open(charFiles + player + ".txt", "r+", encoding="utf-8") as file:
            charData = json.load(file)
            file.close()
        name = charData['name']
        level = charData['level']
        levelList[name] = level
    msg.append("Level " + str(level) + " characters:")
    for key, value in levelList.items():
        if value == int(level):
            response.append(key)
    stringResponse = "\n" + "\n".join(response)
    msg.append(stringResponse)
    return msg

# allows the player to select a trait
def pri_6_trait(gameFiles, charFiles, player, traitList, traitDictionary, trait):
    file = open(charFiles + player + ".txt", 'r', encoding="utf-8")
    charData = json.load(file)
    file.close()
    regeneration = charData['regeneration']
    brawler = charData['traithit']
    thug = charData['traitdamage']
    nimble = charData['traitac']
    thickskinned = charData['traitdr']
    opportunist = charData['initiative']
    nebulous = charData['blur']
    strength = charData['strength']
    dexterity = charData['dexterity']
    constitution = charData['constitution']
    # ap = charData['ap']
    # regeneration = charData['regeneration']
    # print("why?")
    # initiative = charData['initiative']
    # blur = charData['blur']
    # except:
    #     pass
    if charData['trait'] != "":
        msg = "You've already selected a trait. If you wish to change it, you must !respec if you have the points."
    elif strength == 0 and dexterity == 0 and constitution == 0:
        msg = "You need to set up your stats first, before selecting a trait. please use the !stats command."
    else:
        with open(charFiles + player.lower() + ".txt", "r+", encoding="utf-8") as file:
            charData = json.load(file)
            if trait in traitList:
                level = charData['level']
                charData['trait'] = trait
                if trait == 'regeneration' and level == 1:
                    regeneration = 2
                    charData['regeneration'] = regeneration
                    msg = "The trait 'Regeneration' has been added to your character sheet."
                elif trait == 'regeneration' and level < 5:
                    regeneration = 4
                    charData['regeneration'] = regeneration
                    msg = "The trait 'Regeneration' has been added to your character sheet."
                elif trait == 'regeneration' and level < 10:
                    regeneration = 6
                    charData['regeneration'] = regeneration
                    msg = "The trait 'Regeneration' has been added to your character sheet."
                elif trait == 'regeneration' and level < 15:
                    regeneration = 8
                    charData['regeneration'] = regeneration
                    msg = "The trait 'Regeneration' has been added to your character sheet."
                elif trait == 'regeneration' and level >= 20:
                    regeneration = 10
                    charData['regeneration'] = regeneration
                    msg = "The trait 'Regeneration' has been added to your character sheet."
                if trait == 'brawler' and level == 1:
                    brawler = 1
                    charData['traithit'] = brawler
                    msg = "The trait 'Brawler' has been added to your character sheet."
                elif trait == 'brawler' and level < 5:
                    brawler = 2
                    charData['traithit'] = brawler
                    msg = "The trait 'Brawler' has been added to your character sheet."
                elif trait == 'bralwer' and level < 10:
                    brawler = 3
                    charData['traithit'] = brawler
                    msg = "The trait 'Brawler' has been added to your character sheet."
                elif trait == 'brawler' and level < 15:
                    brawler = 4
                    charData['traithit'] = brawler
                    msg = "The trait 'Brawler' has been added to your character sheet."
                elif trait == 'brawler' and level >= 20:
                    brawler = 5
                    charData['traithit'] = brawler
                    msg = "The trait 'Brawler' has been added to your character sheet."
                if trait == 'thug' and level == 1:
                    thug = 1
                    charData['traitdamage'] = thug
                    msg = "The trait 'Thug' has been added to your character sheet."
                elif trait == 'thug' and level < 5:
                    thug = 2
                    charData['traitdamage'] = thug
                    msg = "The trait 'Thug' has been added to your character sheet."
                elif trait == 'thug' and level < 10:
                    thug = 3
                    charData['traitdamage'] = thug
                    msg = "The trait 'Thug' has been added to your character sheet."
                elif trait == 'thug' and level < 15:
                    thug = 4
                    charData['traitdamage'] = thug
                    msg = "The trait 'Thug' has been added to your character sheet."
                elif trait == 'thug' and level >= 20:
                    thug = 5
                    charData['traitdamage'] = thug
                    msg = "The trait 'Thug' has been added to your character sheet."
                if trait == 'hearty' and level == 1:
                    hearty = 5
                    charData['traithp'] = hearty
                    msg = "The trait 'Hearty' has been added to your character sheet."
                elif trait == 'hearty' and level < 5:
                    hearty = 10
                    charData['traithp'] = hearty
                    msg = "The trait 'Hearty' has been added to your character sheet."
                elif trait == 'hearty' and level < 10:
                    hearty = 15
                    charData['traithp'] = hearty
                    msg = "The trait 'Hearty' has been added to your character sheet."
                elif trait == 'hearty' and level < 15:
                    hearty = 20
                    charData['traithp'] = hearty
                    msg = "The trait 'Hearty' has been added to your character sheet."
                elif trait == 'hearty' and level >= 20:
                    hearty = 25
                    charData['traithp'] = hearty
                    msg = "The trait 'Hearty' has been added to your character sheet."
                if trait == 'nimble' and level == 1:
                    nimble = 1
                    charData['traitac'] = nimble
                    msg = "The trait 'Nimble' has been added to your character sheet."
                elif trait == 'nimble' and level < 5:
                    nimble = 2
                    charData['traitac'] = nimble
                    msg = "The trait 'Nimble' has been added to your character sheet."
                elif trait == 'nimble' and level < 10:
                    nimble = 3
                    charData['traitac'] = nimble
                    msg = "The trait 'Nimble' has been added to your character sheet."
                elif trait == 'nimble' and level < 15:
                    nimble = 4
                    charData['traitac'] = nimble
                    msg = "The trait 'Nimble' has been added to your character sheet."
                elif trait == 'nimble' and level >= 20:
                    nimble = 5
                    charData['traitac'] = nimble
                    msg = "The trait 'Nimble' has been added to your character sheet."
                if trait == 'thickskinned' and level == 1:
                    thickskinned = 2
                    charData['traitdr'] = thickskinned
                    msg = "The trait 'Thickskinned' has been added to your character sheet."
                elif trait == 'thickskinned' and level < 5:
                    thickskinned = 3
                    charData['traitdr'] = thickskinned
                    msg = "The trait 'Thickskinned' has been added to your character sheet."
                elif trait == 'thickskinned' and level < 10:
                    thickskinned = 4
                    charData['traitdr'] = thickskinned
                    msg = "The trait 'Thickskinned' has been added to your character sheet."
                elif trait == 'thickskinned' and level < 15:
                    thickskinned = 5
                    charData['traitdr'] = thickskinned
                    msg = "The trait 'Thickskinned' has been added to your character sheet."
                elif trait == 'thickskinned' and level >= 20:
                    thickskinned = 6
                    charData['traitdr'] = thickskinned
                    msg = "The trait 'Thickskinned' has been added to your character sheet."
                if trait == 'opportunist' and level == 1:
                    opportunist = 2
                    charData['initiative'] = opportunist
                    msg = "The trait 'Opportunist' has been added to your character sheet."
                elif trait == 'opportunist' and level < 5:
                    opportunist = 3
                    charData['initiative'] = opportunist
                    msg = "The trait 'Opportunist' has been added to your character sheet."
                elif trait == 'opportunist' and level < 10:
                    opportunist = 4
                    charData['initiative'] = opportunist
                    msg = "The trait 'Opportunist' has been added to your character sheet."
                elif trait == 'opportunist' and level < 15:
                    opportunist = 5
                    charData['initiative'] = opportunist
                    msg = "The trait 'Opportunist' has been added to your character sheet."
                elif trait == 'opportunist' and level >= 20:
                    opportunist = 6
                    charData['initiative'] = opportunist
                    msg = "The trait 'Opportunist' has been added to your character sheet."
                if trait == 'nebulous' and level == 1:
                    nebulous = 1
                    charData['blur'] = nebulous
                    msg = "The trait 'Nebulous' has been added to your character sheet."
                elif trait == 'nebulous' and level < 5:
                    nebulous = 2
                    charData['blur'] = nebulous
                    msg = "The trait 'Nebulous' has been added to your character sheet."
                elif trait == 'nebulous' and level < 10:
                    nebulous = 3
                    charData['blur'] = nebulous
                    msg = "The trait 'Nebulous' has been added to your character sheet."
                elif trait == 'nebulous' and level < 15:
                    nebulous = 4
                    charData['blur'] = nebulous
                    msg = "The trait 'Nebulous' has been added to your character sheet."
                elif trait == 'nebulous' and level >= 20:
                    nebulous = 5
                    charData['blur'] = nebulous
                    msg = "The trait 'Nebulous' has been added to your character sheet."
                file.seek(0)
                file.write(json.dumps(charData, ensure_ascii=False, indent=2))
                file.truncate()
                file.close()


    return msg

# allows the player to select a feat
def pri_10_feat_pick(answer, player, featList, featDictionary, gameFiles, charFiles):
    msg = []
    charSheet = open(charFiles + player.lower() + ".txt", "r", encoding="utf-8")
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
    dexfighter = charData["dexfighter"]
    thp = charData["thp"]
    tac = charData["tac"]
    thit = charData["thit"]
    tdamage = charData["tdamage"]

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
        elif reqStr > strength - charData['armorstrength']:
            msg.append("You do not have the required strength for this feat.")
        # Check to see if they meet the required dexterity for chosen feat. If not, they are an idiot.
        elif reqDex > dexterity - charData['armordexterity']:
            msg.append("You do not have the required dexterity for this feat.")
        # Check to see if they meet the required constitution for chosen feat. If not, they are an idiot.
        elif reqCon > constitution - charData['armorconstitution']:
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

            with open(charFiles + player.lower() + ".txt", "r+", encoding="utf-8") as file:
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
                    charData['strength'] = charData['strength'] + 2
                    charData['abhit'] = int(charData['strength'] / 2)
                    charData['abdamage'] = int(charData['strength'] / 2)
                    index = hasTaken.index("bull strength")
                    hasTaken.pop(index)
                if answer == "greater bull strength":
                    charData['strength'] = charData['strength'] + 2
                    charData['abhit'] = int(charData['strength'] / 2)
                    charData['abdamage'] = int(charData['strength'] / 2)
                    index = hasTaken.index("improved bull strength")
                    hasTaken.pop(index)

                if answer == "cat grace":
                    charData['dexterity'] = charData['dexterity'] + 2
                    charData['abac'] = int(charData['dexterity'] / 2)
                if answer == "improved cat grace":
                    charData['dexterity'] = charData['dexterity'] + 2
                    charData['abac'] = int(charData['dexterity'] / 2)
                    index = hasTaken.index("cat grace")
                    hasTaken.pop(index)
                if answer == "greater cat grace":
                    charData['dexterity'] = charData['dexterity'] + 2
                    charData['abac'] = int(charData['dexterity'] / 2)
                    index = hasTaken.index("improved cat grace")
                    hasTaken.pop(index)

                if answer == "bear endurance":
                    charData['constitution'] = charData['constitution'] + 2
                    charData['abhp'] = charData['abhp'] + 5
                if answer == "improved bear endurance":
                    charData['constitution'] = charData['constitution'] + 2
                    charData['abhp'] = charData['abhp'] + 5
                    index = hasTaken.index("bear endurance")
                    hasTaken.pop(index)
                if answer == "greater bear endurance":
                    charData['constitution'] = charData['constitution'] + 2
                    charData['abhp'] = charData['abhp'] + 5
                    index = hasTaken.index("improved bear endurance")
                    hasTaken.pop(index)

                if answer == "dexterous fighter":
                    dexMod = int(dexterity / 2)
                    strMod = int(strength / 2)
                    switchHit = hit + dexMod - strMod
                    charData["dexfighter"] = switchHit

                if answer == "crushing blow":
                    damageMod = 1
                    charData["featdamage"] += damageMod
                if answer == "improved crushing blow":
                    damageMod = 2
                    charData["featdamage"] += damageMod
                    index = hasTaken.index("crushing blow")
                    hasTaken.pop(index)
                if answer == "greater crushing blow":
                    damageMod = 3
                    charData["featdamage"] += damageMod
                    index = hasTaken.index("improved crushing blow")
                    hasTaken.pop(index)

                if answer == "precision strike":
                    hitMod = 1
                    charData["feathit"] += hitMod
                if answer == "improved precision strike":
                    hitMod = 2
                    charData["feathit"] += hitMod
                    index = hasTaken.index("precision strike")
                    hasTaken.pop(index)
                if answer == "greater precision strike":
                    hitMod = 3
                    charData["feathit"] += hitMod
                    index = hasTaken.index("improved precision strike")
                    hasTaken.pop(index)

                if answer == "lightning reflexes":
                    acMod = 1
                    charData["featac"] += acMod
                if answer == "improved lightning reflexes":
                    acMod = 2
                    charData["featac"] += acMod
                    index = hasTaken.index("lightning reflexes")
                    hasTaken.pop(index)
                if answer == "greater lightning reflexes":
                    acMod = 3
                    charData["featac"] += acMod
                    index = hasTaken.index("improved lightning reflexes")
                    hasTaken.pop(index)

                if answer == "endurance":
                    hpMod = 5
                    charData["feathp"] += hpMod
                if answer == "improved endurance":
                    hpMod = 10
                    charData["feathp"] += hpMod
                    index = hasTaken.index("endurance")
                    hasTaken.pop(index)
                if answer == "greater endurance":
                    hpMod = 15
                    charData["feathp"] += hpMod
                    index = hasTaken.index("improved endurance")
                    hasTaken.pop(index)

                if answer == "improved centered self":
                    index = hasTaken.index("centered self")
                    hasTaken.pop(index)
                if answer == "greater centered self":
                    index = hasTaken.index("improved centered self")
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

                if answer == "improved deaths door":
                    index = hasTaken.index("deaths door")
                    hasTaken.pop(index)
                if answer == "greater deaths door":
                    index = hasTaken.index("improved deaths door")
                    hasTaken.pop(index)

                if answer == "improved lifeleech":
                    index = hasTaken.index("lifeleech")
                    hasTaken.pop(index)
                if answer == "greater lifeleech":
                    index = hasTaken.index("improved lifeleech")
                    hasTaken.pop(index)
                if answer == "lifedrain":
                    index = hasTaken.index("greater lifeleech")
                    hasTaken.pop(index)

                charData["feats taken"] = hasTaken
                charData["hfeats taken"] = hiddenTaken
                charData["remaining feats"] = remainingFeats
                file.seek(0)
                file.write(json.dumps(charData, ensure_ascii=False, indent=2))
                file.truncate()
                file.close()

    return msg

# allows a moderator to stock a new set of 20 potions in the market
def pri_10_stockpotion(commonList, uncommonList, rareList, vrareList, relicList, gameFiles):
    potionFile = open(gameFiles + "potions.txt", "r+", encoding="utf-8")
    potionDictionary = json.load(potionFile)
    potionDictionary[0]['shoplist'] = []
    for num in range(1, 21):
        number = random.randint(1, 100)
        if number in range(97, 101):
            relicPotion = len(relicList)
            index = random.randint(1, (relicPotion - 1))
            chosenPotion = relicList[index]
            potionDictionary[0]['shoplist'].append(chosenPotion)
        elif number in range(91, 97):
            vrarePotion = len(vrareList)
            index = random.randint(1, (vrarePotion - 1))
            chosenPotion = vrareList[index]
            potionDictionary[0]['shoplist'].append(chosenPotion)
        elif number in range(76, 91):
            rarePotion = len(rareList)
            index = random.randint(1, (rarePotion - 1))
            chosenPotion = rareList[index]
            potionDictionary[0]['shoplist'].append(chosenPotion)
        elif number in range(41, 76):
            uncommonPotion = len(uncommonList)
            index = random.randint(1, (uncommonPotion - 1))
            chosenPotion = uncommonList[index]
            potionDictionary[0]['shoplist'].append(chosenPotion)
        elif number in range(1, 41):
            commonPotion = len(commonList)
            index = random.randint(1, (commonPotion - 1))
            chosenPotion = commonList[index]
            potionDictionary[0]['shoplist'].append(chosenPotion)
    shopString = ", ".join(potionDictionary[0]['shoplist'])
    potionFile.seek(0)
    potionFile.write(json.dumps(potionDictionary, ensure_ascii=False, indent=2))
    potionFile.truncate()
    potionFile.close()

    msg = "Shop stocked for the week as follows: \n" + shopString
    return msg

# allows a moderator to stock a 20 new sets of armor in the market
def pri_11_stockarmor(catOneCommonList, catOneUncommonList, catOneRareList, catTwoCommonList, catTwoUncommonList,
                      catTwoRareList, catThreeCommonList, catThreeUncommonList, catThreeRareList, gameFiles):
    armorFile = open(gameFiles + "armor.txt", "r", encoding="utf-8")
    armorDictionary = json.load(armorFile)
    armorFile.close()
    num = 1
    msg = []
    for num in range(1, 21):
        rand = random.randint(1, 100)
        if rand in range(1, 101):
            category = random.randint(1, 100)
            if category in range(96, 101):
                item = []
                randomAttribute = random.choice(catOneRareList)
                item.append(randomAttribute)
            if category in range(76, 96):
                item = []
                randomAttribute = random.choice(catOneUncommonList)
                item.append(randomAttribute)
            if category in range(1, 76):
                item = []
                randomAttribute = random.choice(catOneCommonList)
                item.append(randomAttribute)
        if rand in range(1, 41):
            category = random.randint(1, 100)
            if category in range(96, 101):
                randomAttribute = random.choice(catTwoRareList)
                item.append(randomAttribute)
            if category in range(76, 96):
                randomAttribute = random.choice(catTwoUncommonList)
                item.append(randomAttribute)
            if category in range(1, 76):
                randomAttribute = random.choice(catTwoCommonList)
                item.append(randomAttribute)
        if rand in range(1, 10):
            if category in range(1, 76):
                randomAttribute = random.choice(catThreeCommonList)
                item.append(randomAttribute)
            elif category in range(75, 96):
                randomAttribute = random.choice(catThreeUncommonList)
                item.append(randomAttribute)
            elif category in range(95, 101):
                randomAttribute = random.choice(catThreeRareList)
                item.append(randomAttribute)
        armorDictionary[0]["armorlist"]["armor" + str(num)] = item
    armorFile = open(gameFiles + "armor.txt", "r+", encoding="utf-8")
    armorFile.seek(0)
    armorFile.write(json.dumps(armorDictionary, ensure_ascii=False, indent=2))
    armorFile.truncate()
    armorFile.close()
    num = 1
    # for num in range(1, 21):
    #     msg.append("Armor" + str(num) + " (" + ", ".join(armorDictionary[0]["armorlist"]["armor" + str(num)]) + ")")

    msg = "Armor Shop has been stocked for the week."
    return msg

# allows the player to view pieces of armor for sale
def pri_10_armorshop(gameFiles):
    armorFile = open(gameFiles + "armor.txt", "r", encoding="utf-8")
    armorDictionary = json.load(armorFile)
    armorFile.close()
    armorPrice = []
    myList = []
    for key in armorDictionary[0]["armorlist"]:
        myList.append(armorDictionary[0]["armorlist"][key])
    num = 0
    for item in myList:
        if item == "sold":
            price = 0
            armorPrice.append(price)
        if len(item) == 1:
            stat = " ".join(item)
            if stat in armorDictionary[0]["cat1"]["common"]:
                price = armorDictionary[0]["cat1"]["common"][stat][0]
            elif stat in armorDictionary[0]["cat1"]["uncommon"]:
                price = armorDictionary[0]["cat1"]["uncommon"][stat][0]
            elif stat in armorDictionary[0]["cat1"]["rare"]:
                price = armorDictionary[0]["cat1"]["rare"][stat][0]
            armorPrice.append(price)
        if len(item) == 2:
            wordOne = item[0]
            wordTwo = item[1]
            if wordOne in armorDictionary[0]["cat1"]["common"]:
                priceOne = armorDictionary[0]["cat1"]["common"][wordOne][0]
            elif wordOne in armorDictionary[0]["cat1"]["uncommon"]:
                priceOne = armorDictionary[0]["cat1"]["uncommon"][wordOne][0]
            elif wordOne in armorDictionary[0]["cat1"]["rare"]:
                priceOne = armorDictionary[0]["cat1"]["rare"][wordOne][0]
            if wordTwo in armorDictionary[0]["cat2"]["common"]:
                priceTwo = armorDictionary[0]["cat2"]["common"][wordTwo][0]
            elif wordTwo in armorDictionary[0]["cat2"]["uncommon"]:
                priceTwo = armorDictionary[0]["cat2"]["uncommon"][wordTwo][0]
            elif wordTwo in armorDictionary[0]["cat2"]["rare"]:
                priceTwo = armorDictionary[0]["cat2"]["rare"][wordTwo][0]
            price = priceOne + priceTwo
            armorPrice.append(price)
        if len(item) == 3:
            wordOne = item[0]
            wordTwo = item[1]
            wordThree = item[2]
            if wordOne in armorDictionary[0]["cat1"]["common"]:
                priceOne = armorDictionary[0]["cat1"]["common"][wordOne][0]
            elif wordOne in armorDictionary[0]["cat1"]["uncommon"]:
                priceOne = armorDictionary[0]["cat1"]["uncommon"][wordOne][0]
            elif wordOne in armorDictionary[0]["cat1"]["rare"]:
                priceOne = armorDictionary[0]["cat1"]["rare"][wordOne][0]
            if wordTwo in armorDictionary[0]["cat2"]["common"]:
                priceTwo = armorDictionary[0]["cat2"]["common"][wordTwo][0]
            elif wordTwo in armorDictionary[0]["cat2"]["uncommon"]:
                priceTwo = armorDictionary[0]["cat2"]["uncommon"][wordTwo][0]
            elif wordTwo in armorDictionary[0]["cat2"]["rare"]:
                priceTwo = armorDictionary[0]["cat2"]["rare"][wordTwo][0]
            if wordThree in armorDictionary[0]["cat3"]["common"]:
                priceThree = armorDictionary[0]["cat3"]["common"][wordThree][0]
            elif wordThree in armorDictionary[0]["cat3"]["uncommon"]:
                priceThree = armorDictionary[0]["cat3"]["uncommon"][wordThree][0]
            elif wordThree in armorDictionary[0]["cat3"]["rare"]:
                priceThree = armorDictionary[0]["cat3"]["rare"][wordThree][0]
            price = priceOne + priceTwo + priceThree
            armorPrice.append(price)
        num += 1
    shopList = {}
    num = 1
    for item in myList:
        shopList["Armor" + str(num)] = item
        num += 1
    item = []
    for key in shopList:
        item.append(key)
        item.append(shopList[key])
    msg = "\n".join("{} {}: ({} gold)".format(*i)
                          for i in zip(item[0::2], item[1::2], armorPrice[0:]))
    return msg
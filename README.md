6,162 lines of code. (Including Comments)

v 1.0 (7/20/19)
- Went live

v 1.0.1 (7/28/19)
- added !who command
- added !player command to show win/loss ratio
- moved !score command into !player command. !score no longer exists

v 1.0.2 (8/2/19)
- combat now displays the base roll for attack and damage, so player can see their roll before modifiers are added in
- fixed Auto-Reset timer to actually reset when a fight finishes properly
- Changed deflect to avoid a flat amount of hp, instead of a percentage.
- Added text to deflect feat to show in combat damage received before and after the effect takes place (Reduced x damage to y)
- Fixed a bug that allowed active feats to persist for two rounds, instead of one.
- Decreased Armor Class to +1 every other level, rather than +1 for every level.
- Fixed a bug that would crash bot if stats were attempted to be allocated before character sheet was made.
- XP gain was using an erroneous formula, corrected it to display proper xp gain.
- Loser of a battle now gains half xp of what the winner obtained.
- Fixed a bug that prevented proper level ups from being announced and recorded on to character sheet correctly.
- Added a !leaderboard function.
- Improved !leaderboard command to sort by wins, losses, or percentage using appropriate commands
- buffed AC to start at 10 at level one.
- Fixed a bug that crashed bot if the !roll command was used in PMs

v1.1 (8/12/19)
- Removed the feat combat expertise
- Added in the feat tree 'Nerve Strike'
- Added in the feat tree 'bull strength'
- Added in the feat tree 'cat grace'
- Added in the feat tree 'bear's endurance
- Changed various requirements and availability of numerous feats
- Added in numerous moderator only features

v1.1.1 (8/18/19)
- Fixed a bug that zeroed out current xp on character sheet, rather than add to it, thus preventing level ups
- Fixed a bug that would allow someone to roll a really high result when attempting to hit someone, after a game had just finished previously
- Fixed a bug that allowed people to use power attack, defensive fighting, and masochist without having taken the feat

v1.1.2 (8/27/19)
- Increased damage the deflect tree absorbs from 3/5/7/10 to 1.5x/2x/2.5x/2.5x Dexterity Modifier

v1.1.3 (8/30/19)
- **Added feature that deletes profiles that have been idle for 28 days. Using the !viewchar refreshes this decay.**
- Spent time wondering the point of it all.

v1.1.4 (9/5/19)
- Implemented a choice to use Evasion after seeing the potential damage being dealt. Not using Evasion will allow it to be saved for later use
- Implemented a choice to use Deflect after seeing the potential damage being dealt. Not using Evasion will allow it to be saved for later use
- Removed the feat 'Absorption'
- Decreased Deflection Multiplies from 1.5x/2x/2.5x to 1x/1.5x/2x
- Fixed a bug that interfered with the ability to have both the Evasion Tree, and Deflect Tree as feats.
- Fixed a bug that allowed Player One (the person that used !challenge) to use deflect an unlimited amount of times.
- **finally added in a feature that asks if you are sure you want to delete your character, instead of just...doing it. I know, right? This is the seventh version update! And this just now was added in? WTF man...**
- Adjusted hp scaling per level
- Adjusted xp formula

v 1.1.5 (9/13/19)
- Added !wholevel command. PM it to the bot with desired level (Example: !wholevel 3) to display a list of all characters at that level
- wondered again what the point of this all is

v 1.1.6 (10/25/19)
- Recovered from hopelessness
- Added Traits
- Added 'renown' a currency with intentions to allow for purchase of potions and the like in the future.
- Adjusted HP and attack dice to allow for a bigger range of opponents to challenge, regardless of level
- Adjusted experience point scale

v 1.2 (11/2/19)
- Added a potion shop with following commands: !potionshop (shows potions in shop, and price), !potionbuy (buys potion requested, if enough renown is available.) (See shop dropdown for more information on potions)
- Added in function that rotates potion stock on a weekly bases
- Added in !givepotion, allowing a player to trade a potion to another player
- Added in a inventory strictly to hold potions. Players can hold up to three potions at one time.
- Adjusted the 'Hurt Me' feat scale off of +20%/+40% of strength
- Adjusted the 'Improved Hurt Me' feat to scale off of +40%/+60% of strength
- Adjusted the 'Greater Hurt Me' feat to scale off of +60%/+80% of strength
- Adjusted the 'Hurt Me More' feat to scale off of +60%/+80%/+100% of strength

v 1.2.1 (11/25/19)
- Added Added an armor shop with following commands: !armorshop (shows armor in shop, and price), !armorbuy (buys armor requested, if enough renown is available.) (See shop dropdown for more information on armor)
- Added in function that rotates armor stock on a weekly bases
- Added in a inventory strictly to hold three pieces of armor. Players can only wear one piece at a time.
- Added in command that allows you to rename armor
- Added in a command that allows you to sell a piece of armor
- **Extended feature that deletes profiles that have been idle for 28 days to 112 days. PMing !viewchar to the bot refreshes this decay.**
- Added in 'Nebulous' as a trait 

v 1.2.2 (12/2/19)
- removed Iron Skin feat
- Improved thick skin bonuses to 2/4/6
- reduced damage from the Nerve Strike tree to 1d4/2d4/3d4/3d6
- changed experience formula for combat
- improved number of feats per level to increase every odd level. Max of 11 feats at 20.

v 1.2.3 (12/4/19)
- Fixed a bug that allowed you to have more than one trait when using !respec
- Fixed a bug that gave trait bonuses as if your character was level 1, even if character was level 5+
- Fixed a bug that didn't line up armor properly in the shop list, crashing the bot when attempting to buy armor
- Fixed a bug that crashed the bot when attempting to buy another set of armor after renaming the first one

v 1.2.4 (12/6/19)
- Removed the Thick Skin feat tree
- Reduced Thickskinned trait bonuses to 2/3/4/5/6
- Added feat tree 'Centered Self'
- Added feat tree 'Deaths Door'
- Added feat tree 'lifeleech'
- Adjusted requirements for all feats 
- Added Potions of Respec and Stimulant 

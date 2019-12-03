#! python3

"""
Based on Text Adventure Demo by Al Sweigart from http://inventwithpython.com/blog

"""
import cmd, textwrap, random, time, arcade, os
from worldRooms import *
from worldItems import *
from worldCreatures import *
from variables import *
from random import randint
from colorama import init, Fore, Back, Style

init(convert=True)

def titleScreen():
    global firstName
    global lastName
    print(Fore.MAGENTA + '*=========================================*')
    print('The Mystery of The Great Magical MacGuffin.')
    print('*=========================================*')
    print(Fore.GREEN + '                                                           |>>>\n                   _                      _                |\n    ____________ .\' \'.    _____/----/-\\ .\' \'./========\\   / \\\n   //// ////// /V_.-._\\  |.-.-.|===| _ |-----| u    u |  /___\\\n  // /// // ///==\\ u |.  || | ||===||||| |T| |   ||   | .| u |_ _ _ _ _ _\n ///////-\\////====\\==|:::::::::::::::::::::::::::::::::::|u u| U U U U U\n |----/\\u |--|++++|..|\'\'\'\'\'\'\'\'\'\'\'::::::::::::::\'\'\'\'\'\'\'\'\'\'|+++|+-+-+-+-+-+\n |u u|u | |u ||||||..|              \'::::::::\'           |===|>=== _ _ ==\n |===|  |u|==|++++|==|              .::::::::.           | T |....| V |..\n |u u|u | |u ||HH||         \\|/    .::::::::::.\n |===|_.|u|_.|+HH+|_              .::::::::::::.              _\n                __(_)___         .::::::::::::::.         ___(_)__\n---------------/  / \\  /|       .:::::;;;:::;;:::.       |\\  / \\  \\-------\n______________/_______/ |      .::::::;;:::::;;:::.      | \\_______\\________\n|       |     [===  =] /|     .:::::;;;::::::;;;:::.     |\\ [==  = ]   |\n|_______|_____[ = == ]/ |    .:::::;;;:::::::;;;::::.    | \\[ ===  ]___|____\n     |       |[  === ] /|   .:::::;;;::::::::;;;:::::.   |\\ [=  ===] |\n_____|_______|[== = =]/ |  .:::::;;;::::::::::;;;:::::.  | \\[ ==  =]_|______\n |       |    [ == = ] /| .::::::;;:::::::::::;;;::::::. |\\ [== == ]      |\n_|_______|____[=  == ]/ |.::::::;;:::::::::::::;;;::::::.| \\[  === ]______|_\n   |       |  [ === =] /.::::::;;::::::::::::::;;;:::::::.\\ [===  =]   |\n___|_______|__[ == ==]/.::::::;;;:::::::::::::::;;;:::::::.\\[=  == ]___|_____' + Style.RESET_ALL)
    start = 'test'
    while start != 'start' or 'quit':
        start = input('Type "start" to start and "quit" to quit: ')
        if start == 'start':
            time.sleep(1)
            firstName = input('What is your given name? ')
            time.sleep(0.5)
            lastName = input('What is your family name? ')
            displayIntro()
            while start != 'on' or 'off':
                start = input('Do you want to play with the visuals "on" or "off"? ')
                if start == 'on':
                    print('\n'.join(textwrap.wrap('Due to the inherent limitations of Python Arcade some inputs still require you to type in the text window or some sections aren\'t playable at all', SCREEN_WIDTH)))
                    time.sleep(2)
                    levelUp()
                    equippedCheck()
                    displayLocation(location)
                    bork()    
                    TextAdventureCmd().cmdloop()    
                elif start !=  'on' or 'off':
                    print('Not a valid command.')
                    time.sleep(0.5)
                else:
                    continue
            time.sleep(1)
            levelUp()
            equippedCheck()
            displayLocation(location)
            TextAdventureCmd().cmdloop()
            titleScreen()
        elif start == 'quit':
            print('Goodbye adventurer!')
            time.sleep(1)
            exit()
        else:
            print('Not a valid command.')
            time.sleep(0.5)

def displayIntro():
    global firstName
    global lastName
    print('============================================')
    time.sleep(0.5)
    print('The city of Otolo was a quiet and peaceful place with not much going on.')
    time.sleep(2)
    print('This all changed when a wizard named "The Great Magical MacGuffin" entered the city gates.')
    time.sleep(2)
    print('The Great Magical MacGuffin used his magical powers to create a giant spire.')
    time.sleep(2)
    print('He then challenged every adventurer in the city to come and claim the price at the top of the tower.')
    time.sleep(2)
    print('As one of those brave, or stupid, enough to try this nigh impossible feat.')
    print('You, ' + firstName + ' ' + lastName + ', set out to climb the structure and claim the price at the top!')
    print('============================================')
    time.sleep(1)
    print('(Type "help" for commands.)')
    print()

def displayLocation(loc):
    global roomText
    """A helper function for displaying an area's description and exits."""
    # Print the room name.
    print()
    
    roomText = loc

    if worldRooms[loc].get(COLOR, False) != False:
        if worldRooms[loc][COLOR] == 'RED':
            print(Fore.RED + loc)
        elif worldRooms[loc][COLOR] == 'GREEN':
            print(Fore.GREEN + loc)
        elif worldRooms[loc][COLOR] == 'YELLOW':
            print(Fore.YELLOW + Style.BRIGHT + loc)
        elif worldRooms[loc][COLOR] == 'BLUE':
            print(Fore.BLUE + Style.BRIGHT + loc)
        elif worldRooms[loc][COLOR] == 'MAGENTA':
            print(Fore.MAGENTA + loc)
        elif worldRooms[loc][COLOR] == 'CYAN':
            print(Fore.CYAN + loc)
        elif worldRooms[loc][COLOR] == 'GRAY':
            print(Fore.BLACK + Style.BRIGHT + loc)
    else:
        print(Fore.WHITE + loc)
    print('=' * len(loc))

    # Print the room's description (using textwrap.wrap())
    print('\n'.join(textwrap.wrap(worldRooms[loc][DESC], SCREEN_WIDTH)))

    #Print all creatures in the room.
    if len(worldRooms[loc][CREATURES]) > 0:
        print()
        for item in worldRooms[loc][CREATURES]:
            print('\n'.join(textwrap.wrap(worldCreatures[item][GROUNDDESC], SCREEN_WIDTH)))

    # Print all the items on the ground.
    if len(worldRooms[loc][GROUND]) > 0:
        print()
        for item in worldRooms[loc][GROUND]:
            print(worldItems[item][GROUNDDESC])

    # Print all the exits.
    exits = []
    for direction in (UP, NORTH, EAST, SOUTH, WEST, DOWN):
        if direction in worldRooms[loc].keys():
            exits.append(direction.title())
    print()
    if showFullExits:
        for direction in (UP, NORTH, EAST, SOUTH, WEST, DOWN):
            if direction in worldRooms[location]:
                print('%s: %s' % (direction.title(), worldRooms[location][direction]))
    else:
        print('Exits: %s' % ' '.join(exits))
    
    print('=' * len(loc) + Fore.WHITE)

def moveDirection(direction):
    """A helper function that changes the location of the player."""
    global location
    global old_location
    global inventory
    global expeditionTimer
    
    if direction in worldRooms[location]:
        for item in worldRooms[location][CREATURES]:
            if worldCreatures[item].get(BOSS, False) == True:
                print('You can\'t run from this fight!')
                return
        old_location = location
        location = worldRooms[location][direction]
        if worldRooms[location].get(CUTSCENE, False) == True:
            print('You move %s.' % direction)
            worldRooms[location][CUTSCENE] = False
            cutscene()
            if worldRooms[location].get(CUTSCENE, False) == True:
                location = old_location
                time.sleep(1)
                displayLocation(location)    
                return
            if worldRooms[location].get(WILD, False) == True:
                wild()
            time.sleep(1)
            displayLocation(location)
            return
        if worldRooms[location].get(WILD, False) == True:
            expeditionTimer -= 1
            print('You move %s.' % direction)
            wild()
            time.sleep(1)
            displayLocation(location)
            return
        if worldRooms[location].get(LOCKED, False) == True:
            if inventory.count('Key') > 0:
                print('You used a key to unlock the door.')
                time.sleep(1)
                inventory.remove('Key')
                print('You move %s.' % direction)
                worldRooms[location][LOCKED] = False
                time.sleep(1)
                displayLocation(location)
            else:
                print('You don\'t have a key')
                location = old_location
        else:
            print('You move %s.' % direction)
            #time.sleep(1)
            displayLocation(location)
    else:
        print('You cannot move in that direction')

def getAllDescWords(itemList):
    """Returns a list of "description words" for each item named in itemList."""
    itemList = list(set(itemList)) # make itemList unique
    descWords = []
    for item in itemList:
        descWords.extend(worldItems[item][DESCWORDS])
    return list(set(descWords))

def getAllFirstDescWords(itemList):
    """Returns a list of the first "description word" in the list of
    description words for each item named in itemList."""
    itemList = list(set(itemList)) # make itemList unique
    descWords = []
    for item in itemList:
        descWords.append(worldItems[item][DESCWORDS][0])
    return list(set(descWords))

def getFirstItemMatchingDesc(desc, itemList):
    itemList = list(set(itemList)) # make itemList unique
    for item in itemList:
        if desc in worldItems[item][DESCWORDS]:
            return item
    return None

def getFirstCreatureMatchingDesc(desc, itemList):
    itemList = list(set(itemList)) # make itemList unique
    for item in itemList:
        if desc in worldCreatures[item][DESCWORDS]:
            return item
    return None

def getAllItemsMatchingDesc(desc, itemList):
    itemList = list(set(itemList)) # make itemList unique
    matchingItems = []
    for item in itemList:
        if desc in worldItems[item][DESCWORDS]:
            matchingItems.append(item)
    return matchingItems

def getAllCreaturesMatchingDesc(desc, itemList):
    itemList = list(set(itemList)) # make itemList unique
    matchingItems = []
    for item in itemList:
        if desc in worldCreatures[item][DESCWORDS]:
            matchingItems.append(item)
    return matchingItems

def equippedCheck():
    global head
    global chest
    global hands
    global legs
    global feet

    for item in equipped:
        if worldItems[item][EQUIPTYPE] == 'HEAD':
                head = item
        elif worldItems[item][EQUIPTYPE] == 'CHEST':
                chest = item
        elif worldItems[item][EQUIPTYPE] == 'HANDS':
                hands = item
        elif worldItems[item][EQUIPTYPE] == 'LEGS':
                legs = item
        else:
                feet = item
        
        stats[1] += worldItems[item][STRENGTH]
        stats[2] += worldItems[item][DEFENCE]
        stats[3] += worldItems[item][PERCEPTION]
        stats[4] += worldItems[item][SPEED]

def levelUp():
    global level
    global exp
    global maxHealth
    global maxHealthbar

    while exp >= 450 + level*50:
        exp -= 450 + level*50
        level += 1
        maxHealth += 3
        stats[0] = maxHealth
        maxHealthbar += 10
        stats[1] += 3
        stats[2] += 3
        stats[3] += 0.5
        stats[4] += 2

        time.sleep(0.5)
        print('You are now level ' + str(level))

def enemyKilled():
    global exp
    global gold
    global location
    global enemy

    print(worldCreatures[enemy][SHORTDESC] + ' got killed.')
    time.sleep(0.5)
    exp += int(worldCreatures[enemy][EXP])
    print('You got ' + str(worldCreatures[enemy][EXP]) + ' exp!')
    gold += int(worldCreatures[enemy][GOLD])
    time.sleep(0.5)
    print(worldCreatures[enemy][SHORTDESC] + ' dropped ' + str(worldCreatures[enemy][GOLD]) + ' gold coins.')
    worldCreatures[enemy][HEALTH] = worldCreatures[enemy][MAXHEALTH]
    if worldCreatures[enemy].get(DROPITEM, False) != 0:
        time.sleep(0.5)
        print('You picked up:')
        for item in worldCreatures[enemy][DROPITEM]:
            print('  ' + item)
            inventory.append(item)
    if worldCreatures[enemy].get(DRAGON, False) == True:
        worldItems['Dragonslayer Sword'][STRENGTH] += 3
        worldItems['Dragonslayer Sword'][DEFENCE] += 1
        worldItems['Dragonslayer Sword'][SPEED] += 1
        cutscene()
    worldRooms[location][CREATURES].remove(enemy)
    levelUp()

def knockedOut():
    global gold
    global maxHealth
    global saveloc
    global location
    global enemy
    global expeditionTimer
    global expeditionLength

    print()
    time.sleep(0.5)
    print(worldCreatures[enemy][SHORTDESC] + ' knocked you out.')
    worldCreatures[enemy][HEALTH] = worldCreatures[enemy][MAXHEALTH]
    gold -= int(worldCreatures[enemy][GOLD])
    if gold <= 0:
        time.sleep(0.5)
        print('You dropped all your gold.')
        gold = 0
    else:    
        time.sleep(0.5)
        print('You dropped ' + str(worldCreatures[enemy][GOLD]) + ' gold.')
    expeditionLength = 0
    expeditionTimer = -1
    stats[0] = maxHealth
    location = saveloc
    time.sleep(2)
    displayLocation(location)

def cutscene():
    global firstName
    global lastName
    global location

    if location == 'Black Alley':
        print('\nAs you step outside you feel the wind hit your face. You\'re ready for this adventure.')
    elif location == 'Midori Forest':
        print()
        print('\n'.join(textwrap.wrap('You walk to the edge of the forest, but before you can enter you hear a voice: "STOP!" ', SCREEN_WIDTH)))
        time.sleep(1)
        print('\n'.join(textwrap.wrap('As you look into the direction the voice came from you see a female gnome standing next to a carriage.', SCREEN_WIDTH)))
        time.sleep(1)
        print('\n'.join(textwrap.wrap('\"You weren\'t planning on just wandering into the forrest, were you?\", the gnome continued. \"Urila\'s the name and aiding adventures is my game.\"', SCREEN_WIDTH)))
        time.sleep(1)
        print('\n'.join(textwrap.wrap('\"With the increase in monsters around Otolo, the Council has decided that unplanned expeditions are no longer allowed.\", Urila smiles. \"And that\'s why I\'m here.\"', SCREEN_WIDTH)))
        time.sleep(1)
        print('\n'.join(textwrap.wrap('\"I can take you on guided expeditions, for a small fee of course, and if you survive I will have some great loot for you.\"', SCREEN_WIDTH)))
        time.sleep(1)
        print('\n'.join(textwrap.wrap('\"For beginners I recommend the small 15 minute expedition, but you can of course take on larger expeditions if you like. The longer you\'re out there, the bigger the reward you get from me at the end.\"', SCREEN_WIDTH)))
        time.sleep(1)
    elif location == 'Nate\'s Room':
        yn = input('Nate: \"Do you want to here a joke?\" (y/n) ')
        if yn == 'y':
            print('\n\"So, there\'s a man crawling through the desert.\"')
            time.sleep(1)
            print('\n'.join(textwrap.wrap('\"He\'d decided to try his SUV in a little bit of cross-country travel, had great fun zooming over the badlands and through the sand, got lost, hit a big rock, and then he couldn\'t get it started again. There were no cell phone towers anywhere near, so his cell phone was useless. He had no family, his parents had died a few years before in an auto accident, and his few friends had no idea he was out here.\"', SCREEN_WIDTH)))
            time.sleep(10)
            print('\n'.join(textwrap.wrap('\"He stayed with the car for a day or so, but his one bottle of water ran out and he was getting thirsty. He thought maybe he knew the direction back, now that he\'d paid attention to the sun and thought he\'d figured out which way was north, so he decided to start walking. He figured he only had to go about 30 miles or so and he\'d be back to the small town he\'d gotten gas in last.\"', SCREEN_WIDTH)))
            time.sleep(10)
            print('\n'.join(textwrap.wrap('\"He thinks about walking at night to avoid the heat and sun, but based upon how dark it actually was the night before, and given that he has no flashlight, he\'s afraid that he\'ll break a leg or step on a rattlesnake. So, he puts on some sun block, puts the rest in his pocket for reapplication later, brings an umbrella he\'d had in the back of the SUV with him to give him a little shade, pours the windshield wiper fluid into his water bottle in case he gets that desperate, brings his pocket knife in case he finds a cactus that looks like it might have water in it, and heads out in the direction he thinks is right.\"', SCREEN_WIDTH)))
            time.sleep(10)
            print('\n'.join(textwrap.wrap('\"He walks for the entire day. By the end of the day he\'s really thirsty. He\'s been sweating all day, and his lips are starting to crack. He\'s reapplied the sunblock twice, and tried to stay under the umbrella, but he still feels sunburned. The windshield wiper fluid sloshing in the bottle in his pocket is really getting tempting now. He knows that it\'s mainly water and some ethanol and coloring, but he also knows that they add some kind of poison to it to keep people from drinking it. He wonders what the poison is, and whether the poison would be worse than dying of thirst.\"', SCREEN_WIDTH)))
            time.sleep(2)
            print('\n'.join(textwrap.wrap('\"He pushes on, trying to get to that small town before dark.\"', SCREEN_WIDTH)))
            time.sleep(10)
            print('\n'.join(textwrap.wrap('\"By the end of the day he starts getting worried. He figures he\'s been walking at least 3 miles an hour, according to his watch for over 10 hours. That means that if his estimate was right that he should be close to the town. But he doesn\'t recognize any of this. He had to cross a dry creek bed a mile or two back, and he doesn\'t remember coming through it in the SUV. He figures that maybe he got his direction off just a little and that the dry creek bed was just off to one side of his path. He tells himself that he\'s close, and that after dark he\'ll start seeing the town lights over one of these hills, and that\'ll be all he needs.\"', SCREEN_WIDTH)))
            time.sleep(10)
            print('\n'.join(textwrap.wrap('\"As it gets dim enough that he starts stumbling over small rocks and things, he finds a spot and sits down to wait for full dark and the town lights.\"', SCREEN_WIDTH)))
            time.sleep(10)
            print('\n'.join(textwrap.wrap('\"Full dark comes before he knows it. He must have dozed off. He stands back up and turns all the way around. He sees nothing but stars.\"', SCREEN_WIDTH)))
            time.sleep(10)
            print('\n'.join(textwrap.wrap('\"He wakes up the next morning feeling absolutely lousy. His eyes are gummy and his mouth and nose feel like they\'re full of sand. He so thirsty that he can\'t even swallow. He barely got any sleep because it was so cold. He\'d forgotten how cold it got at night in the desert and hadn\'t noticed it the night before because he\'d been in his car.\"', SCREEN_WIDTH)))
            time.sleep(10)
            print('Five hours later')
            time.sleep(5)
            print('\n'.join(textwrap.wrap('\"Jack took a firmer grip on the steering wheel as the RV ran up on the stone. Shouting to Sammy as he pulled the steering wheel, "Better Nate than lever!", he ran over the snake.\"', SCREEN_WIDTH)))
            time.sleep(1)
            print('\n'.join(textwrap.wrap('\"The end.\"', SCREEN_WIDTH)))
            return
        else:
            print('Too bad, maybe next time?')
            worldRooms[location][CUTSCENE] = True
            return
    elif location == 'Mt. Falco':
        if worldCreatures['Water Dragon'][HEALTH] == 0:
            worldRooms[location][CUTSCENE] = False
            return
        else:
            worldRooms[location][CUTSCENE] = True
            return
    elif location == 'Upper East Wing of the Temple of Fire':
        print('\n'.join(textwrap.wrap('A mage wearing a fancy hat sits in a chair by the fire.', SCREEN_WIDTH)))
        print('\n'.join(textwrap.wrap('He asks: "have you seen my book? it\'s about fire."', SCREEN_WIDTH)))
        if inventory.count('Book') > 0:
            inventory.remove('Book')
            print('\n'.join(textwrap.wrap('you hand over the book.', SCREEN_WIDTH)))
            print('\n'.join(textwrap.wrap('Archmage: "I owe you my friend, you may pass."', SCREEN_WIDTH)))
        else:
            print('\n'.join(textwrap.wrap('You recall the book in the other room, but as you look back, you see another mage take it.', SCREEN_WIDTH)))
            print('\n'.join(textwrap.wrap('Archmage: "Then why are you here anyway? You\'re trespassing!"', SCREEN_WIDTH)))
            worldCreatures['Archmage of the Temple of Fire'][BOSS] = True
    elif location == 'Upper West Wing of the Temple of Fire':
        print('\n'.join(textwrap.wrap('A Huge figure shows off his biceps.', SCREEN_WIDTH)))
        print('\n'.join(textwrap.wrap('He asks: "have you seen my helmet? it\'s huge due to the size of my brain, yaknow?."', SCREEN_WIDTH)))
        if inventory.count('Huge Helmet') > 0:
            inventory.remove('Huge Helmet')
            print('\n'.join(textwrap.wrap('you hand over the helmet.', SCREEN_WIDTH)))
            print('\n'.join(textwrap.wrap('Juggernaut: "Thanks, see ya later."', SCREEN_WIDTH)))
        else:
            print('\n'.join(textwrap.wrap('You recall the helmet in the other room, but as you look back, you see a blacksmith take it.', SCREEN_WIDTH)))
            print('\n'.join(textwrap.wrap('Juggernaut: "He took my helmet! Grrrrrrrrrr!"', SCREEN_WIDTH)))
            worldCreatures['Juggernaut of the Temple of Fire'][BOSS] = True
    elif location == 'Chamber of Ignisius':
        print('\n'.join(textwrap.wrap('As you enter the room, smoke surrounds you, the door shuts and a heavy, raspy voice speaks to you.', SCREEN_WIDTH)))
        yn = input ('\n'.join(textwrap.wrap('"I see you have found my lair, weakling. But are you willing to carry the consequences? For fivehundred fifty two years have I, Ignisius, possessed the minds of those that entered this volcano. i have made them build a temple, dedicated to me. i have blessed them or killed them as i pleased. generations have shuddered and cheared to my name. and why, you ask? all of them challenged me to a duel. I have a sense of mercy, so instead of fiting them to the death, i propose a deal. if they slay me, they become the hero they desire to be. if i defeat them, i spare them. they become my slave, and dedicate their live to me. if you do not like these conditions, you will displease me. i have a short temper, so you do not want to displease me. will you accept my kind offer?" (y/n)', SCREEN_WIDTH)))
        if yn == 'y':
            print('\n'.join(textwrap.wrap('"So it will be a fair fight then. very well. prepare to join my army of slaves!"', SCREEN_WIDTH)))
            print('\n'.join(textwrap.wrap('The smokes fades just enough for the silouette of a huge dragon to become visible. he lets out a powerful screech, and the whole room starts to shake. parts of the ceiling come crashing down, and magma starts to boil up all around you. a way out becomes visible to your right.', SCREEN_WIDTH)))
        else:
            print('\n'.join(textwrap.wrap('"HOW DARE YOU DISOBEY MY RULES IN MY TEMPLE?!"', SCREEN_WIDTH)))
            print('\n'.join(textwrap.wrap('"Rawr"; the dragon eats you alive. You boil and burn to a painful death.', SCREEN_WIDTH)))
            location = saveloc
    elif location == 'Glaucus\'s Gates':
        if worldCreatures['Wind Dragon'][HEALTH] == 0:
            print()
            print('\n'.join(textwrap.wrap('You inhale a big ammount of air before throwing your upper body towards the ground, flipping you over upside down and allowing you to start swimming downwards', SCREEN_WIDTH)))
            print('\n'.join(textwrap.wrap('There is a long ways to go, trenches can reach as far as 10 kilometers down, there is however no reason for you to stress about the inmense water pressure on you that is slowly raising... After all, you will only get down if you just keep swimming...', SCREEN_WIDTH)))
            print('\n'.join(textwrap.wrap('As time passes you start seeing different types of organisms appearing around you. At first, you saw animals that at least kind off resembled regular fish, but down here they look more like individual nightmares than fish...', SCREEN_WIDTH)))
            print('\n'.join(textwrap.wrap('You don\'t know for how long you have been swimming downwards, heck you don\'t even know if you are still swimming downwards as everything around you is pitchblack, unable to see even your own hand moving through the water, your head hurts like crazy and it seems like you have lost your ability to listen, although there could just be no sounds at all as well', SCREEN_WIDTH)))
            print('\n'.join(textwrap.wrap('Then all of the sudden, you bump your head into what seems to be the bottom of the trench, unable to see what\'s going on you turn around right side up out of instinct, you try to look around, nothing... you push yourself downwards a little in order for you to stand on your feet again, that\'s when you spotted the light underneath you, you try to kick away some of the rocks and pebbles that seem to be covering it, you unveil a doorway and before you know it... you get sucked in.', SCREEN_WIDTH)))
            time.sleep(1)
            worldRooms[location][CUTSCENE] = False
            return
        else:
            print()
            print('\n'.join(textwrap.wrap('You spot a deep hole underneath the blue waves, unfortunately it is impossible to swim down there without drowning, you will need to find a way to hold your breath for an extended period of time ', SCREEN_WIDTH)))
            time.sleep(1)
            worldRooms[location][CUTSCENE] = True
            return
    elif location == 'Poseidon\'s Passage':
            print('\n'.join(textwrap.wrap('You found a hidden entrance in the floor, a slim stairway leads you downwards even further, no human has ever entered the place that you are about to enter, watch your step...', SCREEN_WIDTH)))
    elif location == 'Mysterious hole':
        print('\n'.join(textwrap.wrap('\nYou jump down the hole and fall down to a square room with writings in an unknown language on the wall. A man dressed in red speaks to you. \"you have made a mistake to come to the Temple of Fire. Any last words?\"', SCREEN_WIDTH)))
        time.sleep(5)
        location = 'Entrance to the Temple of Fire'
    elif location == 'Glaucus\'s Monument':
        print()
        print('\n'.join(textwrap.wrap('\nBefore entering the room, you hear a light growning, preparing for what is most likely your next main opponent, you slowly enter the room...', SCREEN_WIDTH)))
        print('\n'.join(textwrap.wrap('\nThe moment you set foot into the room, doors slam back behind you and you are left in almost complete darkness, its cold down there, you hear loud bonks coming your way, a deep, dark voice reverbing through the entire room...', SCREEN_WIDTH)))
        print('\n'.join(textwrap.wrap('\nGlaucus: Ive always known that the men who built my temple wouldnt be the last visitors id ever have... I assume that you are here for my elemental powers. You dont seem to want to use them for personal gain, there is only one sword like the one you have on you, MacGuffin seems to trust you, just like he trusted me...', SCREEN_WIDTH)))
        print('\n'.join(textwrap.wrap('\nSee, a couple millenia ago I was captured by humans, and held hostage, MacGuffin saved me and brought my bruised body and ashamed mind with him to Ottolo, there I was healed and respected. I easily could have destroyed the entire city in a blink of an eye, but I was trusted by MacGuffin.', SCREEN_WIDTH)))
        print('\n'.join(textwrap.wrap('\n I never got the chance to repay him that favor... If the issues you are currently facing up there, at earths surface, that your final resort is to take the elemental powers... I wont be the one standing in your way... Take me out... soldier... I trust you.', SCREEN_WIDTH)))
    elif location == 'Not So Mysterious hole':
        print('\n'.join(textwrap.wrap('\nYou jump down the hole and fall down the cave entrance.\"', SCREEN_WIDTH)))
        time.sleep(5)
        location = 'Cave Entrance'
    elif location == 'Realm of the Unicorns':
        print('\nYou sense a strange feeling all around you. An immense pressure is put on your body, and you suddenly find yourself somewhere else...')
        time.sleep(4)
    elif location == 'Lower East Wing of the Temple of Fire':
        yn = input ('\nA sign above the door reads: "The room beyond is stationary, yet the passage is just temporary. it leads you to the library, turn around to enter the armory." Do you want to enter? (y/n)'),
        if yn == 'y':
            print ('\nThe door closes behind you')
        else:
            worldRooms[location][CUTSCENE] = True
            return
    elif location == 'Lower West Wing of the Temple of Fire':
        yn = input ('\nA sign above the door reads: "The room beyond is stationary, yet the passage is just temporary. it leads you to the armory, turn around to enter the library." Do you want to enter? (y/n)'),
        if yn == 'y':
            print ('\nThe door closes behind you')
        else:
            worldRooms[location][CUTSCENE] = True
            return
    elif location == 'Large Stairs':
        print()
        print('\n'.join(textwrap.wrap('As you slowly climb the stairs you hear a deep rumbling.', SCREEN_WIDTH)))
        time.sleep(1)
        print('\n'.join(textwrap.wrap('You see the stone wall parting in the middle and as a doorway is slowly reveal you hear a booming voice echoing through the hall.', SCREEN_WIDTH)))
        time.sleep(1)
        print('\n'.join(textwrap.wrap('\"Welcome Challenger! Do you think you are worthy of claiming my price? Do you think you can beat my challenge?\"', SCREEN_WIDTH)))
        time.sleep(1)
        print('\"You must know that if you enter now, you will not be able to leave.\"')
        time.sleep(1)
        yn = input('\"Do you want to continue?\" (y/n) ')
        if yn == 'y':
            print('\n'.join(textwrap.wrap('\"Well, I hope you made the right decision.\"', SCREEN_WIDTH)))
            time.sleep(1)
            print('A strong wind pushes you through the newly opened doorway and you hear it close behind you.')
            time.sleep(1)
            location = 'Red Floor Save Room'
        else:
            print('\n'.join(textwrap.wrap('\"Then return when you are ready.\"', SCREEN_WIDTH)))
            time.sleep(1)
            worldRooms[location][CUTSCENE] = True
            return
    elif location == 'Earth\'s void':
        print()
        print('\n'.join(textwrap.wrap('The grounds begins to shake. You lose your balance and fall down the hole.', SCREEN_WIDTH)))
        time.sleep(1)
        location= 'Gaea\'s lair'
    elif location == 'Roof of the Tower':
        print()
        print('\n'.join(textwrap.wrap('You climb up the stairs and meet an old looking wizard.The old wizard stops in his meditation and opens his eyes.', SCREEN_WIDTH)))
        time.sleep(0.5)
        print('\n'.join(textwrap.wrap(' "Greetings, you\'re the first one to make it this far. Ironic. That look, those eyes, it brings back fond memories of mine".', SCREEN_WIDTH)))
        time.sleep(0.5)
        print('\n'.join(textwrap.wrap('The wizard walks towards you, he gives off a friendly but immense aura. "My name is MacGuffin, and I deem you worthy of my task.', SCREEN_WIDTH)))
        time.sleep(0.5)
        print('\n'.join(textwrap.wrap('This tower...', SCREEN_WIDTH)))
        time.sleep(0.5)
        print('\n'.join(textwrap.wrap('Everything in this tower was merely a test. There are dangers beyond your imagination, those which should be left alone and those who need to be tackled.', SCREEN_WIDTH)))
        time.sleep(0.5)
        print('\n'.join(textwrap.wrap('Danger is approaching, and we must ready ourself. Youngling your power cannot be wasted in this town, explore the outer world and find true power.', SCREEN_WIDTH)))
        time.sleep(0.5)
        print('\n'.join(textwrap.wrap('You must prepare for this danger. The fastest way to do this is to use this sword".', SCREEN_WIDTH)))
        time.sleep(0.5)
        print('\n'.join(textwrap.wrap('MacGuffin let\'s a sword magically appear and stucks it into the ground.', SCREEN_WIDTH)))
        time.sleep(0.5)
        print('\n'.join(textwrap.wrap('"This is the dragonslayer sword, take it, kill dragons with it and grow fat from strength.', SCREEN_WIDTH)))
        time.sleep(0.5)
        print('\n'.join(textwrap.wrap('See this dragon behind me, kill it. Gain it\'s power', SCREEN_WIDTH)))
        time.sleep(0.5)
    elif location == 'DO NOT ENTER':
        print()
        print('\n'.join(textwrap.wrap('You\'re here atlast, the final moment of your journey. This is what MacGuffin wanted, this is what your Grandfather wanted. You\'re here to slay the dragon that terrorized your village for decades. Ta\'xeq, tthe doom of this city is here. ', SCREEN_WIDTH)))
        time.sleep(0.5)
        print('\n'.join(textwrap.wrap('You step into the dark room and light your torch. A wingless dragon stands before you, his skin dark, his claws green.', SCREEN_WIDTH)))
        time.sleep(0.5)
        print('\n'.join(textwrap.wrap('A deafening roar comes from the dragon. "HAHAHAHAHAHAHAHAHA, YOU FOOL, DO YOU KNOW WHAT YOU HAVE DONE?"', SCREEN_WIDTH)))
        time.sleep(0.5)
        print('\n'.join(textwrap.wrap('"I DO NOT KNOW WHO DESTROYED MY CHAINS BUT I AM THANFULL, I SHALL REWARD YOUR KIND WITH DEATH HAHAHAHAHAHA."', SCREEN_WIDTH)))
        time.sleep(0.5)
        print('\n'.join(textwrap.wrap('"AND WHO ARE YOU? DO YOU THINK YOU CAN SLAY? DO YOU THINK LITTLE SWORD CAN SLAY A DRAGON?"', SCREEN_WIDTH)))
        time.sleep(0.5)
        print('\n'.join(textwrap.wrap('"I HAVE NO TIME FOR THE LIKES OF YOU." The dragon breaks through the ceiling, you decide to follow it.', SCREEN_WIDTH)))
        time.sleep(0.5)
        location='Prism Square Ruined'
    elif location == 'Prism Square Ruined':
        print('\n'.join(textwrap.wrap('You arrive at Prism Square, or something that faguely resembles it. Ta\'xeq went on a rampage and has destroyed nearly everything of Prism Square.', SCREEN_WIDTH)))
        time.sleep(0.5)
        print('\n'.join(textwrap.wrap('"HAHAHAHAH BEHOLD THE MIGHTY POWER OF TA\'XEQ AND QUIVER IN FEAR". The dragon notices your presence"', SCREEN_WIDTH)))
        time.sleep(0.5)
        print('\n'.join(textwrap.wrap('"FOOLISH BOY, FIGHT ME IF THAT IS WHAT YOU DESIRE".', SCREEN_WIDTH)))
        time.sleep(0.5)

def wild():
    global expeditionTimer
    global expeditionLength
    global gold
    global location

    if expeditionTimer < 0:
        yn = input('Urila: \"Do you want to go into the woods today?\" (y/n) ')
        if yn == 'y':
            print('Urila: \"So what will it be today?\"')
            time.sleep(0.5)
            while expeditionLength != 's' or 'm' or 'l':
                expeditionLength = input('\"15, 30 of 50 minutes? (s/m/l) ')
                if expeditionLength == 's':
                    if gold < 5:
                        print('You don\'t have enough money for the expedition')
                        location = old_location
                        return
                    else:
                        expeditionTimer = 15
                        gold -= 5
                        print('You paid 5 gold.')
                        print('Urila: \"Good luck!\"')
                        return
                elif expeditionLength == 'm':
                    if gold < 15:
                        print('You don\'t have enough money for the expedition')
                        location = old_location
                        return
                    else:
                        expeditionTimer = 30
                        gold -= 15
                        print('You paid 15 gold.')
                        print('Urila: \"Good luck!\"')
                        return
                elif expeditionLength == 'l':
                    if gold < 25:
                        print('You don\'t have enough money for the expedition')
                        location = old_location
                        return
                    else:
                        expeditionTimer = 50
                        gold -= 25
                        print('You paid 25 gold.')
                        print('Urila: \"Good luck!\"')
                        return
                else:
                    print('Not a valid command.')
                    time.sleep(0.5)
        else:
            print('Urila: \"Maybe not today.\"')
            location = old_location
            return
    elif expeditionTimer == 0:
        location = 'Urila\'s Survivers Corner'
        print('Urila: \"You actually made it!\"')
        if expeditionLength == 's':
            gold += 15
            print('You received 15 gold.')
        elif expeditionLength == 'm':
            gold += 30
            print('You received 30 gold.')
        elif expeditionLength == 'l':
            gold += 50
            print('You received 50 gold.')
        expeditionLength = 0
        expeditionTimer = -1
        return
    elif expeditionTimer == 1:
        if expeditionLength == 's':
            pass
        elif expeditionLength == 'm':
            pass
        elif expeditionLength == 'l':
            location = 'Realm of the Unicorns'
            cutscene()
    else:
        worldRooms[location][CREATURES] = [] 
        enemyRoll = randint(0, 3)
        if enemyRoll == 0:
            return
        else:
            for x in range(0, enemyRoll):
                typeRoll = randint(1, 100) + (level - 1 * 5)
                if typeRoll <= 30:
                    worldRooms[location][CREATURES].append('Wild Frog')
                elif typeRoll >= 31 and typeRoll <= 55:
                    worldRooms[location][CREATURES].append('Wild Chicken')
                elif typeRoll >= 56 and typeRoll <= 75:
                    worldRooms[location][CREATURES].append('Wild Cow')
                elif typeRoll >= 76 and typeRoll <= 95:
                    worldRooms[location][CREATURES].append('Wild Wolf')
                else:
                    worldRooms[location][CREATURES].append('Wild Unicorn')      

"""def drawRoom():
    if location == 'Your Bedroom':
        arcade.set_background_color(arcade.color.YELLOW)
        arcade.draw_circle_filled(50, 350, 20, arcade.color.BLACK)
    elif location == 'Your Livingroom':
        arcade.set_background_color(arcade.color.YELLOW)
    elif location == 'Black Alley':
        arcade.set_background_color(arcade.color.BLACK)"""


class TextAdventureCmd(cmd.Cmd):

    prompt = '\n> '

    # The default() method is called when none of the other do_*() command methods match.
    def default(self, arg):
        print('I do not understand that command. Type "help" for a list of commands.')

    # A very simple "quit" command to terminate the program:
    def do_quit(self, arg):
        """Quit the game."""
        return True # this exits the Cmd application loop in TextAdventureCmd.cmdloop()

    do_gg = do_quit
    do_commit_die = do_quit

    # These direction commands have a long (i.e. north) and show (i.e. n) form.
    # Since the code is basically the same, I put it in the moveDirection()
    # function.
    def do_north(self, arg):
        """Go to the area to the north, if possible."""
        moveDirection('north')

    def do_south(self, arg):
        """Go to the area to the south, if possible."""
        moveDirection('south')

    def do_east(self, arg):
        """Go to the area to the east, if possible."""
        moveDirection('east')

    def do_west(self, arg):
        """Go to the area to the west, if possible."""
        moveDirection('west')

    def do_up(self, arg):
        """Go to the area upwards, if possible."""
        moveDirection('up')

    def do_down(self, arg):
        """Go to the area downwards, if possible."""
        moveDirection('down')

    # Since the code is the exact same, we can just copy the
    # methods with shortened names:
    do_n = do_north
    do_s = do_south
    do_e = do_east
    do_w = do_west
    do_u = do_up
    do_d = do_down

    def do_exits(self, arg):
        """Toggle showing full exit descriptions or brief exit descriptions."""
        global showFullExits
        showFullExits = not showFullExits
        if showFullExits:
            print('Showing full exit descriptions.')
        else:
            print('Showing brief exit descriptions.')

    def do_inventory(self, arg):
        """Display a list of the items in your possession."""

        if len(inventory) == 0:
            print('Inventory:\n  (nothing)')
            return

        # first get a count of each distinct item in the inventory
        itemCount = {}
        for item in inventory:
            if item in itemCount.keys():
                itemCount[item] += 1
            else:
                itemCount[item] = 1

        # get a list of inventory items with duplicates removed:
        print('Inventory:')
        for item in set(inventory):
            if itemCount[item] > 1:
                print('  %s (%s)' % (item, itemCount[item]))
            else:
                print('  ' + item)

    do_inv = do_inventory

    def do_gold(self, arg):
        """Display the amount of gold of the player"""
        print('Gold: ' + str(gold))
    
    do_g = do_gold

    def do_take(self, arg):
        """"take <item> - Take an item on the ground."""
        global head
        global chest
        global hands
        global legs
        global feet

        # put this value in a more suitably named variable
        itemToTake = arg.lower()

        if itemToTake == '':
            print('Take what? Type "look" the items on the ground here.')
            return

        cantTake = False

        # get the item name that the player's command describes
        for item in getAllItemsMatchingDesc(itemToTake, worldRooms[location][GROUND]):
            if worldItems[item].get(TAKEABLE, True) == False:
                cantTake = True
                continue # there may be other items named this that you can take, so we continue checking
            print('You take %s.' % (worldItems[item][SHORTDESC]))
            worldRooms[location][GROUND].remove(item) # remove from the ground
            if worldItems[item].get(EQUIPABLE, False) == True:
                if worldItems[item][EQUIPTYPE] == 'HEAD':
                    if head != 0:
                        print('You already have ' + worldItems[head][SHORTDESC] + ' equipped.')
                        yn = input('Do you want to switch your items? (y/n) ')
                        if yn == 'y':
                            inventory.append(head)
                            equipped.remove(head)
                            stats[1] -= worldItems[head][STRENGTH]
                            stats[2] -= worldItems[head][DEFENCE]
                            stats[3] -= worldItems[head][PERCEPTION]
                            stats[4] -= worldItems[head][SPEED]
                            head = item
                        else:
                            print('You don\'t equip ' + item)
                            inventory.append(item)
                            return
                    else:
                        head = item
                elif worldItems[item][EQUIPTYPE] == 'CHEST':
                    if chest != 0:
                        print('You already have ' + worldItems[chest][SHORTDESC] + ' equipped.')
                        yn = input('Do you want to switch your items? (y/n) ')
                        if yn == 'y':
                            inventory.append(chest)
                            equipped.remove(chest)
                            stats[1] -= worldItems[chest][STRENGTH]
                            stats[2] -= worldItems[chest][DEFENCE]
                            stats[3] -= worldItems[chest][PERCEPTION]
                            stats[4] -= worldItems[chest][SPEED]
                            chest = item                            
                        else:
                            print('You don\'t equip ' + item)
                            inventory.append(item)
                            return
                    else:
                        chest = item
                elif worldItems[item][EQUIPTYPE] == 'HANDS':
                    if hands != 0:
                        print('You already have ' + worldItems[hands][SHORTDESC] + ' equipped.')
                        yn = input('Do you want to switch your items? (y/n) ')
                        if yn == 'y':
                            inventory.append(hands)
                            equipped.remove(hands)
                            stats[1] -= worldItems[hands][STRENGTH]
                            stats[2] -= worldItems[hands][DEFENCE]
                            stats[3] -= worldItems[hands][PERCEPTION]
                            stats[4] -= worldItems[hands][SPEED]
                            hands = item
                        else:
                            print('You don\'t equip ' + item)
                            inventory.append(item)
                            return
                    else:
                        hands = item
                elif worldItems[item][EQUIPTYPE] == 'LEGS':
                    if legs != 0:
                        print('You already have ' + worldItems[legs][SHORTDESC] + ' equipped.')
                        yn = input('Do you want to switch your items? (y/n) ')
                        if yn == 'y':
                            inventory.append(legs)
                            equipped.remove(legs)
                            stats[1] -= worldItems[legs][STRENGTH]
                            stats[2] -= worldItems[legs][DEFENCE]
                            stats[3] -= worldItems[legs][PERCEPTION]
                            stats[4] -= worldItems[legs][SPEED]
                            legs = item

                        else:
                            print('You don\'t equip ' + item)
                            inventory.append(item)
                            return
                    else:
                        legs = item
                else:
                    if feet != 0:
                        print('You already have ' + worldItems[feet][SHORTDESC] + ' equipped.')
                        yn = input('Do you want to switch your items? (y/n) ')
                        if yn == 'y':
                            inventory.append(feet)
                            equipped.remove(feet)
                            stats[1] -= worldItems[feet][STRENGTH]
                            stats[2] -= worldItems[feet][DEFENCE]
                            stats[3] -= worldItems[feet][PERCEPTION]
                            stats[4] -= worldItems[feet][SPEED]
                            feet = item
                        else:
                            print('You don\'t equip ' + item)
                            inventory.append(item)
                            return
                    else:
                        feet = item

                print('You equip %s' % (worldItems[item][SHORTDESC]))
                
                stats[1] += worldItems[item][STRENGTH]
                stats[2] += worldItems[item][DEFENCE]
                stats[3] += worldItems[item][PERCEPTION]
                stats[4] += worldItems[item][SPEED]
                equipped.append(item)
                return
            inventory.append(item) # add to inventory
            return

        if cantTake:
            print('You cannot take "%s".' % (itemToTake))
        else:
            print('That is not on the ground.')

    def do_drop(self, arg):
        """"drop <item> - Drop an item from your inventory onto the ground."""

        # put this value in a more suitably named variable
        itemToDrop = arg.lower()

        # get a list of all "description words" for each item in the inventory
        invDescWords = getAllDescWords(inventory)

        # find out if the player doesn't have that item
        if itemToDrop not in invDescWords:
            print('You do not have "%s" in your inventory.' % (itemToDrop))
            return

        # get the item name that the player's command describes
        item = getFirstItemMatchingDesc(itemToDrop, inventory)
        if item != None:
            if worldItems[item].get(QUESTITEM, False) == True:
                print('You cannot drop this item.')
                return
            print('You drop %s.' % (worldItems[item][SHORTDESC]))
            inventory.remove(item) # remove from inventory
            worldRooms[location][GROUND].append(item) # add to the ground

    def do_give(self, arg):
            """"give <item> - Give an item from your inventory onto the ground."""

            # put this value in a more suitably named variable
            itemToGive = arg.lower()

            # get a list of all "description words" for each item in the inventory
            invDescWords = getAllDescWords(inventory)

            # find out if the player doesn't have that item
            if itemToGive not in invDescWords:
                print('You do not have "%s" in your inventory.' % (itemToGive))
                return

            if worldRooms[location].get(CREATURES, []) == []:
                print('There\'s no one to give this to.')
                return

            # get the item name that the player's command describes
            item = getFirstItemMatchingDesc(itemToGive, inventory)
            npc = worldRooms[location][CREATURES][0]
            
            if worldCreatures[npc].get(SIDEQUEST, False) == True:
                if item in worldCreatures[npc][SIDEQUESTITEMS]:
                    print('You give ' + worldCreatures[npc][SHORTDESC] + ' %s.' % (worldItems[item][SHORTDESC]))
                    inventory.remove(item)
                    worldCreatures[npc][SIDEQUESTINV].append(item)
                    if set(worldCreatures[npc][SIDEQUESTINV]) == set(worldCreatures[npc][SIDEQUESTITEMS]):
                        time.sleep(0.5)
                        print(worldCreatures[npc][SIDEQUESTEND])
                        for item in worldCreatures[npc][SIDEQUESTREWARD]:
                            inventory.append(item)
                        worldCreatures[npc][SIDEQUEST] = False
                    return  
                else:
                    print('You cannot give this item.')
                    return
            else:
                print('You cannot give them this item.')
                
    def complete_take(self, text, line, begidx, endidx):
        possibleItems = []
        text = text.lower()

        # if the user has only typed "take" but no item name:
        if not text:
            return getAllFirstDescWords(worldRooms[location][GROUND])

        # otherwise, get a list of all "description words" for ground items matching the command text so far:
        for item in list(set(worldRooms[location][GROUND])):
            for descWord in worldItems[item][DESCWORDS]:
                if descWord.startswith(text) and worldItems[item].get(TAKEABLE, True):
                    possibleItems.append(descWord)

        return list(set(possibleItems)) # make list unique

    def complete_drop(self, text, line, begidx, endidx):
        possibleItems = []
        itemToDrop = text.lower()

        # get a list of all "description words" for each item in the inventory
        invDescWords = getAllDescWords(inventory)

        for descWord in invDescWords:
            if line.startswith('drop %s' % (descWord)):
                return [] # command is complete

        # if the user has only typed "drop" but no item name:
        if itemToDrop == '':
            return getAllFirstDescWords(inventory)

        # otherwise, get a list of all "description words" for inventory items matching the command text so far:
        for descWord in invDescWords:
            if descWord.startswith(text):
                possibleItems.append(descWord)

        return list(set(possibleItems)) # make list unique

    def do_look(self, arg):
        """Look at an item, direction, or the area:
        "look" - display the current area's description
        "look <direction>" - display the description of the area in that direction
        "look exits" - display the description of all adjacent areas
        "look <item>" - display the description of an item on the ground or in your inventory"""

        lookingAt = arg.lower()
        if lookingAt == '':
            # "look" will re-print the area description
            displayLocation(location)
            return

        if lookingAt == 'exits':
            for direction in (NORTH, SOUTH, EAST, WEST, UP, DOWN):
                if direction in worldRooms[location]:
                    print('%s: %s' % (direction.title(), worldRooms[location][direction]))
            return

        if lookingAt in ('north', 'west', 'east', 'south', 'up', 'down', 'n', 'w', 'e', 's', 'u', 'd'):
            if lookingAt.startswith('n') and NORTH in worldRooms[location]:
                if worldRooms[direction][LOCKED] == True:
                    print('That place is locked.')
                else:
                    print(worldRooms[location][NORTH])
            elif lookingAt.startswith('w') and WEST in worldRooms[location]:
                if worldRooms[location][LOCKED] == True:
                    print('That place is locked.')
                else:
                    print(worldRooms[location][WEST])
            elif lookingAt.startswith('e') and EAST in worldRooms[location]:
                if worldRooms[location][LOCKED] == True:
                    print('That place is locked.')
                else:
                    print(worldRooms[location][EAST])
            elif lookingAt.startswith('s') and SOUTH in worldRooms[location]:
                if worldRooms[location][LOCKED] == True:
                    print('That place is locked.')
                else:
                    print(worldRooms[location][SOUTH])
            elif lookingAt.startswith('u') and UP in worldRooms[location]:
                if worldRooms[location][LOCKED] == True:
                    print('That place is locked.')
                else:
                    print(worldRooms[location][UP])
            elif lookingAt.startswith('d') and DOWN in worldRooms[location]:
                if worldRooms[location][LOCKED] == True:
                    print('That place is locked.')
                else:
                    print(worldRooms[location][DOWN])
            else:
                print('There is nothing in that direction.')
            return

        # see if the item being looked at is on the ground at this location
        item = getFirstItemMatchingDesc(lookingAt, worldRooms[location][GROUND])
        if item != None:
            print('\n'.join(textwrap.wrap(worldItems[item][LONGDESC], SCREEN_WIDTH)))
            if worldItems[item].get(STATS, False) == True:
                print('\nAttack: ' + str(worldItems[item][STRENGTH]) + '\nDefence: ' + str(worldItems[item][DEFENCE]) + '\nPerception: ' + str(worldItems[item][PERCEPTION]) + '\nSpeed: ' + str(worldItems[item][SPEED]))
            else:
                pass
            return

        item = getFirstCreatureMatchingDesc(lookingAt, worldRooms[location][CREATURES])
        if item != None:
            print('\n'.join(textwrap.wrap(worldCreatures[item][LONGDESC], SCREEN_WIDTH)))
            return

        # see if the item being looked at is in the inventory
        item = getFirstItemMatchingDesc(lookingAt, inventory)
        if item != None:
            print('\n'.join(textwrap.wrap(worldItems[item][LONGDESC], SCREEN_WIDTH)))
            if worldItems[item].get(STATS, False) == True:
                print('\nAttack: ' + str(worldItems[item][STRENGTH]) + '\nDefence: ' + str(worldItems[item][DEFENCE]) + '\nPerception: ' + str(worldItems[item][PERCEPTION]) + '\nSpeed: ' + str(worldItems[item][SPEED]))
            else:
                pass
            return

        item = getFirstItemMatchingDesc(lookingAt, equipped)
        if item != None:
            print('\n'.join(textwrap.wrap(worldItems[item][LONGDESC], SCREEN_WIDTH)))
            if worldItems[item].get(STATS, False) == True:
                print('\nAttack: ' + str(worldItems[item][STRENGTH]) + '\nDefence: ' + str(worldItems[item][DEFENCE]) + '\nPerception: ' + str(worldItems[item][PERCEPTION]) + '\nSpeed: ' + str(worldItems[item][SPEED]))
            else:
                pass
            return
            
        print('You do not see that nearby.')

    def complete_look(self, text, line, begidx, endidx):
        possibleItems = []
        lookingAt = text.lower()

        # get a list of all "description words" for each item in the inventory
        invDescWords = getAllDescWords(inventory)
        groundDescWords = getAllDescWords(worldRooms[location][GROUND])
        shopDescWords = getAllDescWords(worldRooms[location].get(SHOP, []))

        for descWord in invDescWords + groundDescWords + shopDescWords + [NORTH, SOUTH, EAST, WEST, UP, DOWN]:
            if line.startswith('look %s' % (descWord)):
                return [] # command is complete

        # if the user has only typed "look" but no item name, show all items on ground, shop and directions:
        if lookingAt == '':
            possibleItems.extend(getAllFirstDescWords(worldRooms[location][GROUND]))
            possibleItems.extend(getAllFirstDescWords(worldRooms[location].get(SHOP, [])))
            for direction in (NORTH, SOUTH, EAST, WEST, UP, DOWN):
                if direction in worldRooms[location]:
                    possibleItems.append(direction)
            return list(set(possibleItems)) # make list unique

        # otherwise, get a list of all "description words" for ground items matching the command text so far:
        for descWord in groundDescWords:
            if descWord.startswith(lookingAt):
                possibleItems.append(descWord)

        # otherwise, get a list of all "description words" for items for sale at the shop (if this is one):
        for descWord in shopDescWords:
            if descWord.startswith(lookingAt):
                possibleItems.append(descWord)

        # check for matching directions
        for direction in (NORTH, SOUTH, EAST, WEST, UP, DOWN):
            if direction.startswith(lookingAt):
                possibleItems.append(direction)

        # get a list of all "description words" for inventory items matching the command text so far:
        for descWord in invDescWords:
            if descWord.startswith(lookingAt):
                possibleItems.append(descWord)

        return list(set(possibleItems)) # make list unique

    def do_list(self, arg):
        """List the items for sale at the current location's shop. "list full" will show details of the items."""
        if SHOP not in worldRooms[location]:
            print('This is not a shop.')
            return

        arg = arg.lower()

        print('For sale:')
        for item in worldRooms[location][SHOP]:
            print('  - %s' % (item))
            if arg == 'full':
                print('\n'.join(textwrap.wrap(worldItems[item][LONGDESC], SCREEN_WIDTH)))

    def do_buy(self, arg):
        """"buy <item>" - buy an item at the current location's shop."""
        global gold
        if SHOP not in worldRooms[location]:
            print('This is not a shop.')
            return

        itemToBuy = arg.lower()

        if itemToBuy == '':
            print('Buy what? Type "list" or "list full" to see a list of items for sale.')
            return

        item = getFirstItemMatchingDesc(itemToBuy, worldRooms[location][SHOP])
         
        if item != None:
            # NOTE - If you wanted to implement money, here is where you would add
            # code that checks if the player has enough, then deducts the price
            # from their money.
            if int(worldItems[item][PRICE]) > gold:
                print('You don\'t have enough enough gold.')
                return
            else:
                gold -= int(worldItems[item][PRICE])
                print('You have purchased %s' % (worldItems[item][SHORTDESC]))
                inventory.append(item)
                return

        print('"%s" is not sold here. Type "list" or "list full" to see a list of items for sale.' % (itemToBuy))

    def complete_buy(self, text, line, begidx, endidx):
        if SHOP not in worldRooms[location]:
            return []

        itemToBuy = text.lower()
        possibleItems = []

        # if the user has only typed "buy" but no item name:
        if not itemToBuy:
            return getAllFirstDescWords(worldRooms[location][SHOP])

        # otherwise, get a list of all "description words" for shop items matching the command text so far:
        for item in list(set(worldRooms[location][SHOP])):
            for descWord in worldItems[item][DESCWORDS]:
                if descWord.startswith(text):
                    possibleItems.append(descWord)

        return list(set(possibleItems)) # make list unique

    def do_sell(self, arg):
        """"sell <item>" - sell an item at the current location's shop."""
        global gold
        if SHOP not in worldRooms[location]:
            print('This is not a shop.')
            return

        itemToSell = arg.lower()

        if itemToSell == '':
            print('Sell what? Type "inventory" or "inv" to see your inventory.')
            return

        for item in inventory:
            if itemToSell in worldItems[item][DESCWORDS]:
                if worldItems[item].get(QUESTITEM, False) == True:
                    print('You cannot sell this item.')
                    return
                # NOTE - If you wanted to implement money, here is where you would add
                # code that gives the player money for selling the item.
                #for worldItems[item][PRICE] in (0, int(worldItems[item][PRICE])):
                gold += int(worldItems[item][PRICE]*0.75)
                print('You have sold %s for ' % (worldItems[item][SHORTDESC])  + str(worldItems[item][PRICE]*0.75) + ' gold.')
                inventory.remove(item)
                worldRooms[location][SHOP].append(item)
                return

        print('You do not have "%s". Type "inventory" or "inv" to see your inventory.' % (itemToSell))

    def complete_sell(self, text, line, begidx, endidx):
        if SHOP not in worldRooms[location]:
            return []

        itemToSell = text.lower()
        possibleItems = []

        # if the user has only typed "sell" but no item name:
        if not itemToSell:
            return getAllFirstDescWords(inventory)

        # otherwise, get a list of all "description words" for inventory items matching the command text so far:
        for item in list(set(inventory)):
            for descWord in worldItems[item][DESCWORDS]:
                if descWord.startswith(text):
                    possibleItems.append(descWord)

        return list(set(possibleItems)) # make list unique

    def do_eat(self, arg):
        """"eat <item>" - eat an item in your inventory."""
        itemToEat = arg.lower()

        if itemToEat == '':
            print('Eat what? Type "inventory" or "inv" to see your inventory.')
            return

        cantEat = False

        for item in getAllItemsMatchingDesc(itemToEat, inventory):
            if worldItems[item].get(EDIBLE, False) == False:
                cantEat = True
                continue 
            print('You eat %s' % (worldItems[item][SHORTDESC]))
            stats[0] += worldItems[item][HEALTH]
            if stats[0] > maxHealth:
                stats[0] = maxHealth
            inventory.remove(item)
            return

        if cantEat:
            print('You cannot eat that.')
        else:
            print('You do not have "%s". Type "inventory" or "inv" to see your inventory.' % (itemToEat))

    def complete_eat(self, text, line, begidx, endidx):
        itemToEat = text.lower()
        possibleItems = []

        # if the user has only typed "eat" but no item name:
        if itemToEat == '':
            return getAllFirstDescWords(inventory)

        # otherwise, get a list of all "description words" for edible inventory items matching the command text so far:
        for item in list(set(inventory)):
            for descWord in worldItems[item][DESCWORDS]:
                if descWord.startswith(text) and worldItems[item].get(EDIBLE, False):
                    possibleItems.append(descWord)

        return list(set(possibleItems)) # make list unique
    
    def do_drink(self, arg):
        """"drink <item>" - drink an item in your inventory."""
        itemToDrink = arg.lower()

        if itemToDrink == '':
            print('Drink what? Type "inventory" or "inv" to see your inventory.')
            return

        cantdrink = False

        for item in getAllItemsMatchingDesc(itemToDrink, inventory):
            if worldItems[item].get(DRINKABLE, False) == False:
                cantdrink = True
                continue 
            print('You drink %s' % (worldItems[item][SHORTDESC]))
            stats[0] += worldItems[item][HEALTH]
            if stats[0] > maxHealth:
                stats[0] = maxHealth
            inventory.remove(item)
            return

        if cantdrink:
            print('You cannot drink that.')
        else:
            print('You do not have "%s". Type "inventory" or "inv" to see your inventory.' % (itemToDrink))

    def complete_drink(self, text, line, begidx, endidx):
        itemToDrink = text.lower()
        possibleItems = []

        # if the user has only typed "drink" but no item name:
        if itemToDrink == '':
            return getAllFirstDescWords(inventory)

        # otherwise, get a list of all "description words" for DRINKABLE inventory items matching the command text so far:
        for item in list(set(inventory)):
            for descWord in worldItems[item][DESCWORDS]:
                if descWord.startswith(text) and worldItems[item].get(DRINKABLE, False):
                    possibleItems.append(descWord)

        return list(set(possibleItems)) # make list unique
    
    def do_talk(self, arg):
        """"talk <creature> - Talk to any creature in the area."""
        creatureTalk = arg.lower()

        if creatureTalk == '':
            print('Talk to who? Type "look" to see all the creatures in this area.')
            return

        cantTalk = False

        for npc in getAllCreaturesMatchingDesc(creatureTalk, worldRooms[location][CREATURES]):
            if worldCreatures[npc].get(TALKABLE, False) == False:
                cantTalk = True
                continue
            #if worldCreatures[npc].get(CUTSCENE, False) == True:

            time.sleep(0.5)
            print(worldCreatures[npc][GREETING])
            if worldCreatures[npc].get(SIDEQUEST, False) == True:
                time.sleep(0.5)
                print(worldCreatures[npc][SIDEQUESTSTART])
                return
            return

        if cantTalk:
            print(worldCreatures[npc][SHORTDESC] + ' can\'t talk.')
        else:
            print('There is nobody to talk with.')
    
    def complete_talk(self, text, line, begidx, endidx):
        creatureTalk = text.lower()
        possibleItems = []

        # if the user has only typed "talk" but no item name:
        if creatureTalk == '':
            return getAllFirstDescWords(worldRooms[location][CREATURES])

        # otherwise, get a list of all "description words" for edible inventory items matching the command text so far:
        for npc in list(set(worldRooms[location][CREATURES])):
            for descWord in worldCreatures[npc][DESCWORDS]:
                if descWord.startswith(text) and worldCreatures[npc].get(TALKABLE, False):
                    possibleItems.append(descWord)

        return list(set(possibleItems)) # make list unique

    def do_attack(self, arg):
        """"attack <creature> - Attack any creature in the area."""
        global location
        global level
        global exp
        global enemy

        attackRoll = 0
        creatureToAttack = arg.lower()

        if creatureToAttack == '':
            print('Attack what? Type "look" to see all the creatures in this area.')
            return

        enemy = getFirstCreatureMatchingDesc(creatureToAttack, worldRooms[location][CREATURES])
        item = getFirstItemMatchingDesc(creatureToAttack, worldRooms[location][GROUND])

        if enemy in worldRooms[location][CREATURES]:                
            if stats[4] > worldCreatures[enemy][SPEED]:
                attackRoll = randint(1, 20) + stats[3]
                if attackRoll >= worldCreatures[enemy][DEFENCE]:
                    if worldCreatures[enemy].get(SHARK, False) == True and hands == 'Shark Tooth':
                        worldCreatures[enemy][HEALTH] -= stats[1]*2
                        print('You hit for ' + str(stats[1]*2) + ' damage.')
                    else:
                        worldCreatures[enemy][HEALTH] -= stats[1]
                        print('You hit for ' + str(stats[1]) + ' damage.')
                    if worldCreatures[enemy][HEALTH] > 0:
                        defenceRoll = randint(1, 20) + worldCreatures[enemy][PERCEPTION]
                        if defenceRoll >= stats[2]:
                            stats[0] -= worldCreatures[enemy][STRENGTH]
                            print('You got hit for ' + str(worldCreatures[enemy][STRENGTH]) + ' damage.')
                            if stats[0] <= 0:
                                knockedOut()
                        else:
                            print('They miss.')
                    else:
                        enemyKilled()
                else:
                    print('You miss.')
                    defenceRoll = randint(1, 20) + worldCreatures[enemy][PERCEPTION]
                    if defenceRoll >= stats[2]:
                        stats[0] -= worldCreatures[enemy][STRENGTH]
                        print('You got hit for ' + str(worldCreatures[enemy][STRENGTH]) + ' damage.')
                        if stats[0] <= 0:
                            knockedOut()
                    else:   
                        print('They miss.')
            else:
                defenceRoll = randint(1, 20) + worldCreatures[enemy][PERCEPTION]
                if defenceRoll >= stats[2]:
                    stats[0] -= worldCreatures[enemy][STRENGTH]
                    print('You got hit for ' + str(worldCreatures[enemy][STRENGTH]) + ' damage.')
                    if stats[0] > 0:
                        attackRoll = randint(1, 20) + stats[3]
                        if attackRoll >= worldCreatures[enemy][DEFENCE]:
                            if worldCreatures[enemy].get(SHARK, False) == True and hands == 'Shark Tooth':
                                worldCreatures[enemy][HEALTH] -= stats[1]*2
                                print('You hit for ' + str(stats[1]*2) + ' damage.')
                            else:
                                worldCreatures[enemy][HEALTH] -= stats[1]
                                print('You hit for ' + str(stats[1]) + ' damage.')
                            if worldCreatures[enemy][HEALTH] <= 0:
                                enemyKilled()
                        else:
                            print('You miss.')
                    else:
                        knockedOut()
                else:
                    print('They miss.')
                    attackRoll = randint(1, 20) + stats[3]
                    if attackRoll >= worldCreatures[enemy][DEFENCE]:
                        worldCreatures[enemy][HEALTH] -= stats[1]
                        print('You hit for ' + str(stats[1]) + ' damage.')
                        if worldCreatures[enemy][HEALTH] <= 0:
                            enemyKilled()
                    else:
                        print('You miss.')
        elif item in worldRooms[location][GROUND]:
            if worldItems[item].get(TAKEABLE, True) == False:
                worldItems[item][HEALTH] -= stats[1]
                print('You hit for ' + str(stats[1]) + ' damage.')
                if worldItems[item][HEALTH] > 0:
                    return
                else:
                    print('You break ' + worldItems[item][SHORTDESC])
                    worldRooms[location][GROUND].remove(item)
                    worldItems[item][HEALTH] = worldItems[item][MAXHEALTH]
                    if worldItems[item].get(DROPITEM, False) != 0:
                        time.sleep(0.5)
                        print('You picked up:')
                        for item in worldItems[item][DROPITEM]:
                            print('  ' + item)
                            inventory.append(item)
                    return
            else:                    
                print('You can\'t attack that.')
                return
        else:
            print('Attack what? Type "look" to see all the creatures in this area.')
            return

    do_fight = do_attack
    do_a = do_attack

    def do_stats(self, arg):
        """"stats - Look at your stats."""
        print('Level: ' + str(level))
        print('Exp: ' + str(exp) + '/' + str(450 + level*50))
        print('\nHealth: ' + str(stats[0]) + '/' + str(maxHealth) + '\nStrength: ' + str(stats[1]) + '\nDefence: ' + str(stats[2]) + '\nPerception: ' + str(stats[3]) + '\nSpeed: ' + str(stats[4]))
    
    do_level = do_stats
    do_l = do_stats
    do_exp = do_stats
    do_health = do_stats
    do_strength = do_stats
    do_defence = do_stats
    do_perception = do_stats
    do_speed = do_stats

    def do_equip(self, arg):
        """"equip <item>" - equip an item in your inventory."""
        global head
        global chest
        global hands
        global legs
        global feet
        
        itemToEquip = arg.lower()

        if itemToEquip == '':
            print('Equip what? Type "inventory" or "inv" to see your inventory.')
            return

        cantEquip = False

        for item in getAllItemsMatchingDesc(itemToEquip, inventory):
            if worldItems[item].get(EQUIPABLE, False) == False:
                cantEquip = True
                continue 
            else:
                if worldItems[item][EQUIPTYPE] == 'HEAD':
                    if head != 0:
                        print('You can have only one of those equipped.')
                        yn = input('Do you want to switch your items? (y/n) ')
                        if yn == 'y':
                            inventory.append(head)
                            equipped.remove(head)
                            stats[1] -= worldItems[head][STRENGTH]
                            stats[2] -= worldItems[head][DEFENCE]
                            stats[3] -= worldItems[head][PERCEPTION]
                            stats[4] -= worldItems[head][SPEED]
                            head = item
                        else:
                            print('You don\'t equip ' + item)
                            return
                    else:
                        head = item
                elif worldItems[item][EQUIPTYPE] == 'CHEST':
                    if chest != 0:
                        print('You can have only one of those equipped.')
                        yn = input('Do you want to switch your items? (y/n) ')
                        if yn == 'y':
                            inventory.append(chest)
                            equipped.remove(chest)
                            stats[1] -= worldItems[chest][STRENGTH]
                            stats[2] -= worldItems[chest][DEFENCE]
                            stats[3] -= worldItems[chest][PERCEPTION]
                            stats[4] -= worldItems[chest][SPEED]
                            chest = item
                        else:
                            print('You don\'t equip ' + item)
                            return
                    else:
                        chest = item
                elif worldItems[item][EQUIPTYPE] == 'HANDS':
                    if hands != 0:
                        print('You can have only one of those equipped.')
                        yn = input('Do you want to switch your items? (y/n) ')
                        if yn == 'y':
                            inventory.append(hands)
                            equipped.remove(hands)
                            stats[1] -= worldItems[hands][STRENGTH]
                            stats[2] -= worldItems[hands][DEFENCE]
                            stats[3] -= worldItems[hands][PERCEPTION]
                            stats[4] -= worldItems[hands][SPEED]
                            hands = item
                        else:
                            print('You don\'t equip ' + item)
                            return
                    else:
                        hands = item
                elif worldItems[item][EQUIPTYPE] == 'LEGS':
                    if legs != 0:
                        print('You can have only one of those equipped.')
                        yn = input('Do you want to switch your items? (y/n) ')
                        if yn == 'y':
                            inventory.append(legs)
                            equipped.remove(legs)
                            stats[1] -= worldItems[legs][STRENGTH]
                            stats[2] -= worldItems[legs][DEFENCE]
                            stats[3] -= worldItems[legs][PERCEPTION]
                            stats[4] -= worldItems[legs][SPEED]
                            legs = item
                        else:
                            print('You don\'t equip ' + item)
                            return
                    else:
                        legs = item
                else:
                    if feet != 0:
                        print('You can have only one of those equipped.')
                        yn = input('Do you want to switch your items? (y/n) ')
                        if yn == 'y':
                            inventory.append(feet)
                            equipped.remove(feet)
                            stats[1] -= worldItems[feet][STRENGTH]
                            stats[2] -= worldItems[feet][DEFENCE]
                            stats[3] -= worldItems[feet][PERCEPTION]
                            stats[4] -= worldItems[feet][SPEED]
                            feet = item
                        else:
                            print('You don\'t equip ' + item)
                            return
                    else:
                        feet = item

                print('You equip %s' % (worldItems[item][SHORTDESC]))
                
                stats[1] += worldItems[item][STRENGTH]
                stats[2] += worldItems[item][DEFENCE]
                stats[3] += worldItems[item][PERCEPTION]
                stats[4] += worldItems[item][SPEED]
                equipped.append(item)
                inventory.remove(item)
                return

        if cantEquip:
            print('You cannot equip that.')
        else:
            print('You do not have "%s". Type "inventory" or "inv" to see your inventory.' % (itemToEquip))

    def complete_equip(self, text, line, begidx, endidx):
        itemToEquip = text.lower()
        possibleItems = []

        # if the user has only typed "equip" but no item name:
        if itemToEquip == '':
            return getAllFirstDescWords(inventory)

        # otherwise, get a list of all "description words" for EQUIPABLE inventory items matching the command text so far:
        for item in list(set(inventory)):
            for descWord in worldItems[item][DESCWORDS]:
                if descWord.startswith(text) and worldItems[item].get(EQUIPABLE, False):
                    possibleItems.append(descWord)

        return list(set(possibleItems)) # make list unique
    
    def do_equipped(self, arg):
        """Display a list of the items in your possession."""

        if len(equipped) == 0:
            print('Equipped:\n  (nothing)')
            return

        # first get a count of each distinct item in the equipped
        itemCount = {}
        for item in equipped:
            if item in itemCount.keys():
                itemCount[item] += 1
            else:
                itemCount[item] = 1

        # get a list of equipped items with duplicates removed:
        print('Equipped:')
        for item in set(equipped):
            if itemCount[item] > 1:
                print('  %s (%s)' % (item, itemCount[item]))
            else:
                print('  ' + item)

    def do_unequip(self, arg):
        """"unequip <item> - Drop an item from your equipped onto the ground."""
        global stats

        # put this value in a more suitably named variable
        itemToUnequip = arg.lower()

        # get a list of all "description words" for each item in the equipped
        invDescWords = getAllDescWords(equipped)

        # find out if the player doesn't have that item
        if itemToUnequip not in invDescWords:
            print('You do not have "%s" equipped.' % (itemToUnequip))
            return

        # get the item name that the player's command describes
        item = getFirstItemMatchingDesc(itemToUnequip, equipped)
        if item != None:
            print('You unequip %s.' % (worldItems[item][SHORTDESC]))
            if worldItems[item][EQUIPTYPE] == 'HEAD':
                self.head = 0
            elif worldItems[item][EQUIPTYPE] == 'CHEST':
                self.chest = 0
            elif worldItems[item][EQUIPTYPE] == 'HANDS':
                self.hands = 0
            elif worldItems[item][EQUIPTYPE] == 'LEGS':
                self.legs = 0
            else:
                self.feet = 0

            stats[1] -= worldItems[item][STRENGTH]
            stats[2] -= worldItems[item][DEFENCE]
            stats[3] -= worldItems[item][PERCEPTION]
            stats[4] -= worldItems[item][SPEED]
            inventory.append(item)
            equipped.remove(item) # remove from equipped

    def complete_unequip(self, text, line, begidx, endidx):
        possibleItems = []
        itemToUnequip = text.lower()

        # get a list of all "description words" for each item in the equipped
        invDescWords = getAllDescWords(equipped)

        for descWord in invDescWords:
            if line.startswith('unequip %s' % (descWord)):
                return [] # command is complete

        # if the user has only typed "unequip" but no item name:
        if itemToUnequip == '':
            return getAllFirstDescWords(equipped)

        # otherwise, get a list of all "description words" for equipped items matching the command text so far:
        for descWord in invDescWords:
            if descWord.startswith(text):
                possibleItems.append(descWord)

        return list(set(possibleItems)) # make list unique

    def do_keys(self, arg):
        """Display the amount of keys of the player"""
        print('Keys: ' + str(inventory.count('Key')))
    
    do_k = do_keys

    def do_sleep(self, arg):
        """This let's you save your progress, so if you die you return to this location"""
        if worldRooms[location].get(SAVE, False) == True:
            print('You lie down to sleep.')
            time.sleep(1)
            print('...')
            time.sleep(1)
            self.saveloc = location
            stats[0] = maxHealth
            print('You wake up feeling refreshed.')
            time.sleep(0.5)
            print('You\'ve saved your progress.')
        else:
            print('You can\'t sleep here.')
    
    do_save = do_sleep
    
    """
    def do_saveloc(self, arg):
        print(str(self.saveloc))
    """

    def do_jump(self, arg):
        """Type jump to jump."""
        print('You jumped!')

    """
    def do_map(self, arg):
        global location
        mapMiddle = location
        if worldRooms[location][NORTH] != True:
            location = worldRooms[location][WEST]
            if worldRooms[location][NORTH] != True:
                location = worldRooms[location][WEST]
        location = worldRooms[location][NORTH]
        location = worldRooms[location][NORTH]
        location = worldRooms[location][WEST]
        location = worldRooms[location][WEST]
        location = worldRooms[location][WEST]

        for i in range(1, 26):
            if i == 6:
                print(str(i) + ': ' + str(location))
    """

class RoomCreatures(arcade.Sprite):
    def update(self):
        pass

class RoomItems(arcade.Sprite):
    def update(self):
        pass

class ActionBox():

    def __init__(self, left, right, top, bottom, color):

        # Take the parameters of the init function above, and create instance variables out of them.
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self.color = color

    def draw(self):
        """ Draw the balls with the instance variables we have. """
        arcade.draw_lrtb_rectangle_filled(self.left, self.right, self.top, self.bottom, self.color)
        #arcade.draw_lrtb_rectangle_outline(self.left, self.right, self.top, self.bottom, arcade.color.GRAY)

class UI():
    def __init__(self):
        pass

    def setup(self):
        pass

    def draw(self):
        #arcade.start_render()

        arcade.draw_lrtb_rectangle_filled(0, WINDOW_WIDTH, (1/4)*WINDOW_HEIGHT, 0, arcade.color.BLACK)

        arcade.draw_lrtb_rectangle_filled(1200, WINDOW_WIDTH - 20, (1/4)*WINDOW_HEIGHT - 20, 20, arcade.color.DARK_GRAY)
        start_x = 1205
        start_y = (1/4)*WINDOW_HEIGHT - 20
        roomText = '\n'.join(textwrap.wrap(worldRooms[location][DESC], 650))
        arcade.draw_text(location +
                        '\n' + '=' * len(location) +
                        '\n' + roomText,
                        start_x, start_y, arcade.color.WHITE, 12, anchor_x="left", anchor_y="top")

    def update(self, delta_time):
        pass

class Visuals(arcade.Window):
    """ An Arcade game. """

    def __init__(self, width, height, title):
        """ Constructor. """
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, resizable=True, fullscreen=False)
        arcade.set_background_color(WINDOW_BACKGROUND_COLOR)
        self.adv = TextAdventureCmd()
        self.ui = UI()
        self.creature_list = arcade.SpriteList()
        self.creature_sprite = None
        self.item_list = arcade.SpriteList()
        self.item_sprite = None
        width, height = self.get_size()
        self.background = None

        self.ab = ActionBox(20, 100, 100, 20, arcade.color.GRAY)
        self.ab1 = ActionBox(800, 880, 100, 20, arcade.color.GRAY)
        self.ab2 = ActionBox(120, 200, 100, 20, arcade.color.GRAY)
        self.ab3 = ActionBox(220, 300, 100, 20, arcade.color.GRAY)

    def setup(self):
        pass

    def on_resize(self, width, height):
        """ This method is automatically called when the window is resized. """

        # Call the parent. Failing to do this will mess up the coordinates, and default to 0,0 at the center and the
        # edges being -1 to 1.
        super().on_resize(width, height)
        #print(f"Window resized to: {width}, {height}")

    def on_draw(self):
        global displayCreature
        global maxHealthbar
        """ Called whenever we need to draw the window. """
        if worldRooms[location].get(COLOR, False) != False:
            if worldRooms[location][COLOR] == 'RED':
                color = arcade.color.RED
            elif worldRooms[location][COLOR] == 'GREEN':
                color = arcade.color.GREEN
            elif worldRooms[location][COLOR] == 'YELLOW':
                color = arcade.color.YELLOW
            elif worldRooms[location][COLOR] == 'BLUE':
                color = arcade.color.BLUE
            elif worldRooms[location][COLOR] == 'MAGENTA':
                color = arcade.color.MAGENTA
            elif worldRooms[location][COLOR] == 'CYAN':
                color = arcade.color.CYAN
            elif worldRooms[location][COLOR] == 'GRAY':
                color = arcade.color.GRAY
            elif worldRooms[location][COLOR] == 'BEIGE':
                color = arcade.color.BEIGE
        else:
            color = arcade.color.WHITE

        if self.creature_list != worldRooms[location][CREATURES]:
            for x in self.creature_list:
                if len(self.creature_list) > 0:
                    self.creature_list.pop()
                continue
            for item in worldRooms[location][CREATURES]:
                self.creature_sprite = RoomCreatures("sprites/creatures/%s.png" % worldRooms[location][CREATURES][displayCreature])
                self.creature_sprite.center_x = (1/2)*WINDOW_WIDTH + (1/4)*WINDOW_WIDTH
                self.creature_sprite.center_y = (1/2)*WINDOW_HEIGHT
                self.creature_list.append(self.creature_sprite)

        if self.item_list != worldRooms[location][GROUND]:
            for x in self.item_list:
                if len(self.item_list) > 0:
                    self.item_list.pop()
                continue
            for item in worldRooms[location][GROUND]:
                self.item_sprite = RoomCreatures("sprites/items/ground/%s.png" % worldRooms[location][GROUND][0])
                self.item_sprite.center_x = (1/2)*WINDOW_WIDTH - (1/4)*WINDOW_WIDTH
                self.item_sprite.center_y = (1/2)*WINDOW_HEIGHT
                self.item_list.append(self.item_sprite)
 
        arcade.start_render()
        arcade.set_background_color(color)
        arcade.draw_xywh_rectangle_textured(0, WINDOW_HEIGHT-(1080-((1/4)*WINDOW_HEIGHT)), WINDOW_WIDTH, WINDOW_HEIGHT-((1/4)*WINDOW_HEIGHT), self.background)
        self.ui.draw()
        arcade.draw_lrtb_rectangle_outline(20, maxHealthbar, 180, 160, arcade.color.GREEN)
        arcade.draw_lrtb_rectangle_filled(20, self.healthbar, 180, 160, arcade.color.GREEN)
        self.ab.draw()
        start_x = 25
        start_y = 55
        arcade.draw_text("Attack", start_x, start_y, arcade.color.BLACK, 12)
        self.ab1.draw()
        self.ab2.draw()
        start_x = 125
        start_y = 55
        arcade.draw_text("Take", start_x, start_y, arcade.color.BLACK, 12)
        self.ab3.draw()
        start_x = 225
        start_y = 55
        arcade.draw_text("Look", start_x, start_y, arcade.color.BLACK, 12)
        if len(self.creature_list) > 1:
            self.creature_list[displayCreature].draw()
        else:
            self.creature_list.draw()
        self.item_list.draw()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W:
            self.adv.do_north('north')
        elif key == arcade.key.A:
            self.adv.do_west('west')
        elif key == arcade.key.S:
            self.adv.do_south('south')
        elif key == arcade.key.D:
            self.adv.do_east('east')
        elif key == arcade.key.Z:
            self.adv.do_down('down')
        elif key == arcade.key.X:
            self.adv.do_up('up')
        
        if key == arcade.key.F:
            # User hits f. Flip between full and not full screen.
            self.set_fullscreen(not self.fullscreen)

            # Get the window coordinates. Match viewport to window coordinates
            # so there is a one-to-one mapping.
            width, height = self.get_size()
            self.set_viewport(0, width, 0, height)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            if x > self.ab.left and x < self.ab.right and y < self.ab.top and y > self.ab.bottom:
                self.ab.color = arcade.color.DARK_GRAY                
            elif x > self.ab1.left and x < self.ab1.right and y < self.ab1.top and y > self.ab1.bottom:
                self.ab1.color = arcade.color.DARK_GRAY
            elif x > self.ab2.left and x < self.ab2.right and y < self.ab2.top and y > self.ab2.bottom:
                self.ab2.color = arcade.color.DARK_GRAY
            elif x > self.ab3.left and x < self.ab3.right and y < self.ab3.top and y > self.ab3.bottom:
                self.ab3.color = arcade.color.DARK_GRAY   

    def on_mouse_release(self, x, y, button, modifiers):
        global displayCreature
        """
        Called when a user releases a mouse button.
        """
        if button == arcade.MOUSE_BUTTON_LEFT:
            if x > self.ab.left and x < self.ab.right and y < self.ab.top and y > self.ab.bottom:
                self.ab.color = arcade.color.GRAY
                if len(worldRooms[location][CREATURES]) > 0:
                    for item in worldRooms[location][CREATURES]:
                        self.adv.do_attack(worldCreatures[item][DESCWORDS][0])
                        if displayCreature != 0:
                            displayCreature = 0
                else:
                    for x in self.creature_list:
                        if len(self.creature_list) > 0:
                            self.creature_list.pop()
            elif x > self.ab1.left and x < self.ab1.right and y < self.ab1.top and y > self.ab1.bottom:
                self.ab1.color = arcade.color.GRAY
                if displayCreature < len(worldRooms[location][CREATURES]) - 1:
                    displayCreature += 1
                else:
                    displayCreature = 0
            elif x > self.ab2.left and x < self.ab2.right and y < self.ab2.top and y > self.ab2.bottom:
                self.ab2.color = arcade.color.GRAY
                for item in worldRooms[location][GROUND]:
                        self.adv.do_take(worldItems[item][DESCWORDS][0])
            elif x > self.ab3.left and x < self.ab3.right and y < self.ab3.top and y > self.ab3.bottom:
                self.ab3.color = arcade.color.GRAY
                for item in worldRooms[location][GROUND]:
                    self.adv.do_look(worldItems[item][DESCWORDS][0])
                for item in worldRooms[location][CREATURES]:
                    self.adv.do_look(worldCreatures[item][DESCWORDS][0])

    def update(self, delta_time):
        global displayCreature
        """ Called to update our objects. Happens approximately 60 times per second. """
        self.healthbar = (stats[0]/maxHealth)*maxHealthbar

        """
        if len(worldRooms[location][CREATURES]) > 0:
            if len(worldRooms[location][CREATURES]) > 1:
                pass
            for item in worldRooms[location][CREATURES]:
                self.creature_sprite = RoomCreatures("sprites/creatures/%s.png" % worldRooms[location][CREATURES][0])
                self.creature_sprite.center_x = (1/2)*WINDOW_WIDTH + (1/4)*WINDOW_WIDTH
                self.creature_sprite.center_y = (1/2)*WINDOW_HEIGHT
                self.creature_list.append(self.creature_sprite)
        else:
            for x in self.creature_list:
                if len(self.creature_list) > 0:
                    self.creature_list.pop()
        """
        self.background = arcade.load_texture("sprites/rooms/%s.png" % worldRooms[location][SPRITE])

def bork():
    window = Visuals(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    window.setup()
    arcade.run()

if __name__ == '__main__':
    titleScreen()
    levelUp()
    equippedCheck()
    displayLocation(location)
    bork()    
    TextAdventureCmd().cmdloop()


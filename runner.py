#Future improvements:
    #Draw map
    #Add disadvantages based on affinity

from characters import Hero
from items import Item, Location

colors = {
    # Set colors for more readable user output
    'red':'\033[0;31m', #enemy
    'blue':'\033[0;34m', #direction
    'yellow':'\033[1;33m', #hero name
    'purple':'\033[0;35m', #item
    'orange':'\033[0;33m', #damage
    'reset':'\033[0m'
}

def user_continue():
    '''Pause output to improve readability for user'''
    proceed = "hold"
    while proceed != "":
        proceed = input("\nPress enter to continue.")
    return

def user_in(hero,location,in_combat,phrase="\nWhat would you like to do next?"):
    '''Prompt for user input, compare to available options, and perform relevant functions. Return value to loop or end game'''
    valid = False
    while not valid:
        entered = input(phrase).lower()
        split_entry = entered.split(" ",1) #Break off first word for categorization
        item_name = ""
        first_word = split_entry[0]
        if len(split_entry)>1:
            item_name = split_entry[1]
        item_name = item_name.replace("the ","") #Parse out likely extra input from user
        if "with" in item_name: #Look for keyword indicating weapon and strip keyword if found
            with_loc = item_name.find("with")
            item_name = item_name[with_loc+5:]
        elif first_word == "attack": #Prompt for weapon on attack if none specified
            item_name = input("What weapon would you like to attack with?").lower()
            item_name = item_name.replace("the ","")
        entries = {
            #firstword
                #"default" : (is always available, return value/result if available)
                #"combat" : (is allowed in combat, error message if combat status argument doesn't match)
                #"inventory" : (must be in inventory, error message if not in inventory)
                #"location" : (is dependent upon location, error message if not available in location)
                #"help_text" : "explanation given for command by 'help' command"
                #"result" : function to call if validation passes
            "use": {
                "default" : (False,""),
                "combat" : (False,"You can't use items during combat. If you want to attack with a weapon, enter 'attack' or 'attack with [weapon name]'."),
                "inventory" : (True,f"There is no {item_name} in your inventory."),
                "location" : (False,""),
                "help_text" : "Type 'Use [item]' with the name of a consumable item in your inventory to use that item.",
                "result" : hero.use
            },
            "equip": {
                "default" : (False,""),
                "combat" : (False,"You can't equip items during combat. If you want to attack with a weapon, enter 'attack' or 'attack with [weapon name]'."),
                "inventory" : (True,f"There is no {item_name} in your inventory."),
                "location" : (False,""),
                "help_text" : "Type 'Equip [item]' with the name of a shield, piece of armor, or article of clothing in your inventory to equip that item.",
                "result" : hero.equip
            },
            "unequip": {
                "default" : (False,""),
                "combat" : (False,"You can't unequip items during combat. If you want to attack with a new weapon, enter 'attack' or 'attack with [weapon name]'."),
                "inventory" : (True,f"There is no {item_name} in your inventory."),
                "location" : (False,""),
                "help_text" : "Type 'Unequip [item]' with the name of a shield, piece of armor, or article of clothing you currently have equipped to unequip it (making room to equip something else).",
                "result" : hero.unequip
            },
            "attack": {
                "default" : (False,""),
                "combat" : (True,""),
                "inventory" : (True,f"There is no {item_name} in your inventory."),
                "location" : (True,"There is nothing to attack in this area."),
                "help_text" : "Type 'Attack,' 'Attack [enemy]', or 'Attack with [weapon]' to attack an enemy in your area with a selected weapon in your inventory.",
                "result" : hero.attack
            },
            "run": {
                "default" : (False,""),
                "combat" : (True,"You can't run away if you're not in combat. To leave the area, enter 'go [direction]' for the direction you want to go next."),
                "inventory" : (False,""),
                "location" : (False,""),
                "help_text" : "Type 'Run' or 'Run Away' to escape from an enemy during battle. You'll flee to another area in a randomly selected direction.",
                "result" : hero.run
            },
            "go": {
                "default" : (False,""),
                "combat" : (False,"You can't walk out in the middle of combat. If you want to run away from the enemy, enter 'run' or 'run away'."),
                "inventory" : (False,""),
                "location" : (True,"There isn't an exit in that direction."),
                "help_text" : "Type 'Go North,' 'Go East,' 'Go South,' or 'Go West' to move into a new area in the indicated direction. You can only move in directions that have available exits from your current location.",
                "result" : None #defined later to allow use of 'item name'
            },
            "loot": {
                "default" : (False,""),
                "combat" : (False,"You can't loot in the middle of combat."),
                "inventory" : (False,""),
                "location" : (True,"If there was loot here, you got it already."),
                "help_text" : "Type 'Loot' in an area with an enemy you have killed to loot the body of the enemy and gain any items it was carrying.",
                "result" : hero.loot
            },
            "inventory": {
                "default" : (True,hero.print_inventory()),
                "combat" : (True,""),
                "help_text" : "Type 'Inventory' at any time to view the full contents of your inventory."
            },
            "help": {
                "default" : (True,""),
                "combat" : (True,""),
                "help_text" : "Type 'Help' at any time to view the list of commands available to you and what they do."
            },
            "character": {
                "default" : (True,hero),
                "combat" : (True,""),
                "help_text" : "Type 'Character' at any time to view all of your character's information."
            },
            "quit": {
                "default" : (True,('quit',False)),
                "combat" : (True,""),
                "help_text" : "Type 'Quit' at any time to exit the game. Your progress will NOT be saved!"
            }
        }
        entry = entries.get(first_word,False)
        item = False
        if item_name != "": #check if item is in hero inventory
            for owned_item in hero.inventory:
                if owned_item.name.lower() == item_name:
                    item = owned_item
        if not entry:
            #If no match is found to first word, prompt for input again
            print("I'm not sure what you're trying to do.")
            continue
        elif entry["default"][0]:
            #First handle commands that are always available to the user
            if first_word == "help":
                #Print help_text for all allowable commands in current situation
                print(f"\nHere are the commands available to you right now: \n")
                for word,info in entries.items():
                    if (info["combat"][0] and in_combat) or (not info["combat"][0] or word in location.options):
                        cap_word = word.capitalize()
                        print(f"{cap_word:9} : {info['help_text']}\n")
            elif first_word == "quit":
                #Double-check intention and pass value to exit runner loop
                valid = False
                while not valid:
                    yn = input("Are you sure you'd like to quit? Your game will not be saved.").lower()
                    if yn != "y" and yn != "n":
                        print("Your only valid options right now are 'y' and 'n'. If you want to do something else, please enter 'n' and then enter what you would like to do.")
                        continue
                    elif yn == "y":
                        return entry["default"][1]
                    elif yn == "n":
                        break
                return
            else:
                #Handle standard defaults
                print(entry["default"][1])
            continue
        #Run through disallowed entry types: print error message and re-prompt for entry
        elif in_combat != entry["combat"][0] and first_word != "attack":
            print(entry["combat"][1])
            continue
        elif (entry["location"][0] and first_word not in location.options) or (first_word == "go" and ("go "+item_name) not in location.options):
            print(entry["location"][1])
            continue
        elif entry["inventory"][0] and not item:
            print(entry["inventory"][1])
            continue
        #Perform result function for correct, allowable entry types
        elif first_word == "go":
            result = location.connected_locations[item_name].enter(hero)
            return result
        elif first_word in ["use","equip","unequip"]:
            entry["result"](item)
            continue
        elif first_word in ["run","loot"]:
            result = entry["result"](location)
            return result
        elif first_word == "attack":
            result = entry["result"](item,location.enemies,location,in_combat)
            return result
        else:
            result = entry["result"]()
            return result
        
#Run starting game
print("\n\nWelcome to the\n\n\
     xXXXx  X         X XXXXXXX XXXx  XXXx  X     X X    X\n\
    X     X  X       X  X       X   X X   X X     X XX   X\n\
    X     X   X     X   X       X   X X   X X     X X X  X\n\
    X     X    X   X    XXXX    XXX^  XXX^  X     X X  X X\n\
    X     X     X X     X       X  X  X  X  X     X X   XX\n\
     ^XXX^       X      XXXXXXX X   X X   X  ^XXX^  X    X\n\
    \n\
     xXXXx  X     X XXXx  X       XXXXX XXXXXXX XXXXXXX XXXXXXX XXXXXXX\n\
    X     X X     X X   X X         X   X          X       X    X\n\
    X     X X     X X X^  X         X   X          X       X    X\n\
    X     X X     X X Xx  X         X   XXXX       X       X    XXXX\n\
    X     X X     X X   X X         X   X          X       X    X\n\
     ^XXX^   ^XXX^  XXX^  XXXXXXX XXXXX XXXXXXX    X       X    XXXXXXX\n\
    \n")
user_continue()
hero_name = input("\nWhat would you like your hero's name to be?")
hero = Hero(hero_name)
print(f"\nWelcome, {colors['yellow']}{hero.name}{colors['reset']}, to the Overrun Oubliette!\
    \n\nIn this text adventure, you'll fight monsters, gain mythical items, and become a powerful warrior.\
    \n\nThe exact commands available to you at any time will depend on what you're doing, but common ones will include 'go [direction]', 'attack', 'loot', 'equip', and 'use'. Once your adventure begins, type 'help' at any time to see all commands available to you at that moment, with detailed explanations of what they do.")
user_continue()
hero.inventory.append(Item("Rusty Sword","weapon",None,1,0,0,0," a"))
print(hero)
user_continue()
print(f"You've always dreamed of adventure, but the closest you've come is the dead-end job you finally landed mucking out the palace stables. \
One day, as you're raking in the stable yard, you overhear some nobles gossiping about the old dungeons under the forest behind the palace. \
Apparently, it's become overrun with {colors['red']}monsters{colors['reset']} and {colors['red']}evil forces{colors['reset']}. Your ears perk up -- this could be your chance!\
\n\nYou don't bother finishing your day's work; you drop your rake and grab your prize posession: the {colors['purple']}rusty sword{colors['reset']} your mother passed down to you. Adventure awaits.\
\n\nAs you draw near the entrance to the old dungeons, the air grows cold, and you smell a foul, rotting odor drifing out of the tunnels. You take a deep breath, steel your nerves, and plunge in.")
starting_location = Location(hero,"south",True)
start_res = starting_location.enter(hero,True)

res = user_in(hero,start_res[0],start_res[1])
playing = True

while playing:
    #Loop user input until user quits
    if res[0] == 'quit':
        break
    res = user_in(hero,res[0],res[1])

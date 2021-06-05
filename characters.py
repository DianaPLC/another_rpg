from random import randint, choice
from math import log, ceil
from functools import reduce
#from runner import user_in

class Character:
    '''Define an overarching class containing methods used by hero and enemy characters'''

    def __init__(self,name):
        self.name = name
    
    def __repr__(self):
        return f"a character named {self.name}"
    
    colors = {
        # Set colors for more readable output
        'red':'\033[0;31m', #enemy
        'blue':'\033[0;34m', #direction
        'yellow':'\033[1;33m', #hero name
        'purple':'\033[0;35m', #item
        'orange':'\033[0;33m', #damage
        'reset':'\033[0m'
    }

    @staticmethod
    def roll(max):
        '''Simulate rolling [max] 4-sided dice'''
        result = 0
        c = 0
        while c < max:
            result += randint(1,4)
            c += 1
        return result


class Hero(Character):
    '''Define extra attributes of user-controlled characters and methods to manage its levels'''
    
    foci = {
        # Define stat increase rates based on user-selected character focus
        "Earth" : {
            "health": 2,
            "strength": 2,
            "defense": 3,
            "speed": 1
        },
        "Wind" : {
            "health": 2,
            "strength": 1,
            "defense": 2,
            "speed": 3
        },
        "Water" : {
            "health": 3,
            "strength": 2,
            "defense": 1,
            "speed": 2
        },
        "Fire" : {
            "health": 1,
            "strength": 3,
            "defense": 2,
            "speed": 2
        }
    }

    def __init__(self,name):
        self.name = name
        self.affinity = None #To be selected by user at level 1
        self.max_health = 10 #Will increase by level
        self.health = 10
        self.strength = 1
        self.defense = 1
        self.speed = 1
        self.level = 0
        self.experience = 0
        self.inventory = []
    
    def __repr__(self):
        return f"Hero name: {self.name} | Focus: {self.affinity} | Level: {self.level}\
            \nMax Health: {self.max_health} | Current Health: {self.health}\
            \nStrength: {self.strength} | Defense: {self.defense} | Speed: {self.speed}\
            \nInventory: {self.inventory}"

    def __str__(self):
        result = f"\nYou are the hero {self.colors['yellow']}{self.name}{self.colors['reset']}"
        if self.affinity != None:
            focus_str = f", focusing your training on {self.affinity} at level {self.level}."
        else:
            focus_str = ", and you have not yet found your focus."
        result += focus_str + f"\nYou have {self.experience} experience, and will next level up at {5**(self.level+1)} experience.\
            \n ____________ ________________ __________ _________ ______ \
            \n|{'Max Health': ^12}|{'Current Health': ^16}|{'Strength': ^10}|{'Defense': ^9}|{'Speed': ^6}|\
            \n ------------ ---------------- ---------- --------- ------ \
            \n|{self.max_health: ^12}|{self.health: ^16}|{self.strength: ^10}|{self.defense: ^9}|{self.speed: ^6}|\
            \n ‾‾‾‾‾‾‾‾‾‾‾‾ ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾ ‾‾‾‾‾‾‾‾‾‾ ‾‾‾‾‾‾‾‾‾ ‾‾‾‾‾‾ \
            \n\nIn your inventory, you have:\
            \n ________________________________ ____________ _____ _____ _____ _________ __________ \
            \n|{'Item': ^32}|{'Type': ^12}|{'DMG': ^5}|{'DEF': ^5}|{'SPD': ^5}|{'Healing': ^9}|{'Equipped': ^10}|\
            \n -------------------------------- ------------ ----- ----- ----- --------- ---------- "
        for item in self.inventory:
            eq_str = ""
            if item.equipped:
                eq_str = "Yes"
            result += f"\n|{self.colors['purple']}{item.name: ^32}{self.colors['reset']}|{item.category: ^12}|{item.damage: ^5}|{item.defense: ^5}|{item.speed: ^5}|{item.healing: ^9}|{eq_str: ^10}|"
        result += f"\n‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾ ‾‾‾‾‾‾‾‾‾‾‾‾ ‾‾‾‾‾ ‾‾‾‾‾ ‾‾‾‾‾ ‾‾‾‾‾‾‾‾‾ ‾‾‾‾‾‾‾‾‾‾ "
        return result

    def print_inventory(self):
        '''Print just the hero inventory in a readable table'''
        result = f"\nIn your inventory, you have:\
            \n ________________________________ ____________ _____ _____ _____ _________ __________ \
            \n|{'Item': ^32}|{'Type': ^12}|{'DMG': ^5}|{'DEF': ^5}|{'SPD': ^5}|{'Healing': ^9}|{'Equipped': ^10}|\
            \n -------------------------------- ------------ ----- ----- ----- --------- ---------- "
        for item in self.inventory:
            eq_str = ""
            if item.equipped:
                eq_str = "Yes"
            result += f"\n|{self.colors['purple']}{item.name: ^32}{self.colors['reset']}|{item.category: ^12}|{item.damage: ^5}|{item.defense: ^5}|{item.speed: ^5}|{item.healing: ^9}|{eq_str: ^10}|"
        result += f"\n‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾ ‾‾‾‾‾‾‾‾‾‾‾‾ ‾‾‾‾‾ ‾‾‾‾‾ ‾‾‾‾‾ ‾‾‾‾‾‾‾‾‾ ‾‾‾‾‾‾‾‾‾‾ "
        return result
    
    def level_up(self):
        '''Check if hero has sufficient xp to level up, and increase character stats based on selected affinity if so'''
        if log(self.experience,5) >= self.level + 1:
            self.level += 1
            if self.level == 1:
                # Prompt user to select a focus on reaching level 1
                print("\nCongratulations! You're now a level 1 adventurer. It's time to pick your focus.")
                proceed = "hold"
                while proceed != "": #Pause output for ease of user comprehension
                    proceed = input("\nPress enter to continue.")
                print("The focus you select will impact how quickly you progress in your various abilities, and will also give you an affinity for certain weapons and items.\
There are four areas of focus available to you:\
\n\nEarth: A focus in the Earth domain will allow you to reach extraordinary levels of defensive skills, but it will slow you down.\
\nWind: A focus in Wind arts will grant you increasingly superhuman speed, but will weaken your attacks.\
\nWater: A focus in the study of Water will give you boundless health and vitality, but will leave you largely undefended.\
\nFire: A focus in the Fire arcana will allow you to become legendarily strong in combat, but will take a toll on your health.")
                valid = False
                while not valid:
                    selected_affinity = input("\nWhat element will you focus your training on?").capitalize()
                    if selected_affinity not in ["Earth","Wind","Water","Fire"]:
                        print("Please enter 'Earth', 'Wind', 'Water', or 'Fire'.")
                        continue
                    else:
                        self.affinity = selected_affinity
                        valid = True
                for item in self.inventory:
                    # Grant item bonuses upon focus selection if user has already equipped items of the correct affinity
                    if item.affinity == self.affinity and item.equipped:
                        bonus = 0.25
                        self.speed += ceil(item.speed * bonus)
                        self.defense += ceil(item.defense * bonus)
                        self.strength += ceil(item.damage * bonus)
            self.max_health += self.foci[self.affinity]["health"]*2
            self.health = self.max_health
            self.strength += self.foci[self.affinity]["strength"]
            self.defense += self.foci[self.affinity]["defense"]
            self.speed += self.foci[self.affinity]["speed"]
            print(f"\nYou leveled up to level {self.level}! New stats:\
                \nMax Health: {self.max_health} | Current Health: {self.health}\
                \nStrength: {self.strength} | Defense: {self.defense} | Speed: {self.speed}")
    
    def loot(self,location):
        '''Transfer all items in an enemy inventory to the hero inventory'''
        enemy = location.enemies
        loot = enemy.inventory
        if len(loot) == 0:
            print(f"\nYou examine the body, but don't find anything.")
        else:
            for item in loot:
                for owned_item in self.inventory:
                    if owned_item.name == item.name and item.category != "consumable":
                        # Prevent name duplication of non-consumable items
                        self.inventory.remove(owned_item)
                        print(f"You found a better version of the {self.colors['purple']}{item.name}{self.colors['reset']}! You replace the old model in your inventory with the newer, shinier one.")
                self.inventory.append(item)
                print(f"You gained{item.article} {self.colors['purple']}{item.name}{self.colors['reset']}!")
        location.options.remove("loot")
        return(location,False)
    
    def run(self,location):
        '''Terminate combat encounter and send hero in a randomly selected direction from current location'''
        direction = choice(location.exits)
        print(f"\nYou flee to the {self.colors['blue']}{direction}{self.colors['reset']} and live to fight another day.")
        new_location = location.connected_locations[direction]
        result = new_location.enter(self)
        return result
    
    def equip(self,equipment):
        '''Check that an item can be equipped, and perform attribute adjustments to equip it'''
        if equipment.category == "weapon":
            print("\nYou don't need to equip weapons; you can select any weapon in your inventory for each attack.")
            return
        elif equipment.category == "consumable":
            print(f"\nYou can't equip the {self.colors['purple']}{equipment.name}{self.colors['reset']}, but you can use it.")
            self.yn_user_in(f"Would you like to use the {self.colors['purple']}{equipment.name}{self.colors['reset']}?",self.use,equipment)
            return
        for item in self.inventory:
            if item.category == equipment.category and item.equipped == True:
                print(f"\nYou already have the {self.colors['purple']}{item.name}{self.colors['reset']} equipped; you can't equip the {self.colors['purple']}{equipment.name}{self.colors['reset']} at the same time.")
                y = self.yn_user_in(f"Would you like to unequip your {self.colors['purple']}{item.name}{self.colors['reset']}?",self.unequip,item)
                if y:
                    self.yn_user_in(f"\nWould you like to equip the {self.colors['purple']}{equipment.name}{self.colors['reset']}?",self.equip,equipment)
                return
        bonus = 1
        if equipment.affinity == self.affinity:
            bonus = 1.25
        self.speed += ceil(item.speed * bonus)
        self.defense += ceil(item.defense * bonus)
        self.strength += ceil(item.damage * bonus)
        equipment.equipped = True
        result_str = f"\nYou have equipped the {self.colors['purple']}{equipment.name}{self.colors['reset']}!"
        attr_list = {"damage dealt":equipment.damage,"defense":equipment.defense,"speed":equipment.speed}
        for phrase,value in attr_list.items():
            if value > 0:
                result_str += f" This increases your {phrase} by {ceil(value * bonus)}."
        print(result_str)
    
    def unequip(self,equipment):
        '''Check that the equipment is currently equipped, and adjust attributes to unequip if so'''
        if not equipment.equipped:
            print(f"\nYou do not have the {self.colors['purple']}{equipment.name}{self.colors['reset']} equipped.")
            return
        bonus = 1
        if equipment.affinity == self.affinity:
            bonus = 1.25
        self.speed -= ceil(equipment.speed * bonus)
        self.defense -= ceil(equipment.defense * bonus)
        self.strength -= ceil(equipment.damage * bonus)
        equipment.equipped = False
        result_str = f"\nYou have unequipped the {self.colors['purple']}{equipment.name}{self.colors['reset']}."
        attr_list = {"damage dealt":equipment.damage,"defense":equipment.defense,"speed":equipment.speed}
        for phrase,value in attr_list.items():
            if value > 0:
                result_str += f" This decreases your {phrase} by {ceil(value * bonus)}."
        print(result_str)
    
    def use(self,item):
        '''Apply effects of consumable items'''
        if item.category == "weapon":
            print(f"\nYou can't use weapons ouside of attacks. To attack with this weapon, enter 'Attack with {item.name}'")
        elif item.category != "consumable":
            print(f"\nYou can't use {self.colors['purple']}{item.name}{self.colors['reset']}, but you can equip it.")
            self.yn_user_in(f"Would you like ot equip the {self.colors['purple']}{item.name}{self.colors['reset']}?",self.equip,item)
        else:
            bonus = 1
            if item.affinity == self.affinity:
                bonus = 1.1
            self.health = ceil(min(self.health + item.healing,self.max_health) * bonus)
            self.speed += ceil(item.speed * bonus)
            self.defense += ceil(item.defense * bonus)
            self.strength += ceil(item.damage * bonus)
            print(f"\nYou have consumed the {self.colors['purple']}{item.name}{self.colors['reset']}! Current stats:\
                \nMax Health: {self.max_health} | Current Health: {self.health}\
                \nStrength: {self.strength} | Defense: {self.defense} | Speed: {self.speed}")
            self.inventory.remove(item)
    
    def attack(self,weapon,opponent,location,in_combat):
        '''
        If starting a combat, determine first attacker based on speed.
        Calculate hero damage based on stats and weapon and apply damage to enemy based on enemy stats.
        If attack reduces enemy health to zero or below, "kill" enemy and end combat.
        '''

        if not in_combat:
            hero_speed = self.roll(self.speed + 1)
            opponent_speed = self.roll(opponent.speed)
            if hero_speed >= opponent_speed:
                print(f"\nYou rush toward {self.colors['red']}{opponent.name}{self.colors['reset']} and land the first blow.")
            else:
                print(f"\nYou turn to attack the {self.colors['red']}{opponent.name}{self.colors['reset']}, but the {self.colors['red']}{opponent.name}{self.colors['reset']} is too quick!")
                result = opponent.attack(self,location,True)
                return result
        print(f"\nYou strike the {self.colors['red']}{opponent.name}{self.colors['reset']} with your {self.colors['purple']}{weapon.name}{self.colors['reset']}.")
        weapon_damage = weapon.damage
        if weapon.affinity == self.affinity: #increase damage if hero uses weapon matching focus
            weapon_damage *= 1.25
        power = self.roll(self.strength) + weapon_damage
        #print(power) for debugging
        dmg_dealt = round(max(0,power - (self.roll(opponent.defense)/2)))
        opponent.health -= dmg_dealt
        if dmg_dealt > 0:
            print(f"{self.colors['orange']}{dmg_dealt}{self.colors['reset']} damage goes through to the {self.colors['red']}{opponent.name}{self.colors['reset']}.")
        else:
            print(f"The {self.colors['red']}{opponent.name}{self.colors['reset']} blocks your attack.")
        if opponent.health <= 0:
            print(f"\nYou defeated the {self.colors['red']}{opponent.name}{self.colors['reset']}! It falls to the ground, dead.")
            #end combat
            location.options.remove("attack")
            location.options.remove(f"attack {opponent.name}")
            #allow looting
            location.options.append("loot")
            #add experience points
            self.experience += (opponent.strength + opponent.defense + opponent.speed)
            self.level_up()
            return (location,False)
        else:
            result = opponent.attack(self,location,True)
            return result
    
    def yn_user_in(self,phrase,func,param):
        '''Prompt and validate user input for a y/n prompt'''
        valid = False
        while not valid:
            entered = input(phrase).lower()
            if entered == "help":
                print("You can enter 'y' to perform this action or 'n' to not perform it and do something else.")
                continue
            elif entered != "y" and entered != "n":
                print("Your only valid options right now are 'y' and 'n'. If you want to do something else, please enter 'n' and then enter what you would like to do.")
                continue
            elif entered == "y":
                func(param)
                return True
            elif entered == "n":
                return False

class Opponent(Character):
    '''define opponent-spefic attributes, allowing direct input of stats'''
    
    def __init__(self,name,affinity,health,strength,defense,speed,inventory):
        self.name = name
        self.affinity = affinity
        self.health = health
        self.strength = strength
        self.defense = defense
        self.speed = speed
        self.inventory = inventory
        self.weapon = None
    
    def __repr__(self):
        return f"Enemy {self.name} has:\
            \nHealth: {self.health} | Strength: {self.strength}\
            \nDefense: {self.defense} | Speed: {self.speed}\
            \nInventory: {self.inventory}"

    def __str__(self):
        if len(self.inventory) > 0:
            loot_str = "It looks like it has some good gear."
        else:
            loot_str = "It doesn't appear to be carrying anything."
        return f"{self.name} looks dangerous. {loot_str}"
    
    def equip(self,item):
        '''Eliminate printed responses to equip attempts and apply item stats directly to enemy stats'''
        self.inventory.append(item)
        if item.category == "weapon":
            self.weapon = item
        elif item.category != "consumable":
            bonus = 1
            if item.affinity == self.affinity:
                bonus = 1.25
            self.speed += ceil(item.speed * bonus)
            self.defense += ceil(item.defense * bonus)

    def attack(self,hero,location,in_combat):
        '''
        If starting a combat, determine first attacker based on speed.
        Calculate enemy damage based on stats and weapon and apply damage to hero based on hero stats.
        If attack reduces hero health to zero or below end game.
        '''
        
        if not in_combat:
            self_speed = self.roll(self.speed + 1)
            hero_speed = self.roll(hero.speed)
            if self_speed >= hero_speed:
                print(f"\nThe {self.colors['red']}{self.name}{self.colors['reset']} rushes toward you and lands the first blow.")
            else:
                print(f"\n{self.colors['red']}{self.name}{self.colors['reset']} turns to attack you, but you're too quick!")
                return (location,True)
        if self.weapon != None: #if the enemy holds a weapon increase damage
            weapon_damage = self.weapon.damage
            if self.weapon.affinity == self.affinity: #grant enemy an attack bonus for matching weapon affinity
                weapon_damage *= 1.25
            weapon_name = f"{self.colors['purple']}{self.weapon.name}{self.colors['reset']}"
        else:
            weapon_damage = 0
            weapon_name = "bare hands"
        print(f"\nThe {self.colors['red']}{self.name}{self.colors['reset']} attacks you with its {weapon_name}!")
        power = self.roll(self.strength) + weapon_damage
        # print(power) for debugging
        dmg_dealt = round(max(0,power - ceil(self.roll(hero.defense)/1.5)))
        hero.health -= dmg_dealt
        if dmg_dealt > 0:
            print(f"{self.colors['orange']}{dmg_dealt}{self.colors['reset']} damage goes through to you. You're at {hero.health} health.")
        else:
            print(f"You block the {self.colors['red']}{self.name}'s{self.colors['reset']} attack.")
        if hero.health <= 0:
            print(f"\n{self.colors['yellow']}{hero.name}{self.colors['reset']} died in glorious battle.\n\
                 xXXXx       X      X       X XXXXXXX       xXXXx  X         X XXXXXXX XXXx\n\
                X     X     X X     XX     XX X            X     X  X       X  X       X   X\n\
                X          X   X    X X   X X X            X     X   X     X   X       X   X\n\
                X    XXX  XXXXXXX   X  X X  X XXXX         X     X    X   X    XXXX    XXX^\n\
                X     X  X       X  X   X   X X            X     X     X X     X       X  X\n\
                 ^XXX^  X         X X       X XXXXXXX       ^XXX^       X      XXXXXXX X   X\n\
                ")
            quit()
        else:
            return (location,True)
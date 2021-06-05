from random import randint, choice
from characters import Opponent

class Item:
    '''Holder for the attributes of an item that may affect characters, and definition of usage methods'''

    def __init__(self,name,category,affinity,damage,defense,speed,healing,article):
        self.name = name
        self.category = category #weapon, armor, sheild, boots, cloak, consumable
        self.affinity = affinity
        self.damage = damage
        self.defense = defense
        self.speed = speed
        self.healing = healing
        self.equipped = False
        self.article = article

    def __repr__(self):
        return f"Name: {self.name}\
        \nCategory: {self.category}\
        \nDamage: {self.damage}\
        \nDefense: {self.defense}\
        \nSpeed: {self.speed}\
        \nHealing: {self.healing}\
        \nEquipped: {self.equipped}"

    def __str__(self):
        result = f"The {self.name} is a {self.category}."
        if self.equipped:
            result += " It is equipped."
        else:
            result += " It is not equipped."
        if self.category == "weapon":
            result += f" When used to attack, it increases your damage dealt by {self.damage}."
        attr_list = {"increases your damage dealt":self.damage,"increases your defense":self.defense,"increases your speed":self.speed,"heals you":self.healing}
        for phrase,value in attr_list.items():
            result += f" It {phrase} by {value}."
        return result

class Location:
    '''Holder for objects and characters in an area; defines scope of user actions available. Attributes are randomly generated.'''

    colors = {
        # Set colors for more readable user output
        'red':'\033[0;31m', #enemy
        'blue':'\033[0;34m', #direction
        'yellow':'\033[1;33m', #hero name
        'purple':'\033[0;35m', #item
        'orange':'\033[0;33m', #damage
        'reset':'\033[0m'
    }

    directions = ["north","south","east","west"]
    
    direction_reverse = {
        #lookup reverse of each direction for setting entrance
        "north":"south",
        "south":"north",
        "east":"west",
        "west":"east"
    }

    category_effects = {
        #set default stat bonus types for items
        "weapon": "damage",
        "armor": "defense",
        "shield": "defense",
        "boots": "speed",
        "cloak": None,
        "consumable": "healing"
    }

    enemy_options = {
        #set potential enemy names and affinities
        "Fire Demon": "Fire",
        "Rock Giant": "Earth",
        "Tempest Mage": "Wind",
        "Water Nymph": "Water",
        "Dwarf Dragon": "Fire",
        "Earth Elemental": "Earth",
        "Galeforce Roc": "Wind",
        "Aquarian Berzerker": "Water",
        "Rogue Pyromancer": "Fire",
        "Quake Beast": "Earth",
        "Dervish Spirit": "Wind",
        "Triton Assassin": "Water",
        "Magma Golem": "Fire",
        "Avalanche Ogre": "Earth",
        "Hurricane Fiend": "Wind",
        "Riptide Wraith": "Water"
    }
    items = {
        #name: (category,affinity,secondary,article)
        "Flaming Broadsword": ("weapon","Fire",None," a"),
        "Inferno Grenades": ("weapon","Fire",None,""),
        "Flamethrower": ("weapon","Fire",None," a"),
        "Blazing Breastplate": ("armor","Fire",None," a"),
        "Armor of the Sun": ("armor","Fire",None,""),
        "Fire Aura": ("armor","Fire","speed"," a"),
        "Sun Shield": ("shield","Fire",None," a"),
        "Blinding Buckler": ("shield","Fire","damage"," a"),
        "Radiant Deflector": ("shield","Fire",None," a"),
        "Sunstep Boots": ("boots","Fire",None,""),
        "Fire Imp Shoes": ("boots","Fire",None,""),
        "Magma Boots": ("boots","Fire","defense",""),
        "Inferno Cape": ("cloak","Fire","damage"," an"),
        "Flame Hood": ("cloak","Fire","defense"," a"),
        "Comet Cloak": ("cloak","Fire","speed"," a"),
        "Burning Vitality": ("consumable","Fire","defense",""),
        "Lava Flask": ("consumable","Fire",None," a"),
        "Firewhisky": ("consumable","Fire",None,""), #end fire items
        "Shoulder-Mounted Catapault": ("weapon","Earth",None," a"),
        "Sandblaster": ("weapon","Earth",None," a"),
        "Meteor Rapier": ("weapon","Earth",None," a"),
        "Rock Plating": ("armor","Earth",None,""),
        "Mercurial Helm": ("armor","Earth","speed"," a"),
        "Granite Breastplate": ("armor","Earth",None," a"),
        "Crystal Shard Buckler": ("shield","Earth","damage"," a"),
        "Shale Shield": ("shield","Earth",None," a"),
        "Moving Earth Defense": ("shield","Earth",None," a"),
        "Earthquake Boots": ("boots","Earth","damage",""),
        "Rockstrider Shoes": ("boots","Earth",None,""),
        "Rock Climbers": ("boots","Earth",None,""),
        "Avalanche Cloak": ("cloak","Earth","damage"," an"),
        "Robe of Iron": ("cloak","Earth","defense"," a"),
        "Quicksand Cowl": ("cloak","Earth","speed"," a"),
        "Stone Brew": ("consumable","Earth",None," a"),
        "Mountain Elixer": ("consumable","Earth","speed"," a"),
        "Mudder's Milk": ("consumable","Earth",None,""), #end earth items
        "Gale Sword": ("weapon","Wind",None," a"),
        "Personal Tornado": ("weapon","Wind",None," a"),
        "Griffon Feather Scythe": ("weapon","Wind",None," a"),
        "Wearable Force Field": ("armor","Wind","strength"," a"),
        "Cloud Helm": ("armor","Wind",None," a"),
        "Aerosteel Armor": ("armor","Wind",None,""),
        "Buffetting Buckler": ("shield","Wind","strength"," a"),
        "Airwall": ("shield","Wind",None," an"),
        "Hurricane Eye Defense": ("shield","Wind",None," a"),
        "Wind-dodge Sandals": ("boots","Wind","defense",""),
        "Winged Boots": ("boots","Wind",None,""),
        "Airtreader Shoes": ("boots","Wind",None,""),
        "Storm Cape": ("cloak","Wind","damage"," a"),
        "Cloak of Clouds": ("cloak","Wind","defense"," a"),
        "Wearable Wings": ("cloak","Wind","speed",""),
        "Flask of Shifting Winds": ("consumable","Wind","defense"," a"),
        "Bottled Atmosphere": ("consumable","Wind",None,""),
        "Foaming Cordial": ("consumable","Wind",None," a"), #end wind items
        "Ice Shard Bombs": ("weapon","Water",None,""),
        "Water Whip": ("weapon","Water",None," a"),
        "Ice-9 Trident": ("weapon","Water",None," an"),
        "Waterfall Mail": ("armor","Water","speed",""),
        "Hydrogel Plating": ("armor","Water",None,""),
        "Poseidon's Helm": ("armor","Water",None,""),
        "Tidal Wave Defense": ("shield","Water","damage"," a"),
        "Glacier Shield": ("shield","Water",None," a"),
        "Water Wall": ("shield","Water",None," a"),
        "Whirlpool Walkers": ("boots","Water","defense",""),
        "Jetski Boots": ("boots","Water",None,""),
        "Boat Shoes": ("boots","Water",None,""),
        "Kraken Cape": ("cloak","Water","damage"," a"),
        "Ice Cloak": ("cloak","Water","defense"," a"),
        "Wave Hood": ("cloak","Water","speed"," a"),
        "Dam Fine Drink": ("consumable","Water","defense"," a"),
        "Dipper of the Fountain of Youth": ("consumable","Water",None," a"),
        "Aquavitae": ("consumable","Water",None,""), #end Water items
    }
    descriptions = {
        #standard descriptions of locations based on number of entrances
        1: [
            "You've hit a dead-end.",
            "You come into a small, dusty chamber.",
            "You walk into a room without other exits. Your skin crawls at the feeling of being cornered."
        ],
        2: [
            "You enter another stretch of dimly-lit corridor.",
            "A rough-hewn passage stretches away ahead and behind you.",
            "You move into a drafty hallway."
        ],
        3: [
            "The passageway splits here. Where to go?",
            "You hit a fork in the path. Both ways appear to be less traveled...",
            "A new hallway opens up, dimly outlined in the bleak twilight."
        ],
        4: [
            "You find yourself at a sort of crossroads.",
            "You enter what seems to have been a central meeting area, long ago.",
            "Suddenly the air feels less close; you're in a large chamber with several entrances."
        ]
    }

    def __init__(self,hero,entrance,override=False):
        if override:
            #Create an initial location with 4 unentered locations attached
            self.exits = []
            self.options = ["inventory", "help", "character", "quit", "go"]
            for direction in self.directions:
                self.exits.append(direction)
                self.options.append(f"go {direction}")
        else:
            #Add the entrance to the location, followed by a random number ([0,3] of other locations
            self.exits = [entrance]
            self.options = ["inventory", "help", "character", "quit", "go", f"go {entrance}"]
            for direction in self.directions:
                if direction != entrance and self.chance(2):
                    self.exits.append(direction)
                    self.options.append(f"go {direction}")
        self.description = choice(self.descriptions[len(self.exits)])
        self.connected_locations = dict()
        self.entered = False
        self.enemies = None
        hero_level = hero.level
        #if hero.level > 0 and ((5**(hero.level+1) - hero.experience) < (hero.experience - 5**hero.level)):
            #hero_level += 1
        if self.chance(2): #50% chance of adding an enemy
            enemy = choice(list(self.enemy_options.keys()))
            self.enemies = Opponent(
                enemy,
                self.enemy_options[enemy],
                self.roll(hero_level,1,"health")*3,self.roll(hero_level,1,"strength"),self.roll(hero_level,1,"defense"),self.roll(hero_level,0,"speed"),
                []
            )
            c = 0
            while c < 3: #Append up to 3 random items to enemy inventory, 50% chance each
                if self.chance(2):
                    stat_effects = {
                        "damage": 0,
                        "defense": 0,
                        "speed": 0,
                        "healing": 0
                    }
                    item_name = choice(list(self.items.keys()))
                    item_type = self.items[item_name][0]
                    base_stat = self.category_effects[item_type]
                    if hero.level > 0:
                        stat_effects[base_stat] = self.roll(1+hero_level)
                    else:
                        stat_effects[base_stat] = self.roll(hero_level,1)
                    second_stat = self.items[item_name][2]
                    stat_effects[second_stat] = self.roll(hero_level,1)
                    article = self.items[item_name][3]
                    new_item = Item(
                        item_name,
                        item_type,
                        self.items[item_name][1],
                        stat_effects["damage"],stat_effects["defense"],stat_effects["speed"],stat_effects["healing"],
                        article
                    )
                    self.enemies.equip(new_item)
                c += 1
            #print(self.enemies.__repr__())
            
    
    def __str__(self):
        result = self.description
        if self.enemies != None and self.enemies.health > 0:
            result += f" There's a {self.colors['red']}{self.enemies.name}{self.colors['reset']} prowling the area."
        elif self.enemies != None:
            result += f" The corpse of a {self.colors['red']}{self.enemies.name}{self.colors['reset']} lies sprawled on the ground."
        if len(self.exits) == 1:
            result += f" The only exit lies to the {self.colors['blue']}{self.exits[0]}{self.colors['reset']}."
        else:
            result += " There are exits to the "
            for direction in self.exits[:-1]:
                result += (f"{self.colors['blue']}{direction}{self.colors['reset']}, ")
            result += (f"and {self.colors['blue']}{self.exits[-1]}{self.colors['reset']}.")
        return result

    @staticmethod
    def chance(pool):
        '''return true with a probability of 1/pool'''
        chancer = randint(1,pool)
        if chancer == pool:
            return True
        else:
            return False    

    @staticmethod
    def roll(dice,min=0,reason=""):
        '''Simulate rolling [dice] 4-sided dice'''
        result = 0
        c = 0
        while c < dice:
            result += randint(1,4)
            c += 1
        return max(result,min)

    def enter(self,hero,override=False):
        '''Define action options in a space and spawn new created spaces as the user enters a new space'''
        print(self)
        if not self.entered:
            #Generate a location for each entrance to a new location
            if override:
                exit_list = self.exits #Append 4 exits to starting location
            else:
                exit_list = self.exits[1:] #Do not overwrite previous location
            for direction in exit_list:
                self.connected_locations[direction] = Location(hero,self.direction_reverse[direction])
                self.connected_locations[direction].connected_locations[self.direction_reverse[direction]] = self
            self.entered = True
        if self.enemies != None and self.enemies.health > 0: #Allow attack if living enemy present
            self.options.append("attack")
            self.options.append(f"attack {self.enemies.name}")
            if self.chance(3): #33% chance of enemy initiating combat
                result = self.enemies.attack(hero,self,False)
                return result
        return (self,False)

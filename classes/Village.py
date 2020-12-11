import random
import math
from classes.data import *


class Village():
    def __init__(self, name, starting_tech, num_farmers, num_artists, num_scientists, num_knights, companion_name=None):
        self.farmers = [Villager(starting_tech, "farmer") for _ in range(num_farmers)]
        self.artists = [Villager(starting_tech, "artist") for _ in range(num_artists)]
        self.scientists = [Villager(starting_tech, "scientist") for _ in range(num_scientists)]
        self.knights = [Villager(starting_tech, "knight") for _ in range(num_knights)]
        self.dead_villagers = {"farmers": [],
                               "artists": [], "scientists": [], "knights": []}
        self.transfered_villagers = {"farmers": [],
                               "artists": [], "scientists": [], "knights": []}
        
        self.wheat = 100
        self.happiness = 100
        self.science = 0
        self.strength = 0
        self.starting_tech = starting_tech

        self.isAlive = True
        self.new_tech = 10
        self.name = name
        self.notifications = []
        self.companion_name = companion_name
        self.prev_attack = ""

        self.strength = sum([knight.value for knight in self.knights]) # strength is gained immediately from knights

    # override print function
    # prints out village stats
    def __str__(self):
        fmt = '{:<20}{:<20}{:<20}{}'

        output = f"---{self.name}---" + line_ending
        if self.isAlive:
            output += fmt.format('Population:', 'Resources:',
                                'Production:', "Usage:") + line_ending

            population = [f"{len(self.farmers)} farmers", f"{len(self.artists)} artists",
                        f"{len(self.scientists)} scientists", f"{len(self.knights)} knights"]
            resources = [f"{self.wheat} wheat", f"{self.happiness} happiness",
                        f"{self.science} science", f"{self.strength} strength"]
            farmer_value, artist_value, scientist_value, knight_value = self.get_class_values()
            production = [f"{farmer_value*len(self.farmers)} wheat", f"{artist_value*len(self.artists)} happiness",
                f"{scientist_value*len(self.scientists)} science", ""]
            usage = [f"{self.population()} wheat", f"{math.ceil(self.population() / 3)} happiness",
                    "", ""]

            for i, (villager, resource, prod, drain) in enumerate(zip(population, resources, production, usage)):
                output += fmt.format(villager, resource, prod, drain) + line_ending

            output += line_ending + \
                f"Total Population: {self.population()}" + line_ending

            output += line_ending

            if self.companion_name:
                output += f"Message from {self.companion_name}:" + line_ending

                for notif in self.notifications:
                    output += notif + line_ending
                
                for villager_class in self.transfered_villagers.keys():
                    count = len(self.transfered_villagers[villager_class])
                    
                    if count > 0:
                        reason = self.transfered_villagers[villager_class][0].death_case
                        output += f"{count} {villager_class} {reason}." + line_ending

                for villager_class in self.dead_villagers.keys():
                    starve = 0
                    unhappy = 0
                    for villager in self.dead_villagers[villager_class]:
                        if villager.death_case == starve_str:
                            starve += 1
                        else:
                            unhappy += 1

                    if starve > 0:
                        output += f"{starve} {villager_class} {starve_str}." + line_ending

                    if unhappy > 0:
                        output += f"{unhappy} {villager_class} {unhappy_str}." + line_ending

                self.reset_notifs()

                if self.wheat < self.population() + 5:
                    output += "Wheat is low! Villagers may soon require more wheat!" + line_ending

                if self.happiness < math.ceil(self.population() / 3) + 5:
                    output += "Happiness is low! Villagers want more artists or they may leave!" + line_ending

                if self.science < self.new_tech:
                    output += f"{self.new_tech-self.science} more science needed for a technological breakthrough!" + line_ending
                else:
                    output += "You will make a technological breakthrough next turn!" + line_ending
        
        else:
            output += "This village has died off." + line_ending

        return output

    # empties notification data
    def reset_notifs(self):
        self.notifications = []
        self.dead_villagers = {"farmers": [],
                               "artists": [], "scientists": [], "knights": []}
        self.transfered_villagers = {"farmers": [],
                               "artists": [], "scientists": [], "knights": []}

    # returns the total population
    def population(self):
        return (len(self.farmers) + len(self.artists) + len(self.scientists) + len(self.knights))

    # continuously randomly kills a villager until population does not exceed resources
    def cap_population(self):
        while self.population() > self.wheat or self.population() > self.happiness:
            chance = random.random()

            if chance <= 0.25 and len(self.farmers) > 0:
                villager = self.farmers.pop()
                villager.death_case = starve_str if self.population() >= self.wheat else unhappy_str
                self.dead_villagers['farmers'].append(villager)

            elif chance > 0.25 and chance <= 0.5 and len(self.artists) > 0:
                villager = self.artists.pop()
                villager.death_case = starve_str if self.population() >= self.wheat else unhappy_str
                self.dead_villagers['artists'].append(villager)

            elif chance > 0.5 and chance <= 0.75 and len(self.scientists) > 0:
                villager = self.scientists.pop()
                villager.death_case = starve_str if self.population() >= self.wheat else unhappy_str
                self.dead_villagers['scientists'].append(villager)

            elif len(self.knights) > 0:
                villager = self.knights.pop()
                villager.death_case = starve_str if self.population() >= self.wheat else unhappy_str
                self.dead_villagers['knights'].append(villager)
            
            if self.population() == 0:
                self.isAlive = False
                break
    
    # transfers villagers from the current village to another
    def transfer_population(self, other_village, condition):
        val_1 = condition[0] # other village strength
        val_2 = condition[1] # current village strength
        foreign_msg = condition[2]
        local_msg = condition[3]

        farmer_val, artist_val, scientist_val, knight_val = other_village.get_class_values()

        # transfer the number of people based off of net strength
        while val_1 > val_2:
            chance = random.random()

            # transfer a farmer to other village
            if chance <= 0.25 and len(self.farmers) > 0:
                villager = self.farmers.pop()
                villager.value = farmer_val
                other_village.farmers.append(villager)
                
                villager.death_case = foreign_msg
                other_village.transfered_villagers['farmers'].append(villager)
                villager.death_case = local_msg
                self.transfered_villagers['farmers'].append(villager)
                val_1 -= 1
            # transfer an artist to other village
            elif chance > 0.25 and chance <= 0.5 and len(self.artists) > 0:
                villager = self.artists.pop()
                villager.value = artist_val
                other_village.artists.append(villager)

                villager.death_case = foreign_msg
                other_village.transfered_villagers['artists'].append(villager)
                villager.death_case = local_msg
                self.transfered_villagers['artists'].append(villager)
                val_1 -= 1
            # transfer a scientist to other village
            elif chance > 0.5 and chance <= 0.75 and len(self.scientists) > 0:
                villager = self.scientists.pop()
                villager.value = scientist_val
                other_village.scientists.append(villager)

                villager.death_case = foreign_msg
                other_village.transfered_villagers['scientists'].append(villager)
                villager.death_case = local_msg
                self.transfered_villagers['scientists'].append(villager)
                val_1 -= 1
            # transfer a knight to other village
            elif len(self.knights) > 0:
                villager = self.knights.pop()
                villager.value = knight_val
                other_village.knights.append(villager)

                villager.death_case = foreign_msg
                other_village.transfered_villagers['knights'].append(villager)
                villager.death_case = local_msg
                self.transfered_villagers['knights'].append(villager)
                val_1 -= 1
            # if population has been diminished, kill village
            if self.population() == 0:
                self.isAlive = False
                break
    
    # transfer resources from the current village to another
    def transfer_resources(self, village):
        steal_perc = 0.1 # proportion of the resource that is stolen

        # randomly choose one resource to steal that is not empty
        while True:
            chance = random.random()
            if chance <= 0.25 and self.wheat > 0:
                wheat_diff = math.ceil(steal_perc * self.wheat)
                self.notifications.append(f"{wheat_diff} wheat was stolen! Our food supply has diminished!")
                village.notifications.append(f"{wheat_diff} wheat was stolen! Our food supply has increased!")

                self.wheat -= wheat_diff
                village.wheat += wheat_diff
                break
            elif chance > 0.25 and chance <= 0.5 and self.happiness > 0:
                happiness_diff = math.ceil(steal_perc * self.happiness)
                self.notifications.append(f"{happiness_diff} art was stolen! Our people's happiness has lowered!")
                village.notifications.append(f"{happiness_diff} art was stolen! Our people's happiness has increased!")

                self.happiness -= happiness_diff
                village.happiness += happiness_diff
                break
            elif chance > 0.5 and chance <= 0.75 and self.science > 0:
                science_diff = math.ceil(steal_perc * self.science)
                self.notifications.append(f"{science_diff} science was stolen! Our scientists' research has regressed!")
                village.notifications.append(f"{science_diff} science was stolen! Our scientists' research has progressed!")
                self.science -= science_diff
                village.science += science_diff
                break
            elif chance > 0.75:
                self.notifications.append("Nothing has been stolen! They have spared our supplies!")
                village.notifications.append("We were not able to steal any resources!")
                break

    # improves the value of each villager
    def improve_technology(self):
        self.new_tech *= 3

        # choose one class of villager to improve tech
        # village must contain at least 1 villager to improve their tech
        while True:
            chance = random.random()
            if chance <= 0.25 and len(self.farmers) > 0:
                self.notifications.append("Farmers have learned to harvest more crops!")
                for farmer in self.farmers:
                    farmer.value += 1
                break
            elif chance > 0.25 and chance <= 0.5 and len(self.artists) > 0:
                self.notifications.append("Artists have learned new ways to design!")
                for artist in self.artists:
                    artist.value += 1
                break
            elif chance > 0.5 and chance <= 0.75 and len(self.scientists) > 0:
                self.notifications.append("Scientists have learned faster methods of research!")
                for scientist in self.scientists:
                    scientist.value += 1
                break
            elif chance > 0.75 and len(self.knights) > 0:
                self.notifications.append("Knights have learned to make their armour and weapons stronger!")
                for knight in self.knights:
                    knight.value += 1
                break
    
    # add selected class to grow
    def grow(self, class_type):
        farmer_value, artist_value, scientist_value, knight_value = self.get_class_values()

        if class_type == "farmer":
            self.farmers.append(Villager(farmer_value, class_type))
        elif class_type == "artist":
            self.artists.append(Villager(artist_value, class_type))
        elif class_type == "scientist":
            self.scientists.append(Villager(scientist_value, class_type))
        elif class_type == "knight":
            self.knights.append(Villager(knight_value, class_type))

    # iterate the village
    def develop(self):
        if self.isAlive:
            # refill resources through producers
            self.wheat += sum([farmer.value for farmer in self.farmers])
            self.happiness += sum([artist.value for artist in self.artists])
            self.science += sum([scientist.value for scientist in self.scientists])
            self.strength = sum([knight.value for knight in self.knights])

            # kill off population that exceeds resources
            self.cap_population()

            # consume resources
            self.wheat -= self.population()
            self.happiness -= math.ceil(self.population() / 3)

            # kill village if population dies
            if self.population() == 0:
                self.isAlive = False

            # improve tech if enough science
            if self.science >= self.new_tech:
                self.improve_technology()

    # logic for attacking another village
    def attack(self, village):
        # attack fails
        if village.strength > self.strength:
            self.notifications.append(f"We attacked {village.name} and lost!")
            village.notifications.append(f"We were attacked by {self.name} and defended ourselves!")

            num_lost = village.strength - self.strength
            transfer_condition = (num_lost, 0, attack_fail, attack_success)
            self.transfer_population(village, transfer_condition)
            self.transfer_resources(village)

        # stalemate
        elif village.strength == self.strength:
            self.notifications.append(f"We attacked {village.name} and neither side gained or lost anything!")
            village.notifications.append(f"We were attacked by {self.name} and neither side gained or lost anything!")

        # attack successful
        else:
            self.notifications.append(f"We attacked {village.name} and won!")
            village.notifications.append(f"We were attacked by {self.name} and lost!")

            num_lost = self.strength - village.strength
            transfer_condition = (num_lost, 0, attack_success, attack_fail)
            village.transfer_population(self, transfer_condition)
            village.transfer_resources(self)

    # get the value for a given class. 
    # if no villagers in a class, return starting value
    def get_class_values(self):
        farmer_value = self.starting_tech
        artist_value = self.starting_tech
        scientist_value = self.starting_tech
        knight_value = self.starting_tech

        if len(self.farmers) > 0:
            farmer_value = self.farmers[0].value

        if len(self.artists) > 0:
            artist_value = self.artists[0].value

        if len(self.scientists) > 0:
            scientist_value = self.scientists[0].value

        if len(self.knights) > 0:
            knight_value = self.knights[0].value

        return farmer_value, artist_value, scientist_value, knight_value

# data structure to hold villager data
class Villager():
    def __init__(self, initial_value, class_type):
        self.value = initial_value
        self.class_type = class_type
        self.death_case = ""

import random
import math
from classes.data import starve_str, unhappy_str, line_ending


class Village():
    def __init__(self, name, starting_tech, num_farmers, num_artists, num_scientists, num_knights, companion_name=None):
        self.farmers = [Villager(starting_tech, "farmer") for _ in range(num_farmers)]
        self.artists = [Villager(starting_tech, "artist") for _ in range(num_artists)]
        self.scientists = [Villager(starting_tech, "scientist") for _ in range(num_scientists)]
        self.knights = [Villager(starting_tech, "knight") for _ in range(num_knights)]
        self.dead_villagers = {"farmers": [],
                               "artists": [], "scientists": [], "knights": []}

        self.wheat = 100
        self.happiness = 100
        self.science = 0
        self.strength = 0

        self.isAlive = True
        self.new_tech = 10
        self.name = name
        self.notifications = []
        self.companion_name = companion_name

        self.strength = sum([knight.value for knight in self.knights]) # strength is gained immediately from knights

    # override print function
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
            usage = [f"{self.population()} wheat", f"{math.ceil(self.population() / 2)} happiness",
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

                if self.happiness < math.ceil(self.population() / 2) + 5:
                    output += "Happiness is low! Villagers want more artists or they may leave!" + line_ending

                if self.science < self.new_tech:
                    output += f"{self.new_tech-self.science} more science needed for a technological breakthrough!" + line_ending
                else:
                    output += "You will make a technological breakthrough next turn!" + line_ending
        
        else:
            output += "This village has died off." + line_ending

        return output

    def reset_notifs(self):
        self.notifications = []
        self.dead_villagers = {"farmers": [],
                               "artists": [], "scientists": [], "knights": []}

    def population(self):
        return (len(self.farmers) + len(self.artists) + len(self.scientists) + len(self.knights))

    def cap_population(self):
        while self.population() > self.wheat or self.population() > self.happiness:
            chance = random.random()

            if chance <= 0.25 and len(self.farmers) > 0:
                villager = self.farmers.pop()
                villager.death_case = starve_str if self.population() > self.wheat else unhappy_str
                self.dead_villagers['farmers'].append(villager)

            elif chance > 0.25 and chance <= 0.5 and len(self.artists) > 0:
                villager = self.artists.pop()
                villager.death_case = starve_str if self.population() > self.wheat else unhappy_str
                self.dead_villagers['artists'].append(villager)

            elif chance > 0.5 and chance <= 0.75 and len(self.scientists) > 0:
                villager = self.scientists.pop()
                villager.death_case = starve_str if self.population() > self.wheat else unhappy_str
                self.dead_villagers['scientists'].append(villager)

            elif len(self.knights) > 0:
                villager = self.knights.pop()
                villager.death_case = starve_str if self.population() > self.wheat else unhappy_str
                self.dead_villagers['knights'].append(villager)
            
            if self.population() == 0:
                self.isAlive = False
                break

    def improve_technology(self):
        self.new_tech *= round(self.new_tech / 2)

        chance = random.random()
        if chance <= 0.25:
            self.notifications.append(
                "Farmers have learned to harvest more crops!")
            for farmer in self.farmers:
                farmer.value += 1
        elif chance > 0.25 and chance <= 0.5:
            self.notifications.append(
                "Artists have learned new ways to design!")
            for artist in self.artists:
                artist.value += 1
        elif chance > 0.5 and chance <= 0.75:
            self.notifications.append(
                "Scientists have learned faster methods of research!")
            for scientist in self.scientists:
                scientist.value += 1
        else:
            self.notifications.append(
                "Knights have learned to make their armour and weapons stronger!")
            for knight in self.knights:
                knight.value += 1

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

    def develop(self):
        if self.isAlive:
            self.wheat += sum([farmer.value for farmer in self.farmers])
            self.happiness += sum([artist.value for artist in self.artists])
            self.science += sum([scientist.value for scientist in self.scientists])
            self.strength = sum([knight.value for knight in self.knights])

            self.wheat -= self.population()
            self.happiness -= math.ceil(self.population() / 2)

            self.cap_population()

            if self.population() == 0:
                self.isAlive = False

            if self.science >= self.new_tech:
                self.improve_technology()

    def get_class_values(self):
        farmer_value = 0
        artist_value = 0
        scientist_value = 0
        knight_value = 0

        if len(self.farmers) > 0:
            farmer_value = self.farmers[0].value

        if len(self.artists) > 0:
            artist_value = self.artists[0].value

        if len(self.scientists) > 0:
            scientist_value = self.scientists[0].value

        if len(self.knights) > 0:
            knight_value = self.knights[0].value

        return farmer_value, artist_value, scientist_value, knight_value

class Villager():
    def __init__(self, initial_value, class_type):
        self.value = initial_value
        self.class_type = class_type
        self.death_case = ""

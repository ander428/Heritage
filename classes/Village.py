import random


class Village():
    def __init__(self, name, farmers, artists, scientists, knights):
        self.farmers = farmers
        self.artists = artists
        self.scientists = scientists
        self.knights = knights
        self.dead_villagers = []

        self.wheat = 100
        self.happiness = 100
        self.science = 0
        self.strength = 0

        self.isAlive = True
        self.new_tech = 10
        self.name = name

    def __str__(self):
        fmt = '{:<20}{}'
        line_ending = "\n"

        output = f"---{self.name}---" + line_ending
        output += fmt.format('Population:', 'Resources:') + line_ending

        population = [f"{len(self.farmers)} farmers", f"{len(self.artists)} artists",
                      f"{len(self.scientists)} scientists", f"{len(self.knights)} knights"]
        resources = [f"{self.wheat} wheat", f"{self.happiness} happiness",
                     f"{self.science} science", f"{self.strength} strength"]

        for i, (villager, resource) in enumerate(zip(population, resources)):
            output += fmt.format(villager, resource) + line_ending

        output += line_ending

        output += "Notifications:" + line_ending
        if self.wheat < self.population() + 2:
            output += "Wheat is low! Villagers may soon require more wheat!" + line_ending

        if self.happiness < self.population():
            output += "Happiness is low! Villagers want more artists or they may leave!" + line_ending

        if self.science < self.new_tech:
            output += f"{self.new_tech-self.science} science needed for a technological breakthrough!" + line_ending

        return output

    def population(self):
        return (len(self.farmers) + len(self.artists) + len(self.scientists) + len(self.knights))

    def cap_population(self):
        while self.population() > self.wheat or self.population() > self.happiness + 2:
            chance = random.random()
            if chance <= 0.25 and len(self.farmers) > 0:
                self.dead_villagers.append(self.farmers.pop())
            elif chance > 0.25 and chance <= 0.5 and len(self.artists) > 0:
                self.dead_villagers.append(self.artists.pop())
            elif chance > 0.5 and chance <= 0.75 and len(self.scientists) > 0:
                self.dead_villagers.append(self.scientists.pop())
            elif chance > 0.75 and len(self.knights) > 0:
                self.dead_villagers.append(self.knights.pop())

    def improve_technology(self):
        self.new_tech += self.new_tech

        for farmer in self.farmers:
            farmer.value += 1

        for artist in self.artists:
            artist.value += 1

        for knight in self.knights:
            knight.value += 1

    def develop(self):
        if self.isAlive:
            self.wheat += sum([farmer.value for farmer in self.farmers])
            self.happiness += sum([artist.value for artist in self.artists])
            self.science += sum([scientist.value for scientist in self.scientists])
            self.strength = sum([knight.value for knight in self.knights])

            self.wheat -= self.population()
            self.happiness -= self.population()

            if self.wheat < 0:
                self.isAlive = False

            self.cap_population()

            if self.science == self.new_tech:
                self.improve_technology()


class Villager():
    def __init__(self, initial_value, class_type):
        self.value = initial_value
        self.class_type = class_type

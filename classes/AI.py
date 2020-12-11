from classes.Village import Village, Villager
from classes.data import line_ending, AI_counters
import math
import random

class AI(Village):
    def __init__(self, name, starting_tech, num_farmers, num_artists, num_scientists, num_knights, priors):
        super().__init__(name, starting_tech, num_farmers, num_artists, num_scientists, num_knights)

        # AI's prediction of what the player's starting population will be
        self.bayes_priors = {"farmer": priors[0], "artist": priors[1], "scientist": priors[2], "knight": priors[3]}
    
    # override print function
    # prints reduced stats
    def __str__(self):
        fmt = '{}'

        output = f"---{self.name}---" + line_ending

        if self.isAlive:
            output += fmt.format('Population:') + line_ending

            population = [f"{len(self.farmers)} farmers", f"{len(self.artists)} artists",
                        f"{len(self.scientists)} scientists", f"{len(self.knights)} knights"]

            for i, (villager) in enumerate(population):
                output += fmt.format(villager) + line_ending
        
        else:
            output += "This village has died off." + line_ending
        
        return output

    # generate predicted player move
    def predict(self):
        # generate normalized antithetical probabilities of each class
        # if a player has chosen more of one class, they are likely not to choose that class again
        weights = [sum(self.bayes_priors.values()) / self.bayes_priors[key] for key in self.bayes_priors.keys()]
        [choice] = random.choices(list(self.bayes_priors.keys()), weights)
        return choice

    # override growth logic
    def grow(self, player_move):
        # only update priors if player made a selection
        if player_move != "none":
            self.bayes_priors[player_move] += 1
        
        # get production and usage stats
        farmer_value, artist_value, scientist_value, knight_value = self.get_class_values()
        production = [farmer_value*len(self.farmers), artist_value*len(self.artists)]
        usage = [self.population(), math.ceil(self.population() / 2)]

        # constraints
        if production[0] < usage[0] and production[1] < usage[1]:
            if random.random() < 0.5:
                self.farmers.append(Villager(farmer_value, 'farmer'))
            else:
                self.artists.append(Villager(artist_value, 'artist'))
        elif production[0] < usage[0]:
            self.farmers.append(Villager(farmer_value, 'farmer'))
        elif production[1] < usage[1]:
            self.artists.append(Villager(artist_value, 'artist'))

        # constraints met
        else:
            predict_move = self.predict()
            new_villager = Villager(self.starting_tech, AI_counters[predict_move])

            if new_villager.class_type == "farmer":
                self.farmers.append(new_villager)
            elif new_villager.class_type == "artist":
                self.artists.append(new_villager)
            elif new_villager.class_type == "scientist":
                self.scientists.append(new_villager)
            elif new_villager.class_type == "knight":
                self.knights.append(new_villager)

    # helper function to find a valid target to attack
    def find_target_idx(self, country):
        try:
            i = random.randint(0, len(country)-1)
            while country[i].name == self.name:
                i = random.randint(0, len(country))
        except:
            # if there is only 1 other village the only option will be the player
            return 1
        
        return i
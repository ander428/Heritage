from classes.Village import Village, Villager
from classes.data import line_ending, AI_counters
import random

class AI(Village):
    def __init__(self, name, starting_tech, num_farmers, num_artists, num_scientists, num_knights, priors):
        super().__init__(name, starting_tech, num_farmers, num_artists, num_scientists, num_knights)
        self.starting_tech = starting_tech

        # AI's prediction of what the player's starting population will be
        self.bayes_priors = {"farmer": priors[0], "artist": priors[1], "scientist": priors[2], "knight": priors[3]}
    
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

    def predict(self):
        # generate normalized antithetical probabilities of each class
        # if a player has chosen more of one class, they are likely not to choose that class again
        weights = [sum(self.bayes_priors.values()) / self.bayes_priors[key] for key in self.bayes_priors.keys()]
        [choice] = random.choices(list(self.bayes_priors.keys()), weights)
        return choice

    def grow(self, player_move):
        if player_move.lower() != "none":
            self.bayes_priors[player_move] += 1

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


# test = AI("test", 2, 5,5,5,5,[40, 20, 40, 50])

# print(test)
# test.grow()
# print(test)


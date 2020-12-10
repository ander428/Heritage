from classes.AI import AI
from classes.Village import *
from classes.data import *


class Simulation:
    def __init__(self, init_pop, difficulty):
        self.population_size = init_pop
        self.difficulty = difficulty

    def main_menu(self):
        print(title + line_ending)
        print("Welcome settler! Prepare to breed generations of your village stronger than any other!" + line_ending)
        print(game_desc(line_ending) + line_ending)

        while True:
            print("Please select an option:")
            print("1 - Play the game")
            print("2 - View the GA algorithm solutions (pssst this is cheating)")
            print("3 - Quit")
            print()

            option = self.get_int_input("Selection: ")
            if option == 1:
                self.play_game()
            elif option == 2:
                self.show_GA()
            elif option == 3:
                break
            else:
                print("Interesting, you chose a number," +
                      " but one which was not on the list." +
                      line_ending + "Let's try this again..." + line_ending)
                continue

    def get_settings(self):
        print("Before your story can begin, we must know more about your country!")
        print()

        # settings loop
        player_name = ""
        num_enemies = 0

        # set village name
        player_name = self.get_str_input("What is the name of your village? ", "")

        num_enemies = self.get_int_input("How many other villages surround you (1-5)? ", max_val=5, min_val=1)

        print(line_ending + f"Ah, the country where {player_name} lies has {num_enemies} other villages as well." +
                " This will be challenge! Good luck young settler!")
        print()

        return player_name, num_enemies

    def create_player(self, player_name, companion_name):
        num_farmers = 0
        num_artists = 0
        num_scientists = 0
        num_knights = 0

        pop_count = self.population_size
        while pop_count > 0:
            num_farmers = self.get_int_input(f"You have {pop_count} villagers to appoint." + line_ending + 
                                            "How many should be farmers? ", max_val=pop_count)
            pop_count -= num_farmers

            if pop_count == 0:
                break

            num_artists = self.get_int_input(f"You have {pop_count} villagers to appoint." + line_ending + 
                                            "How many should be artists? ", max_val=pop_count)
            pop_count -= num_artists

            if pop_count == 0:
                break

            num_scientists = self.get_int_input(f"You have {pop_count} villagers to appoint." + line_ending +
                                                "How many should be scientists? ", max_val=pop_count)
            pop_count -= num_scientists

            if pop_count == 0:
                break

            print(f"{pop_count} will be knights then!" + line_ending)
            num_knights = pop_count
            pop_count = 0

            break

        print("All the villagers have been appointed!" + line_ending)

        return Village(player_name, default_tech, num_farmers, num_artists, num_scientists, num_knights, companion_name=companion_name)

    def play_game(self):
        country = []

        # draw AI names
        names = random.sample(AI_names, 6)
        companion_name = names[5]

        # get player settings
        player_name, num_enemies = self.get_settings()
        input("Press Enter to continue: ")
        print()

        # create AI
        enemies = []
        enemies.append(AI(f"{names[0]}'s Empire", self.difficulty, *[8,2,2,8], [5,4,1,10]))
        enemies.append(AI(f"{names[1]}'s Grasslands", self.difficulty, *[15,5,0,0], [10,5,4,1]))
        enemies.append(AI(f"{names[2]}'s Monastery", self.difficulty, *[10,10,0,0], [5,4,10,1]))
        enemies.append(AI(f"{names[3]}'s Valley", self.difficulty, *[8,8,2,2], [5,5,1,9]))
        enemies.append(AI(f"{names[4]}'s Kingdom", self.difficulty, *[5,5,5,5], [5,5,5,5]))

        # add enemies to the game's country
        [country.append(enemy) for enemy in random.sample(enemies, num_enemies)]

        # add player to country
        print(f"Welcome! My name is {companion_name}, and I am honored to appoint you as the new leader of our village, {player_name}! " + 
                "Before I leave you to your duties, I must inform you on where your leadership will be of utmost importance." + line_ending)
        print("First, we must appoint those we can to work on the village." + line_ending)
        country.append(self.create_player(player_name, companion_name))
        print("Excellent, we may now get things moving around here!" + line_ending)
        print("Ah, wait! There is one more thing. I will be right back! I must gather some things for you. ")
        input("Press Enter when you are ready for me: ")
        print()
        print("Every year the following will happen, and you will make a decision about how to proceed for the next year:" + line_ending)
        print("\t- Our scouts will inform us of other villages' population." + line_ending +
                "\t- I personally will be sending you messages about updates around the village to keep you aware of how our people are doing." + line_ending +
                "\t- A new child will grow old enough to join the workforce. You may decide to give them a role or let them be." + line_ending +
                "\t- Alternatively, you may need the time to plan an attack another village which if successful, will be a great source of food, art, and new workers." + line_ending)
        print("That is everything! Good luck!" + line_ending)

        input("Press Enter to start your turn: ")

        valid_roles = ['farmer', 'artist', 'scientist', 'knight', 'none']
        count = 1
        play_game = True
        while play_game:
            print(f"YEAR {count}")
            self.print_country(country)

            if country[len(country)-1].isAlive:
                player_move = self.get_str_input("You may grow your workforce by 1 villager! Which would you like to add (farmer, artist, scientist, knight, none)? ", 
                                            "Curious, that is not a role in your village. Maybe try another one.", valid_responses=valid_roles)
                player_move = player_move.lower()

                [village.grow(player_move) for village in country]
                [village.develop() for village in country]

                count += 1
            else:
                print("You have failed! Your village has died off! Others will inhabit" +
                        f" the world without {player_name}.")
                print(f"{player_name} survived {count-1} years." + line_ending)
                input("Press enter to return to main menu: ")
                print()
                play_game = False


    def get_int_input(self, input_msg, max_val=None, min_val=None):
        result = 0
        while True:
            try:
                result = int(input(input_msg))

                if min_val:
                    if result < min_val:
                        print(line_ending + f"The value must not be below {min_val}! Try a larger number." + line_ending)
                        continue
                if max_val:
                    if result > max_val:
                        print(line_ending + "That is too many! Try a smaller number." + line_ending)
                        continue
                
                break
            except:
                print(line_ending + "Blasphemy! You must respond with a number, not letters!" + line_ending)

        return result

    def win_condition(self, country):
        for i in range(len(country)-1):
            if country[i].isAlive:
                return False
        
        return True

    def get_str_input(self, input_msg, err_msg, valid_responses=None):
        result = 0
        while True:
            try:
                result = input(input_msg)

                if result.strip() == "":
                    print("Blasphemy! You responded with nothing!")
                    continue
                elif valid_responses:
                    if not result.lower() in valid_responses:
                        raise Exception()
                
                break
            except:
                print(line_ending + err_msg + line_ending)

        return result

    def print_country(self, country):
        for village in country:
            print(village)
from classes.AI import AI
from classes.Village import *
from classes.data import *


class Simulation:
    def __init__(self, init_pop, difficulty):
        self.population_size = init_pop
        self.difficulty = difficulty

    def main_menu(self):
        while True:
            print(title + line_ending)
            print("Welcome settler! Prepare to breed generations of your village stronger than any other!" + line_ending)
            print(game_desc(line_ending) + line_ending)

            print("Please select an option:")
            print("1 - Play the game")
            print("2 - View how the AI algorithm works (pssst this is cheating)")
            print("3 - Quit")
            print()

            option = self.get_int_input("Selection: ")
            if option == 1:
                self.play_game()
            elif option == 2:
                self.show_AI()
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

        # set difficulty
        self.difficulty = self.get_int_input("What difficulty would you like to play (1-3)? ", min_val=1, max_val=3)

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
        enemies.append(AI(f"{names[0]}'s Empire", self.difficulty+1, *[8,2,2,8], [5,4,1,10]))
        enemies.append(AI(f"{names[1]}'s Grasslands", self.difficulty+1, *[15,5,0,0], [7,5,4,4]))
        enemies.append(AI(f"{names[2]}'s Monastery", self.difficulty+1, *[10,10,0,0], [5,4,7,4]))
        enemies.append(AI(f"{names[3]}'s Valley", self.difficulty+1, *[8,3,7,2], [5,5,3,7]))
        enemies.append(AI(f"{names[4]}'s Kingdom", self.difficulty+1, *[5,5,5,5], [5,5,5,5]))

        # add enemies to the game's country
        [country.append(enemy) for enemy in random.sample(enemies, num_enemies)]

        # add player to country
        country.append(self.introduction(player_name, companion_name))
        input("Press Enter to continue: ")
        print()

        count = 1
        play_game = True
        while play_game:
            if self.win_condition(country):
                print(f"Success! You have done a great job leading {player_name}. We have grown large enough to inhabit the whole country!" + line_ending)
                input("Press enter to return to main menu: ")
                break

            print(f"YEAR {count}")
            self.print_country(country)

            read_player_vals = country[len(country)-1]
            if read_player_vals.isAlive:
                player_move = self.player_move(read_player_vals, country)

                if player_move == 'quit':
                    print(f"You are resigning as our leader? What will we do now?" + line_ending)
                    input("Press enter to return to main menu: ")
                    print()
                    break
            
                
                elif not player_move:
                    player_move = 'none'
                self.AI_move(player_name, player_move, country)
   
                [village.develop() for village in country]

                count += 1
            else:
                print("You have failed! Your village has died off! Others will inhabit" +
                        f" the world without {player_name}.")
                print(f"{player_name} survived {count-1} years." + line_ending)
                input("Press enter to return to main menu: ")
                print()
                play_game = False

    def introduction(self, player_name, companion_name):
        print(f"Welcome! My name is {companion_name}, and I am honored to appoint you as the new leader of our village, {player_name}!" + line_ending +
                "Before I leave you to your duties, I must inform you on where your leadership will be of utmost importance." + line_ending)
        print("First, we must appoint those we can to work on the village." + line_ending)
        player = self.create_player(player_name, companion_name)
        print("Excellent, we may now get things moving around here!" + line_ending)
        print("Ah, wait! There is one more thing. I will be right back! I must gather some things for you. ")
        input("Press Enter when you are ready for me: ")
        print()
        print(turn_info(line_ending))

        return player

    def win_condition(self, country):
        for i in range(len(country)-1):
            if country[i].isAlive:
                return False
        
        return True

    def player_move(self, read_player_vals, country):
        valid_roles = ['farmer', 'artist', 'scientist', 'knight', 'none']

        option = 0
        while True:
            print("Would you like to attack a village or grow the workforce?")
            print("1 - Attack (you must have at least 5 knights)")
            print("2 - Grow")
            print("3 - Quit")
            print()
            option = self.get_int_input("Selection: ", min_val=1, max_val=3)
            print()

            if option == 1 and len(read_player_vals.knights) < 5:
                print(line_ending + "We do not have enough of an army to fight!" + line_ending)
            else:
                break

        if option == 1:
            valid_options = [village.name.lower() for village in country if village.name != read_player_vals.name and village.isAlive and village.name != self.prev_attack]
            move = self.get_str_input("Enter the name of the village you would like to attack: ", 
                                                "We do not know of such village! Maybe a different one?", valid_responses=valid_options)
            target = 0

            for i in range(len(country)):
                if country[i].name.lower() == move.lower():
                    target = i

            country[len(country)-1].attack(country[target])
            return country[target].name
        elif option == 2:
            move = self.get_str_input("You may grow your workforce by 1 villager! Which would you like to add (farmer, artist, scientist, knight, none)? ", 
                                        "Curious, that is not a role in your village. Maybe try another one.", valid_responses=valid_roles)
            move = move.lower()

            country[len(country)-1].grow(move)

            return move
        else:
            return 'quit'

    def AI_move(self, player_name, player_move, country):
        for i in range(len(country)):
            if country[i].name == player_name:
                continue
            elif country[i].isAlive:
                if random.random() < AI_attack_freq and len(country[i].knights) >= 5:
                    while True:
                        target = country[i].find_target_idx(country)
                        if country[target].isAlive and country[target].name != country[i].name and country[target].name != country[i].prev_attack:
                            break
                    country[i].attack(country[target])
                    country[i].prev_attack = country[target].name
                else:
                    country[i].grow(player_move)

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
                        print(line_ending + "That is too large! Try a smaller number." + line_ending)
                        continue
                
                break
            except:
                print(line_ending + "Blasphemy! You must respond with a number, not letters!" + line_ending)

        return result

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

    def show_AI(self):
        print("Hello! Here is where I will explain how the AI makes decisions. First lets make an example." + line_ending)
        input("Press Enter to continue: ")
        print()
        example = AI(f"Josh's Valley", self.difficulty+1, *[8,3,7,2], [5,5,3,7])
        print(example)
        print("This is an AI for Harvest. There is actually some more data behind the scenes as well so lets take a look at that as well." + line_ending)
        input("Press Enter to continue: ")
        print()
        print(f"Difficulty: {self.difficulty+1}" + line_ending + f"Attack Frequency: {AI_attack_freq*100}%" + line_ending + f"Bayesian Priors: {[5,5,3,7]}" + line_ending)
        print("First off the difficulty setting changes the starting technology level of the AI, i.e., changes the productivity of the villagers at the start.")
        print("Attack frequency is the random chance that the village may attack. Each turn, it rolls a die to decide whether it will attack and randomly chooses a target.")
        print("The bayesian priors are weights unique to each AI that are assumptions the AI makes about the player." + line_ending + 
                "Here, it assumes the player will start with 5 farmers, 5 knights, 3 scientists, and 7 knights.")
        print()
        input("Press Enter to learn how the AI chooses villagers: ")
        print()
        fmt = '{:<20}{}'
        output = f"---{example.name}---" + line_ending
        output += fmt.format('Production:', "Usage:") + line_ending
        farmer_value, artist_value, scientist_value, knight_value = example.get_class_values()
        production = [f"{farmer_value*len(example.farmers)} wheat", f"{artist_value*len(example.artists)} happiness",
            f"{scientist_value*len(example.scientists)} science", ""]
        usage = [f"{example.population()} wheat", f"{math.ceil(example.population() / 3)} happiness",
                "", ""]

        for i, (prod, drain) in enumerate(zip(production, usage)):
            output += fmt.format(prod, drain) + line_ending
        print(output)
        print("It will first be constrained by net production of wheat and happiness. If negative, it will prioritize farmers and artists.")
        print("Otherwise, it will weight the best move by sum(priors) / prior_i for each class meaning it will expect the player to add villagers " + 
                "in roles they do not already have." + line_ending)
        print("When a player makes a move, it will then update its priors to be more accurate to the player's actual decisions.")
        print("Here since the net production is in the negative for both wheat and happiness, it will choose either an artist or a farmer." + line_ending)
        input("Press Enter to see how the AI counters the player: ")
        print()
        output = fmt.format("Player Move:", "Counter:") + line_ending
        for key, value in AI_counters.items():
            output += fmt.format(key, value) + line_ending
        print(output)
        print(f"This is the counter lookup table the AI uses. For example, the AI predicts the player will add a knight, it will, constraints permitting, choose a {AI_counters['knight']}.")
        print()
        print("That is all! There are other smaller changes to the AI from a player controlled village, but those can all be viewed in AI.py." + line_ending)
        input("Press Enter to return to main menu: ")
        print()

  
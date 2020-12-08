from classes.Village import *
from classes.data import title, game_desc, line_ending, default_tech


class HeritageGame:
    def __init__(self, init_pop):
        self.population_size = init_pop

    def main_menu(self):
        print(title + line_ending)
        print("Welcome settler! Prepare to breed generations of your village stronger than any other!" + line_ending)
        print(game_desc(line_ending) + line_ending)

        play = True
        while play:
            print("Please select an option:")
            print("1 - Play the game")
            print("2 - View the GA algorithm solutions (pssst this is cheating)" +
                  line_ending + line_ending)

            option = self.get_int_input("Selection: ")
            if option == 1:
                play = self.play_game()
            elif option == 2:
                self.show_GA()
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

        while True:
            # set village name
            while len(player_name) == 0:
                player_name = input("What is the name of your village? ")

                if player_name.strip() == "":
                    print(
                        "Blasphemy! Your village name must not only consist of spaces!")
                    player_name = ""

            num_enemies = self.get_int_input("How many other villages surround you (1-5)? ", max_val=5, min_val=1)

            print(line_ending + f"Ah, the country where {player_name} lies has {num_enemies} other villages as well." +
                  " This will be challenge! Good luck young settler!")
            print()
            break

        return player_name, num_enemies

    def create_player(self, player_name):
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

        return Village(player_name, default_tech, num_farmers, num_artists, num_scientists, num_knights)

    def play_game(self):
        player_name, num_enemies = self.get_settings()
        player = self.create_player(player_name)

        print(player)

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
                print("Blasphemy! You must respond with a number, not letters!" + line_ending)

        return result

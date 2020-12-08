from classes.Village import *
from classes.Simulation import HeritageGame

game = HeritageGame(10)

game.main_menu()

# a = [Villager(3, "farmer") for i in range(2)]
# b = [Villager(3, "artist") for i in range(1)]
# c = [Villager(1, "scientist") for i in range(1)]
# d = [Villager(1, "knight") for i in range(1)]

# player = Village("Your Village", a, b, c, d)
# print(player)

# for _ in range(20):
#     farmer_value = int(input("How many farmers?"))
#     artist_value = int(input("How many artists?"))
#     scientist_value = int(input("How many scientists?"))
#     knight_value = int(input("How many knights?"))
#     player.develop()
#     player.grow(farmer_value, artist_value, scientist_value, knight_value)
#     print(player)

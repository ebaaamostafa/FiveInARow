import algorithms.alphaBetaPruning
import algorithms.minimax
import gameEngine, Players, algorithms

# start game engine
print("""
      Welcome to Five in a Row!\n
      Choose type of the first player: \n
      1. Human Player\n
      2. AI Player\n
    """)
choice = int(input("Enter your choice (1 or 2): "))
player1 = None
player2 = None
if choice == 1:
    name = input("Enter name of the player: ")
    player1 = Players.HumanPlayer(name, "B")
else:
    player1 = Players.AIPlayer("Computer 1", "B", algorithms.alphaBetaPruning.alpha_beta_pruning)

print("""
      Choose type of the second player: \n
      1. Human Player\n
      2. AI Player\n
    """)
choice = int(input("Enter your choice (1 or 2): "))
if choice == 1:
    name = input("Enter name of the player: ")
    player2 = Players.HumanPlayer(name, "W")
else:
    player2 = Players.AIPlayer("Computer 2", "W", algorithms.minimax.minimax)

# start game engine
# board_size = int(input("Enter the size of the board (default is 15): "))
game = gameEngine.GameEngine(player1, player2)
game.start()

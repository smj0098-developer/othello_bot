
import time
from Board import Board
from Game import Game
from Player import Player

start_time = time.time()
initial_board = Board([
    ["0", "0", "0", "0", "0", "0", "0", "0"],
    ["0", "0", "0", "0", "0", "0", "0", "0"],
    ["0", "0", "0", "0", "0", "0", "0", "0"],
    ["0", "0", "0", "w", "b", "0", "0", "0"],
    ["0", "0", "0", "b", "w", "0", "0", "0"],
    ["0", "0", "0", "0", "0", "0", "0", "0"],
    ["0", "0", "0", "0", "0", "0", "0", "0"],
    ["0", "0", "0", "0", "0", "0", "0", "0"]
])

# giving color and cutOff power of each player to them
# cutOff power is basically how deep our player can see in the game tree
blackPlayer = Player("b", 1)
whitePlayer = Player("w", 3)
game = Game(initial_board, blackPlayer, whitePlayer)
game.play()

print("running time :", time.time()-start_time, "seconds")

from Board import Board
from Player import Player
from Strategy import Strategy
import numpy as np
from math import inf


class Game:
    def __init__(self, board: Board, player1: Player, player2: Player):
        self.board = board
        self.player1 = player1
        self.player2 = player2
        # setting initial turn
        if (player1.color == "b"):
            self.activePlayer = player1
        else:
            self.activePlayer = player2

    def play(self):
        st = Strategy()
        while (len(st.successor(self.player1, self.board)) != 0 or len(st.successor(self.player2, self.board)) != 0):
            # keep changing turns and calling minimax until none of the players have any moves
            minimaxResult = st.minimax(self.activePlayer, self.activePlayer, self.player1,
                                       self.player2, self.board, 0, self.activePlayer.cutoff, True, self.board, -inf, +inf)
            self.board = minimaxResult[1]

            tmpMatrix = np.array(self.board.boardMatrix)
            tmpMatrix[tmpMatrix == "0"] = " "
            print(tmpMatrix, "\n")
            # printing the board as a numpy array so that it looks better (to be changed later)

            # the minimax function returns a new board, which is the result of one of the player's move
            self.activePlayer = st.changeTurns(
                self.activePlayer, self.player1, self.player2)

        # winner test must be done here
        self.checkWinner(self.player1, self.player2, self.board)

    def checkWinner(self, player1: Player, player2: Player, board: Board):
        player1FinalUtility = 0
        player2FinalUtility = 0
        for row in board.boardMatrix:
            for cell in row:
                if (cell == player1.color):
                    player1FinalUtility += 1
                elif (cell == player2.color):
                    player2FinalUtility += 1
        if (player1FinalUtility > player2FinalUtility):
            print(player1.color, "won the game",
                  player1FinalUtility, "to", player2FinalUtility)
        elif (player1FinalUtility < player2FinalUtility):
            print(player2.color, "won the game",
                  player2FinalUtility, "to", player1FinalUtility)
        else:
            print("draw")

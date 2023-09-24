from Board import Board
from Player import Player
import copy
from math import inf
from utility import hash_iterable


class Strategy:
    def __init__(self) -> None:
        self.transposition_table: dict = dict()

    def successor(self, activePlayer: Player, board: Board) -> list[Board]:
        # activePlayer is the player whose turn it is
        # Boards are in fact the states. So the output of successor function is a list of Boards
        copiedBoardMatrix = copy.deepcopy(board.boardMatrix)
        return self.find_valid_moves(copiedBoardMatrix, activePlayer)

    def find_valid_moves(self, boardMatrix: list[list[str]], activePlayer: Player) -> list[Board]:
        valid_successors_boards = []
        for cellRow in range(len(boardMatrix)):
            for cellCol in range(len(boardMatrix[cellRow])):
                if boardMatrix[cellRow][cellCol] == "0":
                    copiedBoardMatrix2 = copy.deepcopy(boardMatrix)
                    # checking and applying a possible move by giving cellRow and cellCol of that move to flip_if_valid()
                    # flip_if_valid() both flips beads and returns a boolean value to say whether a move is possible
                    is_valid = self.flip_if_valid(
                        copiedBoardMatrix2, cellRow, cellCol, activePlayer)
                    if (is_valid):
                        # if the move is valid, then change the cell's value to the color of the player whose turn it is
                        # notice that other cells along the way have already changed by means of flip_if_valid()
                        copiedBoardMatrix2[cellRow][cellCol] = activePlayer.color
                        valid_successors_boards.append(
                            Board(copiedBoardMatrix2))
        return valid_successors_boards

    def flip_if_valid(self, boardMatrix: list[list[str]], cellRow: int, cellCol: int, activePlayer: Player):
        # this function checks all 8 squares surrounding the square we are trying to change
        # and then applies changes to boardMatrix, and that is how each successor is generated
        flipList = []
        validOrNot = False
        tmpCellRow = cellRow
        tmpCellCol = cellCol

        conditions = [
            {  # middle bottom side
                'cellRowMinimum': 0,
                'cellRowMaximum': 6,
                'cellColMinimum': 0,
                'cellColMaximum': 7,
                'cellRowChange': 1,
                'cellColChange': 0
            },
            {  # middle top side
                'cellRowMinimum': 1,
                'cellRowMaximum': 7,
                'cellColMinimum': 0,
                'cellColMaximum': 7,
                'cellRowChange': -1,
                'cellColChange': 0
            },
            {  # middle right side
                'cellRowMinimum': 0,
                'cellRowMaximum': 7,
                'cellColMinimum': 0,
                'cellColMaximum': 6,
                'cellRowChange': 0,
                'cellColChange': 1
            },
            {  # middle left side
                'cellRowMinimum': 0,
                'cellRowMaximum': 7,
                'cellColMinimum': 1,
                'cellColMaximum': 7,
                'cellRowChange': 0,
                'cellColChange': -1
            },
            {  # bottom right side
                'cellRowMinimum': 0,
                'cellRowMaximum': 6,
                'cellColMinimum': 0,
                'cellColMaximum': 6,
                'cellRowChange': 1,
                'cellColChange': 1
            },
            {  # bottom left side
                'cellRowMinimum': 0,
                'cellRowMaximum': 6,
                'cellColMinimum': 1,
                'cellColMaximum': 7,
                'cellRowChange': 1,
                'cellColChange': -1
            },
            {  # top right side
                'cellRowMinimum': 1,
                'cellRowMaximum': 7,
                'cellColMinimum': 0,
                'cellColMaximum': 6,
                'cellRowChange': -1,
                'cellColChange': 1
            },
            {  # top left side
                'cellRowMinimum': 1,
                'cellRowMaximum': 7,
                'cellColMinimum': 1,
                'cellColMaximum': 7,
                'cellRowChange': -1,
                'cellColChange': -1
            }
        ]

        for condition in conditions:
            tmpFlipList = []
            tmpCellRow = cellRow
            tmpCellCol = cellCol
            differentColorFound = False
            while (tmpCellCol >= condition['cellColMinimum']
                   and tmpCellRow >= condition['cellRowMinimum']
                   and tmpCellCol <= condition['cellColMaximum']
                   and tmpCellRow <= condition['cellRowMaximum']):
                tmpCellCol += condition['cellColChange']
                tmpCellRow += condition['cellRowChange']
                if (not differentColorFound):
                    if (boardMatrix[tmpCellRow][tmpCellCol] == activePlayer.color or boardMatrix[tmpCellRow][tmpCellCol] == "0"):
                        break
                    if (boardMatrix[tmpCellRow][tmpCellCol] != activePlayer.color and boardMatrix[tmpCellRow][
                            tmpCellCol] != "0"):
                        differentColorFound = True
                        tmpFlipList.append((tmpCellRow, tmpCellCol))
                else:
                    if (boardMatrix[tmpCellRow][tmpCellCol] == "0"):
                        break
                    elif (boardMatrix[tmpCellRow][tmpCellCol] == activePlayer.color):
                        flipList.append(tmpFlipList)
                        validOrNot = True
                        break

                    else:
                        tmpFlipList.append((tmpCellRow, tmpCellCol))

        self.flip(flipList, boardMatrix, activePlayer)
        return validOrNot

    def flip(self, flipList: list[list[tuple[int, int]]], boardMatrix: list[list[str]], activePlayer: Player):
        for cell in flipList:
            for cellRow, cellCol in cell:
                boardMatrix[cellRow][cellCol] = activePlayer.color

    def generate_state_hash(self, currentDepth: int, player: Player, board: Board):
        return f"{currentDepth}_{player.color}_{hash_iterable(board.boardMatrix)}"

    def minimax(self, activePlayer, imaginaryActivePlayer: Player, player1: Player, player2: Player, board: Board, currentDepth, cutOff, maxTurn: bool, levelOneSuccessor: Board, alpha: float, beta: float) -> tuple[float, Board]:
        state_hash = self.generate_state_hash(
            currentDepth, activePlayer, board)

        # imaginaryActivePlayer is the player who is active in each ply of minimax. So the max player imagines that this player is active
        # but activePlayer is the one who has to make a move for real
        # minimax returns a tuple of two values. the first one is the heuristic value and the second one is the best selected successor
        if (currentDepth == cutOff):
            # if the cutOff depth has been reached, do the cutOff
            heuristic_value = self.heuristic(activePlayer, board)
            self.transposition_table[state_hash] = heuristic_value
            return (heuristic_value, levelOneSuccessor)

        successorsList = self.successor(imaginaryActivePlayer, board)
        if (len(successorsList) == 0):
            # if the imaginaryActivePlayer has no moves, do the cutOff
            heuristic_value = self.heuristic(activePlayer, board)
            self.transposition_table[state_hash] = heuristic_value
            return (heuristic_value, levelOneSuccessor)

        pair = (-inf if maxTurn else inf, levelOneSuccessor)

        imaginaryActivePlayer = self.changeTurns(
            imaginaryActivePlayer, player1, player2)

        # Forward pruning only if successorsList is greater than 5
        if (len(successorsList) > 5):
            heuristicsList = []
            for successorBoard in successorsList:
                heuristicsList.append([self.heuristic(
                    activePlayer, successorBoard), successorBoard])

            # Sort heuristicsList by first element of list
            heuristicsList.sort(key=lambda x: x[0])

            # Remove 2 least elements if the length is greater than 5
            heuristicsList = heuristicsList[2:]
            successorsList = [x[1] for x in heuristicsList]
        # End of forward pruning

        for successorBoard in successorsList:

            # Transposition Table
            successor_hash = self.generate_state_hash(
                currentDepth + 1, activePlayer, successorBoard)
            if (successor_hash in self.transposition_table):
                heuristicBoardPair = (
                    self.transposition_table[successor_hash], successorBoard if currentDepth == 0 else levelOneSuccessor)

            else:
                heuristicBoardPair = self.minimax(
                    activePlayer,
                    imaginaryActivePlayer,
                    player1,
                    player2,
                    successorBoard,
                    currentDepth + 1,
                    cutOff,
                    not maxTurn,
                    successorBoard if currentDepth == 0 else levelOneSuccessor,
                    alpha,
                    beta
                )

            if (maxTurn):
                # Max Turn
                if (heuristicBoardPair[0] > pair[0]):
                    pair = (heuristicBoardPair[0], heuristicBoardPair[1])

                alpha = max(alpha, heuristicBoardPair[0])

                if (pair[0] >= beta):
                    return pair

            else:
                # Min Turn
                if (heuristicBoardPair[0] < pair[0]):
                    pair = (heuristicBoardPair[0], heuristicBoardPair[1])

                beta = min(beta, heuristicBoardPair[0])

                if (pair[0] <= alpha):
                    return pair

        return pair

    def heuristic(self, activePlayer, board) -> int:
        # the heuristic must be counted considering the activePlayer, the player whose turn it is.
        activePlayerBeadCount = 0
        opponentPlayerBeadCount = 0
        for row in board.boardMatrix:
            for cell in row:
                if (cell == activePlayer.color):
                    activePlayerBeadCount += 1
                elif (cell != "0" and cell != activePlayer.color):
                    opponentPlayerBeadCount += 1

        return activePlayerBeadCount-opponentPlayerBeadCount

    def changeTurns(self, activePlayer: Player, player1: Player, player2: Player) -> Player:
        if (activePlayer == player1):
            activePlayer = player2
        else:
            activePlayer = player1

        return activePlayer

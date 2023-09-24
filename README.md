# Othello Player Bot

## Initial settings

This part is taking place in main.py file, where the initial board
of the game is passed to a variable called `initial_board`. <BR>
The two `Players` are created
as well as a `Game` on which the `play` function
is invoked, and that is where the game begins.

## Classes and Methods

### class `Player`

This class has two attributes, namely `color` and `cutoff`.<BR>
`color` specifies players' colors, and cutoff determines how deep
the player is allowed to move down the tree while performing
minimax.

### class `Board`

This class has an attribute and a getter function.
Its single attribute is `boardMatrix`
which is a matrix storing data of the `Board`.

### class `Game`

There are two functions here.
`CheckWinner` chooses the winner => time = O(r\*c) : r
is the number of rows. c is the number of columns.<br>
`play` is a function that calls minimax until none of the players
have any moves left.

### class `Strategy`

#### Methods:

`successor` : generates successors of the current state.
Note: all states are `Board`. Therefore, the successor function
returns a list of `Board`s.<Br>
`find_valid_moves` finds all valid moves. It gets
the `Game`'s `Board` and a `Player` as input, and returns a list
of `Board`s as output. => time = O((r*c)^2) : r
is the number of rows. c is the number of columns.<br>
`flip_if_valid` gets one of the cells of the `Board` as well as
a `Player` and `boardMatrix`. It then flips those cells that
must be flipped according to the rules of Othello. => O(1)
<br>
`flip`: It performs the flip procedure => time = O(r*c) : r
is the number of rows. c is the number of columns.<br>
`changeTurns` changes the player whose turn it is to play=> time = O(1)
`heuristic` It is the evaluation function of the minimax algorithm.
It subtracts the number of blacks and whites and returns the resulting number.
O(r\*c) : r
is the number of rows. c is the number of columns.<br>
`Minimax`: it runs the minimax algorithm on a copy of the real world `Board`.
space Comp = O(bm) and time Comp = O(b^m) where b is the
branching factor and m is the maximum depth of the tree.

## Algorithms

### Forward Pruning

We remove the 2 items with least heuristic from successors if the successors length is greater than 5

### Transposition Table

We use a dictionary to store the results of the minimax algorithm. The key is a combination of currentDepth, activePlayer and the board. The value is the heuristic value of the board. We use this dictionary to avoid calculating the minimax algorithm for the same board again.

### Alpha Beta Pruning

The algorithms stops searching the branch if the value of the current node is greater than the value of the best node in the other branch.

It is identical to the Book's algorithm

import random

# this class stores an othello board state
# the state is handled as a 1d list that stores a 10x10 board.  1 and -1 are the two colors, 0 are empty squares
INFIN = 1000000000


class Board:

    # make a starting board.  There are four pieces in the center
    def __init__(self):
        self.state = [0] * 100
        self.state[44] = 1
        self.state[45] = -1
        self.state[54] = -1
        self.state[55] = 1

        # returns the score as the difference between the number of 1s and the number of -1s

    def evaluate(self):
        value = 0
        for i in range(100):
            if self.state[i] == 1:
                value = value + 1
            elif self.state[i] == -1:
                value = value - 1
        return value

        # returns a new board that is a copy of the current board

    def copy(self):
        board = Board()
        for i in range(100):
            board.state[i] = self.state[i]
        return board

    # given a x,y position, returns the tile within the 1d list
    def index(self, x, y):
        if x >= 0 and x < 10 and y >= 0 and y < 10:
            return self.state[x + y * 10]
        else:
            # out of bounds, return -2 for error
            return -2

    # given an x,y coordinate, and an id of 1 or -1, returns true if this is a valid move
    def canplace(self, x, y, id):
        # square is not empty? return false
        if self.index(x, y) != 0:
            return False
        # these functions compute the 8 different directions
        dirs = [(lambda x: x, lambda y: y - 1), (lambda x: x, lambda y: y + 1), (lambda x: x - 1, lambda y: y - 1),
                (lambda x: x - 1, lambda y: y), (lambda x: x - 1, lambda y: y + 1), (lambda x: x + 1, lambda y: y - 1),
                (lambda x: x + 1, lambda y: y), (lambda x: x + 1, lambda y: y + 1)]
        # for each direction...
        for xop, yop in dirs:
            # move one space.  is the piece the opponent's color?
            i, j = xop(x), yop(y)
            if self.index(i, j) != -id:
                # no, then we'll move on to the next direction
                continue
            # keep going until we hit our own piece
            i, j = xop(i), yop(j)
            while self.index(i, j) == -id:
                i, j = xop(i), yop(j)
            # if we found a piece of our own color, then this is a valid move
            if self.index(i, j) == id:
                return True
                # if I can't capture in any direction, I can't place here
        return False

        # given an x,y coordinate, and an id of 1 or -1, place a tile (if valid) at x,y, and modify the state accordingly

    def place(self, x, y, id):
        # don't bother if it isn't a valid move
        if not self.canplace(x, y, id):
            return
        # place your piece at x,y
        self.state[x + y * 10] = id
        dirs = [(lambda x: x, lambda y: y - 1), (lambda x: x, lambda y: y + 1), (lambda x: x - 1, lambda y: y - 1),
                (lambda x: x - 1, lambda y: y), (lambda x: x - 1, lambda y: y + 1), (lambda x: x + 1, lambda y: y - 1),
                (lambda x: x + 1, lambda y: y), (lambda x: x + 1, lambda y: y + 1)]
        # go through each direction
        for xop, yop in dirs:
            i, j = xop(x), yop(y)
            # move one space.  is the piece the opponent's color?
            if self.index(i, j) != -id:
                # no, then we can't capture in this direction.  we'll move on to the next one
                continue
            # keep going until we hit our own piece
            while self.index(i, j) == -id:
                i, j = xop(i), yop(j)
            # if we found a piece of our own color, then this is a valid move
            if self.index(i, j) == id:
                k, l = xop(x), yop(y)
                # go back and flip all the pieces to my color
                while k != i or l != j:
                    self.state[k + l * 10] = id
                    k, l = xop(k), yop(l)

    # returns a list of all valid x,y moves for a given id
    def validmoves(self, id):
        moves = []
        for x in range(10):
            for y in range(10):
                if self.canplace(x, y, id):
                    moves = moves + [(x, y)]
        return moves

        # print out the board.  1 is X, -1 is O

    def printboard(self):
        for y in range(10):
            line = ""
            for x in range(10):
                if self.index(x, y) == 1:
                    line = line + "X"
                elif self.index(x, y) == -1:
                    line = line + "O"
                else:
                    line = line + "."
            print(line)

        # state is an end game if there are no empty places

    def end(self):
        return not 0 in self.state

    def scoring(self):
        nID = 0
        pID = 0
        for i in range(100):
            if self.state[i] == 1:
                pID += 1
            elif self.state[i] == -1:
                nID = +1
        return pID - nID

    def greedyScoring(self, id):
        value = 0
        for i in range(100):
            if id == 1:
                value+=1
            else:
                value-=1


    # grade the position on a board, as corners and edges are move valuable due to the nature of the game.
    # credit to http://dhconnelly.com/paip-python/docs/paip/othello.html for the grade idea

    boardGrade = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  0, 100, -10, 10, 3, 3, 10, -10, 100, 0,
                  0, -10, -20, -3, -3, -3, -3, -20, -10, 0,
                  0, 10, -3, 8, 1, 1, 8, -3, 10, 0,
                  0, 3, -3, 1, 1, 1, 1, -3, 3, 0,
                  0, 3, -3, 1, 1, 1, 1, -3, 3, 0,
                  0, 10, -3, 8, 1, 1, 8, -3, 10, 0,
                  0, -10, -20, -3, -3, -3, -3, -20, -10, 0,
                  0, 100, -10, 10, 3, 3, 10, -10, 100, 0,
                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]

    def eval_board(self):
        grade = 0
        for i in range(100):
            if self.state[i] == 1:
                grade += self.boardGrade[i]
            elif self.state[i] == -1:
                grade -= self.boardGrade[i]
        return grade

    def greedy(self, board, id):
        moves = board.validmoves(id)

        for m in range(len(moves)):
            moves[m] = (self.greedyScoring(id), moves[m])
        moves.sort(reverse=True)
        topscore = moves[0][0]
        # move forward until stop seeing that score
        index = 0
        while index < len(moves) and moves[index][0] == topscore:
            index += 1
        moves = moves[:index]
        # pick one randomly from the best moves
        move = moves[random.randrange(0, len(moves))]
        # remove the score
        move = move[1]
        return move

    def minimax_ndepth(self, board, id, depth):

        if depth == 0:
            return self.evaluate()

        if self.end():
            return print(" Game over: ".self.evalute(), " wins ")

        best_move = None
        best_board_value = None
        searchBoard = board.copy()

        moves = searchBoard.validmoves(id)
        for i in range(len(moves)):
            print("move contains: ", moves, " move[0] is : ", moves[0])
            move = moves[i]
            print("move is holding: ", move)
            if self.canplace(move[0], move[1], id):
                searchBoard.place(move[0], move[1], id)
        # get player +1's best position/movement
        if id == 1:
            for move in moves:
                newBoard = searchBoard.copy()
                newBoard.place(move[0], move[1], id)
                tempVal = self.scoring()
                if best_board_value is None or tempVal > (best_board_value, best_move)[0]:
                    print("TV and move are: ", tempVal, move)
                    (best_board_value, best_move) = (tempVal, move)
        if id == -1:
            for move in moves:
                newBoard = searchBoard.copy()
                newBoard.place(move[0], move[1], id)
                tempVal = self.scoring()
                if best_board_value is None or tempVal > (best_board_value, best_move)[0]:
                    (best_board_value, best_move) = (tempVal, move)
        print("ndepth is returning: ", (best_board_value, best_move)[1])
        return (best_board_value, best_move)[1]

    def alpha_beta_pruning(self, id, depth, alpha, beta):

        if depth == 0:
            return self.eval_board()

        if self.end():
            return self.scoring()

        moves = self.validmoves(id)

        if id == 1:
            for move in moves:
                newBoard = self.copy()
                newBoard.canplace(move[0], move[1], id)

                alpha = max(alpha, self.alpha_beta_pruning(id, depth - 1, alpha, beta))
                if beta <= alpha:
                    return
            return alpha

        if id == -1:
            for move in moves:
                newBoard = self.copy()
                newBoard.canplace(move[0], move[1], id)

                beta = min(beta, self.alpha_beta_pruning(id, depth - 1, alpha, beta))
                if beta <= alpha:
                    return
            return beta

    def next_best_move(self, board, id, depth):

        best_move = None
        print("ndepth is returning: ", board.minimax_ndepth(board, id, depth))
        best_board_value = board.minimax_ndepth(board, id, depth)
        print("BBV is : ", best_board_value)
        moves = board.validmoves(id)

        if id == 1:
            for move in moves:
                newBoard = board.copy()
                newBoard.place(move[0], move[1], id)
            if best_board_value == max(best_board_value, self.alpha_beta_pruning(id, depth, -INFIN, INFIN)):
                best_move = move

        if id == -1:
            for move in moves:
                newBoard = board.copy()
                newBoard.place(move[0], move[1], id)
            if best_board_value == min(best_board_value, self.alpha_beta_pruning(id, depth, -INFIN, INFIN)):
                best_move = move
        return best_move


# this plays a game between two players that will play completely randomly
def game():
    # make the starting board
    board = Board()
    print("starting board:")
    board.printboard()
    # start with player 1
    turn = 1
    while True:
        # get the moves

        # Do this one(v) for Pruning.
        movelist = board.next_best_move(board, turn, 2)

        #do this one for nDepth, Also go to line 213 and change the [0] to a [1]
        #movelist = board.minimax_ndepth(board, turn, 2)

        #do this one for greedy
        # movelist = board.greedy(board, turn)

        print("Move Lsit contains: ", movelist)
        # movelist = board.validmoves(turn)
        # no moves, skip the turn
        if len(movelist) == 0:
            turn = -turn
            continue
        # pick a move totally at random

        # i = random.randint(0, len(movelist) - 1)
        # make a new board
        board = board.copy()
        # make the move
        # since movelist is a tuple, accessing it as [0], [1]
        board.place(movelist[0], movelist[1], turn)
        # board.place(movelist[i][1], movelist[0][i], turn)
        # swap players
        turn = -turn
        # print
        board.printboard()
        # wait for user to press a key
        input()
        # game over? stop.
        if board.end():
            break
    print("Score is", board.evaluate())


game()

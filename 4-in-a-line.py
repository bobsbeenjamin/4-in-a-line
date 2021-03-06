#-----------------------------------------------------------------------------------------
# Name:      4-in-a-line.py
# Authors:   Ben Clifford, Jovanni Cutigni
# Class:     CS 420: AI
# Created:   2014-05-22
# Due:       2014-06-06
#-----------------------------------------------------------------------------------------

# Imports #
import time
from evalboard import evalBoard
# Globals #
logStr = "Welcome to the 4-in-a-line Program!"

##########################################################################################
##############################          MAIN         #####################################
##########################################################################################

def main():
    # Main code is wrapped in a try block in case user needs to interrupt execution early
    try:
        computerFirst, timeLimit = setup()
        board = "----------------------------------------------------------------"
        if computerFirst:
            logMe("I will go first")
            board, nextMove = makeMyMove(board, timeLimit)
            displayBoard(board)
            logMe(nextMove)
        else:
            logMe("You get to go first")
        # Loop exits when there is a winner or the game is a draw
        while True:
            board = getUserMove(board)
            displayBoard(board)
            if winner(board):
                logMe("You win!  :-(")
                break
            board, nextMove = makeMyMove(board, timeLimit)
            displayBoard(board)
            logMe(nextMove)
            if winner(board):
                logMe("I win!  :-)")
                break
            if drawGame(board):
                logMe("Game is a draw!  :-/")
                break

    # This ensures that output will still be printed
    except KeyboardInterrupt:
        logMe("Keyboard interrupt detected")
        return

    finally:
        logMe("End of program")
        # It is very handy to always create the log file
        createOutputFile()


##########################################################################################
##############################        HELPERS        #####################################
##########################################################################################

def setup():
    """Gets some info from the user that will be used throughout the game.
    @return computerFirst: True if the computer will go first; False otherwise
    @return timeLimit: int with number of seconds for the computer to 'think'"""
    computerFirst = raw_input("Would you like to go first? (y/n): ")=='n' # <- notice this
    timeLimit = raw_input("How long should the computer think (in sec)? : ")
    return computerFirst, int(timeLimit)


def getUserMove(board):
    """Prompts the user for a move, and (if needed) reprompts until the user enters a
    valid move. A valid move is of the form 'B6', where the first character is in the
    range A-H, and the second character is in the range 1-8. The user's move is then
    converted to an int representing the index in board (which is a string). Finally,
    board is updated and returned.
    @return board, updated with userMove"""
    # Used to catch bad moves
    class BadMoveException:
        pass
    # Returns once user enters an acceptable move
    while True:
        try:
            userMove = raw_input("Choose your next move: ")
            if not len(userMove)==2:
                raise BadMoveException
            # Inspect first char (row)
            row = userMove[0]
            row = ord(row) - 65 # 65 is ASCII char 'A'
            if row > 8: # allow the user to enter a lower-case character
                row -= 32
            if not(row>=0 and row<=7):
                raise BadMoveException
            # Inspect second char (column)
            col = userMove[1]
            col = ord(col) - 49 # 49 is ASCII char '1'
            if not(col>=0 and col<=7):
                raise BadMoveException
            # Convert userMove to int, and perform one last check to ensure cell is empty
            userMove = row*8 + col
            if board[userMove] != '-':
                raise BadMoveException
            board = board[:userMove] + "O" + board[userMove+1:]
            return board
        except BadMoveException:
            print "Not a legal move!"
            continue


def makeMyMove(board, timeLimit):
    """Generates a 'smart' move, using MINIMAX with alpha-beta pruning. Updates board with
    the move.
    @return Board: Original board, updated with the computer's next move
    @return string: A sentence describing the computer's next move"""
    startTime = time.clock()
    depth = 0
    x_or_o = "X"
    rootBoard = Board(board, 0, None)
    frontier = [rootBoard]
    # Loop exits when time runs out
    while True:
        depth += 1
        newFrontier = []
        for board in frontier:
            # Don't generate successors to a board after we've lost
            if abs(board.value) > -1000000:
                newFrontier.extend(getBestChildren(board, x_or_o))
            if time.clock()-startTime >= timeLimit:
                logMe( "Depth: " + str(depth) + ", Width: " + str(len(newFrontier)) + \
                      " / " + str(len(frontier)) )
                if len(newFrontier) > len(frontier):
                    newFrontier.sort(key=Board.getSortKey)
                    return getBestBoardPlusMove(newFrontier.pop())
                else:
                    frontier.sort(key=Board.getSortKey)
                    return getBestBoardPlusMove(frontier.pop())
        # Overwrite the frontier on each iteration
        frontier = newFrontier
        x_or_o = "X" if x_or_o=="O" else "O"


def getBestChildren(parent, x_or_o):
    """Expands all possible children of parent, prunes away the worst ones, and returns 
    the remaining ones as a set. parent should be a Board object. x_or_o is used both to 
    build the children, and to determine whether 'best' means a high or low minimax value.
    @return set with parent's best children"""
    holdingCell = [] # empty list to hold all possible chilren before pruning
    parentBoard = parent.board # convenient alias
    for cell in range(64):
        if parentBoard[cell]=='-': # only look at 'empty' cells
            newBoard = parentBoard[:cell] + x_or_o + parentBoard[cell+1:]
            value = evalBoard(newBoard)
            newChild = Board(newBoard, value, parent)
            holdingCell.append(newChild)
    # Sort the holdingCell by board value, from highest to lowest value
    holdingCell.sort(key=Board.getSortKey, reverse=True)
    percentageToKeep = .5
    # Make sure that we always keep at least 1
    numToKeep = max(int(len(holdingCell)*percentageToKeep), 1)
    if x_or_o=="X":
        children = set(holdingCell[:numToKeep])
    else:
        children = set(holdingCell[-numToKeep:])
    return children


def getBestBoardPlusMove(leaf):
    """Chains back from leaf to root, then keeps the direct child of root that led to
    leaf. The board of this child is then compared to the board of parent, and the changed
    element is noted.
    @return Board: Best child of root
    @return string: Sentence stating next best move"""
    parent = leaf.parent
    while parent.parent:
        me = parent
        parent = me.parent
    # parent is now root, and me is now its best child
    for idx, cell in enumerate(range(64)):
        if me.board[cell] != parent.board[cell]:
            return me.board, idxToNextMove(idx)
    else:
        logMe("ERROR: root and its best child have identical boards")
        raise Exception


def idxToNextMove(idx):
    """Builds and returns a sentence describing the computer's move, based on idx.
    Example: idx is 10 -> output is "Computer move: b2"
    @return A human-readable sentence"""
    rowElement, colElement = divmod(idx, 8)
    rowElement = chr(rowElement + ord('a'))
    colElement = str(colElement + 1)
    return "Computer move: " + rowElement + colElement


def winner(board):
    """@return -1 if the computer won, 1 if the user won, or 0 if there is no winner"""
    for row in range(0, 64, 8):
        row = board[row:row+8]
        if "XXXX" in row:
            return -1
        if "OOOO" in row:
            return 1
    for col in range(8):
        # Build a string for each column
        col = "".join([board[cell] for cell in range(col, 64, 8)])
        if "XXXX" in col:
            return -1
        if "OOOO" in col:
            return 1
    return 0 # no wins found


def drawGame(board):
    """@return True if the game is tied; False otherwise"""
    return '-' not in board


##########################################################################################
##############################       UTILITIES       #####################################
##########################################################################################

def displayBoard(board):
    """Displays board nicely."""
    logMe() # empty line
    logMe("  1 2 3 4 5 6 7 8")
    boardStr = ""
    for piece in board:
        boardStr += " " + piece
    # Each row is now twice as long
    for row in range(0, 128, 16):
        # Start with the appropriate letter, then add the now-expanded row string
        logMe(chr(row/16+65) + boardStr[row:row+16])


def logMe(strToLog=""):
    """Prints strToLog and adds it to the global logStr, both on a newline. logMe is used
    so that all output is collected on the fly, for easy file storage later."""
    global logStr # allow modification of the global var logStr
    logStr += "\n" + str(strToLog)
    print strToLog


def createOutputFile():
    """Creates a file with all output."""
    with open("output.log", 'w') as output:
        output.write(logStr)


##########################################################################################
################################    BOARD CLASS    #######################################
##########################################################################################

class Board:
    # Constructor
    def __init__(self, board, value, parent):
        self.board = board
        self.value = value
        self.parent = parent

    # These functions allow Python to store instances of Board in containters that require
    # immutable objects, such as sets
    def __hash__(self):
        return hash(self.board)
    def __eq__(self, other):
        return self.board==other.board
    
    # Python's built-in sort can use a function that returns the key to sort by.
    # This is that function.
    def getSortKey(self):
        return self.value


# Required when running Python on Windows (doesn't break code when run on Linux)
if __name__ == '__main__':
    main()

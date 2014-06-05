#-----------------------------------------------------------------------------------------
# Name:      4-in-a-line.py
# Authors:   Ben Clifford, Jovanni Cutigni
# Class:     CS 420: AI
# Created:   2014-05-22
# Due:       2014-06-06
#-----------------------------------------------------------------------------------------

# Imports #
import multiprocessing, random, time
# Globals #
logStr = "Welcome to the 4-in-a-line Program!"

##########################################################################################
##############################          MAIN         #####################################
##########################################################################################

def main():
    # Main code is wrapped in a try block in case user needs to interrupt execution early
    try:
        meFirst, timeLimit = setup()
        board = "----------------------------------------------------------------"
        if meFirst:
            logMe("I will go first")
            board, nextMove = makeMyMove(board, timeLimit)
            displayBoard(board)
            logMe(nextMove)
        else:
            logMe("You get to go first")
        # Loop forcefully exits when there is a winner or the game is a draw
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
    @return meFirst: True if the computer will go first; False otherwise
    @return timeLimit: int with number of seconds for the computer to 'think'"""
    meFirst = raw_input("Would you like to go first? (y/n): ")=='n'
    timeLimit = raw_input("How long should the computer think (in sec)? : ")
    return meFirst, int(timeLimit)
    

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
    while True:
        try:
            userMove = raw_input("Choose your next move: ")
            if not len(userMove)==2:
                raise BadMoveException
            # Inspect first char (row)
            row = userMove[0]
            row = ord(row) - 65 # 65 is ASCII char 'A'
            if row > 8: # maybe the user entered a lower-case character
                row -= 32
            if not(row>=0 and row<=7):
                raise BadMoveException
            # Inspect second char (column)
            col = userMove[1]
            col = ord(col) - 49 # 65 is ASCII char '1'
            if not(col>=0 and col<=7):
                raise BadMoveException
            # Convert userMove to int, and perform one last check to ensure spot is empty
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
    while True:
        depth += 1
        newFrontier = []
        for board in frontier:
            children = getBestChildren(board, x_or_o)
            newFrontier.extend(children)
            if time.clock()-startTime >= timeLimit:
                logMe("Depth: " + str(depth))
                if newFrontier > frontier:
                    newFrontier.sort(key=Board.getSortKey)
                    return getBestBoardPlusMove(newFrontier.pop())
                else:
                    frontier.sort(key=Board.getSortKey)
                    return getBestBoardPlusMove(frontier.pop())
        frontier = newFrontier
        x_or_o = "X" if x_or_o=="O" else "O"
    

def getBestChildren(parent, x_or_o):
    """Expand all possible children of board, prune away the worst ones, and return the 
    remaining ones as a set. board should be a Board object.
    @return set with board's best children"""
    holdingCell = [] # empty list to hold all possible chilren before pruning 
    parentBoard = parent.board # alias
    for cell in range(64):
        if parentBoard[cell]=='-':
            newBoard = parentBoard[:cell] + x_or_o + parentBoard[cell+1:]
            value = evalBoard(newBoard)
            newChild = Board(newBoard, value, parent)
            holdingCell.append(newChild)
    # Sort the holdingCell by board value, from best to worst
    holdingCell.sort(key=Board.getSortKey, reverse=True)
    percentageToKeep = .5
    numToKeep = max(int(len(holdingCell)*percentageToKeep), 1)
    if x_or_o=="X":
        children = set(holdingCell[:numToKeep])
    else:
        children = set(holdingCell[-numToKeep:])
    return children
    

def evalBoard(board):
    """Utility function that takes a board and returns an integer rating of
    the desirability of that state of that board"""
    sum = 0
    # scan every column
    for colStart in xrange(0, 8, 1):
        sum += evalLine(board, xrange(colStart, 64, 8))
    # scan every row
    for rowStart in xrange(0, 64, 8):
        sum += evalLine(board, xrange(rowStart, rowStart + 8, 1))
    return sum
    

def evalLine(board, line):
    """Utility value of a single board line"""
    signFor = lambda c: 1 if c == 'X' else -1 if c == 'O' else 0
    def valueOf(run, count, space):
        if run >= 4:
            # won.
            return 16384
        elif count + space < 4:
            # a non-winning run with no room to expand is worthless
            return 0
        elif count > 0:
            # straight run is best, nearby pieces seperated by spaces good,
            # room to expand is desirable
            bonus = count - run
            return (4 ** run) + (2 ** bonus if bonus > 0 else 0) + space
        else:
            return 0

    total = 0 # sum

    space = 0 # spaces on the ends or within this stretch
    carry = 0 # straight space that carries over
    count = 0 # count of symbols in this stretch (non-contigious)
    run = 0   # count of contigioius symbols
    maxrun = 0
    last = '' # last player symbol encountered

    for i in line:
        c = board[i]

        # total and switch if we encounter a different player symbol
        if c != last and c != '-':
            # switch symbols, end run
            total += valueOf(maxrun, count, space) * signFor(last)
            space, count, run, maxrun = carry, 0, 0, 0
            last = c

        # count it
        if c == '-':
            space += 1
            carry += 1
            run = 0 # run broken by space
        else:
            if carry > 2 and len(last) > 0:
                # too much space between same symbol, end run
                total += valueOf(maxrun, count, space) * signFor(last)
                space, count, run, maxrun = carry, 0, 0, 0
                # don't reset last
            run += 1
            maxrun = max(run, maxrun)
            count += 1
            carry = 0 # space run broken

    #finished scanning line
    if (count > 0):
        # have leftovers, end run
        total += valueOf(maxrun, count, space) * signFor(last)
        space, count, run, maxrun = carry, 0, 0, 0
        last = ''

    return total
    

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
    """@return a nice string representation of the idx on a board"""
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
##        self.depth = depth
    
    # These functions allow Python to store instances of Board in containters that require 
    # immutable objects, such as sets
    def __hash__(self):
        return hash(self.board)
    def __eq__(self, other):
        return self.board==other.board
    
    def getSortKey(self):
        """Python's built-in sort can use a function that returns the key to sort by.
        This is it."""
        return self.value
    

# Required when running Python on Windows (doesn't break code when run on Linux)
if __name__ == '__main__':
    main()

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
            board = makeMyMove(board)
            displayBoard(board)
        else:
            logMe("You get to go first")
        # Loop forcefully exits when there is a winner or the game is a draw
        while True:
            board = getUserMove(board)
            displayBoard(board)
            if winner(board):
                logMe("You win!  :-(")
                break
            board = makeMyMove(board, timeLimit)
            displayBoard(board)
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
    the move, and returns it.
    @return board, updated with userMove"""
    startTime = time.clock()
    frontier = [board]
    while True:
        for board in frontier:
            pass

def evalBoard(board):
    """Utility function that takes a board and returns an integer rating of
    the desirability of that state of that board
    @return int, where the larger the number the better the move (negative is bad)"""
    sum = 0
    # scan every column
    for colStart in xrange(0, 8, 1):
        sum += evalLine(board, xrange(colStart, 64, 8))
    # scan every row
    for rowStart in xrange(0, 64, 8):
        sum += evalLine(board, xrange(rowStart, 64, 1))
    return sum
    

def evalLine(board, line):
    """Utility value of a single board line"""
    signFor = lambda c: 1 if c == 'X' else -1 if c == 'O' else 0
    def valueOf(count, space):
        return 2048 if length >= 4 else (2 ** length) + space

    total = 0 # sum
    space = 0 # spaces on the ends or within this run
    carry = 0 # straight space that carries over
    count = 0 # contiguous run length of player symbols
    last = '' # last player symbol encountered

    for i in line:
        c = board[i]

        # total and switch if we encounter a different player symbol
        if c != last and c != '-':
            # switch symbols, end run
            total += valueOf(count, space) * signFor(last)
            space = carry
            count = 0
            last = c

        # count it
        if c == '-':
            space += 1
            carry += 1
            if carry >= 3 and len(last) > 0:
                # too much contigious space, end run
                total += valueOf(count, space) * signFor(last)
                space = carry
                count = 0
                last = ''
        else:
            count += 1
            carry = 0

    if (count > 0):
        # have leftovers, end run
        total += valueOf(count, space) * signFor(last)
        space = carry
        count = 0
        last = ''
    

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
        col = "".join([board[cell+col] for cell in range(0, 64, 8)])
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

# NOTE to Jovanni: This board class may be useful. But it's still a work in progress. Of 
# course, we may just forget this and use another data structure entirely. :-/
class Board:
    # Constructor
    def __init__(self, board, minimax, depth):
        self.board = board
##        self.xBoard, self.oBoard = self.encodeBoard(board)
        self.minimax = minimax
        self.depth = depth
        
    def encodeBoard(self, board):
        """Boards can be stored as 32 character strings rather than 64 character ones."""
        # Encode X's
        bitString = "".join(["1" if piece=="X" else "0" for piece in board])
        xBoard = int(bitString, 2)
##        xBoard = '{0:16x}'.format(xBoard)
        # Encode O's
        bitString = "".join(["1" if piece=="O" else "0" for piece in board])
        oBoard = int(bitString, 2)
##        oBoard = '{0:16x}'.format(oBoard)
        # Joing together into unified string and return it
        return xBoard, oBoard
        
    def getOrder(self):
        """Python's built-in sort can use a function that returns the key to sort by.
        This is it."""
        return self.depth
    

# Required when running Python on Windows (doesn't break code when run on Linux)
if __name__ == '__main__':
    main()

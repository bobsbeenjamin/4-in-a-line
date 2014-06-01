#-----------------------------------------------------------------------------------------
# Name:      4-in-a-line_PregameComputer.py
# Authors:   Ben Clifford, Jovanni Cutigni
# Class:     CS 420: AI
# Created:   2014-05-24
# Due:       2014-06-06
#-----------------------------------------------------------------------------------------

# Imports #
import multiprocessing, random, time
# Globals #
logStr = "This is the pregame computer..."
boardDict = []

##########################################################################################
##############################          MAIN         #####################################
##########################################################################################

def main():
    # Main code is wrapped in a try block in case user needs to interrupt execution early
    try:
        option = raw_input("Enter 1 to precompute, or 2 to interpret results")
        if option=="1":
            depth = raw_input("How deep to start computations?")
            logMe("Values will be calculated starting at depth " + depth)
            time.clock() # start timer
            precompute(depth)
        else:
            time.clock() # start timer
            interpret()
        # log time difference in seconds
        logMe("Operation took " + str(time.clock()) )
    
    # This ensures that output/computations will still be printed 
    except KeyboardInterrupt:
        logMe("Keyboard interrupt detected")
        return
    
    finally:
        if option=="1":
            dumpValues()
            createOutputFile("precomputedValues.dat")
        if option=="2":
            createOutputFile("pickledValues.dat")
        logMe("End of program")
    

##########################################################################################
##############################      MAIN METHODS     #####################################
##########################################################################################

def precompute(depth):
    """Generates all possible board states consisting of depth number of pieces on board, 
    then recursively determines actual minimax values for all board states starting at 
    level depth and reaching down to level 64 (full board).
    @return Array with all computed boards, stored as Board objects"""
    # NOTE to Jovanni: This is not working yet. The function documentation shows what it 
    # should do.
    boards = createAllBoardsAtSingleDepth(int(depth), False, 1)
    logMe( "Number of boards created: " + str(len(boards)) )
##    return # comment this out to see all of the boards
    for board in boards:
        logMe(board)
        return
        displayBoard(board)
    

def createAllBoardsAtSingleDepth(depth, partialBoard, x_or_o):
    """Recursively creates all board states with depth number of pieces. When this is 
    called outside of itself, partialBoard should be False, and x_or_o should be 1.
    @return Array with all created boards, stored as arrays of -1's , 0's and 1's"""
    boards = [] # this holds all boards that will actually be returned by this function
    x_or_o = 1
    n = 0 # this is unnecessary, but makes the code more readable
    while n < depth:
        # Holds all valid boards with (depth-n) pieces; clear array for each n
        boardsAtThisSubLevel = [] 
        # Base case: for each spot on the board, create a unique board with an X 
        if n==0:
            for idx in range(64):
                newBoard = [0]*64
                newBoard[idx] = x_or_o
                boardsAtThisSubLevel.append(newBoard)
        # The 'recursive' part of this iterative function
        else:
            for prevBoard in boardsAtPrevSubLevel:
                for idx in range(64):
                    if not prevBoard[idx]: # only place piece on empty spot
                        newBoard = prevBoard[:] # local copy
                        newBoard[idx] = x_or_o
                        boardsAtThisSubLevel.append(newBoard)
        # Combine new boards with master set
        boards = boardsAtThisSubLevel
        # This effectively copies the current board set to a new variable (quick style)
        boardsAtPrevSubLevel = boardsAtThisSubLevel
        # Update move value (x_or_o) and sublevel (n)
        x_or_o *= -1
        n += 1
    return boardsAtThisSubLevel
    

def interpret():
    """This will turn a nice output file into a pickle file"""
    pass
    

def dumpValues():
    """This will prepare all values for printing to a file"""
    pass
    

##########################################################################################
##############################       UTILITIES       #####################################
##########################################################################################

def displayBoard(board):
    """Displays board nicely."""
    logMe("  1 2 3 4 5 6 7 8")
    boardStr = ""
    for piece in board:
        if piece==1:
            boardStr += " X"
        if piece==-1:
            boardStr += " O"
        if piece==0:
            boardStr += " -"
    for row in range(0, 128, 16):
        logMe(chr(row/8+65) + boardStr[row:row+16])
    # NOTE to Jovanni: The commented code below is an alternate way to display the board 
    # that works well too. I was testing both to see which performs faster (this is useful
    # for testing). The 2 algorithms perform about the same, so I kept the easier read.
##    for row in range(8):
##        # Start with one of the characters A-H
##        rowStr = chr(row+65) + " "
##        # Set up string builder
##        row *= 8
##        row = board[row:row+8]
##        # Build each row via list comprehension and display it
##        rowStr += " ".join(["X" if cell==1 else "O" if cell==-1 else "-" for cell in row])
##        logMe(rowStr)
    

def logMe(strToLog="", runSilent=False):
    """Prints strToLog and adds it to the global logStr, both on a newline. logMe is used 
    so that all output is collected on the fly, for easy file storage later."""
    global logStr # this allows modification of the global var logStr
    logStr += "\n" + str(strToLog)
    if not runSilent:
        print strToLog
    

def createOutputFile(fileName="output.log"):
    """Creates a file with all output."""
    with open(fileName, 'wb') as output:
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

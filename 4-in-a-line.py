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
        board = "----------------------------------------------------------------"
        move = getUserMove(board)
        board = board[:move] + "O" + board[move+1:]
        displayBoard(board)
    
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

def getUserMove(board):
    """Prompts the user for a move, and (if needed) reprompts until the user enters a 
    valid move. A valid move is of the form 'B6', where the first character is in the 
    range A-H, and the second character is in the range 1-8. The user's move is then 
    converted and returned as an int representing the index in a 1-D 64-length board.
    @return a valid move entered by the user"""
    while True:
        try:
            userMove = raw_input("Choose your next move: ")
            if not len(userMove)==2:
                raise Exception
            # Inspect first char (row)
            row = userMove[0]
            row = ord(row) - 65 # 65 is ASCII char 'A'
            if row > 8: # maybe the user entered a lower-case character
                row -= 32
            if not(row>=0 and row<=7):
                raise Exception
            # Inspect second char (column)
            col = userMove[1]
            col = ord(col) - 49 # 65 is ASCII char '1'
            if not(col>=0 and col<=7):
                raise Exception
            # Convert userMove to int, and perform one last check to ensure spot is empty
            userMove = row*8 + col
            if board[userMove] != '-':
                raise Exception
            return userMove
        except:
            print "Not a legal move!"
            continue
    

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

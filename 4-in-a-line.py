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
        pass
   
    # This ensures that output will still be printed 
    except KeyboardInterrupt:
        logMe("Keyboard interrupt detected")
        return
    
    finally:
        logMe("End of program")
        # It is very handy to always create the log file
        createOutputFile()
    

##########################################################################################
##############################       UTILITIES       #####################################
##########################################################################################

# TODO: Rewrite
def displayBoard(board):
    """Prints board to stdout in a friendly format."""
    # Empty board
    if not board:
        logMe("No solution found :-(")
        return
    # Note: List comprehension is used a few times below for speed
    # Print column 'header'
    header = "  |" + "|".join([str(i).rjust(2) for i in range(n)])
    logMe(header)
    for idx, queen in enumerate(board):
        # Print a clean seperator between rows
        sep = "--+" + "+".join(["--" for i in range(n)])
        logMe(sep)
        # Print idx, right justified, then print the remaining line
        line = str(idx).rjust(2)  + "|" \
               + "|".join(["Q " if i==queen else "  " for i in range(n)])
        logMe(line)
    

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

# TODO: Rewrite
class Board:
    # Constructor
    def __init__(self, board, fitness):
        self.board = board
        self.fitness = fitness
    
    # Python's built-in sort can use a function that returns the key to sort by
    def getFitness(self):
        return self.fitness


# Required when running Python on Windows (doesn't break code when run on Linux)
if __name__ == '__main__':
    main()

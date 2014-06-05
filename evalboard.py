#-----------------------------------------------------------------------------------------
# Name:      evalboard.py
# Authors:   Ben Clifford, Jovanni Cutigni
# Class:     CS 420: AI
# Created:   2014-06-05
# Due:       2014-06-06
#-----------------------------------------------------------------------------------------

def evalBoard(board):
    """Utility function that takes a board and returns an integer rating of
    the desirability of that state of that board"""
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

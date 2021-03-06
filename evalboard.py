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
        sum += evalLine(board, xrange(rowStart, rowStart + 8, 1))
    return sum

def evalLine(board, line):
    """Utility value of a single board line"""
    signedFor = lambda x, c: x if c == 'X' else (-x * 12) / 10 if c == 'O' else 0
    def valueOf(run, count, space):
        if run >= 4:
            # won.
            return 100000000
        elif count + space < 4:
            # a non-winning run with no room to expand is worthless
            return 0
        elif count > 0:
            # straight run is best, nearby pieces seperated by spaces good,
            # room to expand is desirable
            bonus = count - run
            space = min(space, 5 - run)
            return (run ** 8) + (bonus ** 4 if bonus > 0 else 0) + space ** 2
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
            total += signedFor(valueOf(maxrun, count, space), last)
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
                total += signedFor(valueOf(maxrun, count, space), last)
                space, count, run, maxrun = carry, 0, 0, 0
                # don't reset last
            run += 1
            maxrun = max(run, maxrun)
            count += 1
            carry = 0 # space run broken

    #finished scanning line
    if (count > 0):
        # have leftovers, end run
        total += signedFor(valueOf(maxrun, count, space), last)
        space, count, run, maxrun = carry, 0, 0, 0
        last = ''

    return total

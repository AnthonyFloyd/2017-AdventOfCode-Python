'''
Advent of Code 2017
Day 10: Knot Hash

'''

TEST_INPUT = '3,4,1,5'
TEST_SIZE = 5

NROUNDS = 64

DAY10_INPUT = '225,171,131,2,35,5,0,13,1,246,54,97,255,98,254,110'
DAY10_SIZE = 256

def computeHashCheck(ringInputString, ringSize):
    """Calculate the knot hash check.

    Args:
        ringInputString (str): The list of ints to be hashed as a comma-separated list.
        ringSize (int): The size of the ring to be \"knotted\".

    Returns:
       int: Value of the hash check.

    """

    ringInputList = [int(i) for i in ringInputString.split(',')]
    ringContents = [i for i in range(ringSize)]

    cursorPosition = 0
    skipSize = 0

    # Hashing algorithm as defined in AoC Day 10 instructions...
    for length in ringInputList:
        #
        # Duplicate the ring contents to allow for exceeding the length of the original list
        #
        doubleContents = ringContents + ringContents

        # Reverse the order of that length of elements in the list, starting with the element
        # at the current position
        sublist = doubleContents[cursorPosition:cursorPosition+length]
        sublist.reverse()
        doubleContents[cursorPosition:cursorPosition+length] = sublist

        if cursorPosition + length > ringSize:
            ringContents = doubleContents[ringSize:cursorPosition+ringSize] + doubleContents[cursorPosition:ringSize]
        else:
            ringContents = doubleContents[:ringSize]

        # Move the current position forward by that length plus the skip size
        cursorPosition = cursorPosition + length + skipSize

        # Deal with going around the ring
        if cursorPosition > ringSize:
            cursorPosition -= ringSize

        # Increase the skip size by one
        skipSize += 1

    # The hash is then the product of the first two elements in the transformed list
    check = ringContents[0] * ringContents[1]

    #print(ringContents)

    return check

def computeKnot(ringInputString, ringSize):
    """Calculate the knot hash.

    Args:
        ringInputString (str): A string of bytes (characters) for hashing.
        ringSize (int): The size of the ring to be \"knotted\".

    Returns:
       str: Dense hash expressed in hex.

    """
    # First convert the string characters to their corresponding ASCII code,
    # put them into a nice list
    ringInputList = [ord(i) for i in ringInputString]
    ringContents = [i for i in range(ringSize)]

    # add salt
    ringInputList.extend([17, 31, 73, 47, 23])

    cursorPosition = 0
    skipSize = 0

    # The knotting algorithm specifies 64 rounds of knotting
    # Same algorithm as above, reproduced to avoid the "checking" part of
    # the algorithm
    for _ in range(NROUNDS):
        # Knotting algorithm as before
        for length in ringInputList:
            # Double the ring
            doubleContents = ringContents + ringContents

            # Reverse the specified range
            sublist = doubleContents[cursorPosition:cursorPosition+length]
            sublist.reverse()
            doubleContents[cursorPosition:cursorPosition+length] = sublist

            # Account for going over the size of the ring
            if cursorPosition + length > ringSize:
                ringContents = doubleContents[ringSize:cursorPosition+ringSize] + doubleContents[cursorPosition:ringSize]
            else:
                ringContents = doubleContents[:ringSize]

            # Adjust the cursor position by adding the length and the skip size, accounting for going around the ring
            cursorPosition += length + skipSize
            cursorPosition = cursorPosition % ringSize

            # The skip size increments by one each round
            skipSize += 1

    # make dense hash
    denseHash = []

    for counter in range(16):
        #
        # NB: This only works for a dense hash size of 16
        #
        # Calculates a bitwise XOR on each consecutive block of 16 numbers
        #
        subHash = ringContents[0 + counter*16] ^ \
            ringContents[1 + counter*16] ^ \
            ringContents[2 + counter*16] ^ \
            ringContents[3 + counter*16] ^ \
            ringContents[4 + counter*16] ^ \
            ringContents[5 + counter*16] ^ \
            ringContents[6 + counter*16] ^ \
            ringContents[7 + counter*16] ^ \
            ringContents[8 + counter*16] ^ \
            ringContents[9 + counter*16] ^ \
            ringContents[10 + counter*16] ^ \
            ringContents[11 + counter*16] ^ \
            ringContents[12 + counter*16] ^ \
            ringContents[13 + counter*16] ^ \
            ringContents[14 + counter*16] ^ \
            ringContents[15 + counter*16]

        denseHash.append(subHash)

    # convert the dense hash values to a concatenated string of two-digit hex numbers
    denseHashString = ''.join(['{0:02x}'.format(i) for i in denseHash])

    return denseHashString

if __name__ == '__main__':

    testCheck = computeHashCheck(TEST_INPUT, TEST_SIZE)
    print('Test check: {0:d}'.format(testCheck))

    part1Check = computeHashCheck(DAY10_INPUT, DAY10_SIZE)
    print('Part 1 check: {0:d}'.format(part1Check))

    part2Hash = computeKnot('1,2,3', DAY10_SIZE)
    print('Part 2 test 1 hash: {0}'.format(part2Hash))

    part2Hash = computeKnot(DAY10_INPUT, DAY10_SIZE)
    print('Part 2 hash: {0}'.format(part2Hash))


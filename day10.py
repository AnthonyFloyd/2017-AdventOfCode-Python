'''
Advent of Code 2017
Day 10: Knot Hash

'''

TEST_INPUT = '3,4,1,5'
TEST_SIZE = 5

DAY10_INPUT = '225,171,131,2,35,5,0,13,1,246,54,97,255,98,254,110'
DAY10_SIZE = 256

def computeHash(ringInputString, ringSize):



    ringInputList = [int(i) for i in ringInputString.split(',')]
    ringContents = [i for i in range(ringSize)]

    cursorPosition = 0
    skipSize = 0

    for length in ringInputList:
        doubleContents = ringContents + ringContents

        sublist = doubleContents[cursorPosition:cursorPosition+length]
        sublist.reverse()

        doubleContents[cursorPosition:cursorPosition+length] = sublist

        if cursorPosition + length > ringSize:
            ringContents = doubleContents[ringSize:cursorPosition+ringSize] + doubleContents[cursorPosition:ringSize]
        else:
            ringContents = doubleContents[:ringSize]

        cursorPosition = cursorPosition + length + skipSize
        if cursorPosition > ringSize:
            cursorPosition -= ringSize

        skipSize += 1

    check = ringContents[0] * ringContents[1]

    print(ringContents)

    return check

def computeKnot(ringInputString, ringSize):

    ringInputList = [ord(i) for i in ringInputString]
    ringContents = [i for i in range(ringSize)]

    # add salt
    ringInputList.extend([17, 31, 73, 47, 23])

    cursorPosition = 0
    skipSize = 0

    for round in range(64):
        for length in ringInputList:
            doubleContents = ringContents + ringContents

            sublist = doubleContents[cursorPosition:cursorPosition+length]
            sublist.reverse()

            doubleContents[cursorPosition:cursorPosition+length] = sublist

            if cursorPosition + length > ringSize:
                ringContents = doubleContents[ringSize:cursorPosition+ringSize] + doubleContents[cursorPosition:ringSize]
            else:
                ringContents = doubleContents[:ringSize]

            cursorPosition += length + skipSize
            cursorPosition = cursorPosition % ringSize

            skipSize += 1

    # make dense hash
    denseHash = []

    for counter in range(16):
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

    # convert to hex

    denseHashString = ''.join(['{0:02x}'.format(i) for i in denseHash])

    #print(denseHashString)

    return denseHashString

if __name__ == '__main__':

    testCheck = computeHash(TEST_INPUT, TEST_SIZE)
    print('Test check: {0:d}'.format(testCheck))

    part1Check = computeHash(DAY10_INPUT, DAY10_SIZE)
    print('Part 1 check: {0:d}'.format(part1Check))

    part2Hash = computeKnot('1,2,3', DAY10_SIZE)
    print('Part 2 test 1 hash: {0}'.format(part2Hash))

    part2Hash = computeKnot(DAY10_INPUT, DAY10_SIZE)
    print('Part 2 hash: {0}'.format(part2Hash))





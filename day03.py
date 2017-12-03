'''
Advent of Code 2017
Day 3: Spiral Memory

'''

import unittest
import numpy

# Inputs and tests

PART1_TESTS = [(1, 0),
               (12, 3),
               (23, 2),
               (1024, 31)]

PART1_END = 289326

PART2_TESTS = [(2, 4),
               (4, 5),
               (5, 10),
               (10, 11),
               (11, 23),
               (59, 122),
               (747, 806),
               (800, 806)]

PART2_TARGET = PART1_END

DEBUG = False

# Solution

def findCoordinates(squareID):
    '''
    Finds the x,y coordinates of a particular squareID.

    Input is the squareID as an integer, output is a tuple
    containing the integer coordinates of the square (x, y)

    '''

    global DEBUG

    # The squares are arranged in a counter-clockwise spiral
    # The origin square, 1, is taken at (0, 0)

    # Spiral consists of rings of increasing size: 1, 3, 5, 7, etc
    # The number of new squares in each ring is:
    #   newSquares = size * 2 + (size - 2) * 2
    #              = 4 * size - 4 = 4 * (size - 1)

    # This doesn't work for square 1, special exception for it
    if squareID == 1:
        return (0, 0)

    size = getLastFullRingSize(squareID)

    currentRingStartID = size ** 2 + 1
    distanceFromRingStart = squareID - currentRingStartID

    # now we need to find the location of the target in the next ring
    size += 2

    # ok, now find the (x, y) coordinates the distance along the ring
    # 3 = (1, 0)
    # 5 = (2, 1)
    # 7 = (3, 2)
    # n = ((n-1)/2, (n-1)/2-1)

    location = [(size - 1)//2, 1 - (size - 1)//2]

    # march around the ring

    remainingDistance = distanceFromRingStart

    # up
    if remainingDistance <= (size - 2):
        # we only need to go up
        location = [location[0], location[1] + remainingDistance]
        remainingDistance = 0
    else:
        # go up as much as possible
        location = [location[0], location[1] + (size - 2)]
        remainingDistance -= (size - 2)

    # left
    if remainingDistance <= (size - 1):
        # only need to go left
        location = [location[0] - remainingDistance, location[1]]
        remainingDistance = 0
    else:
        # go left as much as possible
        location = [location[0] - (size - 1), location[1]]
        remainingDistance -= (size - 1)

    # down
    if remainingDistance <= (size - 1):
        # only need to go down
        location = [location[0], location[1] - remainingDistance]
        remainingDistance = 0
    else:
        # go down as much as possible
        location = [location[0], location[1] - (size - 1)]
        remainingDistance -= (size - 1)

    # can only go right now
    location = [location[0] + remainingDistance, location[1]]

    # we're done! return the location

    return (location[0], location[1])

def getLastFullRingSize(squareID):
    '''
    Returns the size of the last full "ring" in the spiral.

    Input is the squareID as an int, output is the ring size as an int.
    '''

    global DEBUG

    if squareID == 1:
        return 1

    # Find the biggest ring that doesn't contain the target square

    size = -1 # Need to start at zero, but sizes are odd, so
    totalSquares = 1 # And, because we have a special exception for the first one, we need to count it

    while True:
        size += 2
        totalSquares += 4 * (size - 1)

        # If squareID is bigger than then current number of squares
        # and less than the current squares + the next layer
        # then we've found the right ring

        if squareID > totalSquares  and squareID <= totalSquares + 4 * (size + 1):
            # found the right ring size
            break

    return size


def findManhattanDistance(start, end):
    '''
    Finds the 'Manhattan Distance' between two squares on the spiral.

    Inputs are the integer square IDs, output is the integer distance.

    '''

    global DEBUG

    # Find the start and end coordinates
    startLocation = findCoordinates(start)
    endLocation = findCoordinates(end)

    # The Manhattan Distance is just the sum of the delta x and delta y
    distance = abs(startLocation[0] - endLocation[0]) + abs(startLocation[1] - endLocation[1])

    return int(distance)

def findNextAccumulation(target):
    '''
    Finds the smallest value larger than the input in the spiral accumulation.

    Input is the target value that needs to be exceeded, output is the next value in the accumulation sequence.

    '''

    global DEBUG

    # special exception for the first square
    if target == 1:
        return 1

    # We're going to need to keep track of old values in a matrix
    # The matrix size is no larger than the ring size that holds the target value

    matrixSize = getLastFullRingSize(target) + 4
    spiralMatrix = numpy.zeros((matrixSize, matrixSize), dtype=int)

    # populate the spiral until we exceed the target
    x1 = (matrixSize - 1) // 2
    y1 = x1

    # start at the beginning
    location = [x1, y1] # (0, 0)
    total = 1
    spiralMatrix[location[0]][location[1]] = total
    currentSquareID = 1

    # Loop until we've exceeded the target value
    while total <= target:
        # move to the next location
        currentSquareID += 1

        # do we need to move to the next ring?

        size = getLastFullRingSize(currentSquareID)
        currentRingStartID = size ** 2 + 1
        distanceFromRingStart = currentSquareID - currentRingStartID

        if DEBUG:
            print('Square {:d} is {:d} from the start of the ring'.format(currentSquareID, distanceFromRingStart))

        size += 2 # Sizes are always odd

        if distanceFromRingStart == 0:
            # start a new ring, move right one, down one
            if DEBUG:
                print("Starting new ring")
                print("Old location: {:d}, {:d}".format(location[0] - x1, location[1] - y1))

            location = [location[0] + 1, location[1]]

        else:
            # move the current location based on where we are along the perimeter
            if distanceFromRingStart <= (size - 2):
                # go up one
                location = [location[0], location[1] + 1]
            elif distanceFromRingStart <= ((size - 2) + (size - 1)):
                # go left
                location = [location[0] - 1, location[1]]
            elif distanceFromRingStart <= ((size - 2) + 2*(size - 1)):
                # go down
                location = [location[0], location[1] - 1]
            else:
                # go right
                location = [location[0] + 1, location[1]]

        # find the value to put in the new spot
        # find sum of all neighbours
        if DEBUG:
            print("New location: {:d}, {:d}".format(location[0] - x1, location[1] - y1))

        # For code clarity
        x = location[0]
        y = location[1]


        # NB: Can't just assign this to spiralMatrix[x, y] because we break of the while loop based on total
        # and x and y change as we march around the spiral

        total = spiralMatrix[x+1][y] + spiralMatrix[x+1][y+1] + spiralMatrix[x][y+1] + spiralMatrix[x-1][y+1] \
            + spiralMatrix[x-1][y] + spiralMatrix[x-1][y-1] + spiralMatrix[x][y-1] + spiralMatrix[x+1][y-1]

        spiralMatrix[x, y] = total

    # only get here if we found a value bigger than the target!

    if DEBUG:
        print("Location: {:d},{:d}".format(x, y))
        print("{:6d} {:6d} {:6d}".format(spiralMatrix[x-1][y+1], spiralMatrix[x][y+1], spiralMatrix[x+1][y+1]))
        print("{:6d} {:6d} {:6d}".format(spiralMatrix[x-1][y], spiralMatrix[x][y], spiralMatrix[x+1][y]))
        print("{:6d} {:6d} {:6d}".format(spiralMatrix[x-1][y-1], spiralMatrix[x][y-1], spiralMatrix[x+1][y-1]))

    return total

# Unit tests

class TestDistance(unittest.TestCase):
    '''
    Tests for Part 1

    '''

    global DEBUG

    # Part 1

    def test_part1(self):
        '''
        Part 1 tests

        '''
        global DEBUG

        DEBUG = True

        for (end, distance) in PART1_TESTS:
            self.assertEqual(findManhattanDistance(1, end), distance)

    # Part 2

    def test_part2(self):
        '''
        Part 2 tests

        '''

        global DEBUG

        DEBUG = True

        for (target, nextResult) in PART2_TESTS:
            self.assertEqual(findNextAccumulation(target), nextResult)

if __name__ == '__main__':

    print('Advent of Code\nDay 3: Spiral Memory\n')
    print('Part 1: {0:d}'.format(findManhattanDistance(1, PART1_END)))
    print('Part 2: {0:d}'.format(findNextAccumulation(PART2_TARGET)))

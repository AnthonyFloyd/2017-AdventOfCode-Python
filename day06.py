'''
Advent of Code 2017
Day 6: Memory Reallocation

'''

import unittest

TEST_BANKS = ('0 2 7 0', 5, 4)
INPUT_BANKS = '0	5	10	0	11	14	13	4	11	8	8	7	1	4	12	11'

def findInfiniteLoop(memoryBanks):
    '''
    Finds the number of iterations required to detect an infinite loop with the given start condition.

    memoryBanks is a list of integers, representing a number of memory banks with items in each.
    Returns the number of iterations until an infinite loop is detected, and the size of the loop.

    '''

    nIterations = 0
    nBanks = len(memoryBanks)
    foundLoop = False

    # create a history of known configurations, starting with the current one
    # use a list instead of a set because sets reorder the items
    # use strings instead of frozensets because frozensets reorder the items

    resultList = [' '.join([str(i) for i in memoryBanks]),]

    while not foundLoop:
        # find the memory bank with the largest quanity
        maximumItems = max(memoryBanks)
        index = memoryBanks.index(maximumItems)

        # Redistribute the items by emptying out the current bank and then
        # giving the rest one of them, looping around the banks
        nIterations += 1
        memoryBanks[index] = 0

        for counter in range(maximumItems):
            index += 1
            if index == nBanks:
                index = 0
            memoryBanks[index] += 1

        # check to see if the current state has been seen before
        currentState = ' '.join([str(i) for i in memoryBanks])

        if currentState in resultList:
            foundLoop = True
            sizeOfLoop = nIterations - resultList.index(currentState)
        else:
            resultList.append(currentState)


    return (nIterations, sizeOfLoop)


# Unit tests

class TestLoops(unittest.TestCase):
    '''
    Tests for Part 1 and Part 2

    '''

    # Part 1

    def test_part1(self):
        '''
        Part 1 tests

        '''

        self.assertEqual(findInfiniteLoop([int(i) for i in TEST_BANKS[0].strip().split()])[0], TEST_BANKS[1])

    ## Part 2

    def test_part2(self):
        '''
        Part 2 tests

        '''

        self.assertEqual(findInfiniteLoop([int(i) for i in TEST_BANKS[0].strip().split()])[1], TEST_BANKS[2])

if __name__ == '__main__':

    print('Advent of Code\nDay 6: Memory Reallocation\n')
    (iterations, loopSize) = findInfiniteLoop([int(i) for i in INPUT_BANKS.strip().split()])
    print('Part 1: {0:d} iterations to infinite loop'.format(iterations))
    print('Part 2: The loop is {0:d} iterations'.format(loopSize))

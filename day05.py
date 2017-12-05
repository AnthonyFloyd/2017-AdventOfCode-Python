'''
Advent of Code 2017
Day 5: A Maze of Twisty Trampolines, All Alike

'''

import unittest

TEST_INSTRUCTIONS = ['0', '3', '0', '1', '-3']
INPUT_INSTRUCTIONS = open('day05-input.txt').readlines()

def followInstructions(instructionString, method=1):
    '''
    Based on a list of jump instructions, determine how many jumps to exit the list.
    After jumping, change the jump instruction just executed.

    Method 1: Increment the jump by 1
    Method 2: If the jump >= 3, decrement by 1. Otherwise increment by 1.

    Input is a list of string integer instructions. Output is the count of jumps to
    exit the list.

    '''

    # turn the jump instructions into a list of ints
    instructionList = [int(i) for i in instructionString]

    # initialize the counter, cursor, and exit flag

    counter = 0
    index = 0
    inList = True
    nInstructions = len(instructionList)

    while inList:
        # we need to hold the current index so we can modify the instruction after we jump
        currentIndex = index

        # move the cursor using the jump instruction at the current location
        index += instructionList[currentIndex]

        # we jumped! Increment the counter
        counter += 1

        # Check to see if we're out of the list
        if index >= nInstructions or index < 0:
            inList = False
        else:
            # still in the list, change the last jump instruction according to the method
            if method == 2 and instructionList[currentIndex] >= 3:
                instructionList[currentIndex] -= 1
            else:
                instructionList[currentIndex] += 1

    return counter

# Unit tests

class TestJumps(unittest.TestCase):
    '''
    Tests for Part 1 and Part 2

    '''

    # Part 1

    def test_part1(self):
        '''
        Part 1 tests

        '''

        # Test the row checksum algorithm
        self.assertEqual(followInstructions(TEST_INSTRUCTIONS, 1), 5)

    # Part 2

    def test_part2(self):
        '''
        Part 2 tests

        '''

        # Test the row checksum algorithm
        self.assertEqual(followInstructions(TEST_INSTRUCTIONS, 2), 10)

if __name__ == '__main__':

    print('Advent of Code\nDay 5: A Maze of Twisty Trampolines, All Alike\n')
    print('Part 1: {0:d} instructions to escape the maze'.format(followInstructions(INPUT_INSTRUCTIONS)))
    print('Part 2: {0:d} instructions to escape the maze'.format(followInstructions(INPUT_INSTRUCTIONS, 2)))

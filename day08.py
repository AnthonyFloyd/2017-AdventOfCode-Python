'''
Advent of Code 2017
Day 8: I Heard You Like Registers

'''

import unittest

# Inputs and tests

TEST_INPUT = """b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10
"""

TEST_RESULTS = (1, 10)

INPUT = open('day08-input.txt').readlines()

COMPARISONS = {
    '>': lambda x, y: x > y,
    '<': lambda x, y: x < y,
    '==': lambda x, y: x == y,
    '>=': lambda x, y: x >= y,
    '<=': lambda x, y: x <= y,
    '!=': lambda x, y: x != y,
}

DIRECTION = {'inc': 1,
             'dec': -1}

# Solution

def doInstructions(inputStringList):
    '''
    With a list of structured instructions detailing how to change values held in
    notional registers, determine the maximum value in a register and the maximum
    value ever containted in a register.

    The input is a list of structured instruction strings. Each instruction string
    has the form:

      <register> <inc|dec> <value> if <register> <op> <threshold>

    Output is a tuple of (currentMax, largestMax)

    '''

    memory = {} # register: value
    absoluteMax = 0

    # Loop over all the instructions
    for inputString in inputStringList:
        (register, direction, value, ifDummy, testRegister, test, testThreshold) = inputString.split()

        # check that both the target and test registers exist, if not, initialize them
        if memory.get(register) is None:
            memory[register] = 0

        if memory.get(testRegister) is None:
            memory[testRegister] = 0

        # "Execute" the comparision in the instruction and add the value if comparison passes
        if COMPARISONS[test](memory[testRegister], int(testThreshold)):
            memory[register] += DIRECTION[direction] * int(value)

        # update the absolute maximum seen
        absoluteMax = max(max(memory.values()), absoluteMax)

    # return both the current maximum and the maximum, ever

    return (max(memory.values()), absoluteMax)

# Unit tests

class TestDoInstructions(unittest.TestCase):
    '''
    Unit tests for Day 8

    '''
    def test_both_parts(self):
        '''
        Tests both Part 1 and Part 2

        '''

        result = doInstructions(TEST_INPUT.splitlines())

        self.assertEqual(result[0], TEST_RESULTS[0])
        self.assertEqual(result[1], TEST_RESULTS[1])


if __name__ == '__main__':
    print('Advent of Code\nDay 8: I Heard You Like Registers\n')

    (maximum, absoluteMaximumEver) = doInstructions(INPUT)
    print('Part 1: The maximum value in a register is {0:d}'.format(maximum))
    print('Part 2: The maximum value, ever, in a register is {0:d}'.format(absoluteMaximumEver))

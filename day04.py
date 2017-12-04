'''
Advent of Code 2017
Day 4: High-Entropy Passphrases

'''

import unittest

# Inputs and tests

PART1_TESTS = [('aa bb cc dd ee', True),
               ('aa bb cc dd aa', False),
               ('aa bb cc dd aaa', True)]

PART1_LINES = open('day04-input.txt').readlines()

DEBUG = False

# Solution

def evaluatePassPhrase(passPhrase):
    '''
    Check a string for repeated words. Returns True if there are no repeats,
    False if there are.

    Input is a string of space-separated words. Output is boolean.

    '''

    global DEBUG

    words = []

    for word in passPhrase.split():
        if word in words:
            return False
        words.append(word)

    return True

# Unit tests

class TestPassPhrase(unittest.TestCase):
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

        for (passPhrase, validity) in PART1_TESTS:
            self.assertEqual(evaluatePassPhrase(passPhrase), validity)

if __name__ == '__main__':

    print('Advent of Code\nDay 4: High-Entropy Passphrases\n')

    validPassphraseCount = 0

    for line in PART1_LINES:
        result = evaluatePassPhrase(line)
        if result:
            validPassphraseCount += 1

    print('Part 1: {0:d} valid passphrases'.format(validPassphraseCount))

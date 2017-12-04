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

PART2_TESTS = [('abcde fghij', True),
               ('abcde xyz ecdab', False),
               ('a ab abc abd abf abj', True),
               ('iiii oiii ooii oooi oooo', True),
               ('oiii ioii iioi iiio', False)]

PART2_LINES = PART1_LINES

DEBUG = False

# Solution

def evaluatePassPhrase1(passPhrase):
    '''
    Check a string for repeated words. Returns True if there are no repeats,
    False if there are.

    Input is a string of space-separated words. Output is boolean.

    '''

    global DEBUG

    # Keep a list of all the words in the passphrase
    words = []

    # Loop over all the words in the passphrase and if a duplicate exists,
    # it's a repeat and an invalid passphrase.

    for word in passPhrase.split():
        if word in words:
            return False
        words.append(word)

    # If we get here, we've not encountered any duplicates, and it's a valid
    # passphrase

    return True

# Part 2. No anagrams

class Word(object):
    '''
    Class for passphrase words that keeps track of the letters in the words and provides
    a comparison that looks at the letters and their frequency but doesn't care about
    their order. The net result is that anagrams compare True.

    '''
    def __init__(self, word):
        '''
        'word' must be a string.

        '''
        self._originalWord = word
        self._letters = {}

        # take the letters in the source word, and count the frequency of letters in the word
        for letter in word:
            if letter in self._letters:
                self._letters[letter] += 1
            else:
                self._letters[letter] = 1

    def __eq__(self, other):
        '''
        Comparison operator for this class that checks for anagrams.

        '''
        # If it's not a Word class, then it's a False comparison
        if not isinstance(other, Word):
            return False

        # Grab the list of letters in the other Word
        otherLetters = other._letters.keys()

        # If the set of letters don't match,  it's a False comparison
        if set(otherLetters) != set(self._letters.keys()):
            return False

        # Check the frequency of occurence of letters. If the counts
        # don't match, it's a False comparison
        for letter in otherLetters:
            if self._letters[letter] != other._letters[letter]:
                return False

        # That's all the conditions. If we're here, it's a match!
        return True

def evaluatePassPhrase2(passPhrase):
    '''
    Check a string for anagram words. Returns True if there are no anagrams,
    False if there are.

    Input is a string of space-separated words. Output is boolean.

    '''

    global DEBUG

    # Split out the words from the phrase
    words = [Word(word) for word in passPhrase.split()]

    # check each word against the others
    # If we encounter one anagram, it's a False passphrase
    for (index, word) in enumerate(words):
        for other in words[index+1:]:
            if word == other:
                return False

    # If we get here, it's a valid passphrase
    return True

# Unit tests

class TestPassPhrase(unittest.TestCase):
    '''
    Tests for Part 1 and Part 2

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
            self.assertEqual(evaluatePassPhrase1(passPhrase), validity)

    def test_part2(self):
        '''
        Part 2 tests

        '''
        global DEBUG

        DEBUG = True

        for (passPhrase, validity) in PART2_TESTS:
            self.assertEqual(evaluatePassPhrase2(passPhrase), validity)

if __name__ == '__main__':

    print('Advent of Code\nDay 4: High-Entropy Passphrases\n')

    # Loop over all the input lines, count the valid passphrases using method 1
    validPassphraseCount = 0

    for line in PART1_LINES:
        result = evaluatePassPhrase1(line)
        if result:
            validPassphraseCount += 1

    print('Part 1: {0:d} valid passphrases'.format(validPassphraseCount))

    # Loop over all the input lines, count the valid passphrases using method 2
    validPassphraseCount = 0

    for line in PART2_LINES:
        result = evaluatePassPhrase2(line)
        if result:
            validPassphraseCount += 1

    print('Part 2: {0:d} valid passphrases'.format(validPassphraseCount))

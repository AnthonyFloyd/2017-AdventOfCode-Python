'''
Advent of Code 2017
Day 2: Corruption Checksum

'''

import unittest

# Inputs and tests

PART1_TEST_SPREADSHEET = '''5 1 9 5
7 5 3
2 4 6 8'''

PART2_TEST_SPREADSHEET = '''5 9 2 8
9 4 7 3
3 8 6 5'''

PART1_TESTS = [(PART1_TEST_SPREADSHEET, (8, 4, 6), 18),]
PART2_TESTS = [(PART2_TEST_SPREADSHEET, (4, 3, 2), 9),]

PART1_INPUT_SPREADSHEET = '''104	240	147	246	123	175	372	71	116	230	260	118	202	270	277	292
740	755	135	205	429	822	844	90	828	115	440	805	526	91	519	373
1630	991	1471	1294	52	1566	50	1508	1367	1489	55	547	342	512	323	51
1356	178	1705	119	1609	1409	245	292	1434	694	405	1692	247	193	1482	1407
2235	3321	3647	212	1402	3711	3641	1287	2725	692	1235	3100	123	144	104	101
1306	1224	1238	186	751	734	1204	1275	366	149	1114	166	1118	239	153	943
132	1547	1564	512	2643	2376	2324	2159	1658	107	1604	145	2407	131	2073	1878
1845	91	1662	108	92	1706	1815	1797	1728	1150	1576	83	97	547	1267	261
78	558	419	435	565	107	638	173	93	580	338	52	633	256	377	73
1143	3516	4205	3523	148	401	3996	3588	300	1117	2915	1649	135	134	182	267
156	2760	1816	2442	2985	990	2598	1273	167	821	138	141	2761	2399	1330	1276
3746	3979	2989	161	4554	156	3359	173	3319	192	3707	264	762	2672	4423	2924
3098	4309	4971	5439	131	171	5544	595	154	571	4399	4294	160	6201	4329	5244
728	249	1728	305	2407	239	691	2241	2545	1543	55	2303	1020	753	193	1638
260	352	190	877	118	77	1065	1105	1085	1032	71	87	851	56	1161	667
1763	464	182	1932	1209	640	545	931	1979	197	1774	174	2074	1800	939	161'''

PART2_INPUT_SPREADSHEET = PART1_INPUT_SPREADSHEET

# Solution

def calculateRowChecksum1(rowString):
    '''
    Calculates a checksum by calculating the difference between the maximum and minimum value in a row.

    Input is rowString, a string of space-separated integers.
    Returns an integer difference based on the checksum algorithm.

    '''
    # Convert the row to a list of integers
    integerList = [int(c) for c in rowString.strip().split()]

    # calculate the checksum (range in the list)
    return max(integerList) - min(integerList)

def calculateRowChecksum2(rowString):
    '''
    Calculates a checksum by finding the only two numbers in a list that are evenly divisible,
    and then returning the largest result of their division.

    Input is rowString, a string of space-separated integers.
    Returns an integer based on the checksum algorithm.

    '''

    # Convert the row to a list of integers
    integerList = [int(c) for c in rowString.strip().split()]

    # Sort the list to put the smallest integers at the front
    integerList.sort()

    # work our way through the list until we find
    # the equally divisible ones
    # assumes there will always be an answer!

    for (index, denominator) in enumerate(integerList):
        # now search through the rest to see if the current integer
        # divides evenly into any of them
        #
        # no need to search through the previous integers
        # also, search from the back because the nearest ints
        # are unlikely to be equally divisible
        #
        for numerator in reversed(integerList[index + 1:]):
            if numerator % denominator == 0:
                return numerator // denominator

    raise RuntimeError('Unable to find solution for a row')

CHECKSUM_ALGORITHMS = (calculateRowChecksum1, calculateRowChecksum2)

def calculateSpreadsheetChecksum(spreadsheetString, method=1):
    '''
    Calculates a checksum for a whole spreadsheet, using specified method,
    defaults to 1.

    Input is the default AoC spreadsheet string,
    Returns an integer checksum.

    '''

    # initialize the tally
    total = 0

    # Find the checksum algorithm, once
    # Better to apologize than ask permission
    try:
        calculateRowChecksum = CHECKSUM_ALGORITHMS[method-1] # 0-indexed lists, 1-indexed methods
    except IndexError:
        raise RuntimeError('Unknown checksum algorithm {0:d}'.format(method))

    # Step through each row in the input, keeping a tally of all the rows
    for row in convertToRows(spreadsheetString):
        total += calculateRowChecksum(row)

    return total

def convertToRows(fullArrayString):
    '''
    Converts the AoC input format to a list of rows (as strings).

    '''

    return fullArrayString.strip().split('\n')

# Unit tests

class TestChecksums(unittest.TestCase):
    '''
    Tests for Part 1 and Part 2

    '''

    # Part 1

    def test_part1(self):
        '''
        Part 1 tests

        '''

        # Test the row checksum algorithm
        for (index, row) in enumerate(convertToRows(PART1_TESTS[0][0])):
            self.assertEqual(calculateRowChecksum1(row), PART1_TESTS[0][1][index])

        # Test we get the right answer for the whole spreadsheet
        self.assertEqual(calculateSpreadsheetChecksum(PART1_TESTS[0][0], 1), PART1_TESTS[0][2])

    # Part 2

    def test_part2(self):
        '''
        Part 2 tests

        '''

        # Test the row checksum algorithm
        for (index, row) in enumerate(convertToRows(PART2_TESTS[0][0])):
            self.assertEqual(calculateRowChecksum2(row), PART2_TESTS[0][1][index])

        # Test we get the right answer for the whole spreadsheet
        self.assertEqual(calculateSpreadsheetChecksum(PART2_TESTS[0][0], 2), PART2_TESTS[0][2])


if __name__ == '__main__':

    print('Advent of Code\nDay 2: Corruption Checksum\n')
    print('Part 1: {0:d}'.format(calculateSpreadsheetChecksum(PART1_INPUT_SPREADSHEET, 1)))
    print('Part 2: {0:d}'.format(calculateSpreadsheetChecksum(PART2_INPUT_SPREADSHEET, 2)))

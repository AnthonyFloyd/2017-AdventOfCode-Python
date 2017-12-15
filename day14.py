'''
Advent of Code 2017
Day 14: Disk Defragmentation

'''

from day10 import computeKnot

DAY14_INPUT = 'hxtvlmkl'
DAY14_SIZE = 128

usedCounter = 0

for rowString in [DAY14_INPUT + '-%d' % i for i in range(DAY14_SIZE)]:
    knot = computeKnot(rowString, 256)
    binaryKnotString = bin(int(knot, 16))[2:].zfill(128)
    usedCounter += binaryKnotString.count('1')

print("{0:d} blocks are used".format(usedCounter))




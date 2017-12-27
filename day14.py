'''
Advent of Code 2017
Day 14: Disk Defragmentation

'''

from day10 import computeKnot
import numpy as np

DAY14_TEST = 'flqrgnkx'
DAY14_INPUT = 'hxtvlmkl'

GRIDSIZE = 128

usedCounter = 0
diskMapList = []

# Part 1, block counting

for rowString in [DAY14_INPUT + '-%d' % i for i in range(GRIDSIZE)]:
    knot = computeKnot(rowString, 256)
    binaryKnotString = bin(int(knot, 16))[2:].zfill(GRIDSIZE)
    binaryKnotList = [int(i) for i in binaryKnotString]
    diskMapList.append(binaryKnotList)
    usedCounter += binaryKnotString.count('1')

print("{0:d} blocks are used".format(usedCounter))

# Part 2, region counting

diskMap = np.array(diskMapList)
regionMap = np.zeros((GRIDSIZE,GRIDSIZE), dtype=int)

#
# March through each location.
# if a region hasn't been assigned, assign a new region
# then explore in all directions, not including diagonals
# Exploring means checking for adjacents to current location,
# and if any are discovered, add those to the list of unchecked
# for this location. Also, assign the region ID to those locations,
# marking them as part of this region. Repeat for each item in the
# unchecked list for this location until the unchecked list is
# exhausted. Then move on to the next location
#

cursorLocation = [0,0]
regionCounter = 0

for rowCounter in range(GRIDSIZE):
    for colCounter in range(GRIDSIZE):
        # check to see if this is part of a region
        # First of all, it needs to be use in the disk map
        # and it needs to be not part of a region
        if diskMap[rowCounter,colCounter] == 1 and regionMap[rowCounter,colCounter] == 0:
            # new region!
            regionCounter += 1
            uncheckedRegionLocations = [(rowCounter,colCounter),]
            while len(uncheckedRegionLocations) > 0:
                # take one down, pass it around
                (y, x) = uncheckedRegionLocations.pop(0)
                regionMap[y, x] = regionCounter
                # check north, west, south, east
                # watch for boundaries
                if y - 1 >= 0:
                    if diskMap[y - 1, x] == 1 and regionMap[y - 1, x] == 0:
                        uncheckedRegionLocations.append((y - 1, x))
                if x - 1 >= 0:
                    if diskMap[y, x - 1] == 1 and regionMap[y, x - 1] == 0:
                        uncheckedRegionLocations.append((y, x - 1))
                if y + 1 < GRIDSIZE:
                    if diskMap[y + 1, x] == 1 and regionMap[y + 1, x] == 0:
                        uncheckedRegionLocations.append((y + 1, x))
                if x + 1 < GRIDSIZE:
                    if diskMap[y, x + 1] == 1 and regionMap[y, x + 1] == 0:
                        uncheckedRegionLocations.append((y, x + 1))

print("Found {0:d} regions".format(regionCounter))




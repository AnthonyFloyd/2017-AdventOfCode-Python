'''
Advent of Code 2017
Day 14: Disk Defragmentation

'''

import numpy as np

from day10 import computeKnot

DAY14_TEST = 'flqrgnkx'
DAY14_INPUT = 'hxtvlmkl'

GRIDSIZE = 128

class Disk(object):
    """A structure representing a disk.

    """

    def __init__(self, seedString, diskSize=GRIDSIZE):
        """Init Disk class.

        Args:
            seedString (str): Seed for the knot algorithm.
            diskSize (int): Disk size.

        """

        self.seed = seedString
        self.diskSize = diskSize

        self.diskMap = None # Numpy array containing the disk contents
        self.regionMap = None # Numpy array containing the regions

        self.__nUsedBlocks = 0 # Counter for the number of used blocks
        self.__nRegions = 0 # Counter for the number of regions

        self.createDisk()

    @property
    def nUsedBlocks(self):
        """Return the number of used blocks on the disk."""

        # NB: Used as a property to prevent setting it external to the class

        return self.__nUsedBlocks

    @property
    def nRegions(self):
        """Return the number of discrete regions on the disk.

        This is a lazy property, calculated when needed.

        """

        if self.regionMap is None:
            self.countRegions()

        return self.__nRegions

    def createDisk(self, seedString=None):
        """Create the state of the disk.

        Based on a knot hash algorithm with the given seed string.

        Args:
            seedString: Optional string argument with the seed for the knot
                algorithm. Defaults to initial seed string.

        """

        diskMapList = []
        self.__nUsedBlocks = 0

        if seedString is not None:
            self.seed = seedString

        # Each knot hash corresponds to a row, free == 0, used ==1
        # Create the disk map, counting used blocks as we go

        for rowString in [self.seed + '-%d' % i for i in range(self.diskSize)]:
            # Use the Day 10 algorithm to compute the knot hash
            knot = computeKnot(rowString, 256)

            # Convert the knot hash (hex) to a binary string of correct length (ie zero-padded)
            binaryKnotString = bin(int(knot, 16))[2:].zfill(self.diskSize)

            # Convert the string to a list of ints for easy tracking in the grid
            binaryKnotList = [int(i) for i in binaryKnotString]
            diskMapList.append(binaryKnotList)

            # Count used blocks
            self.__nUsedBlocks += binaryKnotString.count('1')

        # Convert the disk map into a numpy array for easy indexing (not really necessary)
        self.diskMap = np.array(diskMapList)

    def countRegions(self):
        """Count the number of discrete regions on the disk.

        With the disk map, find all regions consisting of adjacent used blocks.
        Adjacency is only measured horizontally and vertically, not diagonally.

        Returns:
            int: Number of regions found.

        """

        # Create a map of regions instead of used/free
        self.regionMap = np.zeros((self.diskSize, self.diskSize), dtype=int)

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

        # Use a cursor concept to move through the grid

        self.__nRegions = 0

        for rowCounter in range(self.diskSize):
            for colCounter in range(self.diskSize):
                # check to see if this is part of a region
                # First of all, it needs to be use in the disk map
                # and it needs to be not part of a region

                if (self.diskMap[rowCounter,colCounter] == 1 and
                    self.regionMap[rowCounter,colCounter] == 0):

                    # new region!
                    self.__nRegions += 1
                    uncheckedRegionLocations = [(rowCounter,colCounter),]

                    while uncheckedRegionLocations:
                        # take one down, pass it around
                        (y, x) = uncheckedRegionLocations.pop(0)
                        self.regionMap[y, x] = self.__nRegions
                        # check north, west, south, east
                        # watch for boundaries
                        if y - 1 >= 0:
                            if (self.diskMap[y - 1, x] == 1 and
                                self.regionMap[y - 1, x] == 0):
                                uncheckedRegionLocations.append((y - 1, x))
                        if x - 1 >= 0:
                            if (self.diskMap[y, x - 1] == 1 and
                                self.regionMap[y, x - 1] == 0):
                                uncheckedRegionLocations.append((y, x - 1))
                        if y + 1 < self.diskSize:
                            if (self.diskMap[y + 1, x] == 1 and
                                self.regionMap[y + 1, x] == 0):
                                uncheckedRegionLocations.append((y + 1, x))
                        if x + 1 < self.diskSize:
                            if (self.diskMap[y, x + 1] == 1 and
                                self.regionMap[y, x + 1] == 0):
                                uncheckedRegionLocations.append((y, x + 1))

        return self.__nRegions

if __name__ == '__main__':
    import time

    startTime = time.clock()

    disk = Disk(DAY14_INPUT)

    endTime = time.clock()

    print("Advent of Code Day 14")
    # Part 1, block counting
    #
    # Disk is a 128x128 grid, each square on grid is free or used
    # State of the grid is tracked by bits in a knot hash (see Day 10)
    #
    # Note that usedBlocks is calculated when the disk is created above
    #
    print("{0:d} blocks are used. (Took {1:.3f} seconds to run)".format(disk.nUsedBlocks, endTime - startTime))

    # Part 2, region counting
    # With the disk map, find all regions consisting of adjacent used blocks
    # Adjaceny is only measured horizontally and vertically, not diagonally
    #
    # In this case, nRegions is a LongRunningTask and is a lazy calculation
    # and is only calculated when it's needed (below)
    #
    startTime = time.clock()
    nRegions = disk.nRegions
    endTime = time.clock()

    print("The disk contains {0:d} regions. (Took {1:.3f} seconds to run)".format(disk.nRegions, endTime - startTime))

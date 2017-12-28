'''
Advent of Code 2017
Day 11: Hex Ed

'''

DAY11_TEST_INPUT = 'se,sw,se,sw,sw'
DAY11_INPUT = open('day11-input.txt').read()

MOVE = {'n': [0, 1, -1],
        'ne': [1, 0, -1],
        'se': [1, -1, 0],
        's': [0, -1, 1],
        'sw': [-1, 0, 1],
        'nw': [-1, 1, 0]
        }

class Coordinate(object):
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
        self.maxDistance = 0

    def distanceTo(self, destination):
        assert isinstance(destination, Coordinate)

        return ((abs(destination.x - self.x) + abs(destination.y - self.y) +
                 abs(destination.z - self.z)) / 2)

    def distanceFromStart(self):
        return ((abs(self.x) + abs(self.y) + abs(self.z)) / 2)

    def processMove(self, move):
        self.x += move[0]
        self.y += move[1]
        self.z += move[2]

        currentDistance = self.distanceFromStart()
        self.maxDistance = max(self.maxDistance, currentDistance)

def processMoves(moveList, startLocation):
    assert isinstance(startLocation, Coordinate)

    moves = moveList.strip().split(',')

    for move in moves:
        startLocation.processMove(MOVE[move])

if __name__ == '__main__':

    start = Coordinate()
    location = Coordinate()

    processMoves(DAY11_TEST_INPUT, location)
    print("Test: Distance from start: {0:f}".format(location.distanceTo(start)))

    location= Coordinate()
    processMoves(DAY11_INPUT, location)
    print("Part 1 distance from start: {0:f}".format(location.distanceTo(start)))
    print("Part 1 max distance from start: {0:f}".format(location.maxDistance))


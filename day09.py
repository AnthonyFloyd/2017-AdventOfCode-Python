'''
Advent of Code 2017
Day 9: Stream Processing

'''

INPUT = open('day09-input.txt').read()

def scoreStream(inputString):

    currentDepth = 0
    runningScore = 0
    inGarbage = False
    ignoreNext = False

    garbageCharacters = 0

    for c in inputString:
        if ignoreNext:
            ignoreNext = False
        else:
            if inGarbage:
                if c == '!':
                    ignoreNext = True
                elif c == '>':
                    inGarbage = False
                else:
                    garbageCharacters += 1
            else:
                if c == '{':
                    currentDepth += 1
                    runningScore += currentDepth
                elif c == '}':
                    currentDepth -= 1
                elif c == '<':
                    inGarbage = True

    return (runningScore, garbageCharacters)

if __name__ == '__main__':

    print('Advent of Code\nDay 9: Stream Processing\n')
    (score, garbage) = scoreStream(INPUT)
    print('Part 1: The score is {0:d}'.format(score))
    print('Part 2: The number of garbage characters is {0:d}'.format(garbage))

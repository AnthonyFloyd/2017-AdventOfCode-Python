'''
Advent of Code 2017
Day 23: Coprocessor Conflagration

'''

from day18 import Processor

class ProcessorD23(Processor):
    def __init__(self):
        Processor.__init__(self)

    def sub(self, register, value):
        """
        Subtract an integer (positive or negative) from the register.

        """
        try:
            self._registers[register] -= int(value)
        except ValueError:
            self._registers[register] -= self._registers[value]

    def add(self, *args, **kwargs):
        raise NotImplementedError

    def mod(self, *args, **kwargs):
        raise NotImplementedError

def processInstructions(instructionList, processor):

    position = 0
    multCounter = 0
    nInstructions = len(instructionList)

    while True:
        instructionLine = instructionList[position]
        instructionBits = [i.strip() for i in instructionLine.split()]
        if len(instructionBits) == 3:
            (instruction, register, value) = instructionBits
        else:
            (instruction, register) = instructionBits
            value = None

        jump = 1

        #print("L{0:d} '{1}' a:{2:d} b:{3:d} c:{4:d} d:{5:d} e:{6:d} f:{7:d} g:{8:d} h:{9:d}".format(position+1, instructionLine.strip(),
                                                                                                    #processor.get('a'),
                                                                                                    #processor.get('b'),
                                                                                                    #processor.get('c'),
                                                                                                    #processor.get('d'),
                                                                                                    #processor.get('e'),
                                                                                                    #processor.get('f'),
                                                                                                    #processor.get('g'),
                                                                                                    #processor.get('h'),))

        if instruction == 'set':
            processor.set(register, value)
        elif instruction == 'sub':
            processor.sub(register, value)
        elif instruction == 'mul':
            processor.mult(register, value)
            multCounter += 1
        elif instruction == 'jnz':
            try:
                if int(register) != 0:
                    try:
                        jump = int(value)
                    except ValueError:
                        jump = processor.get(register)
            except ValueError:
                if processor.get(register) != 0:
                    try:
                        jump = int(value)
                    except ValueError:
                        jump = processor.get(register)

        position += jump

        if position >= nInstructions or position < 0:
            break

    return multCounter

if __name__ == '__main__':

    # Part 1
    instructions = open('day23-input.txt').readlines()

    processor = ProcessorD23()
    nMults = processInstructions(instructions, processor)
    print("Part 1: {0:d} mul instructions executed.".format(nMults))

    # Part 2

    processor = ProcessorD23()
    processor.set('a',1)
    processInstructions(instructions, processor)
    print("Part 2: register h ends with value {0:d}".format(processor.get('h')))


'''
Advent of Code 2017
Day 18: Duet

'''

import time
import queue
import threading

from collections import defaultdict

SUCCESS = 0
FAIL = 1

DAY18_TEST_PART1 = '''set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2'''

DAY18_TEST_PART2 = '''snd 1
snd 2
snd p
rcv a
rcv b
rcv c
rcv d'''

class Processor(object):
    '''
    Super class that performs the instructions on the intenal registers. Must override
    the snd and rcv classes for all implementations.

    Note that each method may receive either a register name (character) or an integer.
    If the method receives a register name, then the method should use the value stored
    in the register. If the method receives an integer, use the integer.

    '''

    def __init__(self):
        self._registers = defaultdict(int)

    def add(self, register, value):
        """
        Add an integer (positive or negative) to the register.

        """
        try:
            self._registers[register] += int(value)
        except ValueError:
            self._registers[register] += self._registers[value]

    def set(self, register, value):
        """
        Set a register to the value.

        """
        try:
            self._registers[register] = int(value)
        except ValueError:
            self._registers[register] = self._registers[value]

    def mult(self, register1, value):
        """
        Multiply the register value by the supplied value.

        """
        try:
            self._registers[register1] = self._registers[register1] * int(value)
        except ValueError:
            self._registers[register1] = self._registers[register1] * self._registers[value]

    def mod(self, register1, value):
        """
        Store the modulo of the register value with the supplied value.

        """
        try:
            self._registers[register1] = self._registers[register1] % int(value)
        except ValueError:
            self._registers[register1] = self._registers[register1] % self._registers[value]

    def get(self, register):
        """
        Retrieve the register value.

        """
        return self._registers[register]

    def snd(self, *args, **kwargs):
        """
        Implement the snd method for each specific subclass.

        """
        raise NotImplementedError

    def rcv(self, *args, **kwargs):
        """
        Implement the rcv method of each specific subclass.

        """
        raise NotImplementedError

class ProcessorPart1(Processor):
    """
    Processor for AoC2017 Day 18 Part 1. Implements the snd and rcv methods as methods
    relating to sounds.
    """
    def __init__(self):
        Processor.__init__(self)
        self._lastFrequency = None

    def snd(self, register):
        """
        'Play' a sound using the register value as the frequency, and remember the frequency.

        """
        self._lastFrequency = self._registers[register]

    def rcv(self, register):
        """
        Retrieve the last frequency played, if non-zero.

        """
        if self._registers[register] != 0:
            return self._lastFrequency
        else:
            return None

class ProcessorPart2(Processor):
    """
    Processor for AoC2017 Day 18 Part 2. Implements the snd and rcv methods as send and receive
    methods for IPC.

    Initialization parameters

    pid: process ID
    """
    def __init__(self, pid):
        Processor.__init__(self)
        self.pid = pid # Remember the assigned PID
        self._registers['p'] = pid # Store the PID in register 'p'
        self.sendCalls = 0 # Count the number of 'send' calls
        self.inputQueue = None # Queue to receive values
        self.outputQueue = None # Queue to send values

    def snd(self, register):
        """
        Send the value in the given register to the output queue.

        """

        self.outputQueue.put(self._registers[register])

        # Increment the send counter
        self.sendCalls += 1

    def rcv(self, register):
        """
        Get the next value from the input queue
        Mind, if both the input and output queue are empty and TIMEOUT passes, we're done. Exit.

        """
        while True:
            try:
                newValue = self.inputQueue.get(timeout=1)
            except queue.Empty:
                if self.outputQueue.empty():
                    return FAIL # both queues empty, we must be done
                else:
                    pass # keep waiting, other processes have processing to do
            else:
                # got a new value, store it, exit wait loop
                self._registers[register] = newValue
                return SUCCESS

def processInstructionsAsSounds(instructionList):

    position = 0
    processor = ProcessorPart1()

    while True:
        instructionLine = instructionList[position]
        instructionBits = [i.strip() for i in instructionLine.split()]
        if len(instructionBits) == 3:
            (instruction, register, value) = instructionBits
        else:
            (instruction, register) = instructionBits
            value = None

        jump = 1

        if instruction == 'snd':
            processor.snd(register)
        elif instruction == 'set':
            processor.set(register, value)
        elif instruction == 'add':
            processor.add(register, value)
        elif instruction == 'mul':
            processor.mult(register, value)
        elif instruction == 'mod':
            processor.mod(register, value)
        elif instruction == 'rcv':
            recoveredValue = processor.rcv(register)
            if recoveredValue is not None:
                print('Part 1: recovered value is {0:d}'.format(recoveredValue))
                break
        elif instruction == 'jgz':
            if processor.get(register) > 0:
                jump = int(value)

        #print('a: {0:d}'.format(registerBank('a')))
        position += jump

        if position > len(instructionList) or position < 0:
            break

class Process(threading.Thread):
    """
    Thread for each process in part 2.
    Pass the PID, the input and output queues, and the instruction list.

    """
    def __init__(self, pid, inputQueue, outputQueue, instructionList):
        threading.Thread.__init__(self)
        self.processor = ProcessorPart2(pid)
        self.processor.inputQueue = inputQueue
        self.processor.outputQueue = outputQueue
        self.instructions = instructionList

    def run(self):
        # Thread main loop

        if self.instructions is not None:
            nInstructions = len(self.instructions)
            position = 0

            while True:
                # Get the next instruction, split it up
                instructionLine = self.instructions[position]
                instructionBits = [i.strip() for i in instructionLine.split()]

                # Depending if we have 2 or 3 bits, assign reasonable names to the bits
                if len(instructionBits) == 3:
                    (instruction, register, value) = instructionBits
                else:
                    (instruction, register) = instructionBits
                    value = None

                # we usually jump to the next line at the end, but this can be modified by the
                # jgz instruction

                jump = 1

                # Parse and execute the instruction
                if instruction == 'snd':
                    self.processor.snd(register)
                elif instruction == 'set':
                    self.processor.set(register, value)
                elif instruction == 'add':
                    self.processor.add(register, value)
                elif instruction == 'mul':
                    self.processor.mult(register, value)
                elif instruction == 'mod':
                    self.processor.mod(register, value)
                elif instruction == 'rcv':
                    # The receive instruction. If we don't receive a value (FAIL) then
                    # exit the main loop
                    success = self.processor.rcv(register)
                    if success == FAIL:
                        break
                elif instruction == 'jgz':
                    # Need to check to see if the jgz instruction supplies a register or value as the
                    # first argument

                    try:
                        if int(register) > 0:
                            try:
                                jump = int(value)
                            except ValueError:
                                jump = self.processor.get(register)
                    except ValueError:
                        if self.processor.get(register) > 0:
                            try:
                                jump = int(value)
                            except ValueError:
                                jump = self.processor.get(register)

                # Set up the next jump
                position += jump

                # Check to see if we're outside the instruction list
                if position > nInstructions or position < 0:
                    break

            # The exercise requires us to know how many sends PID1 made in the end
            if self.processor.pid == 1:
                print("Part 2: process {0:d} made {1:d} sends".format(self.processor.pid,
                                                                      self.processor.sendCalls))


if __name__ == '__main__':

    # Part 1
    #processInstructions(DAY18_TEST_PART1.splitlines())
    instructions = open('day18-input.txt').readlines()

    processInstructionsAsSounds(instructions)

    # Part 2

    #instructions = DAY18_TEST_PART2.splitlines()

    # Set up the queues and threads, start them up, wait for them to end
    queue1 = queue.Queue()
    queue2 = queue.Queue()

    thread0 = Process(pid=0, inputQueue=queue1, outputQueue=queue2, instructionList=instructions)
    thread1 = Process(pid=1, inputQueue=queue2, outputQueue=queue1, instructionList=instructions)

    threads = [thread0, thread1]

    for t in threads:
        t.start()

    for t in threads:
        t.join()


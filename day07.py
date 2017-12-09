'''
Advent of Code 2017
Day 7: Recursive Circus

'''

import unittest
from collections import Counter

TEST_TREE = '''pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)'''

INPUT_TREE = open('day07-input.txt').readlines()

class Node(object):
    '''
    A node in a tree with a parent (or not) and children (or none) and weight

    '''
    def __init__(self, name, weight=0):
        self.name = name
        self.weight = weight
        self.parent = None
        self.children = []
        self.totalWeight = 0

def buildTree(treeList):
    '''
    Build up a tree of Nodes from the string instructions

    The instructions are node definitions with optional children of the form

    <node name> (<weight>) -> <child name 1>, <child name 2>, <...>

    '''

    hasNoParent = [] # list of nodes without parents
    nodeIndex = {} # keep an index of nodes for easy reference nodeName: Node

    # parse the input
    for row in treeList:
        rowBits = row.split('->')
        name, weightString = rowBits[0].strip().split(' ')
        weight=int(weightString.replace('(','').replace(')',''))

        # if the name isn't in the node index, it's a new node
        if name not in nodeIndex:
            newNode = Node(name, weight)
            nodeIndex[name] = newNode
            hasNoParent.append(newNode)
        else:
            # here if the node was created as a child node, but without weight details
            newNode = nodeIndex[name]
            newNode.weight = weight

        # check to see if any children were defined
        if len(rowBits) > 1:
            children = [item.strip() for item in rowBits[1].strip().split(',')]

            # step through all the children, create the parent-child relationships
            # create new nodes if they haven't already been created

            for child in children:
                if child not in nodeIndex.keys():
                    # Haven't seen this name before, create a node
                    childNode = Node(child)
                    nodeIndex[child] = childNode
                else:
                    # We have seen this name before, grab the node
                    childNode = nodeIndex[child]

                # If the childNode is in the hasNoParent list, un-orphan it
                if childNode in hasNoParent:
                    hasNoParent.remove(childNode)

                # Create the familial relationships
                newNode.children.append(childNode)
                childNode.parent = newNode

    # Only one node should have no parent, and that's the root node
    rootNode = hasNoParent[0]

    return(rootNode)

def findBranchWeights(node):
    '''
    Build up the total weights of each node by adding up the total weight of its children

    Recursive to properly navigate the tree. Returns nothing.

    '''

    # Start the weight from the node's own weight
    node.totalWeight = node.weight

    # Add the total weight of all children
    # But make sure they're updated first

    for childNode in node.children:
        findBranchWeights(childNode)
        node.totalWeight += childNode.totalWeight

def findNewWeight(rootNode):
    '''
    Only one weight needs to be adjusted in the tree to make all the branches balanced. This
    routine finds that one node and return the node with corrected weight.

    '''
    # Go down the tree, following the imbalance until we find a balanced node (or end node)
    # Once we find a balanced node, it is the one that needs changing
    # And it needs changing based on the totalweights of its siblings

    # First, update the weights everywhere
    findBranchWeights(rootNode)

    # Now, follow the imbalances to find the furthest balanced node

    imbalanced = True
    currentNode = rootNode

    while imbalanced:
        currentBranchWeights = [node.totalWeight for node in currentNode.children]

        # are there any differences?
        if len(set(currentBranchWeights)) > 1:
            # yes!

            # find the most common weight (there'll only be one)
            leastCommonTotalWeight = Counter(currentBranchWeights).most_common(2)[1][0]

            # that one is:
            currentNode = currentNode.children[currentBranchWeights.index(leastCommonTotalWeight)]
        else:
            # no!
            # so we need to change this weight based on siblings

            siblings = currentNode.parent.children
            siblingWeights = [node.totalWeight for node in siblings]

            mostCommonTotalWeight = Counter(siblingWeights).most_common(1)[0][0]

            # this node's total weight must match the most common
            #childrensWeight = currentNode.totalWeight - currentNode.weight
            deltaWeight = mostCommonTotalWeight - currentNode.totalWeight
            currentNode.weight = currentNode.weight + deltaWeight

            imbalanced = False

    return currentNode

# Unit tests

class TestLoops(unittest.TestCase):
    '''
    Tests for Part 1 and Part 2

    '''

    # Part 1

    def test_part1(self):
        '''
        Part 1 tests

        '''

        rootNodeName = buildTree(TEST_TREE.splitlines()).name

        self.assertEqual(rootNodeName, 'tknk')

    ## Part 2

    def test_part2(self):
        '''
        Part 2 tests

        '''

        newWeight = findNewWeight(buildTree(TEST_TREE.splitlines()))
        self.assertEqual(newWeight.weight, 60)



if __name__ == '__main__':

    print('Advent of Code\nDay 7: Recursive Circus\n')
    rootNode = buildTree(INPUT_TREE)
    print('Part 1: The root node name is {}'.format(rootNode.name))

    newWeightNode = findNewWeight(rootNode)
    print('Part 2: The new weight of node {0} is {1:d}'.format(newWeightNode.name, newWeightNode.weight))

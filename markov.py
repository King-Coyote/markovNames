import bisect
import random
import math

START = "[[START]]"
END = "[[END]]"

def accumulateList(itemList):
    '''
    Creates a list where each element is the sum of the elements in the list that came before it
    e.g. [1, 2, 3] would give [1, 3, 6]
    '''
    itemList = iter(itemList)
    total = next(itemList)
    yield total
    for element in itemList:
        total = total + element
        yield total

class MarkovNode:

    def __init__(self, data):
        self.data = data
        self.connectedData = dict()
        self.bakedConnections = list()
        self.bakedCumWeights = list()

    def addToConnection(self, data):
        if data in self.connectedData:
            self.connectedData[data] += 1
        else:
            self.connectedData[data] = 1

    def bakeProbability(self):
        self.bakedConnections, weights = zip(*self.connectedData.items())
        self.bakedCumWeights = list(accumulateList(weights))

    def getNext(self):
        index = random.random() * self.bakedCumWeights[-1]
        return self.bakedConnections[bisect.bisect(self.bakedCumWeights, index)]


class MarkovChain:

    def __init__(self):
        self.nodes = dict()
        self.min = math.inf
        self.max = 0
        
    def munchData(self, iterable):
        '''
        mmm yuss i fkn love data num num num
        '''
        iterable = iter(iterable)
        current = next(iterable)
        self.addToNode(START, current)
        while current != END:
            try:
                nextElement = next(iterable)
            except StopIteration:
                nextElement = END
            self.addToNode(current, nextElement)
            current = nextElement

    def addToNode(self, node, data):
        if node not in self.nodes:
            self.nodes[node] = MarkovNode(node)
        self.nodes[node].addToConnection(data)

    def bakeProbabilities(self):
        for node in self.nodes.values():
            node.bakeProbability()

    def walkDataString(self):
        current = self.nodes[START].getNext()
        while current != END:
            yield current
            current = self.nodes[current].getNext()
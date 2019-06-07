import math


class Node(object):
    def __init__(self, label, adjacentNodes={}):
        self.label = label
        self.parent = 0
        self.distance = 0
        self.adjacentNodes = dict(adjacentNodes)
    def __iter__(self):
        return iter(self.adjacentNodes.items())
    def addConnection(self, node, distance):
        self.adjacentNodes[node] = distance
    def removeConnection(self, node):
        del self.adjacentNodes[node]
    def setParent(self, node):
        self.parent = node
    def getParent(self):
        return self.parent
    def setDistance(self, distance):
        self.distance = distance
    def getDistance(self):
        return self.distance

class Graph(object):
    def __init__(self, nodes=[]):
        self._nodes = list(nodes)
        self._minPriorityQueue = []
    def __iter__(self):
        return iter(self._nodes)
    def addNode(self, label, adjacentNodes={}):
        node = label
        for key, value in adjacentNodes.items():
            node.connect(key, value)
        self._nodes.append(node)
    def removeNode(self, label):
        for i in range(self._nodes):
            if self._nodes[i] == label:
                del self._nodes[i]
                break
    def minPriorityQueue(self, node):
        self._minPriorityQueue.append(node)
    def removeFromMinPriorityQueue(self):
        if len(self._minPriorityQueue) <= 0:
            return None
        else:
            node = self._minPriorityQueue[0]
            del self._minPriorityQueue[0]
            return node

    def sortMinPriorityQueue(self): #using babble sort
        priorityQueue = [i.distance for i in self._minPriorityQueue]
        n = len(priorityQueue)
        for i in range(n):
            for j in range(0, n - i - 1):
                if priorityQueue[j] > priorityQueue[j + 1]:
                    priorityQueue[j], priorityQueue[j + 1] = priorityQueue[j + 1], priorityQueue[j]
        temp = []
        for i in priorityQueue:
            for node in self._minPriorityQueue:
                if node.distance == i and not (node in temp):
                    temp.append(node)
                    break
        self._minPriorityQueue = temp


class Djikstra(object):
    graph = 0
    def __init__(self, graph):
        self.graph = graph
    def setGraph(self, graph):
        self.graph = graph
    def getGraph(self):
        return self.graph
    def path(self, source, target):
        for node in self.graph:
            node.setParent(None)
            node.setDistance(math.inf)
        for i in self.graph:
            if i.label == source:
                source = i
                break
        for i in self.graph:
            if i.label == target:
                target = i
                break
        deleted = self.graph.removeFromMinPriorityQueue()
        while deleted != None:
            deleted = self.graph.removeFromMinPriorityQueue()
        source.setDistance(0)
        self.graph.minPriorityQueue(source)
        deleted = self.graph.removeFromMinPriorityQueue()
        while deleted != None:
            for node, distance in deleted:
                distance = distance + deleted.getDistance()
                if distance < node.getDistance():
                    node.setDistance(distance)
                    node.setParent(deleted)
                    self.graph.minPriorityQueue(node)
            deleted = self.graph.removeFromMinPriorityQueue()
        if target.getParent() == None:
            return None, math.inf
        path = [target]
        while path[0] != source:
            node = path[0]
            path.insert(0, node.getParent())
        totalDistance = target.getDistance()
        return path, totalDistance

graph = Graph()
germanCities = ['Cologne', 'Dresden', 'Bremen', 'Augsburg', 'Kassel', 'Rostock']

locations = {}
for city in germanCities:
    locations[city] = Node(city)
    graph.addNode(locations[city])

routes = {
    'Augsburg': {'Cologne': 111, 'Bremen': 222, 'Kassel': 333},
    'Dresden': {},
    'Kassel': {'Rostock': 444, 'Augsburg': 333},
    'Cologne': {'Augsburg': 111},
    'Rostock': {'Kassel': 444},
    'Bremen': {'Augsburg': 222}
}

for city in germanCities:
    for destination, distance in routes[city].items():
        locations[city].addConnection(locations[destination], distance)

shortestPath = Djikstra(graph)

def printPath(source, target):
    path, distance = shortestPath.path(source, target)
    if type(source) != str:
        source = source.label
    if type(target) != str:
        target = target.label

    print('From: ' + source + '<----> To: ' + target)

    if path == None:
        print('Route Does not Exist')
    else:
        for i in path:
            print(i.label, end=" , ")
        print('Total distance: ' + str(distance))


print('German Cities:')
print(germanCities)

travels = {'Dresden': 'Kassel'}

for source, target in travels.items():
    printPath(source, target)

travels = {locations['Augsburg']: locations['Bremen']}

for source, target in travels.items():
    printPath(source, target)
from plot import Plot
from collections import defaultdict, deque


class Main:
    # creating adjList from the given edges
    def getadjList(self, edges):
        adjList = defaultdict(list)
        for i in edges:
            adjList[i[0]].append(i[1])
            adjList[i[1]].append(i[0])
        return adjList

    def find(self, node, dictu):
        if node not in dictu:
            dictu[node] = [node, 1]
        elif dictu[node][0] != node:
            dictu[node][0] = self.find(dictu[node][0], dictu)
        return dictu[node][0]

    # Union Find
    def unionFind(self, adjList, node, dictu, deleted):
        if node in adjList:
            p1 = self.find(node, dictu)
            for i in adjList[node]:
                if i not in deleted:
                    p2 = self.find(i, dictu)
                    if p1 != p2:
                        if dictu[p1][1] >= dictu[p2][1]:
                            dictu[p2][0] = p1
                            dictu[p1][1] += dictu[p2][1]
                            dictu[i][0] = p1
                            dictu[node][0] = p1
                        else:
                            dictu[p1][0] = p2
                            dictu[p2][1] += dictu[p1][1]
                            dictu[i][0] = p2
                            dictu[node][0] = p2
        return dictu

    # finding whether the system is up/down using Union Find method
    def isConnected1(self, adjList, connected, deleted, nodes):
        if len(deleted) == len(nodes):
            return False
        dictu = defaultdict(list)
        for i in connected:
            if i not in deleted:
                self.unionFind(adjList, i, dictu, deleted)
        prev = None
        for i in dictu:
            if not prev:
                prev = dictu[i][0]
            elif dictu[i][0] != prev:
                return False
        return True

    # finding whether the system is up/down using BFS method
    def isConnected2(self, adjList, connected, nodes, deleted):
        if len(nodes) == len(deleted):
            return False
        queue = deque()
        if 0 in connected:
            connected.remove(0)
        if len(connected) > 0:
            queue.append(connected.pop())
        while queue:
            pop = queue.popleft()
            for i in adjList[pop]:
                if i in connected:
                    queue.append(i)
                    connected.remove(i)
        return len(connected) == 0

    # creating 2**n combinations, where n == number of nodes
    def getCombinations(self, lst, index, combinations, deleted):
        # base
        if index == len(lst):
            combined = [lst.copy(), deleted.copy()]
            combinations.append(combined)
            return combinations
        # logic
        # not making the particular node down
        combinations = self.getCombinations(lst, index+1, combinations, deleted)
        # making the node at index down
        temp = lst[index]
        lst[index] = 0
        deleted.add(temp)
        combinations = self.getCombinations(lst, index+1, combinations, deleted)
        lst[index] = temp
        deleted.remove(temp)
        return combinations

    def getReliabilityValue(self, p, up, down):
        return (p**up)*((1-p)**down)

    def helper(self, adjList, nodes, range, increment):
        # getting 2^n combinations
        combinations = self.getCombinations(nodes, 0, [], set())
        upSystems = []
        for i in combinations:
            connected, deleted = i[0], i[1]
            flag1 = self.isConnected1(adjList, connected, deleted, nodes)
            flag2 = self.isConnected2(adjList, set(connected), nodes, deleted)
            if (not flag1 and flag2) or (flag1 and not flag2):
                print("There is an error in checking whether the system is Up/Down")
                return
            if flag1 and flag2:
                upSystems.append([len(nodes)-len(deleted), len(deleted)])
        return upSystems

    def getReliability(self, edges, range, increment):
        adjList = self.getadjList(edges)
        nodes = list(adjList.keys())
        upSystems = self.helper(adjList, nodes, range, increment)
        x = []
        y = []
        start = range[0]
        end = range[1]
        p = start
        while p <= end:
            reliability = 0
            for i in upSystems:
                reliability += self.getReliabilityValue(p, i[0], i[1])
            x.append(p)
            y.append(reliability)
            print("Reliability of the network when p = {0} is".format(p), reliability)
            p += increment
            p = round(p, 2)
        # plotting Reliability vs p graph.
        Plot().plot(x, y)
        return


print(Main().getReliability([[1, 2], [1, 3], [1, 5], [1, 7], [2, 6], [2, 3], [3, 5], [3, 4],
                             [4, 7], [4, 6], [5, 8], [5, 6], [6, 7], [6, 8], [7, 8]], [0.05, 1], 0.05))


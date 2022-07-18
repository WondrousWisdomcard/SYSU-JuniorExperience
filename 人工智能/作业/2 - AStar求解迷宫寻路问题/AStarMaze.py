import numpy as np
from queue import PriorityQueue

class Point:

    def __init__(self, x, y, parent=None, d=0):
        self.x = x
        self.y = y
        self.f = 0
        self.d = d
        self.parent = parent

    def setF(self, f):
        self.f = f

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        return self.f < other.f

    def __hash__(self):
        return self.x * 1000 + self.y

    # 计算估价函数值： f = g + h, g = depth, h 为距离终点的曼哈顿距离
    def getFunctionValue(self, end):
        dist = abs(self.x - end.x) + abs(self.y - end.y)
        return dist + self.d

class Solution:

    # 初始化A*搜索
    def __init__(self, map, start_point, end_point):
        self.map = map
        self.openTable = PriorityQueue()
        self.closeTable = {}
        self.bestPath = []
        self.beginPoint = start_point
        self.destPoint = end_point
        self.currentPoint = None
        self.searchCount = 0

    # 获取 openTable 中估值函数最小的节点
    def getBestPointInOpenList(self):
        return self.openTable.get() # 返回并删除

    # 判断一个点是否被访问过，即是否位于 closeTable
    def isVisited(self, nextPoint):
        if self.closeTable.get(nextPoint) == None:
            return False
        else:
            return True

    # 生成从起点到当前节点的位置
    def getPath(self):
        tempPoint = self.currentPoint
        self.bestPath.append(self.destPoint)

        while tempPoint.parent and tempPoint.parent != self.beginPoint:
            self.bestPath.append(tempPoint.parent)
            tempPoint = tempPoint.parent

        self.bestPath.append(self.beginPoint)
        self.bestPath.reverse()

    # 搜寻当前节点的下一步可行解点，加入到 openTable 和 closeTable 当中
    def nextStep(self):

        nextPoints = []
        boarder = len(self.map) - 1
        x = self.currentPoint.x
        y = self.currentPoint.y
        d = self.currentPoint.d

        # 往左走
        if y > 0 and self.map[x][y - 1] == 0:
            nextPoints.append(Point(x, y - 1, self.currentPoint, d + 1))
        # 往上走
        if x > 0 and self.map[x - 1][y] == 0:
            nextPoints.append(Point(x - 1, y, self.currentPoint, d + 1))
        # 往下走
        if x < boarder and self.map[x + 1][y] == 0:
            nextPoints.append(Point(x + 1, y, self.currentPoint, d + 1))
        # 往右走
        if y < boarder and self.map[x][y + 1] == 0:
            nextPoints.append(Point(x, y + 1, self.currentPoint, d + 1))

        for nextPoint in nextPoints:
            if nextPoint not in self.closeTable:

                self.searchCount += 1
                if self.searchCount % 10 == 0:
                    print("Search point is up to " + str(self.searchCount))

                nextPoint.setF(nextPoint.getFunctionValue(self.destPoint))
                self.openTable.put(nextPoint)
                self.closeTable[nextPoint] = nextPoint

    # 求解迷宫问题
    def AStarSolve(self):

        self.openTable.put(self.beginPoint)
        self.closeTable[self.beginPoint] = self.beginPoint

        while not self.openTable.empty():

            self.currentPoint = self.getBestPointInOpenList()

            if(self.currentPoint == self.destPoint):
                self.getPath()
                break

            self.nextStep()

    # 展示最后结果，最短路径用 `*` 表示，访问过但不是最短路径的点用 `C` 表示
    def showInfo(self):
        for i in range(len(self.map)):
            for j in range(len(self.map)):
                if Point(i, j) in self.bestPath:
                    # 正确路径用‘*’表示
                    print('*', end='  ')
                elif Point(i,j) in self.closeTable:
                    # 搜寻过的结点用‘C’表示
                    print('C', end='  ')
                else:
                    print(self.map[i, j], end='  ')
            print("")
        return


if __name__ == '__main__':

    # state = np.array([[0, 0, 0, 0, 0],
    #                   [1, 0, 0, 0, 0],
    #                   [0, 0, 1, 1, 0],
    #                   [0, 1, 1, 0, 0],
    #                   [0, 0, 0, 0, 0]])

    # state = np.array([[0, 0, 0, 0, 0],
    #                   [1, 0, 1, 0, 1],
    #                   [0, 0, 1, 1, 1],
    #                   [0, 1, 0, 0, 0],
    #                   [0, 0, 0, 1, 0]])

    state=np.array([[0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1],
                    [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1],
                    [0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1],
                    [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1],
                    [1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1],
                    [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1],
                    [0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1],
                    [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1],
                    [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1],
                    [0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0],
                    [0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1],
                    [0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1],
                    [0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1],
                    [1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                    [0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0],
                    [0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0]])

    # 起点终点
    start_point = Point(0, 0)
    end_point = Point(len(state) - 1, len(state) - 1)

    # 最终路径
    solution = Solution(state, start_point, end_point)
    solution.AStarSolve()
    print('Best Way:')
    solution.showInfo()

    print("Total search steps is %d" % solution.searchCount)
    print("Total steps is %d" % (len(solution.bestPath) - 1))
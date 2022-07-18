import numpy as np

class State:

    count = 0

    # self.state        当前状态的数码矩阵
    # self.direction    当前空块的可移动方向
    # self.parent       当前状态的上一个状态
    # self.f            当前状态的估价函数值
    # self.search_times 到现在为止的搜索次数

    # 初始化一个状态
    def __init__(self, state, directionFlag=None, parent=None, f=0):

        # State.count += 1

        self.state = state
        self.direction = ['up', 'down', 'right', 'left']
        if directionFlag:
            self.direction.remove(directionFlag)
        self.parent = parent

        self.f = f

    # 获得当前状态下空快可移动的方向
    def getDirection(self):
        return self.direction

    # 设置状态的估价函数值
    def setF(self, f):
        self.f = f
        return

    # 打印一个状态的数码矩阵
    def showInfo(self):
        for i in range(len(self.state)):
            for j in range(len(self.state)):
                print(self.state[i, j], end='  ')
            print("\n")
        print('->')
        return

    # 获取0点（即空块在矩阵中的位置）
    def getZeroPos(self):
        postion = np.where(self.state == 0)
        return postion

    # 曼哈顿距离  f = g + h，g=1，如果用宽度优先的评估函数可以不调用该函数
    def getFunctionValue(self):
        cur_node = self.state.copy()
        fin_node = self.answer.copy()
        dist = 0
        error_num = 0

        N = len(cur_node)

        for i in range(N):
            for j in range(N):
                if cur_node[i][j] != fin_node[i][j]:
                    index = np.argwhere(fin_node == cur_node[i][j])
                    x = index[0][0]  # 最终x距离
                    y = index[0][1]  # 最终y距离
                    dist += (abs(x - i) + abs(y - j))

                    error_num += 1

        return dist + 1 + error_num



    # 寻找当前状态的下一个可行状态集合，从中选取评估函数值最小的状态
    def nextStep(self):
        if not self.direction:
            return []
        subStates = []
        boarder = len(self.state) - 1
        # 获取0点位置
        x, y = self.getZeroPos()
        # 向左
        if 'left' in self.direction and y > 0:
            s = self.state.copy()
            tmp = s[x, y - 1]
            s[x, y - 1] = s[x, y]
            s[x, y] = tmp
            news = State(s, directionFlag='right', parent=self)
            news.setF(news.getFunctionValue())
            subStates.append(news)
        # 向上
        if 'up' in self.direction and x > 0:
            # it can move to upper place
            s = self.state.copy()
            tmp = s[x - 1, y]
            s[x - 1, y] = s[x, y]
            s[x, y] = tmp
            news = State(s, directionFlag='down', parent=self)
            news.setF(news.getFunctionValue())
            subStates.append(news)
        # 向下
        if 'down' in self.direction and x < boarder:
            # it can move to down place
            s = self.state.copy()
            tmp = s[x + 1, y]
            s[x + 1, y] = s[x, y]
            s[x, y] = tmp
            news = State(s, directionFlag='up', parent=self)
            news.setF(news.getFunctionValue())
            subStates.append(news)
        # 向右
        if self.direction.count('right') and y < boarder:
            # it can move to right place
            s = self.state.copy()
            tmp = s[x, y + 1]
            s[x, y + 1] = s[x, y]
            s[x, y] = tmp
            news = State(s, directionFlag='left', parent=self)
            news.setF(news.getFunctionValue())
            subStates.append(news)
        # 返回F值最小的下一个点
        subStates.sort(key=compareNum)
        return subStates[0]

    # A* 迭代
    def solve(self):

        # openList
        openTable = []
        # closeList
        closeTable = []

        openTable.append(self)
        while len(openTable) > 0:

            State.count += 1
            print(State.count)

            # 下一步的点移除open
            n = openTable.pop(0)
            # 加入close
            closeTable.append(n)
            # 确定下一步点
            subStates = n.nextStep()
            path = []
            # 判断是否和最终结果相同
            if (subStates.state == subStates.answer).all():
                while subStates.parent and subStates.parent != originState:
                    path.append(subStates.parent)
                    subStates = subStates.parent
                path.reverse()
                return path
            openTable.append(subStates)
        else:
            return None, None


def compareNum(state):
    return state.f


if __name__ == '__main__':
    # originState = State(np.array([[1, 5, 2], [7, 0, 4], [6, 3, 8]]))
    # State.answer = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])

    originState = State(np.array([[1, 5, 2],
                            [7, 0, 4],
                            [6, 3, 8]]))

    State.answer = np.array([[1, 2, 3],
                          [4, 5, 6],
                          [7, 8, 0]])

    s1 = State(state=originState.state)
    path = s1.solve()
    if path:
        for node in path:
            node.showInfo()
        print(State.answer)
        print("Total steps is %d" % len(path))
        print("Total count is %d" % State.count)

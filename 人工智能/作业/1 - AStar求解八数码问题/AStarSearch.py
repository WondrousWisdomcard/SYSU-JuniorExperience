import numpy as np
import time

class Solution:

    # State:   self.begin_state   起始状态
    # State:   self.end_state     结束状态
    # State:   self.current_state 当前状态
    # int:     self.searched_num  搜索结点总数
    # State[]: self.explore_list  待检查状态链表
    # State[]: self.visited_list  已检查状态链表
    # State[]: self.path_list     搜索最优路径

    # 初始化A*搜索
    def __init__(self, begin_state, end_state):
        self.begin_state = begin_state
        self.end_state = end_state
        self.current_state = None
        self.searched_num = 0
        self.explore_list = []
        self.visited_list = []
        self.path_list = []

    # 返回 explore_list 中 估价函数最小的节点
    def getBestState(self):

        return_state = self.explore_list[0]
        for explore_state in self.explore_list:
            if explore_state.f < return_state.f:
                return_state = explore_state

        return return_state


    # isVisited 返回 True 如果该状态已经存在于 visited_state 中
    def isVisited(self, next_state):
        for visited_state in self.visited_list:
            if (visited_state.state == next_state.state).all():
                return True
        return False

    # getPath 获取最终解路径，保存在 path_list 中
    def getPath(self):
        temp_state = self.current_state
        self.path_list.append(self.end_state)

        while temp_state.parent and temp_state.parent != self.begin_state:
            self.path_list.append(temp_state.parent)
            temp_state = temp_state.parent

        self.path_list.append(self.begin_state)
        self.path_list.reverse()

    # AStarSolve 搜索
    def AStarSolve(self):

        # 将起始节点放入 explore_list 中
        self.explore_list.append(self.begin_state)
        self.visited_list.append(self.begin_state)

        # 如果 explore_list 为空，则搜索失败，问题无解，否则循环求解
        while len(self.explore_list) > 0:
            self.searched_num += 1
            if self.searched_num % 1000 == 0:
                print(self.searched_num)

            # 取出 explore_list 的估价函数最小的节点，置为当前节点 current_state
            # 若 current_state 为目标节点，则搜索成功，计算解路径，退出
            self.current_state = self.getBestState()
            self.explore_list.remove(self.current_state)
            if (self.current_state.state == self.end_state.state).all():
                self.getPath()
                break

            # 寻找所有与 current_state 邻接且未曾被发现的节点，插入到 explore_list 中
            # 并加入 visited_list 中，表示已发现
            next_list = self.current_state.nextStep()
            for next_state in next_list:
                if not self.isVisited(next_state):
                    self.explore_list.append(next_state)
                    self.visited_list.append(next_state)

    # BFS 用于测试A*是否求得了最优解
    def BFSSolve(self):

        # 将起始节点放入 explore_list 中
        self.explore_list.append(self.begin_state)
        self.visited_list.append(self.begin_state)

        # 如果 explore_list 为空，则搜索失败，问题无解，否则循环求解
        while len(self.explore_list) > 0:
            self.searched_num += 1
            if self.searched_num % 1000 == 0:
                print(self.searched_num)

            # 取出 explore_list 的估价函数最小的节点，置为当前节点 current_state
            # 若 current_state 为目标节点，则搜索成功，计算解路径，退出
            self.current_state = self.explore_list[0]
            del(self.explore_list[0])
            if (self.current_state.state == self.end_state.state).all():
                self.getPath()
                break

            # 寻找所有与 current_state 邻接且未曾被发现的节点，插入到 explore_list 中
            # 并加入 visited_list 中，表示已发现
            next_list = self.current_state.nextStep()
            for next_state in next_list:
                if not self.isVisited(next_state):
                    self.explore_list.append(next_state)
                    self.visited_list.append(next_state)


class State:

    # int[][]:  self.state        当前状态的数码矩阵
    # string[]: self.direction    当前空块的可移动方向
    # State:    self.parent       当前状态的上一个状态
    # int:      self.f            当前状态的估价函数值
    # int:      self.d            当前状态的深度

    dist_state = None

    # 初始化一个状态
    def __init__(self, state, directionFlag=None, parent=None, f=0, d=0):
        self.state = state
        self.direction = ['up', 'down', 'right', 'left']
        if directionFlag:
            self.direction.remove(directionFlag)
        self.parent = parent
        self.f = f
        self.d = d

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
                print(self.state[i, j], end=' ')
            print(" ")
        print('->')
        return

    # 获取0点（即空块在矩阵中的位置）
    def getZeroPos(self):
        postion = np.where(self.state == 0)
        return postion

    # 评估函数计算：目前的评估函数为当前状态与目标状态的哈夫曼距离
    def getFunctionValue(self):
        cur_node = self.state.copy()
        fin_node = self.dist_state.state.copy()
        dist = 0
        error = 0
        N = len(cur_node)
        for i in range(N):
            for j in range(N):
                if cur_node[i][j] != fin_node[i][j]:
                    index = np.argwhere(fin_node == cur_node[i][j])
                    x = index[0][0]  # 最终x距离
                    y = index[0][1]  # 最终y距离
                    dist += (abs(x - i) + abs(y - j))
                    error += 1

        return dist + self.d

    # 寻找当前状态的下一个可行状态集合
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
            news = State(s, directionFlag='right', parent=self, d=self.d + 1)
            news.setF(news.getFunctionValue())
            subStates.append(news)
        # 向上
        if 'up' in self.direction and x > 0:
            # it can move to upper place
            s = self.state.copy()
            tmp = s[x - 1, y]
            s[x - 1, y] = s[x, y]
            s[x, y] = tmp
            news = State(s, directionFlag='down', parent=self, d=self.d + 1)
            news.setF(news.getFunctionValue())
            subStates.append(news)
        # 向下
        if 'down' in self.direction and x < boarder:
            # it can move to down place
            s = self.state.copy()
            tmp = s[x + 1, y]
            s[x + 1, y] = s[x, y]
            s[x, y] = tmp
            news = State(s, directionFlag='up', parent=self, d=self.d + 1)
            news.setF(news.getFunctionValue())
            subStates.append(news)
        # 向右
        if self.direction.count('right') and y < boarder:
            # it can move to right place
            s = self.state.copy()
            tmp = s[x, y + 1]
            s[x, y + 1] = s[x, y]
            s[x, y] = tmp
            news = State(s, directionFlag='left', parent=self, d=self.d + 1)
            news.setF(news.getFunctionValue())
            subStates.append(news)
        # 所有状态
        return subStates


if __name__ == '__main__':

    begin = State(np.array([[1, 5, 2],
                            [7, 0, 4],
                            [6, 3, 8]]))

    # begin = State(np.array([[1, 0, 6],
    #                         [2, 3, 8],
    #                         [5, 4, 7]]))

    # begin = State(np.array([[1, 3, 2],
    #                         [4, 5, 6],
    #                         [8, 7, 0]]))

    end = State(np.array([[1, 2, 3],
                          [4, 5, 6],
                          [7, 8, 0]]))

    State.dist_state = end

    time_start = time.time()
    solution = Solution(begin, end)
    solution.AStarSolve()
    # solution.BFSSolve()
    time_end = time.time()

    if solution.path_list:
        i = 0
        for node in solution.path_list:
            i += 1
            print(str(i) + ": ")
            node.showInfo()

        print("Total search node is %d" % solution.searched_num)
        print("Total steps is %d" % (len(solution.path_list) - 1))

    print('Totally cost is', time_end - time_start, "s")
import datetime
import numpy as np
from matplotlib.ticker import MultipleLocator
from numpy.ma import cos
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import math

DNA_SIZE = 12  # 编码长度
POP_SIZE = 100  # 种群大小
CROSS_RATE = 0.8  # 交叉率
MUTA_RATE = 0.8  # 变异率
Iterations = 100  # 代次数

# 最大值问题范围
X_BOUND = [0, 10]  # X区间
Y_BOUND = [0, 10]  # Y区间

# 最小值问题范围
# X_BOUND = [1, 2]  # X区间
# Y_BOUND = [1, 2]  # Y区间

def F(x, y):  # 问题函数
    # 最大值问题
    return (6.452 * (x + 0.125 * y) * (cos(x) - cos(2 * y)) ** 2) / (0.8 + (x - 4.2) ** 2 + 2 * (y - 7) ** 2) + 3.226 * y
    # 最小值问题
    # return -(20+x**2+y**2-10*(cos(2*math.pi*x)+cos(2*math.pi*y)))

def decodeDNA(pop):  # 基因解码
    x1_pop = pop[:, 0::4]
    y1_pop = pop[:, 1::4]
    x2_pop = pop[:, 2::4]
    y2_pop = pop[:, 3::4]

    x1 = x1_pop.dot(2 ** np.arange(DNA_SIZE)[::-1]) / float(2 ** DNA_SIZE - 1) * (X_BOUND[1] - X_BOUND[0]) + X_BOUND[0]
    y1 = y1_pop.dot(2 ** np.arange(DNA_SIZE)[::-1]) / float(2 ** DNA_SIZE - 1) * (Y_BOUND[1] - Y_BOUND[0]) + Y_BOUND[0]
    x2 = x2_pop.dot(2 ** np.arange(DNA_SIZE)[::-1]) / float(2 ** DNA_SIZE - 1) * (X_BOUND[1] - X_BOUND[0]) + X_BOUND[0]
    y2 = y2_pop.dot(2 ** np.arange(DNA_SIZE)[::-1]) / float(2 ** DNA_SIZE - 1) * (Y_BOUND[1] - Y_BOUND[0]) + Y_BOUND[0]

    x = []
    y = []
    for i in range(POP_SIZE):
        if F(x1[i],y1[i]) > F(x2[i],y2[i]):
            x.append(x1[i])
            y.append(y1[i])
        else:
            x.append(x2[i])
            y.append(y2[i])
    return x, y

def getfitness(pop):  # 计算适应度函数
    x, y = decodeDNA(pop)
    temp = []
    for i in range(POP_SIZE):
        temp.append(F(x[i], y[i]))
    return (temp - np.min(temp)) + 0.0001  # 减去最小的适应度是为了防止适应度出现负数

def select(pop, fitness):  # 根据适应度选择（蒙特卡罗）
    temp = np.random.choice(np.arange(POP_SIZE), size=POP_SIZE, replace=True, p=(fitness) / (fitness.sum()))
    return pop[temp]

def merge(i, j):
    temp = []

    i_x1_pop, i_y1_pop = i[0::4], i[1::4]
    i_x2_pop, i_y2_pop = i[2::4], i[3::4]
    j_x1_pop, j_y1_pop = j[0::4], j[1::4]
    j_x2_pop, j_y2_pop = j[2::4], j[3::4]

    i_x1 = i_x1_pop.dot(2 ** np.arange(DNA_SIZE)[::-1]) / float(2 ** DNA_SIZE - 1) * (X_BOUND[1] - X_BOUND[0]) + X_BOUND[0]
    i_y1 = i_y1_pop.dot(2 ** np.arange(DNA_SIZE)[::-1]) / float(2 ** DNA_SIZE - 1) * (Y_BOUND[1] - Y_BOUND[0]) + Y_BOUND[0]
    i_x2 = i_x2_pop.dot(2 ** np.arange(DNA_SIZE)[::-1]) / float(2 ** DNA_SIZE - 1) * (X_BOUND[1] - X_BOUND[0]) + X_BOUND[0]
    i_y2 = i_y2_pop.dot(2 ** np.arange(DNA_SIZE)[::-1]) / float(2 ** DNA_SIZE - 1) * (Y_BOUND[1] - Y_BOUND[0]) + Y_BOUND[0]

    j_x1 = j_x1_pop.dot(2 ** np.arange(DNA_SIZE)[::-1]) / float(2 ** DNA_SIZE - 1) * (X_BOUND[1] - X_BOUND[0]) + X_BOUND[0]
    j_y1 = j_y1_pop.dot(2 ** np.arange(DNA_SIZE)[::-1]) / float(2 ** DNA_SIZE - 1) * (Y_BOUND[1] - Y_BOUND[0]) + Y_BOUND[0]
    j_x2 = j_x2_pop.dot(2 ** np.arange(DNA_SIZE)[::-1]) / float(2 ** DNA_SIZE - 1) * (X_BOUND[1] - X_BOUND[0]) + X_BOUND[0]
    j_y2 = j_y2_pop.dot(2 ** np.arange(DNA_SIZE)[::-1]) / float(2 ** DNA_SIZE - 1) * (Y_BOUND[1] - Y_BOUND[0]) + Y_BOUND[0]

    if F(i_x1, i_y1) > F(i_x2, i_y2):
        i_x_pop = i_x1_pop
        i_y_pop = i_y1_pop
    else:
        i_x_pop = i_x2_pop
        i_y_pop = i_y2_pop

    if F(j_x1, j_y1) > F(j_x2, j_y2):
        j_x_pop = j_x1_pop
        j_y_pop = j_y1_pop
    else:
        j_x_pop = j_x2_pop
        j_y_pop = j_y2_pop

    for i in range(DNA_SIZE):
        temp.append(i_x_pop[i])
        temp.append(i_y_pop[i])
        temp.append(j_x_pop[i])
        temp.append(j_y_pop[i])

    return temp

def crossmuta(pop, CROSS_RATE):  # 种群的交叉变异操作
    new_pop = []
    for i in pop:  # 遍历种群中的每一个个体，将该个体作为父代
        j = pop[np.random.randint(POP_SIZE)]  # 从种群中随机选择另一个个体，并将该个体作为母代
        temp = merge(i, j)                    # 两个个体的显性基因相结合成新个体
        if np.random.rand() < CROSS_RATE:  # 以交叉概率发生交叉
            cpoints1 = np.random.randint(0, DNA_SIZE * 4 - 1)  # 随机产生交叉的两个点（区间：[cpoints1, cpoints2]）
            cpoints2 = np.random.randint(cpoints1, DNA_SIZE * 4)
            temp[cpoints1:cpoints2] = j[cpoints1:cpoints2]  # 子代得到位于交叉点后的母代的基因

        mutation(temp, MUTA_RATE)  # 每一个后代以变异率发生变异
        new_pop.append(temp)
    return new_pop

def mutation(temp, MUTA_RATE):
    if np.random.rand() < MUTA_RATE:  # 以MUTA_RATE的概率进行变异
        mutate_point = np.random.randint(0, DNA_SIZE * 4)  # 随机产生一个实数，代表要变异基因的位置
        temp[mutate_point] = temp[mutate_point] ^ 1  # 将变异点的二进制为反转

# 画图
def plot_3d(ax):
    X = np.linspace(*X_BOUND, 100)
    Y = np.linspace(*Y_BOUND, 100)
    X, Y = np.meshgrid(X, Y)
    Z = F(X, Y)
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm)
    ax.set_zlim(-20, 100)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    plt.pause(3)
    plt.show()

def OPT2_TEST():
    i_list = range(100)
    best_fitness = []
    best_f = []
    for i in i_list:
        print(i)
        pop = np.random.randint(2, size=(POP_SIZE, DNA_SIZE * 4))  # pop（二维矩阵） = (种群数) * (DNA长度 * 4) 个 0,1 随机数
        for _ in range(Iterations):  # 迭代 N 代
            pop = np.array(crossmuta(pop, CROSS_RATE))  # 对种群进行交叉（cross）和变异（muta）
            fitness = getfitness(pop)  # 计算种群每一个基因的适应度函数
            pop = select(pop, fitness)  # 选择生成新的种群

        fitness = getfitness(pop)
        maxfitness = np.argmax(fitness)
        x, y = decodeDNA(pop)
        best_fitness.append(fitness[maxfitness])
        best_f.append(F(x[maxfitness], y[maxfitness]))

    best_f.sort()
    plt.plot(i_list, best_f, marker='o', label="F_max(x,y)")
    plt.gca().xaxis.set_major_locator(MultipleLocator(10))
    plt.legend()
    plt.show()

def print_info(pop):  # 用于输出结果
    fitness = getfitness(pop)
    maxfitness = np.argmax(fitness)  # 返回最大值的索引值
    print("迭代次数: ", Iterations)
    print("最大适应度: ", fitness[maxfitness])
    x,y = decodeDNA(pop)
    print("最优基因型: ", pop[maxfitness])
    print("最优解 (x,y) = ", (x[maxfitness], y[maxfitness]))
    print("最优值 F(x,y) = ", F(x[maxfitness],y[maxfitness]))

if __name__ == "__main__":

    # OPT2_TEST()

    fig = plt.figure()
    ax = Axes3D(fig)
    plt.ion()
    plot_3d(ax)

    start_t = datetime.datetime.now()
    pop = np.random.randint(2, size=(POP_SIZE, DNA_SIZE * 4))  # pop（二维矩阵） = 种群数 * (DNA长度 * 2) 个 0,1 随机数
    for _ in range(Iterations):  # 迭代 N 代
        x, y = decodeDNA(pop)
        temp = []
        for i in range(POP_SIZE):
            temp.append(F(x[i], y[i]))
        # 更新画图
        if 'sca' in locals():
            sca.remove()
        sca = ax.scatter(x, y, temp, c='black', marker='o')
        plt.show()
        plt.pause(0.1)

        pop = np.array(crossmuta(pop, CROSS_RATE))  # 对种群进行交叉（cross）和变异（muta）
        fitness = getfitness(pop)  # 计算种群每一个基因的适应度函数
        pop = select(pop, fitness)  # 选择生成新的种群

    end_t = datetime.datetime.now()
    print("耗时: ", (end_t - start_t))
    print_info(pop)
    plt.ioff()
    plot_3d(ax)


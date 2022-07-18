import numpy as np
import random
import matplotlib.pyplot as plt
import copy


#各个城市的坐标
# City_Map = [[106.54,29.59]
# ,[91.11,29.97]
# ,[87.68,43.77]
# ,[106.27,38.47]
# ,[111.65,40.82]
# ,[108.33,22.84]
# ,[126.63,45.75]
# ,[125.35,43.88]
# ,[123.38,41.8]
# ,[114.48,38.03]
# ,[112.53,37.87]
# ,[101.74,36.56]
# ,[117,36.65]
# ,[113.6,34.76]
# ,[118.78,32.04]
# ,[117.27,31.86]]

City_Map = 100 * np.random.rand(20, 2)#随机产生20个城市

DNA_SIZE = len(City_Map) #编码长度

POP_SIZE = 200 #种群大小
CROSS_RATE = 0.6 #交叉率
MUTA_RATE = 0.2 #变异率
Iterations = 1000 #迭代次数


def distance(DNA):#根据DNA的路线计算距离
    dis = 0
    temp = City_Map[DNA[0]]
    for i in DNA[1:]:
        dis = dis + ((City_Map[i][0]-temp[0])**2+(City_Map[i][1]-temp[1])**2)**0.5
        temp = City_Map[i]
    return dis+((temp[0]-City_Map[DNA[0]][0])**2+(temp[1]-City_Map[DNA[0]][1])**2)**0.5

def getfitness(pop):#计算种群适应度，这里适应度用距离的倒数表示
    temp = []
    for i in range(len(pop)):
        temp.append(1/(distance(pop[i])))
    return  temp-np.min(temp)

def select(pop, fitness):    # 根据适应度选择，以赌轮盘的形式，适应度越大的个体被选中的概率越大
    s = fitness.sum()
    temp = np.random.choice(np.arange(len(pop)), size=POP_SIZE, replace=True,p=(fitness/s))
    p = []
    for i in temp:
        p.append(pop[i])
    return p

def mutation(DNA, MUTA_RATE):#进行变异
    if np.random.rand() < MUTA_RATE: 				#以MUTA_RATE的概率进行变异
        mutate_point1 = np.random.randint(0, DNA_SIZE)#随机产生一个实数，代表要变异基因的位置
        mutate_point2 = np.random.randint(0,DNA_SIZE)#随机产生一个实数，代表要变异基因的位置
        while(mutate_point1 == mutate_point2):#保证2个所选位置不相等
            mutate_point2 = np.random.randint(0,DNA_SIZE)
        DNA[mutate_point1],DNA[mutate_point2] = DNA[mutate_point2],DNA[mutate_point1] #2个所选位置进行互换

def crossmuta(pop, CROSS_RATE):#交叉变异
    new_pop = []
    for i in range(len(pop)):#遍历种群中的每一个个体，将该个体作为父代
        n=np.random.rand()
        if n>=CROSS_RATE:#大于交叉概率时不发生变异，该子代直接进入下一代
            temp = pop[i].copy()
            new_pop.append(temp)

        if n<CROSS_RATE:#小于交叉概率时发生变异
            list1 = pop[i].copy()
            list2 = pop[np.random.randint(POP_SIZE)].copy()#选取种群中另一个个体进行交叉
            status = True
            while status:#产生2个不相等的节点，中间部分作为交叉段，采用部分匹配交叉
                k1 = random.randint(0, len(list1) - 1)
                k2 = random.randint(0, len(list2) - 1)
                if k1 < k2:
                    status = False

            k11 = k1

            fragment1 = list1[k1: k2]
            fragment2 = list2[k1: k2]

            list1[k1: k2] = fragment2
            list2[k1: k2] = fragment1

            del list1[k1: k2]
            left1 = list1

            offspring1 = []
            for pos in left1:
                if pos in fragment2:
                    pos = fragment1[fragment2.index(pos)]
                    while pos in fragment2:
                        pos = fragment1[fragment2.index(pos)]
                    offspring1.append(pos)
                    continue
                offspring1.append(pos)
            for i in range(0, len(fragment2)):
                offspring1.insert(k11, fragment2[i])
                k11 += 1
            temp = offspring1.copy()
            mutation(temp,MUTA_RATE)

            new_pop.append(temp)#把部分匹配交叉后形成的合法个体加入到下一代种群

    return new_pop


def print_info(pop):#用于输出结果
    fitness = getfitness(pop)
    maxfitness = np.argmax(fitness)#得到种群中最大适应度个体的索引
    #打印结果
    print("最优的基因型：", pop[maxfitness])
    print("最短距离：",distance(pop[maxfitness]))
    #按最优结果顺序把地图上的点加入到best_map列表中
    best_map = []
    for i in pop[maxfitness]:
        best_map.append(City_Map[i])
    best_map.append(City_Map[pop[maxfitness][0]])
    X = np.array((best_map))[:,0]
    Y = np.array((best_map))[:,1]
    #绘制地图以及路线
    plt.figure()
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.scatter(X,Y)
    for dot in range(len(X)-1):
        plt.annotate(pop[maxfitness][dot],xy=(X[dot],Y[dot]),xytext = (X[dot],Y[dot]))
    plt.annotate('start',xy=(X[0],Y[0]),xytext = (X[0]+1,Y[0]))
    plt.plot(X,Y)


if __name__ == "__main__":#主循环
    #生成初代种群pop
    pop = []
    list = list(range(DNA_SIZE))
    for i in range(POP_SIZE):
        random.shuffle(list)
        l = list.copy()
        pop.append(l)
    best_dis= []
    #进行选择，交叉，变异，并把每代的最优个体保存在best_dis中
    for i in range(Iterations):  # 迭代N代
        pop = crossmuta(pop, CROSS_RATE)
        fitness = getfitness(pop)
        maxfitness = np.argmax(fitness)
        best_dis.append(distance(pop[maxfitness]))
        pop = select(pop, fitness)  # 选择生成新的种群

    print_info(pop)#打印信息

    print('逐代的最小距离：',best_dis)

#画图
plt.figure()
plt.plot(range(Iterations),best_dis)
plt.show()
plt.close()


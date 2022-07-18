import numpy as np
from numpy.ma import cos
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import math

DNA_SIZE = 24 #编码长度
POP_SIZE = 200 #种群大小
CROSS_RATE = 0.5 #交叉率
MUTA_RATE = 0.015 #变异率
Iterations = 50 #迭代次数
X_BOUND = [1,2]#X区间
Y_BOUND = [1,2]#Y区间

def F(x, y): #适应度函数
    return 20+x**2+y**2-10*(cos(2*math.pi*x)+cos(2*math.pi*y))


def decodeDNA(pop):#解码
    x_pop = pop[:,1::2]#奇数列表示X
    y_pop = pop[:,::2] #偶数列表示y
    x = x_pop.dot(2**np.arange(DNA_SIZE)[::-1])/float(2**DNA_SIZE-1)*(X_BOUND[1]-X_BOUND[0])+X_BOUND[0]
    y = y_pop.dot(2**np.arange(DNA_SIZE)[::-1])/float(2**DNA_SIZE-1)*(Y_BOUND[1]-Y_BOUND[0])+Y_BOUND[0]
    return x,y

def getfitness(pop):
    x,y = decodeDNA(pop)
    temp = F(x, y)
    return -(temp - np.max(temp)) + 0.0001  # 减去最大的适应度是为了防止适应度出现负数

def select(pop, fitness):    # 根据适应度选择
	temp = np.random.choice(np.arange(POP_SIZE), size=POP_SIZE, replace=True,p=(fitness)/(fitness.sum()))
	return pop[temp]


def crossmuta(pop, CROSS_RATE):
	new_pop = []
	for i in pop:		#遍历种群中的每一个个体，将该个体作为父代
		temp = i		#子代先得到父亲的全部基因
		if np.random.rand() < CROSS_RATE:			#以交叉概率发生交叉
			j = pop[np.random.randint(POP_SIZE)]	#从种群中随机选择另一个个体，并将该个体作为母代
			cpoints1 = np.random.randint(0, DNA_SIZE*2-1)	#随机产生交叉的点
			cpoints2 = np.random.randint(cpoints1,DNA_SIZE*2)
			temp[cpoints1:cpoints2] = j[cpoints1:cpoints2]		#子代得到位于交叉点后的母代的基因
		mutation(temp,MUTA_RATE)	#后代以变异率发生变异
		new_pop.append(temp)
	return new_pop

def mutation(temp, MUTA_RATE):
	if np.random.rand() < MUTA_RATE: 				#以MUTA_RATE的概率进行变异
		mutate_point = np.random.randint(0, DNA_SIZE)	#随机产生一个实数，代表要变异基因的位置
		temp[mutate_point] = temp[mutate_point]^1 	#将变异点的二进制为反转

def print_info(pop):#用于输出结果
	fitness = getfitness(pop)
	minfitness = np.argmin(fitness)
	print("min_fitness:", fitness[minfitness])
	x,y = decodeDNA(pop)
	print("最优的基因型：", pop[minfitness])
	print("(x, y):", (x[minfitness], y[minfitness]))
	print("F(x,y)_min = ",F(x[minfitness],y[minfitness]))

def plot_3d(ax):
	X = np.linspace(*X_BOUND, 100)
	Y = np.linspace(*Y_BOUND, 100)
	X, Y = np.meshgrid(X, Y)
	Z = F(X, Y)
	ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm)
	ax.set_zlim(-20, 40)
	ax.set_xlabel('x')
	ax.set_ylabel('y')
	ax.set_zlabel('z')
	plt.pause(3)
	plt.show()

if __name__ == "__main__":
	fig = plt.figure()
	ax = Axes3D(fig)
	plt.ion()
	plot_3d(ax)

	pop = np.random.randint(2, size=(POP_SIZE, DNA_SIZE * 2))
	for _ in range(Iterations):  # 迭代N代
		x, y = decodeDNA(pop)
		if 'sca' in locals():
			sca.remove()
		sca = ax.scatter(x, y, F(x, y), c='black', marker='o');
		plt.show();
		plt.pause(0.1)
		pop = np.array(crossmuta(pop, CROSS_RATE))
		fitness = getfitness(pop)
		pop = select(pop, fitness)  # 选择生成新的种群

print_info(pop)
plt.ioff()
plot_3d(ax)
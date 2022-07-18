import numpy as np

class SoftmaxLinearClassifier(object):

    def __init__(self):
        """
        初始化
        - W: (D, C) 权重矩阵
            - D: 样本的维度
            - C: 类别的数目权重向量
        - reg_style: (string) "L2" or "L1" 指定采用的正则化方法
        - reg_strength: (float) 正则化的强度
        """
        self.W = None
        self.reg_style = None
        self.reg_strength = 0

    def train(self, X, y, learning_rate=1e-3, reg_style="L2", reg_strength=1e-5,
              ite_num=100, batch_size=100, print_times=-1, m=0, v=0, t=0):
        """
        训练 使用 SGD（随机梯度下降）训练模型

        Inputs:
        - X: (N,D) numpy array 训练样本
            - N: 训练样本数目
            - D: 样本的维度
        - y: (N, ) numpy array 训练标签
        - learning_rate: (float) 学习率
        - reg_style: (string) "L2" or "L1" 指定采用的正则化方法
        - reg_strength: (float) 正则化的强度
        - ite_num: (integer) 迭代次数，每次迭代结束进行权重优化
        - batch_size: (integer) 每次迭代选取的样本数目
        - print_times: (integer) 训练过程中输出训练损失的次数，-1即不输出

        Output:
        - loss_history: (list) 记录每一次迭代损失函数的变化
        """

        bias_x = np.ones(X.shape[0]).reshape(-1, 1)
        X = np.concatenate((X, bias_x), axis=1)

        loss_history = []
        train_num, train_dim = X.shape
        class_num = np.max(y) + 1

        if self.W is None:
            self.W = np.random.randn(train_dim, class_num)
        self.reg_style = reg_style
        self.reg_strength = reg_strength

        for ite in range(ite_num):

            batch_mask = np.random.choice(train_num, batch_size)
            X_batch = X[batch_mask]
            y_batch = y[batch_mask]

            loss, grad = self.loss(X_batch, y_batch)
            loss_history.append(loss)

            self.W -= grad * learning_rate

            # Adam 自适应梯度下降 效果一般
            # beta1 = 0.9
            # beta2 = 0.999
            # eps = 1e-8
            # t += 1
            #
            # m = beta1 * m + (1 - beta1) * grad
            # mt = m / (1 - beta1 ** t)
            # v = beta2 * v + (1 - beta2) * (grad ** 2)
            # vt = v / (1 - beta2 ** t)
            # self.W += - learning_rate * mt / (np.sqrt(vt) + eps)

            if print_times != -1:
                if (ite % (ite_num / print_times) == 0) or (ite == ite_num - 1):
                    print("Iteration %d / %d: Loss %f" % (ite, ite_num, loss))

        return loss_history

    def loss(self, X, y):
        """
        计算损失函数

        Inputs:
        - X: (N,D) numpy array 训练样本
            - N: 训练样本数目
            - D: 样本的维度
        - y: (N, ) numpy array 训练标签

        Outputs:
        - loss: (float) 损失值
        - dW: (D, C) numpy array 权重损失梯度
            - D: 样本的维度
            - C: 类别的数目
        """
        train_num, train_dim = X.shape

        s = np.matmul(X, self.W)
        s -= np.max(s, axis=1, keepdims=True)
        p = np.exp(s) / np.sum(np.exp(s), axis=1, keepdims=True)
        loss = -1 * np.sum(np.log(p[range(train_num), y])) / train_num

        p[range(train_num), y] -= 1
        dW = np.matmul(X.T, p) / train_num

        if self.reg_style == "L2":
            loss += self.reg_strength * np.sum(self.W * self.W)
            dW += 2 * self.reg_strength * self.W
        elif self.reg_style == "L1":
            loss += self.reg_strength * np.sum(np.fabs(self.W))
            dW += self.reg_strength * self.W / np.fabs(self.W)
        return loss, dW

    def predict(self, X):
        """
        预测 对样本的标签进行预测

        Inputs:
        - X: (M,D) numpy array 待预测样本
            - M: 样本的数目
            - D: 样本的维度

        Outputs:
        - y_pred: (M,)  numpy array 待预测样本的预测标签
        """
        bias_x = np.ones(X.shape[0]).reshape(-1, 1)
        X = np.concatenate((X, bias_x), axis=1)

        y_pred = np.argmax(X.dot(self.W), axis=1)
        return y_pred



class SoftmaxNonlinearClassifier(SoftmaxLinearClassifier):

    def __init__(self, kernel_function=None):
        """
        初始化
        - W: (D, C) 权重矩阵
            - D: 样本的维度
            - C: 类别的数目权重向量
        - reg_style: (string) "L2" or "L1" 指定采用的正则化方法
        - reg_strength: (float) 正则化的强度
        """
        self.kernel_function = kernel_function
        super().__init__()

    def train(self, X, y, learning_rate=1e-3, reg_style="L2", reg_strength=1e-5,
              ite_num=100, batch_size=100, print_times=-1):

        if self.kernel_function is not None:
            X = self.kernel_function(X)

        return super().train(X, y, learning_rate, reg_style, reg_strength, ite_num, batch_size, print_times)

    def predict(self, X):

        if self.kernel_function is not None:
            X = self.kernel_function(X)

        return super().predict(X)




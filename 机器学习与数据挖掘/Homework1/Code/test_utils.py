import matplotlib.pyplot as plt
from time import time
import numpy as np
import matplotlib.pyplot as plt

from sklearn.manifold import TSNE

from data_utils import *
from visual_utils import *
from Classifiers.softmax_classifier import SoftmaxLinearClassifier
from Classifiers.softmax_classifier import SoftmaxNonlinearClassifier
from Classifiers.kernel import *

def learning_rate_cross_validition(X, y, ite_num=2000, batch_size=500, learning_rates=None, nonlinear_kernel=None):
    """
    学习率交叉验证
    * 交叉验证的次数（Fold）：10
    * 迭代次数：2000
    * 每次迭代处理样本数：500
    * 正则化类型及系数：无
    """
    num_folds = 10
    if learning_rates is None:
        learning_rates = [10, 5, 2, 1.5, 1, 0.5, 0.1]

    X_train_folds = np.array_split(X, num_folds)
    y_train_folds = np.array_split(y, num_folds)
    k_to_accuracies = {}
    num_folds_count = np.ceil(X.shape[0] / num_folds)

    for lr in learning_rates:
        k_to_accuracies[lr] = []
        for j in range(num_folds):
            X_train_folds_train = X_train_folds[0]
            y_train_folds_train = y_train_folds[0]
            for k in range(num_folds):
                if k != j:
                    X_train_folds_train = np.concatenate((X_train_folds_train, X_train_folds[k]), axis=0)
                    y_train_folds_train = np.concatenate((y_train_folds_train, y_train_folds[k]), axis=0)
            X_train_folds_train = X_train_folds_train[len(X_train_folds[0]):]
            y_train_folds_train = y_train_folds_train[len(y_train_folds[0]):]

            if nonlinear_kernel is None:
                softmax = SoftmaxLinearClassifier()
            else:
                softmax = SoftmaxNonlinearClassifier(nonlinear_kernel)

            loss_history = softmax.train(X_train_folds_train, y_train_folds_train, learning_rate=lr, reg_style="L2",
                                         reg_strength=0,
                                         ite_num=ite_num, batch_size=batch_size, print_times=-1)

            y_test_pred = softmax.predict(X_train_folds[j])
            num_correct = np.sum(y_test_pred == y_train_folds[j])
            accuracy = float(num_correct) / len(y_train_folds[j])
            k_to_accuracies[lr].append(accuracy)

    # 散点图显示交叉验证正确率
    for k in learning_rates:
        accuracies = k_to_accuracies[k]
        plt.scatter([k] * len(accuracies), accuracies)

    # 显示均值和方差
    accuracies_mean = np.array([np.mean(v) for k, v in k_to_accuracies.items()])
    accuracies_std = np.array([np.std(v) for k, v in k_to_accuracies.items()])
    plt.errorbar(learning_rates, accuracies_mean, yerr=accuracies_std)
    plt.title('Cross-validation on Learning Rate')
    plt.xlabel('Learning Rate')
    plt.ylabel('Cross-validation accuracy')
    plt.show()


def normalization_cross_validition(X, y, ite_num=1000, batch_size=100, reg_styles=None, nonlinear_kernel=None):
    """
    正则化方法及系数交叉验证
    * 交叉验证的次数（Fold）：10
    * 迭代次数：2000
    * 每次迭代处理样本数：500
    * 学习率：1.5
    """
    num_folds = 10
    if reg_styles is None:
        reg_styles = [-1e-3, -1e-4, -1e-5, 0, 1e-5, 1e-4, 1e-3]

    X_train_folds = np.array_split(X, num_folds)
    y_train_folds = np.array_split(y, num_folds)
    k_to_accuracies = {}
    num_folds_count = np.ceil(X.shape[0] / num_folds)

    for rs in reg_styles:
        k_to_accuracies[rs] = []
        for j in range(num_folds):
            X_train_folds_train = X_train_folds[0]
            y_train_folds_train = y_train_folds[0]
            for k in range(num_folds):
                if k != j:
                    X_train_folds_train = np.concatenate((X_train_folds_train, X_train_folds[k]), axis=0)
                    y_train_folds_train = np.concatenate((y_train_folds_train, y_train_folds[k]), axis=0)
            X_train_folds_train = X_train_folds_train[len(X_train_folds[0]):]
            y_train_folds_train = y_train_folds_train[len(y_train_folds[0]):]

            if nonlinear_kernel is None:
                softmax = SoftmaxLinearClassifier()
            else:
                softmax = SoftmaxNonlinearClassifier(nonlinear_kernel)

            if rs < 0:
                strength = -rs
                style = "L1"
            else:
                style = "L2"
                strength = rs

            loss_history = softmax.train(X_train_folds_train, y_train_folds_train, learning_rate=2, reg_style=style,
                                         reg_strength=strength,
                                         ite_num=ite_num, batch_size=batch_size, print_times=-1)

            y_test_pred = softmax.predict(X_train_folds[j])
            num_correct = np.sum(y_test_pred == y_train_folds[j])
            accuracy = float(num_correct) / len(y_train_folds[j])
            k_to_accuracies[rs].append(accuracy)

    # 散点图显示交叉验证正确率
    l = [-3, -2, -1, 0, 1, 2, 3]
    i = 0
    for k in reg_styles:
        accuracies = k_to_accuracies[k]
        plt.scatter([l[i]] * len(accuracies), accuracies)
        i += 1

    # 显示均值和方差
    accuracies_mean = np.array([np.mean(v) for k, v in k_to_accuracies.items()])
    accuracies_std = np.array([np.std(v) for k, v in k_to_accuracies.items()])
    plt.errorbar(l, accuracies_mean, yerr=accuracies_std)
    plt.xticks(l, ["1e-3 L1", "1e-4 L1", "1e-5 L1", "None", "1e-5 L2", "1e-4 L2", "1e-3 L2"])
    plt.title('Cross-validation on Normalization')
    plt.xlabel('Normalization Strength & Style')
    plt.ylabel('Cross-validation accuracy')
    plt.show()


def softmax_validition(X, y, ite_num=1000, batch_size=100, reg_style="L1"):
    """
    分类器交叉验证：线性、三阶非线性、五阶非线性
    * 交叉验证的次数（Fold）：10
    * 迭代次数：2000
    * 每次迭代处理样本数：500
    * 学习率：1.5
    """
    num_folds = 10

    kernel = [("Linear", None), ("X_3_Nonlinear",x_3_kernel), ("X_5_Nonlinear", x_5_kernel)]
    reg_style = ["L0", "L1", "L2"]

    X_train_folds = np.array_split(X, num_folds)
    y_train_folds = np.array_split(y, num_folds)
    k_to_accuracies = {}
    num_folds_count = np.ceil(X.shape[0] / num_folds)

    for n, ke in kernel:
        k_to_accuracies[n] = []
        for j in range(num_folds):
            X_train_folds_train = X_train_folds[0]
            y_train_folds_train = y_train_folds[0]
            for k in range(num_folds):
                if k != j:
                    X_train_folds_train = np.concatenate((X_train_folds_train, X_train_folds[k]), axis=0)
                    y_train_folds_train = np.concatenate((y_train_folds_train, y_train_folds[k]), axis=0)
            X_train_folds_train = X_train_folds_train[len(X_train_folds[0]):]
            y_train_folds_train = y_train_folds_train[len(y_train_folds[0]):]

            softmax = SoftmaxNonlinearClassifier(kernel_function=ke)

            loss_history = softmax.train(X_train_folds_train, y_train_folds_train, learning_rate=1.5, reg_style="L1",
                                         reg_strength=1e-4, ite_num=ite_num, batch_size=batch_size, print_times=-1)

            y_test_pred = softmax.predict(X_train_folds[j])
            num_correct = np.sum(y_test_pred == y_train_folds[j])
            accuracy = float(num_correct) / len(y_train_folds[j])
            k_to_accuracies[n].append(accuracy)

    # 散点图显示交叉验证正确率
    l = [-1, 0, 1]
    i = 0
    for n, k in kernel:
        accuracies = k_to_accuracies[n]
        plt.scatter([l[i]] * len(accuracies), accuracies)
        i += 1

    # 显示均值和方差
    accuracies_mean = np.array([np.mean(v) for k, v in k_to_accuracies.items()])
    accuracies_std = np.array([np.std(v) for k, v in k_to_accuracies.items()])
    plt.errorbar(l, accuracies_mean, yerr=accuracies_std)
    plt.xticks(l, ["Linear", "X_3_Nonlinear", "X_5_Nonlinear"])
    plt.title('Cross-validation on Classifier')
    plt.xlabel('Classifier Type')
    plt.ylabel('Cross-validation accuracy')
    plt.show()

def test_acc(X, y, softmax, ite_num=2000, check_frequency=10, reg_style="L1", reg_strength=1e-4):
    """
    测试：准确率-生成准确率迭代曲线
    """
    num = int(len(y) * 0.9)
    X_train = X[:num]
    y_train = y[:num]
    X_test = X[num:]
    y_test = y[num:]

    test_accuracy = []
    train_accuracy = []

    for i in range(ite_num // check_frequency):
        softmax.train(X_train, y_train, learning_rate=1.5, reg_style=reg_style, reg_strength=reg_strength,
                      ite_num=check_frequency, batch_size=1000)

        y_pred_train = softmax.predict(X_train)
        y_pred_test = softmax.predict(X_test)
        train_accuracy.append(np.mean(y_train == y_pred_train))
        test_accuracy.append(np.mean(y_test == y_pred_test))

    show_acc(train_accuracy, test_accuracy)


def get_precision_and_recall(y, y_pred, classes):
    """
    计算：Precision 和 Recall 并返回
    """
    cn = len(classes)
    mat = np.zeros((cn, cn))

    for i in range(len(y)):
        mat[y_pred[i]][y[i]] += 1

    precision_sum = np.sum(mat, axis=1)
    recall_sum = np.sum(mat, axis=0)

    precision = []
    recall = []
    for i in range(cn):
        precision.append(mat[i][i] / (precision_sum[i] + 0.01))
        recall.append(mat[i][i] / (recall_sum[i] + 0.01))

    return precision, recall


def test_pre_rec(X, y, attrs, classes, softmax):
    """
    测试：
    - Precision 和 Recall，并生成柱状图
    - 生成权重矩阵
    - 生成损失函数折线图
    """
    num = int(len(y) * 0.9)
    X_train = X[:num]
    y_train = y[:num]
    X_test = X[num:]
    y_test = y[num:]

    loss_history = softmax.train(X_train, y_train, learning_rate=1.5, reg_style="L1", reg_strength=1e-4,
                                 ite_num=2000, batch_size=500)

    y_pred_train = softmax.predict(X_train)
    y_pred_test = softmax.predict(X_test)

    acc_train = np.mean(y_train == y_pred_train)
    acc_test = np.mean(y_test == y_pred_test)

    precision, recall = get_precision_and_recall(y_train, y_pred_train, classes)
    precision_t, recall_t = get_precision_and_recall(y_test, y_pred_test, classes)
    print(precision)
    print(recall)
    print(precision_t)
    print(recall_t)
    show_bar(classes, precision, precision_t, title="Precision")
    show_bar(classes, recall, recall_t, title="Recall")


def gen_w_loss(X, y, attrs, classes, softmax):
    """
    测试：
    - Precision 和 Recall，并生成柱状图
    - 生成权重矩阵
    - 生成损失函数折线图
    """
    num = int(len(y) * 0.9)
    X_train = X[:num]
    y_train = y[:num]
    X_test = X[num:]
    y_test = y[num:]

    loss_history = softmax.train(X_train, y_train, learning_rate=1.5, reg_style="L1", reg_strength=1e-4,
                                 ite_num=2000, batch_size=500)

    y_pred_train = softmax.predict(X_train)
    y_pred_test = softmax.predict(X_test)

    acc_train = np.mean(y_train == y_pred_train)
    acc_test = np.mean(y_test == y_pred_test)

    print(loss_history)

    show_W(softmax.W, "Dimision", "Category", "Wine Quality Classification", attrs, classes,
           kernel_string=["", "^2", "^3", "^4", "^5"])
    show_loss(loss_history)

def t_sne(data, label, classes):
    """
    t-sne 数据降维, 输出降维后的图像
    """
    n_samples, n_features = data.shape
    tsne = TSNE(n_components=2, init='pca', random_state=0)
    t0 = time()
    result = tsne.fit_transform(data)

    fig = show_t_sne(result, label, classes,
                     't-SNE embedding of the digits (time %.2fs)'
                     % (time() - t0))


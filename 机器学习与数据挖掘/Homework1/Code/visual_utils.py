import numpy as np
from matplotlib import pyplot as plt

def show_W(W, xlabel=None, ylabel=None, title=None, xticks = None, yticks = None, kernel_string=None):
    """
    绘制权重矩阵
    """
    plt.imshow(W.T, interpolation='nearest', cmap='plasma', origin='upper')
    plt.colorbar(shrink=0.9)
    if xlabel is not None:
        plt.xlabel(xlabel)
    if ylabel is not None:
        plt.ylabel(ylabel)
    if title is not None:
        plt.title(title)
    if xticks is not None:
        llx = []
        for i in range(int(W.shape[0] / len(xticks))):
            for j in range(len(xticks)):
                llx.append(xticks[j] + kernel_string[i])
        llx.append("Bias")
        plt.xticks(range(W.shape[0]), llx)
        plt.xticks(rotation=90)
    if yticks is not None:
        print(yticks)
        plt.yticks(range(W.shape[1]), yticks[:W.shape[1]])
    plt.gcf().subplots_adjust(bottom=0.3)
    plt.show()

def show_loss(loss_history, xlabel=None, ylabel=None, title=None):
    """
    绘制损失函数曲线
    """
    ma = []
    for i in range(5, len(loss_history) - 5):
        ma.append(np.mean(loss_history[i - 5: i + 5]))

    plt.plot(loss_history)
    plt.plot(range(5, len(loss_history) - 5), ma)
    if xlabel is not None:
        plt.xlabel(xlabel)
    if ylabel is not None:
        plt.ylabel(ylabel)
    if title is not None:
        plt.title(title)
    plt.show()

def show_acc(train_acc, test_acc, title=None):
    """
    绘制正确率曲线
    """
    plt.plot(train_acc, label="Train Accuracy")
    plt.plot(test_acc, label="Test Accuracy")
    if title is not None:
        plt.title(title)
    plt.yticks(np.arange(0.5, 1, 0.1))
    plt.legend()
    plt.show()

def show_t_sne(data, label, classes, title):
    """
    绘制降维 t-sne 图像
    """
    x_min, x_max = np.min(data, 0), np.max(data, 0)
    data = (data - x_min) / (x_max - x_min)

    for i in range(data.shape[0]):
        plt.scatter(data[i, 0], data[i, 1], color=plt.cm.hsv(label[i] / len(classes)))
    plt.xticks([])
    plt.yticks([])
    plt.title(title)
    plt.show()

def show_bar(x, y1, y2, title=None):
    """
    绘制 Precision 和 Recall 的柱状图
    """
    width = 0.35  # the width of the bars
    i = np.arange(len(x))

    fig, ax = plt.subplots()
    rects1 = ax.bar(i - width / 2, y1, width, label='Train')
    rects2 = ax.bar(i + width / 2, y2, width, label='Test')

    if title is not None:
        ax.set_title(title)
    ax.legend()
    ax.set_xticks(i, x)
    ax.bar_label(rects1, fmt='%.3f', padding=3)
    ax.bar_label(rects2, fmt='%.3f', padding=3)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    fig.tight_layout()
    plt.show()
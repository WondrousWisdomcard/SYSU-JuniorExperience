import numpy as np
from time import time
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import os

colormap = ["#AADDFF", "#AAFFDD", "#DDAAFF", "#DDFFAA", "#FFAADD", "#FFDDAA", "#AADDAA", "#DDAADD",
            "#AA55FF", "#AA55DD", "#DD55FF", "#DD55AA", "#FF55DD", "#FF55AA", "#AA55AA", "#DD55DD",
            "#55DDFF", "#55FFDD", "#55AAFF", "#55FFAA", "#55AADD", "#55DDAA", "#55DDAA", "#55AADD",
            "#AADD55", "#AAFF55", "#DDAA55", "#DDFF55", "#FFAA55", "#FFDD55", "#AADD55", "#DDAA55"]
colormap2 = ["#00DDFF", "#00FFDD", "#DD00FF", "#DDFF00", "#FF00DD", "#FFDD00", "#33DD33", "#DD33DD",
             "#AA33FF", "#AA33DD", "#DD33FF", "#DD33AA", "#FF33DD", "#FF33AA", "#AA33AA", "#DD33DD",
             "#33DDFF", "#33FFDD", "#33AAFF", "#33FFAA", "#33AADD", "#33DDAA", "#33DDAA", "#33AADD",
             "#AADD33", "#AAFF33", "#DDAA33", "#DDFF33", "#FFAA33", "#FFDD33", "#AADD33", "#DDAA33"]


def show_data2D(data, label, classes, title, path):
    x_min, x_max = np.min(data, 0), np.max(data, 0)
    data = (data - x_min) / (x_max - x_min)

    for i in range(data.shape[0]):
        plt.scatter(data[i, 0], data[i, 1], color=colormap[int(label[i])])
    plt.title(title)
    print("Save Pic: ", path)
    plt.savefig(path)
    plt.clf()


def show_t_sne(data, label, classes, name=""):
    """
    t-sne 数据降维, 输出降维后的图像
    """
    path = "../DataImage/"
    if not os.path.exists(path):
        os.makedirs(path)
    tsne = TSNE(n_components=2, init='pca', random_state=0)
    t0 = time()
    result = tsne.fit_transform(data)
    path = path + name + "_tsne.jpg"
    show_data2D(result, label, classes,
                'Dataset: ' + name + ' t-SNE embedding of the digits (time %.2fs)'
                % (time() - t0), path)


def show_pca(data, label, classes, name=""):
    """
    pca 数据降维, 输出降维后的图像
    """
    path = "../DataImage/"
    if not os.path.exists(path):
        os.makedirs(path)
    pca = PCA(n_components=2)
    t0 = time()
    result = pca.fit_transform(data)
    path = path + name + "_pca.jpg"
    show_data2D(result, label, classes,
                'Dataset: ' + name + 'PCA embedding of the digits (time %.2fs)'
                % (time() - t0), path)


def show_anim(data, labels, centers, name=""):
    path = "../AnimImage"
    if not os.path.exists(path):
        os.makedirs(path)

    pca = PCA(n_components=2)
    vcenters = []
    for i in range(len(centers)):
        for j in range(len(centers[0])):
            vcenters.append(centers[i][j])
    datecenter = np.vstack((data, vcenters))
    datacenter = pca.fit_transform(datecenter)
    l = len(data)
    data = datacenter[:l]
    vcenters = datacenter[l:]
    ncenters = []
    for i in range(len(centers)):
        t = []
        for j in range(len(centers[0])):
            t.append(vcenters[i * len(centers[0]) + j])
        ncenters.append(t)

    # for i in ncenters:
    #     print(i)

    for j in range(len(labels)):
        for i in range(data.shape[0]):
            plt.scatter(data[i][0], data[i][1], color=colormap[int(labels[j][i])])

        center = ncenters[j]
        for i in range(len(center)):
            plt.scatter(center[i][0], center[i][1], color=colormap2[i], marker='^', s=120)
        filepath = path + "/" + name + "_" + str(j) + ".jpg"
        print("Saving:", filepath)
        plt.savefig(filepath, dpi=300)
        plt.clf()


def validition_visual(x, y, xlabel="", ylabel="", xtick=None, name="val"):
    # x: 超参量列表（用整形标识）
    # y: 超参测试结果的字典

    path = "../ValImage/"
    if not os.path.exists(path):
        os.makedirs(path)

    plt.figure(figsize=(16, 9))
    # 绘制散点
    for k in x:
        accuracies = y[k]
        plt.scatter([k] * len(accuracies), accuracies)

    # 绘制均值和方差
    val_mean = np.array([np.mean(v) for k, v in y.items()])
    val_std = np.array([np.std(v) for k, v in y.items()])

    print("Mean: ", val_mean)
    print("Std: ", val_std)

    plt.errorbar(x, val_mean, yerr=val_std)
    plt.title("Dataset: " + name)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    if xtick is not None:
        plt.xticks(x, xtick)
    filepath = path + name + ".jpg"
    plt.savefig(filepath, dpi=1200)
    print("Saving:", filepath)

def show_j(x, y_6, label_list, name="j"):
    """
    绘制 J 变化曲线
    """
    path = "../JImage/"
    if not os.path.exists(path):
        os.makedirs(path)
    _, ax = plt.subplots()
    for i in range(6):
        plt.plot(x, y_6[i], c=colormap[i], label=label_list[i])

    plt.title("J Curve of Dataset " + name)
    plt.xticks(x, x)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    filepath = path + name + ".jpg"
    plt.legend()
    plt.savefig(filepath, dpi=600)
    print("Saving:", filepath)

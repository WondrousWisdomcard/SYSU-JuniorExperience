import numpy as np
from matplotlib import pyplot as plt
import os

"""
* show_curve 迭代结果（例如损失函数、正确率）可视化，并将结果保存为PNG图片
* params:
    * train: [] 测试训练结果
    * test: [] 测试训练结果
    * xlabel: String X轴标签
    * ylabel: String Y轴标签
    * xtick: [] of String 超参列表的数值/方法
    * title: String 图片标题
    * path: String 保存的图片的文件夹路径
    * name: String 保存的图片的文件名
"""
def show_curve(train=None, test=None, xlabel="", ylabel="", xtick=None, title=None, path="./", name="curve"):

    if not os.path.exists(path):
        os.makedirs(path)
    plt.figure(figsize=(16, 9))

    l = []
    if train is not None:
        l = range(len(train))
        plt.plot(train, label=("train " + name))
    if test is not None:
        l = range(len(test))
        plt.plot(test, label=("test " + name))

    if title is not None:
        plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if xtick is not None:
        plt.xticks(l, xtick)
    filepath = path + name + ".jpg"
    plt.legend()
    plt.savefig(filepath, dpi=400)
    plt.show()
    print("Saving:", filepath)

"""
* show_curves 迭代结果（例如损失函数、正确率）可视化，并将结果保存为PNG图片
* params:
    * train: [] of [] 测试训练结果
    * test: [] of [] 测试训练结果
    * labels: [] 每条曲线的标签
    * xlabel: String X轴标签
    * ylabel: String Y轴标签
    * xtick: [] of String 超参列表的数值/方法
    * title: String 图片标题
    * path: String 保存的图片的文件夹路径
    * name: String 保存的图片的文件名
"""
def show_curves(train=None, test=None, labels=None, xlabel="", ylabel="", xtick=None, title=None, path="./", name="curve"):

    if not os.path.exists(path):
        os.makedirs(path)
    plt.figure(figsize=(16, 9))

    if train is not None:
        for t in range(len(train)):
            plt.plot(train[t], label=(labels[t] + " train"))
    if test is not None:
        for t in range(len(test)):
            plt.plot(test[t], label=(labels[t] +  " test"))

    if title is not None:
        plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if xtick is not None:
        plt.xticks(x, xtick)
    filepath = path + name + ".jpg"
    plt.legend()
    plt.savefig(filepath, dpi=400)
    plt.show()
    print("Saving:", filepath)

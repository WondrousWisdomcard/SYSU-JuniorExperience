import numpy as np
import pandas as pd


def normalization(data):
    """
    归一化：(data - min) / (max - min)
    Outputs:
    - data_norm: 归一化后的数据
    """
    data_max = np.max(data, axis=0)
    data_min = np.min(data, axis=0)
    data_norm = (data - data_min) / (data_max - data_min + 0.0001)
    return data_norm


def load_iris():
    """
    载入鸢尾数据，并对数据进行归一化和打散
    Outputs:
    - data: (N, D) numpy array 样本属性数据
    - label: (N,) numpy array 样本类别标签
    - feature_names: 样本属性名称
    - classes: list 样本类别名称
    """
    filepath = "../Datasets/Iris/iris.data"
    data = pd.read_csv(filepath,
                       sep=",",
                       header=None,
                       names=["A1", "A2", "A3", "A4", "L"])
    attributes = data.columns

    def class_to_int(type):
        if type == "Iris-setosa":
            return 0
        elif type == "Iris-versicolor":
            return 1
        elif type == "Iris-virginica":
            return 2
        else:
            return -1

    # 打乱数据
    data = data.sample(frac=1).reset_index(drop=True)
    data.loc[:, "L"] = data["L"].map(class_to_int)

    feature_names = attributes[:-1]
    label_names = attributes[-1]
    feature = data[feature_names]
    label = data[label_names]

    # 数据归一化
    feature = normalization(feature)

    classes = ["Iris Setosa", "Iris Versicolour", "Iris Virginica"]
    return np.array(feature), np.array(label), feature_names, classes


def load_wine():
    """
    载入葡萄酒数据，并对数据进行归一化和打散
    Outputs:
    - data: (N, D) numpy array 样本属性数据
    - label: (N,) numpy array 样本类别标签
    - feature_names: 样本属性名称
    - classes: list 样本类别名称
    """
    filepath = "../Datasets/Wine/wine.data"
    data = pd.read_csv(filepath,
                       sep=",",
                       header=None,
                       names=["L", "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10", "A11", "A12", "A13"])
    attributes = data.columns

    # 打乱数据
    data = data.sample(frac=1).reset_index(drop=True)

    feature_names = attributes[1:]
    label_names = attributes[0]
    feature = data[feature_names]
    label = data[label_names]

    # 数据归一化
    feature = normalization(feature)

    classes = [1, 2, 3]
    return np.array(feature), np.array(label), feature_names, classes


def load_seed():
    """
    载入种子数据，并对数据进行归一化和打散
    Outputs:
    - data: (N, D) numpy array 样本属性数据
    - label: (N,) numpy array 样本类别标签
    - feature_names: 样本属性名称
    - classes: list 样本类别名称
    """
    filepath = "../Datasets/Seed/seeds_dataset.txt"
    data = pd.read_csv(filepath,
                       sep=",",
                       header=None,
                       names=["A1", "A2", "A3", "A4", "A5", "A6", "A7", "L"])
    attributes = data.columns

    # 打乱数据
    data = data.sample(frac=1).reset_index(drop=True)

    feature_names = attributes[:-1]
    label_names = attributes[-1]
    feature = data[feature_names]
    label = data[label_names]

    # 数据归一化
    feature = normalization(feature)

    classes = [1, 2, 3]
    return np.array(feature), np.array(label), feature_names, classes


def load_glass():
    """
    载入草数据，并对数据进行归一化和打散
    Outputs:
    - data: (N, D) numpy array 样本属性数据
    - label: (N,) numpy array 样本类别标签
    - feature_names: 样本属性名称
    - classes: list 样本类别名称
    """
    filepath = "../Datasets/Glass/glass.data"
    data = pd.read_csv(filepath,
                       sep=",",
                       header=None,
                       names=["Id", "RI", "Na", "Mg", "Al", "Si", "K", "Ca", "Ba", "Fe", "L"])
    attributes = data.columns

    # 打乱数据
    data = data.sample(frac=1).reset_index(drop=True)

    feature_names = attributes[1:-1]
    label_names = attributes[-1]
    feature = data[feature_names]
    label = data[label_names]

    # 数据归一化
    feature = normalization(feature)

    classes = [1, 2, 3, 4, 5, 6, 7]
    return np.array(feature), np.array(label), feature_names, classes


def load_drybean():
    """
    载入干豆数据，并对数据进行归一化和打散
    Outputs:
    - data: (N, D) numpy array 样本属性数据
    - label: (N,) numpy array 样本类别标签
    - feature_names: 样本属性名称
    - classes: list 样本类别名称
    """
    filepath = "../Datasets/DryBean/Dry_Bean_Dataset.csv"
    data = pd.read_csv(filepath)
    attributes = data.columns

    def drybean_to_int(type):
        if type == "SEKER":
            return 0
        elif type == "BARBUNYA":
            return 1
        elif type == "BOMBAY":
            return 2
        elif type == "CALI":
            return 3
        elif type == "DERMASON":
            return 4
        elif type == "HOROZ":
            return 5
        elif type == "SIRA":
            return 6
        else:
            return -1

    # 打乱数据
    data = data.sample(frac=1).reset_index(drop=True)

    data.loc[:, "Class"] = data["Class"].map(drybean_to_int)

    feature_names = attributes[:-1]
    label_names = attributes[-1]
    feature = data[feature_names]
    label = data[label_names]

    # 数据归一化
    feature = normalization(feature)

    classes = ["SEKER", "BARBUNYA", "BOMBAY", "CALI", "DERMOSAN", "HOROZ", "SIRA"]
    return np.array(feature), np.array(label), feature_names, classes


def load_parkinsons():
    """
    载入帕金森数据，并对数据进行归一化和打散
    Outputs:
    - data: (N, D) numpy array 样本属性数据
    - label: (N,) numpy array 样本类别标签
    - feature_names: 样本属性名称
    - classes: list 样本类别名称
    """
    filepath = "../Datasets/Parkinsons/parkinsons.data"
    data = pd.read_csv(filepath,
                       sep=",")
    attributes = data.columns

    # 打乱数据
    data = data.sample(frac=1).reset_index(drop=True)

    feature_names = attributes[1:].drop("status")
    label_names = "status"
    feature = data[feature_names]
    label = data[label_names]

    # 数据归一化
    feature = normalization(feature)

    classes = [0, 1]
    return np.array(feature), np.array(label), feature_names, classes


def load_ionosphere():
    """
    载入电离层数据，并对数据进行归一化和打散
    Outputs:
    - data: (N, D) numpy array 样本属性数据
    - label: (N,) numpy array 样本类别标签
    - feature_names: 样本属性名称
    - classes: list 样本类别名称
    """

    name = []
    for i in range(1, 35):
        name.append("A" + str(i))
    name.append("L")
    filepath = "../Datasets/Ionosphere/ionosphere.data"
    data = pd.read_csv(filepath,
                       sep=",",
                       header=None,
                       names=name)
    attributes = data.columns

    def class_to_int(type):
        if type == "b":
            return 0
        elif type == "g":
            return 1
        else:
            return -1

    # 打乱数据
    data = data.sample(frac=1).reset_index(drop=True)
    data.loc[:, "L"] = data["L"].map(class_to_int)

    feature_names = attributes[:-1]
    label_names = attributes[-1]
    feature = data[feature_names]
    label = data[label_names]

    # 数据归一化
    feature = normalization(feature)

    classes = ["b", "g"]
    return np.array(feature), np.array(label), feature_names, classes


def load_letter():
    """
    载入字符数据，并对数据进行归一化和打散
    Outputs:
    - data: (N, D) numpy array 样本属性数据
    - label: (N,) numpy array 样本类别标签
    - feature_names: 样本属性名称
    - classes: list 样本类别名称
    """

    name = []
    name.append("L")
    for i in range(1, 17):
        name.append("A" + str(i))

    filepath = "../Datasets/Letter/letter-recognition.data"
    data = pd.read_csv(filepath,
                       sep=",",
                       header=None,
                       names=name)
    attributes = data.columns

    def letter_to_int(letter):
        charr = ["A","B","C","D","E","F","G","H","I",
                 "J","K","L","M","N","O","P","Q","R",
                 "S","T","U","V","W","X","Y","Z"]
        intt = range(26)
        for i in range(len(charr)):
            if letter == charr[i]:
                return intt[i]
        return -1

    # 打乱数据
    data = data.sample(frac=1).reset_index(drop=True)

    data.loc[:, "L"] = data["L"].map(letter_to_int)

    feature_names = attributes[1:]
    label_names = attributes[0]
    feature = data[feature_names]
    label = data[label_names]

    # 数据归一化
    feature = normalization(feature)

    classes = ["A","B","C","D","E","F","G","H","I",
               "J","K","L","M","N","O","P","Q","R",
               "S","T","U","V","W","X","Y","Z"]
    return np.array(feature), np.array(label), feature_names, classes
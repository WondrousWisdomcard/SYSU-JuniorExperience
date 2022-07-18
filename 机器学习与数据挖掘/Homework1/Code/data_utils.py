import pandas as pd
import numpy as np
import os


def load_red_wine_quality():
    """
    载入红葡萄酒数据
    Outputs:
    - data: (N, D) numpy array 样本属性数据
    - label: (N,) numpy array 样本类别标签
    - feature_names: 样本属性名称
    - classes: list 样本类别名称
    """
    filepath = "../Datasets/WineQuality/winequality-red.csv"
    return load_wine_quality(filepath)


def load_white_wine_quality():
    """
    载入白葡萄酒数据
    Outputs:
    - data: (N, D) numpy array 样本属性数据
    - label: (N,) numpy array 样本类别标签
    - feature_names: 样本属性名称
    - classes: list 样本类别名称
    """
    filepath = "../Datasets/WineQuality/winequality-white.csv"
    return load_wine_quality(filepath)


def load_wine_quality(filepath):
    """
    载入葡萄酒数据，并对数据进行归一化和打散
    Input:
    - filepath: string 数据文件路径
    Outputs:
    - data: (N, D) numpy array 样本属性数据
    - label: (N,) numpy array 样本类别标签
    - feature_names: 样本属性名称
    - classes: list 样本类别名称
    """
    data = pd.read_csv(filepath, sep=";")
    attributes = data.columns

    # 打乱数据
    data = data.sample(frac=1).reset_index(drop=True)

    feature_names = attributes[:-1]
    label_names = attributes[-1]
    feature = data[feature_names]
    label = data[label_names]

    # 数据归一化
    feature_max = np.max(feature, axis=0)
    feature_min = np.min(feature, axis=0)
    feature = (feature - feature_min) / (feature_max - feature_min)

    classes = range(10)
    return np.array(feature), np.array(label), feature_names, classes


def load_obesity():
    """
    载入肥胖症数据，并对数据进行归一化和打散
    Input:
    - filepath: string 数据文件路径
    Outputs:
    - data: (N, D) numpy array 样本属性数据
    - label: (N,) numpy array 样本类别标签
    - feature_names: 样本属性名称
    - classes: list 样本类别名称
    """
    filepath = "../Datasets/Obesity/ObesityDataSet_raw_and_data_sinthetic.csv"
    data = pd.read_csv(filepath)
    attributes = data.columns

    def gender_to_int(gender):
        if gender == "Female":
            return 1
        else:
            return 0

    def bool_to_int(boool):
        if boool == "yes":
            return 1
        else:
            return 0

    def state_to_int(state):
        if state == "no":
            return 0
        elif state == "Sometimes":
            return 1
        elif state == "Frequently":
            return 2
        elif state == "Always":
            return 3
        else:
            return -1

    def trans_to_int(trans):
        if trans == "Automobile":
            return 0
        elif trans == "Motorbike":
            return 1
        elif trans == "Bike":
            return 3
        elif trans == "Public_Transportation":
            return 2
        else:  # Walking
            return 4

    def obes_to_int(obes):
        if obes == "Insufficient_Weight":
            return 0
        elif obes == "Normal_Weight":
            return 1
        elif obes == "Overweight_Level_I":
            return 2
        elif obes == "Overweight_Level_II":
            return 3
        elif obes == "Obesity_Type_I":
            return 4
        elif obes == "Obesity_Type_II":
            return 5
        elif obes == "Obesity_Type_III":
            return 6
        else:
            return -1

    # 将非数字类型变量数字化
    data.loc[:, "Gender"] = data["Gender"].map(gender_to_int)
    data.loc[:, "family_history_with_overweight"] = data["family_history_with_overweight"].map(bool_to_int)
    data.loc[:, "FAVC"] = data["FAVC"].map(bool_to_int)
    data.loc[:, "SMOKE"] = data["SMOKE"].map(bool_to_int)
    data.loc[:, "SCC"] = data["SCC"].map(bool_to_int)
    data.loc[:, "CAEC"] = data["CAEC"].map(state_to_int)
    data.loc[:, "CALC"] = data["CALC"].map(state_to_int)
    data.loc[:, "MTRANS"] = data["MTRANS"].map(trans_to_int)
    data.loc[:, "NObeyesdad"] = data["NObeyesdad"].map(obes_to_int)

    # 打乱数据
    data = data.sample(frac=1).reset_index(drop=True)

    feature_names = attributes[:-1]
    label_names = attributes[-1]
    feature = data[feature_names]
    label = data[label_names]

    # 数据归一化
    feature_max = np.max(feature, axis=0)
    feature_min = np.min(feature, axis=0)
    feature = (feature - feature_min) / (feature_max - feature_min)


    classes = ["Insufficient_Weight", "Normal_Weight", "Overweight_Level_I",
               "Overweight_Level_II", "Obesity_Type_I", "Obesity_Type_II", "Obesity_Type_III"]
    return np.array(feature), np.array(label), feature_names, classes


def load_drybean():
    """
    载入干豆数据，并对数据进行归一化和打散
    Input:
    - filepath: string 数据文件路径
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
    feature_max = np.max(feature, axis=0)
    feature_min = np.min(feature, axis=0)
    feature = (feature - feature_min) / (feature_max - feature_min)

    classes = ["SEKER", "BARBUNYA", "BOMBAY", "CALI", "DERMOSAN", "HOROZ", "SIRA"]
    return np.array(feature), np.array(label), feature_names, classes

import numpy as np


def x_3_kernel(X):
    """
    三阶非线性基函数：[x] -> [x, x^2, x^3]
    """
    return np.hstack((X, X ** 2, X ** 3))


def x_5_kernel(X):
    """
    五阶非线性基函数：[x] -> [x, x^2, x^3, x^4, x^5]
    """
    return np.hstack((X, X ** 2, X ** 3, X ** 4, X ** 5))

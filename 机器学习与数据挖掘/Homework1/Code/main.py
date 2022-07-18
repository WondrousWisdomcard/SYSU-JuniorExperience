from test_utils import *
from Classifiers.softmax_classifier import SoftmaxLinearClassifier
from Classifiers.softmax_classifier import SoftmaxNonlinearClassifier
from Classifiers.kernel import *


if __name__ == "__main__":

    # 载入数据集
    # X, y, attrs, classes = load_red_wine_quality()
    # X, y, attrs, classes = load_white_wine_quality()
    # X, y, attrs, classes = load_obesity()
    X, y, attrs, classes = load_drybean()

    # 数据降维可视化
    # t_sne(X, y, classes)

    # 交叉验证
    # learning_rate_cross_validition(X, y, ite_num=2000, batch_size=500)
    # normalization_cross_validition(X, y, ite_num=2000, batch_size=500)
    # learning_rate_cross_validition(X, y, ite_num=2000, batch_size=500, nonlinear_kernel=x_3_kernel)
    # normalization_cross_validition(X, y, ite_num=2000, batch_size=500, nonlinear_kernel=x_3_kernel)
    # learning_rate_cross_validition(X, y, ite_num=2000, batch_size=500, nonlinear_kernel=x_5_kernel)
    # normalization_cross_validition(X, y, ite_num=2000, batch_size=500, nonlinear_kernel=x_5_kernel)

    softmax_validition(X, y, ite_num=2000, batch_size=500, reg_style="L0")
    softmax_validition(X, y, ite_num=2000, batch_size=500, reg_style="L1")
    softmax_validition(X, y, ite_num=2000, batch_size=500, reg_style="L2")

    # 计算生成权重矩阵
    # softmax = SoftmaxNonlinearClassifier(x_5_kernel)
    # gen_w_loss(X, y, attrs, classes, softmax)

    kernel = [None, x_3_kernel, x_5_kernel]
    reg_style = ["L0", "L1", "L2"]

    # 测试准确率
    # for k in kernel:
    #     for r in reg_style:
    #         softmax = SoftmaxNonlinearClassifier(kernel_function=k)
    #         test_acc(X, y, softmax,ite_num=500, reg_style=r, reg_strength=1e-4)

    # 测试 Precision、Recall
    # for k in kernel:
    #     softmax = SoftmaxNonlinearClassifier(kernel_function=k)
    #     test_pre_rec(X, y, attrs, classes, softmax)
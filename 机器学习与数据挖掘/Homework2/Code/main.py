from visual_utils import *
from data_utils import *
from kmeans import *
from sklearn.metrics.cluster import normalized_mutual_info_score
from sklearn.cluster import KMeans


if __name__ == "__main__":
    # 载入数据集
    data, label, col_name, classes = load_iris()
    name = "iris"

    # 对于样本太多的数据集，取一部分样本进行测试
    # data = data[:5000]
    # label = label[:5000]

    # 真实分类的数据降维可视化
    # show_t_sne(data, label, classes, name)
    # show_pca(data, label, classes, name)

    # 生成Kmean聚类过程中聚类的变化图，结果保存在 AnimImage 文件夹
    # 运行可能需要较长时间

    # 随机初始化
    # name1 = name
    # c, y, more = kmeans(data, len(classes), ite_max=50, centers_init=get_random_centers)
    # s = normalized_mutual_info_score(y, label)
    # print(name1, "NMI: ", s)
    # show_anim(data, more["labels"], more["centers"], name=name1)

    # 距离初始化
    # name2 = name + "_dis"
    # c, y, more = kmeans(data, len(classes), ite_max=50, centers_init=get_distance_based_centers)
    # s = normalized_mutual_info_score(y, label)
    # print(name2, "NMI: ", s)
    # show_anim(data, more["labels"], more["centers"], name=name2)

    # 随机距离初始化
    # name3 = name  + "_randis"
    # c, y, more = kmeans(data, len(classes), ite_max=50, centers_init=get_randis_centers)
    # s = normalized_mutual_info_score(y, label)
    # print(name3, "NMI: ", s)
    # show_anim(data, more["labels"], more["centers"], name=name3)


    # 【可选】：对数据先进行 PCA 降维
    # dim = 8
    # pca = PCA(n_components=dim)
    # data = pca.fit_transform(data)


    # 比较不同初始化方法和距离选择的效果
    # t = 20
    # k = {}
    # cen = [get_random_centers, get_distance_based_centers, get_randis_centers]
    # dis = [d_eculidean, d_manhattan]
    # idx = range(len(cen) * len(dis))
    # xtick = ["eculidean\nrandom_centers", "eculidean\ndistance_based_centers", "eculidean\nrandis_centers",
    #          "manhattan\nrandom_centers", "manhattan\ndistance_based_centers", "manhattan\nrandis_centers"]
    # err_limit = 0.0
    # for i in idx:
    #     k[i] = []
    #
    # for i in idx:
    #     for j in range(t):
    #         centers, y_kmeans, _ = kmeans(data, len(classes), ite_max=100, centers_init=cen[i % len(cen)] , distance=dis[i // len(cen)])
    #         res = normalized_mutual_info_score(y_kmeans, label)
    #         print(xtick[i], res)
    #         if res > err_limit:
    #             k[i].append(res)
    #
    # validition_visual(idx, k, ylabel="NMI", xtick=xtick, name=name)


    # sklearn kmean模型聚类，与我们的实现结果进行比较
    # kmean = KMeans(n_clusters=len(classes))
    # kmean.fit(data)
    # y_kmeans = kmean.predict(data)
    # s = normalized_mutual_info_score(y_kmeans, label)
    # print("SkLearn kmeans: ", s)

    # 对分类结果进行降维（t-sne 或 pca）可视化
    # show_t_sne(data, y_kmeans, classes)
    # show_pca(data, y_kmeans, classes)

    # 计算样本与聚类中心的距离和
    # x = range(1, 20)
    # y = []
    # l = 5
    # for k in x:
    #     j = 0
    #     for i in range(l):
    #         centers, data_class, _ = kmeans(data, k, ite_max=100, centers_init=get_distance_based_centers)
    #         j += get_total_distance(data, centers, data_class)
    #     y.append(j / l)
    # show_j(x, y, name=name)

    # 比较不同初始化方法和距离选择的 J 效果
    # t = 20
    # k = {}
    # cen = [get_random_centers, get_distance_based_centers, get_randis_centers]
    # dis = [d_eculidean, d_manhattan]
    # idx = range(len(cen) * len(dis))
    # label_list = ["eculidean + random", "eculidean + distance", "eculidean + randis",
    #          "manhattan + random", "manhattan + distance", "manhattan + randis"]
    #
    # y_6 = []
    # # x = range(1, 20)
    # x = range(1, 50, 4) # for Letter dataset
    # for i in idx:
    #     y = []
    #     # l = 5
    #     l = 3 # for Letter Dataset
    #     for k in x:
    #         j = 0
    #         for i in range(l):
    #             centers, y_kmeans, _ = kmeans(data, k, ite_max=100000, centers_init=cen[i % len(cen)] , distance=dis[i // len(cen)])
    #             j += get_total_distance(data, centers, y_kmeans)
    #         y.append(j / l)
    #     y_6.append(y)
    # show_j(x, y_6, label_list, name=name)


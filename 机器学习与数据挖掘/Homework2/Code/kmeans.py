import numpy as np

# Distance Evalutation
# 1. Euclidean
def d_eculidean(a1, a2):
    a = a1 - a2
    d = np.matmul(a, a.T)
    return np.sqrt(d)


# 2. Manhattan
def d_manhattan(a1, a2):
    a = np.abs(a1 - a2)
    d = np.sum(a)
    return d


# Initialization Methods
# 1. Random Method
def get_random_centers(data, k):
    mask = np.random.choice(data.shape[0], k, replace=False)
    return data[mask]


# 2. Distance-based Method
def get_distance_based_centers(data, k, distance=d_eculidean):
    centers = []

    center = data[np.random.choice(data.shape[0])]
    centers.append(center)

    n, dim = data.shape
    for i in range(k - 1):
        farest = center
        farest_distance = 0
        for j in range(n):
            temp_distance = distance(center, data[j])
            if farest_distance < temp_distance:
                farest = data[j]
                farest_distance = temp_distance

        centers.append(farest)
        center = np.mean(centers, axis=0)

    return np.array(centers)


# 3. Random + Distance Method
def get_randis_centers(data, k, rate=0.5, distance=d_eculidean):
    ran_num = int(rate * data.shape[0])
    data_ran = get_random_centers(data, ran_num)
    return get_distance_based_centers(data_ran, k, distance=distance)

# Normalized Mutual Information
# We use "normalized_mutual_info_score(a, b)" from sklearn


# K-means
def kmeans(data, k, ite_max=100, distance=d_eculidean, centers_init=get_random_centers):
    '''
    Input:
    - data: 样本数据
    - k: 簇的数目
    - ite_max: 最大迭代次数
    - distance: 选择计算距离的函数，默认欧几里得距离
    - center_init: 选择中心初始化函数，默认随机选择
    Output:
    - centers: K个样本中心
    - data_class: 样本聚类结果
    - more: 每次迭代的簇中心和聚类结果
    '''

    n, dim = data.shape
    data_class = np.zeros(n)

    more = {}
    more["centers"] = []
    more["labels"] = []

    ite = 0
    change = True

    centers = centers_init(data, k)

    centerlist = []
    for i in centers:
        centerlist.append(list(i))
    more["centers"].append(centerlist)
    more["labels"].append(list(data_class))

    while ite < ite_max and change:
        ite += 1
        change = False
        data_num = np.zeros(k)
        data_sum = np.zeros((k, dim))

        for i in range(n):
            i_class = -1
            i_dist = np.inf

            for j in range(k):
                dist = distance(data[i], centers[j])
                if dist < i_dist:
                    i_class = j
                    i_dist = dist

            if data_class[i] != i_class:
                change = True
            data_class[i] = i_class
            data_num[i_class] += 1
            data_sum[i_class] += data[i]

        for i in range(k):
            if data_num[i] != 0:
                centers[i] = data_sum[i] / data_num[i]

        centerlist = []
        for i in centers:
            centerlist.append(list(i))
        more["centers"].append(centerlist)
        more["labels"].append(list(data_class))

    print("Finish! Ite: ", ite)

    return centers, data_class, more

# Get Total Distance J
def get_total_distance(data, centers, data_class, distance=d_eculidean):
    n, dim = data.shape
    j = 0

    for i in range(n):
        c = int(data_class[i])
        j += distance(data[i], centers[c])

    return j / n

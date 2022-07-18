import pandas as pd
import os
import numpy as np
import time
from matplotlib import pyplot as plt


"""
* SAVE_MATRIX_TO_PICKLE 将 DataFrame 压缩保存至压缩文件中
* input:
    * matrix: DataFrame 待保存的矩阵数据
    * dir_path: String 文件夹路径
    * file_name: String 文件名，不含后缀
"""
def save_matrix_to_pickle(matrix, dir_path, file_name):
    if os.path.exists(dir_path) is False:
        os.mkdir(dir_path)
    file_path = os.path.join(dir_path, file_name + ".pkl")
    print("Save Matrix to", file_path)
    matrix.to_pickle(file_path)


"""
* LOAD_MATRIX_FROM_PICKLE 读取 pkl 压缩文件中的 DataFrame 并返回
* input:    
    * file_path: String 文件路径
* return:
    * matrix: DataFrame 矩阵数据
"""
def load_matrix_from_pickle(file_path):
    print("Load Matrix from", file_path)
    matrix = pd.read_pickle(file_path)
    return matrix


"""
* LOAD_DATA_TO_MATRIX 读入载入用户-项评分表文件，转化为 DataFrame 输出
* input:
    * file_path: String 数据文件路径
    * step: String 文件分隔符，默认","
* output: 
    * rating_matrix: DataFrame 评分矩阵
"""
def load_data_to_matrix(file_path, step=","):
    print(f"Load Data From {file_path} to matrix")
    data = pd.read_csv(file_path, dtype={"userId": np.int32, "movieId": np.int32, "rating": np.float32},
                       usecols=range(3), sep=step)
    rating_matrix = data.pivot_table(index=["userId"], columns="movieId", values="rating")
    print(f"Shape of Rating Matrix (Users, Movies): {rating_matrix.shape}")
    return rating_matrix


"""
* COMPUTE_SIMILARITY 计算用户/项的相似度矩阵
* input:
    * rating_matrix: DataFrame 评分矩阵
    * based_type: "user" or "item" 分别表示计算用户相似度矩阵和项的相似度矩阵
* return:
    * similarity_matrix: DataFrame 相似度矩阵
"""
def compute_similarity(rating_matrix, based_type="user"):
    if based_type == "user":
        similarity_matrix = rating_matrix.T.corr(method="pearson")
    elif based_type == "item":
        similarity_matrix = rating_matrix.corr(method="pearson")
    else:
        print("Unknown Based-type, Support 'user' and 'item' only.")
        similarity_matrix = None
    return similarity_matrix


"""
* PREDICT_ITEM_SCORE_FOR_USER 预测用户 i 对电影 j 的评分
* input:
    * user_id: Integer 用户 ID
    * item_id: Integer 电影 ID
    * rating_movie: DataFrame 评分矩阵
    * similarity_matrix: DataFrame 相似性矩阵
    * based_type: "user" or "item" 相似性矩阵的类型（用户/项）
    * k: Integer 计算预测分数的近邻个数，默认-1，表示计算所有相似度大于0的相似项
* return:
    * r: Integer 用户对该电影评分的预测值
"""
def predict_item_score_for_user(user_id, item_id, rating_matrix, similarity_matrix, based_type="user", k=-1):
    if based_type == "user":
        similar_users = similarity_matrix[user_id].drop(user_id).dropna()
        similar_users = similar_users.where(similar_users > 0).dropna()
        if similar_users.empty:
            # print(f"User {user_id} don't have similar users.")
            return None

        have_item_users = rating_matrix[item_id].dropna()
        have_item_similar_users = similar_users.loc[list(set(similar_users.index) & set(have_item_users.index))]
        have_item_similar_users.sort_values(ascending=False, inplace=True)
        # print("Similar users that have rated item:", have_item_similar_users.shape)

        a = 0
        b = 0
        c = 0
        for similar_user, similarity in have_item_similar_users.iteritems():
            a += similarity * rating_matrix.loc[similar_user, item_id]
            b += similarity
            c += 1
            if c == k:
                break
        if b == 0:
            # print(f"User {user_id} don't have any similar users that have score item {item_id}")
            return None

    elif based_type == "item":
        similar_items = similarity_matrix[item_id].drop(item_id).dropna()
        similar_items = similar_items.where(similar_items > 0).dropna()
        if similar_items.empty:
            # print(f"Item {item_id} don't have similar items.")
            return None

        user_rated_items = rating_matrix.loc[user_id].dropna()
        user_rated_similar_items = similar_items.loc[list(set(similar_items.index) & set(user_rated_items.index))]
        user_rated_similar_items.sort_values(ascending=False, inplace=True)
        # print("Similar items that had rated by user:", user_rated_similar_items.shape)

        a = 0
        b = 0
        c = 0
        for similar_item, similarity in user_rated_similar_items.iteritems():
            a += similarity * rating_matrix.loc[user_id, similar_item]
            b += similarity
            c += 1
            if c == k:
                break
        if b == 0:
            # print(f"User {user_id} don't have any rated item that similar to item {item_id}")
            return None
    else:
        print("Unknown Based-type, Support 'user' and 'item' only.")
        return None

    r = a / b
    # 避免浮点数处理出现 5.000000000000001 的情况
    if r > 5.0:
        r = 5.0
    return r


"""
* PREDICT_ALL_ITEMS_SCORE_FOR_USER 跟据用户相似性矩阵预测用户 i 对非冷门未评分的项的评分
* input:
    * user_id: Integer 用户 ID
    * item_id: Integer 电影 ID
    * rating_movie: DataFrame 评分矩阵
    * similarity_matrix: DataFrame 相似性矩阵
    * cold: Integer 非冷门项要求必须存在大于等于 cold 个用户对其评分，否则为冷门项，因评分数据少不值得考虑
    * based_type: "user" or "item" 相似性矩阵的类型（用户/项）
    * k: Integer 计算预测分数的近邻个数，默认-1，表示计算所有相似度大于0的相似项
* return:
    * predict_rating: {} Key: 项的ID, Value: 预测分数
"""
def predict_all_items_score_for_user(user_id, rating_matrix, similarity_matrix, cold=10, based_type="user", k=-1):
    # 过滤冷门电影
    score_count = rating_matrix.count()
    hot_items = score_count.where(score_count > cold).dropna()

    # 过滤已经评分的电影
    items = rating_matrix.loc[user_id]
    unrated_items = items[items.isnull()]

    predict_items = set(hot_items.index) & set(unrated_items.index)

    predict_rating = {}
    for item_id in predict_items:
        pr = predict_item_score_for_user(user_id, item_id, rating_matrix, similarity_matrix, based_type=based_type, k=k)
        if pr is not None:
            predict_rating[item_id] = pr

    return predict_rating


"""
* CF 类: 
* attributes:
    * _based_type: "user" or "item" 协同滤波算法的类型
    * _matrix_path: String 储存各类临时文件的文件夹路径
    * _val: Boolean 是否为验证模式，验证模式下空出一块预取的评分来进行验证测试
    * _rating_matrix: DataFrame 评分矩阵
    * _similarity_matrix: DataFrame 相似度矩阵
    * _mask_ground_truth: (val mode only) [] 储存空出一块用于预取评分的真实值
* methods:
    * __INIT__: 初始化评分矩阵和相似度矩阵
    * TOP_N_RECOMMEND: 为一个用户推荐 N 个项
    * SCORE_PREDICT_VAL: (val mode only) 验证测试，返回结果四元组和 RMSE
"""
class CF:

    """
    * __INIT__ 初始化评分矩阵和相似度矩阵
    * input:
        * based_type: "user" or "item" 协同滤波算法的类型
        * data_name: String 数据集名称标识
        * data_file_path: String 评分数据文件路径
        * step: String 评分数据文件的分隔符
        * val: Boolean 是否为验证模式，验证模式下空出一块预取的评分来进行验证测试
        * val_mask: ((a, b), (c, d)) 验证模式下评分矩阵空出一块的范围：a:b行，c:d列
    """
    def __init__(self, based_type, data_name, data_file_path, step=",", val=True, val_mask=((0, 100), (0, 200))):
        self._based_type = based_type
        self._matrix_path = "./Matrix/"
        self._val = val

        # 载入/计算评分矩阵
        file_name = data_name + "-rating"
        save_file_path = self._matrix_path + file_name + ".pkl"
        start = time.time()
        if os.path.exists(save_file_path):
            self._rating_matrix = load_matrix_from_pickle(save_file_path)
        else:
            self._rating_matrix = load_data_to_matrix(file_path=data_file_path, step=step)
            save_matrix_to_pickle(self._rating_matrix, self._matrix_path, file_name)
        end = time.time()
        # print("Rating Matrix:")
        # print(self._rating_matrix, "\n")
        print("Time Cost of Loading Rating Matrix: %.2f s" % (end - start))

        # Mask
        if val:
            (u_l, u_r), (i_l, i_r) = val_mask
            self._mask_ground_truth = self._rating_matrix.iloc[u_l:u_r, i_l:i_r].copy()
            self._rating_matrix.iloc[u_l:u_r, i_l:i_r] = np.nan
            # print("Mask Ground Truth Matrix:")
            # print(self._mask_ground_truth, "\n")
            # print("Mask Rating Matrix:")
            # print(self._rating_matrix, "\n")

        # 载入/计算相似矩阵
        file_name = data_name + f"-{self._based_type}-similarity"
        if val:
            file_name += "-val"
        save_file_path = self._matrix_path + file_name + ".pkl"
        start = time.time()
        if os.path.exists(save_file_path):
            self._similarity_matrix = load_matrix_from_pickle(save_file_path)
        else:
            self._similarity_matrix = compute_similarity(self._rating_matrix, based_type=self._based_type)
            save_matrix_to_pickle(self._similarity_matrix, self._matrix_path, file_name)
        end = time.time()
        # print(f"Similarity Matrix ({self._based_type}):")
        # print(self._similarity_matrix, "\n")
        print("Time Cost of Loading Similarity Matrix: %.2f s" % (end - start))

    """
    * TOP_N_RECOMMEND 为一个用户推荐 N 个预测评分最高的项
    * input:
        * user_id: Integer 用户 ID
        * n: Integer 返回的推荐项的个数
        * k: Integer 预测分数时考虑的相似用户个数
    * return:
        * predict_result: [] 每一个元素是由 Item ID 和 预测评分组成的元组
    """
    def top_n_recommend(self, user_id, n, k=-1):
        start = time.time()
        pr = predict_all_items_score_for_user(user_id, self._rating_matrix, self._similarity_matrix,
                                              cold=10, based_type=self._based_type, k=k)
        predict_result = sorted(pr.items(), key=lambda x: -x[1])
        end = time.time()
        # print(f"Predict Score: ({len(pr.keys())} Items)")
        # print(pr, "\n")
        print("Time Cost of Top N Recommend: %.2f s" % (end - start))
        return predict_result[:n]

    """
    * SCORE_PREDICT_VAL 验证测试
    * input:
        * k: Integer 预测分数时考虑的相似用户个数
    * return:
        * res: [] of (User ID, Item ID, Truth Score, Predict Score)
        * rmse: Float 度量结果
    """
    def score_predict_val(self, k):
        if not self._val:
            raise Exception("Only 'val' mode can call this method.")

        res = []
        rmse = 0
        count = 0
        start = time.time()
        for i in self._mask_ground_truth.index:
            for j in self._mask_ground_truth.columns:
                if self._mask_ground_truth.loc[i, j] > 0:
                    truth_score = self._mask_ground_truth.loc[i, j]
                    predict_score = predict_item_score_for_user(i, j, self._rating_matrix, self._similarity_matrix,
                                                                based_type=self._based_type, k=k)
                    if predict_score is not None:
                        rmse += (truth_score - predict_score) ** 2
                        count += 1
                        res.append((i, j, truth_score, predict_score))
                        # print(f"[User {i}, Item {j}] TruthScore: {truth_score} PredictScore: {predict_score}")

        rmse = (rmse / count) ** 0.5
        end = time.time()
        print("Time Cost of Score Predict Val: %.2f s " % (end - start))
        return res, rmse


if __name__ == "__main__":

    data_name = "ml-latest-small"
    # data_name = "ml-1m"

    if data_name == "ml-latest-small":
        cf_u = CF("user", data_name, "./Datasets/ml-latest-small/ratings.csv", )
        cf_i = CF("item", data_name, "./Datasets/ml-latest-small/ratings.csv")
    else:
        cf_u = CF("user", data_name, "./Datasets/ml-1m/ratings.dat", step="::")
        cf_i = CF("item", data_name, "./Datasets/ml-1m/ratings.dat", step="::")

    # 推荐测试
    print("5 User-based Recommend Moveis for User 3:", cf_u.top_n_recommend(3, n=5, k=10))
    print("5 Item-based Recommend Moveis for User 3:", cf_i.top_n_recommend(3, n=5, k=10))

    # 验证测试可视化
    k_l_u = []
    k_l_i = []
    r = range(1, 100, 1)
    for k in r:
        print(f"Ite: {k}")
        _, rmse_u = cf_u.score_predict_val(k)
        k_l_u.append(rmse_u)
        _, rmse_i = cf_i.score_predict_val(k)
        k_l_i.append(rmse_i)

    min_u = np.argmin(k_l_u)
    min_i = np.argmin(k_l_i)
    u, uu = min_u + 1, k_l_u[min_u]
    i, ii = min_i + 1, k_l_i[min_i]

    plt.title("Dataset: " + data_name)
    plt.plot(r, k_l_u, label="User CF")
    plt.plot(r, k_l_i, label="Item CF")
    plt.scatter(u, uu)
    plt.scatter(i, ii)
    plt.annotate("(%d, %.2f)" % (u, uu), xy=(u, uu), xytext=(-20, 10), textcoords='offset points')
    plt.annotate("(%d, %.2f)" % (i, ii), xy=(i, ii), xytext=(-20, 10), textcoords='offset points')
    plt.legend()
    plt.savefig("./Image/" + data_name + ".png")
    plt.show()
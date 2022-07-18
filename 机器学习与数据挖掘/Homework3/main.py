import random
import time
import community as community_louvain
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from sklearn.metrics import normalized_mutual_info_score
from Homework3.data_utils import *


def compute_modularity(communities, graph):
    m = len(graph.edges(None, False))
    q = 0.0
    for community in communities:
        e = 0.0
        for vid_i in community:
            for vid_j in community:
                if graph.has_edge(vid_i, vid_j):
                    e += 1.0
        q += e / (2 * m)
        a = 0.0
        for vid in community:
            a += len([x for x in graph.neighbors(vid)])
        q -= (a / (2 * m)) ** 2
    return q


class Vertex:
    def __init__(self, vid, cid, nodes, k_in=0):
        self._vid = vid  # 节点编号
        self._cid = cid  # 社区编号
        self._nodes = nodes  # 保存节点对应的原先网络社区内的节点
        self._k_in = k_in  # 节点内部的边权重


class GenLouvain:

    def __init__(self, graph):
        self._graph = graph     # 图： Key: vid, Value: vid of neighbor
        self._m = 0             # 边数
        self._vertices = {}     # 节点： Key: vid, Value: Vertex of vid
        self._community = {}    # 社区： Key: cid, Value: {} of vid

        for vid in self._graph.keys():
            self._community[vid] = {vid}  # 为每一个节点创建一个社区
            self._vertices[vid] = Vertex(vid, vid, self._community[vid])
            neighbor_vids = self._graph[vid].keys()
            self._m += len(neighbor_vids)
        self._m //= 2  # 边数 = 总度数 / 2

    def phase_1(self):

        change = False  # 该 phase1 是否使网络结构发生改变
        stop = False  # 模块度不在增加时， phase1 可以结束
        visit_seq = list(self._graph.keys())
        random.shuffle(visit_seq)

        while stop is False:
            stop = True
            for vid_i in visit_seq:  # 访问每一个节点 i
                neighbor_i = self._graph[vid_i]  # 节点 i 关联的边(Key: 邻接结点, Edge: 边权)
                vertex_i = self._vertices[vid_i]  # 节点 i 的 Vertex 对象
                cid_i = vertex_i._cid  # 节点 i 所在的社区
                k_i = vertex_i._k_in + sum(neighbor_i.values())  # 节点 i 的权重：内部边权 + 外部边权

                cid_mg = {}  # 保存每个社区的模块度增益 Map of cid which modularity gain
                cid_max = -1
                mg_max = 0

                for vid_j in neighbor_i.keys():  # 遍历节点 i 的所有邻接节点 j
                    vertex_j = self._vertices[vid_j]  # 节点 j 的 Vertex 对象
                    cid_j = vertex_j._cid  # 节点 j 所在的社区

                    if cid_j in cid_mg:  # 如果节点 j 所在社区已经被计算过，则跳过下面的步骤
                        continue

                    tot = 0  # 关联到节点 j 所在的社区中的节点的链路上的权重的总和
                    for vid_k in self._community[cid_j]:  # 遍历节点 j 所在的社区内的所有节点 k
                        neighbor_k = self._graph[vid_k]  # 节点 k 的邻居节点
                        vertex_k = self._vertices[vid_k]  # 节点 k 的 Vertex
                        tot += vertex_k._k_in + sum(neighbor_k.values())  # 节点 k 的权重：内部边权 + 外部边权
                    if cid_i == cid_j:
                        tot -= k_i  # 避免上上行的重复计算

                    k_i_in = 0  # 从节点 i 连接到节点 j 所在的社区中的节点的链路的总和
                    for vid_l, w_l in neighbor_i.items(): # 遍历节点 i 的邻接结点 l
                        if vid_l in self._community[cid_j]:
                            k_i_in += w_l

                    cid_mg[cid_j] = (k_i_in - k_i * tot / self._m) / (self._m * 2)
                    if mg_max < cid_mg[cid_j]:
                        mg_max = cid_mg[cid_j]
                        cid_max = cid_j

                if mg_max > 0.0 and cid_max != cid_i:  # 如果增益为正
                    self._vertices[vid_i]._cid = cid_max  # 将节点 i 加入社区 cid_max
                    self._community[cid_max].add(vid_i)
                    self._community[cid_i].remove(vid_i)  # 将节点 i 从原社区移除

                    stop = False  # 网络结构改变，模块度可能还会增加，需要迭代
                    change = True


            if stop:
                break
        return change

    def phase_2(self):

        graph = collections.defaultdict(dict)  # 新的网络
        community = {}  # 新的社区
        vertices = {}  # 新的节点

        for cid, community_vids in self._community.items():  # 遍历所有社区
            if len(community_vids) == 0:  # 空社区
                continue

            vertex_i = Vertex(cid, cid, set())  # 跟据社区创建新网络的节点
            for vid_i in community_vids:  # 遍历社区内的节点
                vertex_i._nodes.update(self._vertices[vid_i]._nodes)  # 保存社区的节点
                vertex_i._k_in += self._vertices[vid_i]._k_in  # 更新节点内部权重
                neighbor_i = self._graph[vid_i]
                for vid_j, w_j in neighbor_i.items():  # 遍历节点 i 的邻接节点 j
                    if vid_j in community_vids:
                        vertex_i._k_in += w_j / 2.0  # 因为会重复计算，所以 / 2

            # 为社区在新的网络中创造一个节点
            community[cid] = {cid}
            vertices[cid] = vertex_i

        for cid_i, community_i in self._community.items():  # 遍历原社区，更新 graph
            if len(community_i) == 0:
                continue

            for cid_j, community_j in self._community.items():
                if cid_i >= cid_j or len(community_j) == 0:  # 避免重复
                    continue

                w = 0.0  # 新网络，社区 i 生成的节点与社区 j 生成的节点的边权
                for vid_i in community_i:
                    for vid_j, w_j in self._graph[vid_i].items():  # 遍历系欸但 i 的邻接节点
                        if vid_j in community_j:
                            w += w_j
                if w != 0:
                    graph[cid_i][cid_j] = w
                    graph[cid_j][cid_i] = w

        # 更新网络、社区和节点
        self._graph = graph
        self._community = community
        self._vertices = vertices

    def get_communities(self):
        communities = []
        for cid, community in self._community.items():
            if len(community) == 0:
                continue
            c = set()
            for vid in community:
                c.update(self._vertices[vid]._nodes)
            communities.append(list(c))
        return communities

    def get_predict_result(self):
        pr = {}
        max_vid = 0
        for cid, community in self._community.items():
            for vid in self._vertices[cid]._nodes:
                pr[vid] = cid
                if max_vid < vid:
                    max_vid = vid
        predict_res = []
        for i in range(0, max_vid + 1):
            predict_res.append(pr[i])
        return predict_res

    def execute(self):
        ite = 1
        while True:
            print("Ite ", ite)
            ite += 1
            if self.phase_1():
                self.phase_2()
            else:
                break
        return self.get_communities()


"""
# Dataset: Facebook
graph_file = "./Datasets/facebook/facebook_combined.txt"
ground_truth_file = ""

# Dataset: PolBooks
graph_file = "./Datasets/polbooks/polbooks.gml"
ground_truth_file = graph_file

# Dataset: Football
graph_file = "./Datasets/football/football.gml"
ground_truth_file = graph_file

# Dataset: Email-Eu
graph_file = "./Datasets/email-Eu-core/email-Eu-core.txt"
ground_truth_file = "./Datasets/email-Eu-core/email-Eu-core-department-labels.txt"

# Dataset: Lastfm-Asia
graph_file = "./Datasets/lasftm_asia/lastfm_asia_edges.csv"
ground_truth_file = "./Datasets/lasftm_asia/lastfm_asia_target.csv"
"""

if __name__ == '__main__':

    # Dataset: PolBooks
    graph_file = "./Datasets/polbooks/polbooks.gml"
    ground_truth_file = graph_file

    # Load Graph File
    print("Graph File Path:", graph_file)
    print("Ground Truth File Path:", ground_truth_file)
    graph = load_graph(graph_file)
    nxgraph = load_nxgraph(graph_file)
    ground_truth = load_ground_truth(ground_truth_file)

    # Standard Louvain
    start_time = time.time()
    partition = community_louvain.best_partition(nxgraph, random_state=1)
    print("Standard Louvain Cost Time: ", time.time() - start_time)
    std_predict_res = list(partition.values())

    std_communities = []
    cids = []
    for vid, cid in partition.items():
        if cid not in cids:
            cids.append(cid)
    for cid in cids:
        std_communities.append([])
    for vid, cid in partition.items():
        std_communities[cid].append(vid)
    std_modularity = compute_modularity(std_communities, nxgraph)
    std_nmi = normalized_mutual_info_score(std_predict_res, ground_truth)
    print("Standard Modularity:", std_modularity)
    print("Standard NMI:", std_nmi)
    print("Standard Communities:", len(std_communities))

    # My Louvain
    start_time = time.time()
    louvain = GenLouvain(graph)
    communities = louvain.execute()
    print("My Louvain Cost Time: ", time.time() - start_time)
    predict_res = louvain.get_predict_result()
    modularity = compute_modularity(communities, nxgraph)
    my_nmi = normalized_mutual_info_score(predict_res, ground_truth)
    print("My Modularity:", modularity)
    print("My NMI:", my_nmi)
    print("My Communities:", len(communities))

    # # Draw
    # pos = nx.spring_layout(nxgraph)
    #
    # # Standard Graph
    # nx.draw_networkx_nodes(nxgraph, pos, partition.keys(), node_size=20, node_color=list(partition.values()))
    # nx.draw_networkx_edges(nxgraph, pos, alpha=0.3)
    # plt.show()
    #
    # # My graph
    # partition = {}
    # cids = {}
    # idx = 1
    # for i in predict_res:
    #     if i not in cids:
    #         cids[i] = idx
    #         idx += 1
    # for i in range(len(predict_res)):
    #     partition[i] = cids[predict_res[i]]
    # nx.draw_networkx_nodes(nxgraph, pos, partition.keys(), node_size=20, node_color=list(partition.values()))
    # nx.draw_networkx_edges(nxgraph, pos, alpha=0.3)
    # plt.show()


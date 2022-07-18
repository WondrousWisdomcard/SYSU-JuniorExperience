import collections
import networkx as nx


def load_graph(path):
    n = 0
    m = 0
    graph = collections.defaultdict(dict)
    if path.endswith('.txt'):
        with open(path) as text:
            for line in text:
                v = line.strip().split()
                v_i, v_j = int(v[0]), int(v[1])
                w = 1.0
                graph[v_i][v_j] = w
                graph[v_j][v_i] = w
                m += 1
            n = len(graph)
    elif path.endswith(".gml"):
        G = nx.read_gml(path, label='id')
        for v_i, v_j in G.edges:
            w = 1.0
            graph[v_i][v_j] = w
            graph[v_j][v_i] = w
        n = len(G.nodes)
        m = len(G.edges)
    elif path.endswith(".csv"):
        with open(path) as text:
            for line in text:
                v = line.strip().split(',')
                v_i, v_j = int(v[0]), int(v[1])
                w = 1.0
                graph[v_i][v_j] = w
                graph[v_j][v_i] = w
                m += 1
            n = len(graph)
    else:
        print("Unknown File Type, support 'csv' 'cmty.txt' 'txt' and 'gml' only")

    print("Finish Loading Graph.")
    print("n:", n)
    print("m:", m)
    return graph


def load_nxgraph(path):
    if path.endswith(".txt"):
        nxgraph = nx.Graph()
        with open(path) as text:
            for line in text:
                v = line.strip().split()
                v_i, v_j = int(v[0]), int(v[1])
                w = 1.0
                nxgraph.add_edge(v_i, v_j, weight=w)
                nxgraph.add_edge(v_j, v_i, weight=w)
        print("Finish Loading nxGraph.")
        return nxgraph
    elif path.endswith(".gml"):
        print("Finish Loading nxGraph.")
        return nx.read_gml(path, label='id')
    elif path.endswith(".csv"):
        nxgraph = nx.Graph()
        with open(path) as text:
            for line in text:
                v = line.strip().split(",")
                v_i, v_j = int(v[0]), int(v[1])
                w = 1.0
                nxgraph.add_edge(v_i, v_j, weight=w)
                nxgraph.add_edge(v_j, v_i, weight=w)
        print("Finish Loading nxGraph.")
        return nxgraph
    else:
        print("Unknown File Type, support 'csv' 'cmty.txt' 'txt' and 'gml' only")


def load_ground_truth(path):
    gt = []
    if path.endswith(".cmty.txt"):
        id = 1
        d = {}
        with open(path) as text:
            for line in text:
                v = line.strip().split()
                for i in v:
                    d[i] = id
                id += 1
        l = sorted(d.items(), key=lambda x: x[0])
        for _, g in l:
            gt.append(g)
    elif path.endswith(".txt"):
        with open(path) as text:
            for line in text:
                v = line.strip().split()
                vid, civ = int(v[0]), int(v[1])
                gt.append(civ)
    elif path.endswith(".csv"):
        with open(path) as text:
            for line in text:
                v = line.strip().split(',')
                vid, civ = int(v[0]), int(v[1])
                gt.append(civ)
    elif path.endswith(".gml"):
        G = nx.read_gml(path, label='id')
        for i in range(len(G.nodes)):
            gt.append(G.nodes[i]['value'])
    else:
        print("Unknown File Type, support 'csv' 'cmty.txt' 'txt' and 'gml' only")

    dt_s = {}
    c = 0
    for i in gt:
        if i not in dt_s:
            dt_s[i] = 1
            c += 1
    print("Finish Loading Ground Truth.")
    print(c, "Communities")
    return gt

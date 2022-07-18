import pydotplus as pdp

if __name__ == '__main__':

    f = open("treemap.txt", "r+")
    map = f.read()
    graph = pdp.graph_from_dot_data(map)
    graph.write_png("tree.png")


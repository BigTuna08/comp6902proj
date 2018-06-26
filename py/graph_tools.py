from sys import stdout

def count_edges(g_file):
    g = load_graph_and_info(g_file)
    print(g)
    s = sum([sum(row) for row in g])/2
    return s


def load_graph_and_info(file_name):
    g = []
    m0, m, n, alpha = None, None, None, None
    with open(file_name) as f:
        l = f.readline().split()
        m0, m, n, alpha = (int(l[0]), int(l[1]), int(l[2]), float(l[3]))
        for line in f.readlines():
            g.append([int(i) for i in line.strip().split()])

    return g, m0, m, n, alpha


def get_graph_info(file_name):
    with open(file_name) as f:
        l = f.readline().split()
        m0, m, n, alpha = (int(l[0]), int(l[1]), int(l[2]), float(l[3]))
        return m0, m, n, alpha

###          Graph printing methods    ###

# print graph as edge list
def print_el(g, out=stdout):
    print("source\ttarget", file=out)
    for i in range(len(g)):
        for j in g[i]:
            if i > j: # only print each edge once
                print("{}\t{}".format( i, j), file=out)


# print graph as adjacency matrix
def print_adj_matrix(g):
    n = len(g)
    for i in range(n):
        for j in range(n):
            val = 1 if j in g[i] else 0
            print(val, end=" ")
        print()


# print graph as vertex list
def print_g(g):
    for i in range(len(g)):
        print(i, g[i])

# # print graph as edge list
# def print_el(g, out=stdout):
#     print("source\ttarget", file=out)
#     for i in range(len(g)):
#         for j in range(i + 1, len(g)):
#             if g[i][j]:
#                 print("{}\t{}".format(i, j), file=out)
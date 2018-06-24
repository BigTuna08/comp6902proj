import sys
import random


def build_graph(m0, m, n, alpha):
    # print("making graph...")
    # print("m0= ", m0)
    # print("m= ", m)
    # print("n= ", n)
    # print("alpha= ", alpha)

    #make empty graph
    g = []
    for i in range(n):
        g.append(set())

    #create cycle
    for i in range(m0-1):
        add_edge(i,i+1, g)
    add_edge(0, m0-1, g)

    # add (n-m0) nodes with m edges each, accoriding to pref
    # attachement with strength alpha
    for i in range(m0,n):
        targets = choose_attach_targets(i, m, alpha, g)
        for j in targets:
            add_edge(i, j, g)  # add edge between i and j

    return g


def choose_attach_targets(node_i, m, alpha, g):
    targets = []
    weights = [len(row) ** alpha for row in g]
    total_weight = sum(weights)
    # print(weights)
    # print(g[0])
    # print(g[1])
    # print(g[2])
    # print(g[3])
    # print(g[4], "\n\n")
    # # print_g(g)
    # if node_i == 6:
    #     raise "quit"

    for _i in range(m):
        r = random.random() * total_weight
        s = 0
        # pick target for new edge based on pref attach
        for j in range(node_i):
            s += weights[j]
            if s > r:
                targets.append(j) #pick node j
                total_weight -= weights[j]
                weights[j] = 0 # dont pick it twice
                break

    if len(targets) != m:
        print("m=", m, "n_i=", node_i, "targets=", targets)
        raise "Error picking random edges, no target selected" # should never be here

    return targets






def print_el(g):
    for i in range(len(g)):
        for j in g[i]:
            print("{}\t{}".format( i, j))


def print_adj_matrix(g):
    n = len(g)
    for i in range(n):
        for j in range(n):
            val = 1 if j in g[i] else 0
            print(val, end=" ")
        print()


def write_graph(g, f_name, m, m0, n, alpha):
    with open(f_name, 'w') as f:
        print(m, m0, n, alpha, file=f)
        for i in range(n):
            for j in range(n):
                val = 1 if j in g[i] else 0
                print(val, end=" ", file=f)
            print(file=f)

def print_g(g):
    for i in range(len(g)):
        print(i, g[i])


def add_edge(n1, n2, g):
    g[n1].add(n2)
    g[n2].add(n1)


def get_pref_sum(g, alpha):
    s = 0
    for vert_list in g:
        s += len(vert_list) ** alpha
    return s

def parse_args(args):
    m0, m, n, alpha = (int(args[1]), int(args[2]), int(args[3]), float(args[4]))
    assert m0 >= m, "m0 must be >= m"
    assert n >= m0, "m0 must be >= n"
    return m0, m, n, alpha



# m0, m, n, alpha
if __name__ == '__main__':
    if len(sys.argv) > 4:
        m, m0, n, alpha = parse_args(sys.argv)
        g = build_graph(m, m0, n, alpha)

        if len(sys.argv) > 5:
            write_graph(g, sys.argv[5], m, m0, n, alpha)
        else:
            # print_el(g)
            # print_g(g)
            print_adj_matrix(g)
    else:
        print('Requires 4 arguments: m0, m, n, alpha\n'
              'm0: number of initial nodes\n'
              'm: average number of edges,'
              'n: total nodes\n'
              'alpha: preferential attachment strength\n'
              '\t < 1: sub-linear\n'
              '\t 1: linear (scale free model)\n'
              '\t > 1: super-linear attachment')

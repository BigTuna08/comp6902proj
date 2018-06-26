import sys
import random
from graph_tools import print_el

###          Graph creation methods    ###

def build_graph(m0, m, n, alpha):
    print("building graph with..", m0, m, n, alpha)
    #make empty graph
    g = []
    for i in range(n):
        g.append(set())

    #create initial cycle
    for i in range(m0-1):
        add_undir_edge(i, i + 1, g)
    add_undir_edge(0, m0 - 1, g)

    # add (n - m0) nodes with m edges each, accoriding to pref
    # attachement with strength alpha
    for i in range(m0,n):
        targets = choose_attach_targets(i, m, alpha, g)
        for j in targets:
            add_undir_edge(i, j, g)  # add edge between i and j

    return g


def choose_attach_targets(node_i, m, alpha, g):
    targets = []
    weights = [len(row) ** alpha for row in g]
    total_weight = sum(weights)

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
        print("\n\n\nm=", m, "n_i=", node_i, "targets=", targets)
        print(g)
        print("\n\n")
        raise "Error picking random edges, no target selected" # should never be here

    return targets


###   Creates graph file for reduction    ###
# write graph info and adj matrix to file
def write_graph(g, f_name, m, m0, n, alpha):
    with open(f_name, 'w') as f:
        print(m, m0, n, alpha, file=f)
        for i in range(n):
            for j in range(n):
                val = 1 if j in g[i] else 0
                print(val, end=" ", file=f)
            print(file=f)


# add edge between 2 nodes in g
def add_undir_edge(n1, n2, g):
    g[n1].add(n2)
    g[n2].add(n1)


def make_graph(m0, m, n, alpha, out_file):
    g = build_graph(m, m0, n, alpha)
    write_graph(g, "graphs/" + out_file, m, m0, n, alpha)
    with open("graphs/edge_list/" + out_file, "w") as f:
        print_el(g, f)


###          Run file          ###

# m0: number of initial nodes
# m: average number of edges
# n: total nodes
# alpha: preferential attachment strength
def parse_args(args):
    m0, m, n, alpha = (int(args[1]), int(args[2]), int(args[3]), float(args[4]))
    assert m0 >= m, "m0 must be >= m"
    assert n >= m0, "m0 must be >= n"
    return m0, m, n, alpha


if __name__ == '__main__':
    if len(sys.argv) > 5:
        m, m0, n, alpha = parse_args(sys.argv)
        g = build_graph(m, m0, n, alpha)
        write_graph(g, "graphs/" + sys.argv[5], m, m0, n, alpha)

    else:
        print('Requires 5 arguments: m0, m, n, alpha\n'
              'm0: number of initial nodes\n'
              'm: average number of edges,'
              'n: total nodes\n'
              'alpha: preferential attachment strength\n'
              '\t < 1: sub-linear\n'
              '\t 1: linear (scale free model)\n'
              '\t > 1: super-linear attachment'
              'graph_id: used for filename in ../graphs directory')
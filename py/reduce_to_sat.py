import sys
from CNFVarManager import  CNFVarManager
from get_clause_count import get_clause_count




def count_edges(g_file):
    g = load_graph(g_file)
    print(g)
    s = sum([sum(row) for row in g])/2
    return s

def parse_args(args):
    return args[1], args[2], int(args[3]), args[4]


def load_graph(file_name):
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


def add_type1_clauses(var_mnger, out):
    count = 0
    # for G
    for sg_i in range(var_mnger.k): # sg_i = sub graph index
        clause = ""
        for node_i in range(var_mnger.n_g):
            clause += str(var_mnger.var_index('g', node_i, sg_i)) + " "
        clause += "0"
        print(clause, file=out)

        count += 1

    # for H
    for sg_i in range(var_mnger.k):
        clause = ""
        for node_i in range(var_mnger.n_h):
            clause += str(var_mnger.var_index('h', node_i, sg_i)) + " "
        clause += "0"
        print(clause, file=out)

        count += 1

    print(count, "type 1")
    return count


def add_type2_clauses(var_mnger, out):
    count = 0
    # for G
    for sg_i in range(var_mnger.k- 1):  # sg_i, sg_j = pair of sub graph indexes
        for sg_j in range(sg_i+ 1, var_mnger.k):
            for node_i in range(var_mnger.n_g):
                clause = str(-var_mnger.var_index('g', node_i, sg_i)) + " " +\
                         str(-var_mnger.var_index('g', node_i, sg_j)) + " 0"
                print(clause, file=out)
                count += 1

    # for H
    for sg_i in range(var_mnger.k- 1):  # sg_i, sg_j = pair of sub graph indexes
        for sg_j in range(sg_i+ 1, var_mnger.k):
            for node_i in range(var_mnger.n_h):
                clause = str(-var_mnger.var_index('h', node_i, sg_i)) + " " +\
                         str(-var_mnger.var_index('h', node_i, sg_j)) + " 0"
                print(clause, file=out)
                count += 1

    print(count, "type 2")
    return count


def add_type3_clauses(g, h, var_mnger, out):
    count = 0

    for m in range(var_mnger.n_g-1):
        for n in range(m+1, var_mnger.n_g):
            for q in range(var_mnger.n_h - 1):
                for r in range(q + 1, var_mnger.n_h):
                    for i in range(var_mnger.k - 1):  # sg_i, sg_j = pair of sub graph indexes
                        for j in range(i + 1, var_mnger.k):
                            if g[m][n] != h[q][r]: # edge between exactly one
                                clause = str(-var_mnger.var_index('g', m, i)) + " " + \
                                         str(-var_mnger.var_index('g', n, j)) + " " +\
                                         str(-var_mnger.var_index('h', q, i)) + " " + \
                                         str(-var_mnger.var_index('h', r, j)) + " 0"
                                count += 1
                                print(clause, file=out)
    print(count, "type 3")
    return count



# def create_clause_list(g, h, var_mnger):
#     clause_list = []
#     add_type1_clauses(clause_list, var_mnger)
#     add_type2_clauses(clause_list, var_mnger)
#     add_type3_clauses(clause_list, g, h, var_mnger)
#     return clause_list
#
#
# def write_output(clause_list, var_manger, file_name):
#     with open(file_name, 'w') as f:
#         print('p cnf', var_manger.n_vars(), len(clause_list), file=f)
#         for clause in clause_list:
#             print(clause, file=f)


def reduce_to_sat(g, h, k, computed_clause_count, out):
    mnger = CNFVarManager(g, h, k)
    print("p cnf", mnger.n_vars(), computed_clause_count, file=out)

    clause_count = 0
    clause_count += add_type1_clauses(mnger, out)
    clause_count += add_type2_clauses(mnger, out)
    clause_count += add_type3_clauses(g, h, mnger, out)

    assert clause_count == computed_clause_count, "Badness! " + str(clause_count) + " != " + str(computed_clause_count)




# g, h, k
if __name__ == '__main__':
    if len(sys.argv) > 3:

        g_file, h_file, k, out_file = parse_args(sys.argv)
        g, _, m_g, n_g, _ = load_graph(g_file)
        h, _, m_h, n_h, _ = load_graph(h_file)

        with open(out_file, "w") as f:
            computed_clause_count = get_clause_count(n_g, k, m_g, m_h)
            reduce_to_sat(g,h,k,computed_clause_count,f)





    else:
        print('Requires 3 arguments: g_file, h_file, k\n'
              'g_file: number of initial nodes\n'
              'h_file: average number of edges,'
              'k: total nodes\n')
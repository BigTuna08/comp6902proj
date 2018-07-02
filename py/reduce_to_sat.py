import sys
from SatManager import CNFVarManager
from get_clause_count import get_clause_count
from tool_box import load_graph_and_info, line_prepender


###          clause making methods    ###

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
    for sg_i in range(var_mnger.k):  # sg_i, sg_j = pair of sub graph indexes
        for sg_j in range(var_mnger.k):
            if sg_i == sg_j:
                continue
            for node_i in range(var_mnger.n_g):
                clause = str(-var_mnger.var_index('g', node_i, sg_i)) + " " +\
                         str(-var_mnger.var_index('g', node_i, sg_j)) + " 0"
                print(clause, file=out)
                count += 1

    # for H
    for sg_i in range(var_mnger.k):  # sg_i, sg_j = pair of sub graph indexes
        for sg_j in range(var_mnger.k):
            if sg_i == sg_j:
                continue
            for node_i in range(var_mnger.n_h):
                clause = str(-var_mnger.var_index('h', node_i, sg_i)) + " " +\
                         str(-var_mnger.var_index('h', node_i, sg_j)) + " 0"
                print(clause, file=out)
                count += 1

    print(count, "type 2")
    return count


def add_type3_clauses(g, h, var_mnger, out):
    count = 0

    for m in range(var_mnger.n_g):
        for n in range(var_mnger.n_g):
            if m == n:
                continue
            for q in range(var_mnger.n_h):
                for r in range(var_mnger.n_h):
                    if q == r:
                        continue
                    for i in range(var_mnger.k):  # sg_i, sg_j = pair of sub graph indexes
                        for j in range(var_mnger.k):
                            if i == j:
                                continue
                            if g[m][n] != h[q][r]: # edge between exactly one
                                clause = str(-var_mnger.var_index('g', m, i)) + " " + \
                                         str(-var_mnger.var_index('g', n, j)) + " " +\
                                         str(-var_mnger.var_index('h', q, i)) + " " + \
                                         str(-var_mnger.var_index('h', r, j)) + " 0"
                                count += 1
                                print(clause, file=out)
    print(count, "type 3")
    return count


###          Run File    ###


# 'g_file_name: number of input file used as input graph G (file in ../graphs)\n'
# 'h_file: number of input file used as input graph H (file in ../graphs)\n'
# 'k: total nodes\n'
# 'out_file: name of output file in ../cnf (no extension)')
def parse_args(args):
    return args[1], args[2], int(args[3]), args[4]




def reduce_to_sat(g_id, h_id, k, out_file):
    g, _, m_g, n_g, _ = load_graph_and_info("graphs/" + g_id)
    h, _, m_h, n_h, _ = load_graph_and_info("graphs/" + h_id)

    with open("cnf/" + out_file + ".cnf", "w") as out:
        computed_clause_count = get_clause_count(n_g, k, m_g, m_h)
        mnger = CNFVarManager(g, h, k)
        # print("p cnf", mnger.n_vars(), int(computed_clause_count), file=out)

        clause_count = 0
        clause_count += add_type1_clauses(mnger, out)
        clause_count += add_type2_clauses(mnger, out)
        clause_count += add_type3_clauses(g, h, mnger, out)

        mnger.write_to_file("cnf/recover/" + out_file)

        # assert clause_count == computed_clause_count, "Badness! " + str(clause_count) + " != " + str(
        #     computed_clause_count)
    line = "p cnf" + str(mnger.n_vars()) + " " + str(int(clause_count))
    line_prepender("cnf/" + out_file + ".cnf", line)


if __name__ == '__main__':
    if len(sys.argv) > 4:
        g_file, h_file, k, out_file = parse_args(sys.argv)
        reduce_to_sat(g_file, h_file, k, out_file)
    else:
        print('Requires 4 arguments: g_file, h_file, k and out_file\n'
              'g_file_name: number of input file used as input graph G (file in ../graphs)\n'
              'h_file: number of input file used as input graph H (file in ../graphs)\n'
              'k: total nodes\n'
              'out_file: name of output file in ../cnf (no extension)')





#
# ###          clause making methods    ###
#
# def add_type1_clauses(var_mnger, out):
#     count = 0
#     # for G
#     for sg_i in range(var_mnger.k): # sg_i = sub graph index
#         clause = ""
#         for node_i in range(var_mnger.n_g):
#             clause += str(var_mnger.var_index('g', node_i, sg_i)) + " "
#         clause += "0"
#         print(clause, file=out)
#
#         count += 1
#
#     # for H
#     for sg_i in range(var_mnger.k):
#         clause = ""
#         for node_i in range(var_mnger.n_h):
#             clause += str(var_mnger.var_index('h', node_i, sg_i)) + " "
#         clause += "0"
#         print(clause, file=out)
#
#         count += 1
#
#     print(count, "type 1")
#     return count
#
#
# def add_type2_clauses(var_mnger, out):
#     count = 0
#     # for G
#     for sg_i in range(var_mnger.k- 1):  # sg_i, sg_j = pair of sub graph indexes
#         for sg_j in range(sg_i+ 1, var_mnger.k):
#             for node_i in range(var_mnger.n_g):
#                 clause = str(-var_mnger.var_index('g', node_i, sg_i)) + " " +\
#                          str(-var_mnger.var_index('g', node_i, sg_j)) + " 0"
#                 print(clause, file=out)
#                 count += 1
#
#     # for H
#     for sg_i in range(var_mnger.k- 1):  # sg_i, sg_j = pair of sub graph indexes
#         for sg_j in range(sg_i+ 1, var_mnger.k):
#             for node_i in range(var_mnger.n_h):
#                 clause = str(-var_mnger.var_index('h', node_i, sg_i)) + " " +\
#                          str(-var_mnger.var_index('h', node_i, sg_j)) + " 0"
#                 print(clause, file=out)
#                 count += 1
#
#     print(count, "type 2")
#     return count
#
#
# def add_type3_clauses(g, h, var_mnger, out):
#     count = 0
#
#     for m in range(var_mnger.n_g-1):
#         for n in range(m+1, var_mnger.n_g):
#             for q in range(var_mnger.n_h - 1):
#                 for r in range(q + 1, var_mnger.n_h):
#                     for i in range(var_mnger.k - 1):  # sg_i, sg_j = pair of sub graph indexes
#                         for j in range(i + 1, var_mnger.k):
#                             if g[m][n] != h[q][r]: # edge between exactly one
#                                 clause = str(-var_mnger.var_index('g', m, i)) + " " + \
#                                          str(-var_mnger.var_index('g', n, j)) + " " +\
#                                          str(-var_mnger.var_index('h', q, i)) + " " + \
#                                          str(-var_mnger.var_index('h', r, j)) + " 0"
#                                 count += 1
#                                 print(clause, file=out)
#     print(count, "type 3")
#     return count
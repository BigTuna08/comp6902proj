import sys

from tool_box import load_graph_and_info, print_adj_m
from verifier import verify_clique_reduction
from tool_box import line_prepender
from CliqueManager import IndManger



#
# def reduce_to_clique(g_file, h_file, k, out_id):
#     g, _, m_g, n_g, _ = load_graph_and_info("graphs/" + g_file)
#     h, _, m_h, n_h, _ = load_graph_and_info("graphs/" + h_file)
#     mnger = IndManger(n_g, n_h)
#     out_file = "cliques/" + out_id + ".mtx"
#     count = 0
#     print("Reducing {} to clique... > {}".format(out_id, out_file))
#     with open(out_file, "w") as out:
#         for g_src in range(n_g):
#             for g_targ in range(g_src+1, n_g): #only upper triangle of matrix
#                 for h_src in range(n_h):
#                     for h_targ in range(h_src+1, n_h):  #only upper triangle of matrix
#                         if g[g_src][g_targ] == h[h_src][h_targ]:
#                             src = mnger.get_combo_ind(g_src, h_src)
#                             targ = mnger.get_combo_ind(g_targ, h_targ)
#                             # print(out)
#                             print(targ, src, sep="\t", file=out)  # edge list with weight 1 for all edges
#                             count += 1
#     header = "%%MatrixMarket matrix coordinate pattern symmetric\n" +\
#              str(n_g*n_h) + "\t" + str(n_g*n_h) + "\t" + str(count)
#     line_prepender(out_file, header)


def reduce_to_clique(g_file, h_file, k, out_id):
    g, _, m_g, n_g, _ = load_graph_and_info("graphs/" + g_file)
    h, _, m_h, n_h, _ = load_graph_and_info("graphs/" + h_file)
    mnger = IndManger(n_g, n_h)
    out_file = "cliques/" + out_id + ".mtx"
    count = 0
    edge_strings = []
    print("Reducing {} to clique... > {}".format(out_id, out_file))


    assert n_g == len(g), "Just checking"
    assert n_h == len(h), "Just checking"
    assert n_h == n_g, "just check"

    n = n_g * n_h + 1  # +1 for 1 indexed

    graph_prod = []
    graph_prod.append([0]*n)
    for src in range(1,n):
        row = [0]
        for targ in range(1,n):
            g_src, h_src = mnger.ind_to_combo(src)
            g_targ, h_targ = mnger.ind_to_combo(targ)
            same_i = (g_src == g_targ) or (h_src == h_targ)
            val = 0 if same_i or (g[g_src][g_targ] != h[h_src][h_targ]) else 1
            row.append(val)
        graph_prod.append(row)

    # for g_src in range(n_g):
    #     for g_targ in range(n_g): #only upper triangle of matrix
    #
    #         for h_src in range(n_h):
    #             for h_targ in range(n_h):  #only upper triangle of matrix
    #
    #                 if g[g_src][g_targ] == h[h_src][h_targ]:
    #                     src = mnger.get_combo_ind(g_src, h_src)
    #                     targ = mnger.get_combo_ind(g_targ, h_targ)
    #                     graph_prod[src][targ] = 1
    #                     graph_prod[targ][src] = 1



    for src in range(n):
        for targ in range(src+1, n): #only upper triangle of matrix
            if graph_prod[src][targ] == 1:
                edge_strings.append(str(targ) + "\t" + str(src))
                count += 1


    header = "%%MatrixMarket matrix coordinate pattern symmetric\n" +\
             str(n_g*n_h) + "\t" + str(n_g*n_h) + "\t" + str(count) +"\n"

    with open(out_file, "w") as f:
        f.write(header)
        f.write("\n".join(edge_strings))

    # print_adj_m(g, "g")
    # print_adj_m(h, "h")
    # print_adj_m(graph_prod, "prod")
    # verify_clique_reduction(out_id)




#faster
# def reduce_to_clique2(g_file, h_file, k, out_id):
#
#     g, _, m_g, n_g, _ = load_graph_and_info("graphs/" + g_file)
#     h, _, m_h, n_h, _ = load_graph_and_info("graphs/" + h_file)
#
#     mnger = IndManger(n_g, n_h)
#     out_file = "cliques/" + out_id + ".mtx"
#     print("Reducing {} to clique... > {}".format(out_id, out_file))
#
#     count = 0
#     edge_strings = []
#     assert n_g == len(g), "Just checking"
#     assert n_h == len(h), "Just checking"
#     assert n_h == n_g, "Just checking"
#
#     for g_src in range(n_g):
#         for g_targ in range(g_src+1, n_g): #only upper triangle of matrix
#
#             for h_src in range(n_h):
#                 for h_targ in range(h_src+1, n_h):  #only upper triangle of matrix
#
#                     if g[g_src][g_targ] == h[h_src][h_targ]:
#                         src = mnger.get_combo_ind(g_src, h_src)   # index of src_node in product graph
#                         targ = mnger.get_combo_ind(g_targ, h_targ)  # index of targ_node in product graph
#                         edge_strings.append(str(targ) + "\t" + str(src))   # add edge
#                         count += 1
#
#
#     header = "%%MatrixMarket matrix coordinate pattern symmetric\n" +\
#              str(n_g*n_h) + "\t" + str(n_g*n_h) + "\t" + str(count) + "\n"
#
#     with open(out_file, "w") as f:
#         f.write(header)
#         f.write("\n".join(edge_strings))




# 'g_file_name: number of input file used as input graph G (file in ../graphs)\n'
# 'h_file: number of input file used as input graph H (file in ../graphs)\n'
# 'k: total nodes\n'
# 'out_file: name of output file in ../cliques (no extension)')
def parse_args(args):
    return args[1], args[2], int(args[3]), args[4]


if __name__ == '__main__':
    if len(sys.argv) > 4:
        g_file, h_file, k, out_id = parse_args(sys.argv)
        reduce_to_clique(g_file, h_file, k, out_id)


    else:
        print('Requires 4 arguments: g_file, h_file, k\n'
              'g_file: number of initial nodes\n'
              'h_file: average number of edges\n'
              'k: total nodes\n'
              'out_file: name of output file in cliques directory')

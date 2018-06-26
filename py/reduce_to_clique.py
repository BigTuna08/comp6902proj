import sys
from graph_tools import load_graph_and_info


# Still not fully tested
class IndManger:
    def __init__(self, n_g, n_h):
        self.n_g = n_g #most significant
        self.n_h = n_h

    def get_combo_ind(self, g_i, h_i):
        return g_i*self.n_h + h_i

    def ind_to_combo(self, ind):
        return (ind//self.n_h, ind % self.n_h)



def reduce_to_clique(g, h, n_g, n_h, k, out):
    mnger = IndManger(n_g, n_h)
    for g_src in range(n_g):
        for g_targ in range(n_g):
            for h_src in range(n_h):
                for h_targ in range(n_h):
                    if g[g_src][g_targ] == h[h_src][h_targ]:
                        src = mnger.get_combo_ind(g_src, h_src)
                        targ = mnger.get_combo_ind(g_targ, h_targ)
                        print(src, targ, 1, sep="\t", file=out) # edge list with weight 1 for all edges


# 'g_file_name: number of input file used as input graph G (file in ../graphs)\n'
# 'h_file: number of input file used as input graph H (file in ../graphs)\n'
# 'k: total nodes\n'
# 'out_file: name of output file in ../cliques (no extension)')
def parse_args(args):
    return args[1], args[2], int(args[3]), args[4]


if __name__ == '__main__':
    if len(sys.argv) > 4:
        g_file, h_file, k, out_file = parse_args(sys.argv)
        g, _, m_g, n_g, _ = load_graph_and_info("graphs/" + g_file)
        h, _, m_h, n_h, _ = load_graph_and_info("graphs/" + h_file)

        with open("cliques/" + out_file + ".out", "w") as f:
            reduce_to_clique(g,h , n_g, n_h, k, f)

    else:
        print('Requires 4 arguments: g_file, h_file, k\n'
              'g_file: number of initial nodes\n'
              'h_file: average number of edges\n'
              'k: total nodes\n'
              'out_file: name of output file in cliques directory')
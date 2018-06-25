import sys
from graph_tools import load_graph_and_info

if __name__ == '__main__':
    if len(sys.argv) > 4:
        g_file, h_file, k, out_file = parse_args(sys.argv)
        g, _, m_g, n_g, _ = load_graph_and_info("graphs/" + g_file)
        h, _, m_h, n_h, _ = load_graph_and_info("graphs/" + h_file)

        with open("cnf/" + out_file + ".cnf", "w") as f:
            computed_clause_count = get_clause_count(n_g, k, m_g, m_h)
            reduce_to_sat(g,h,k,computed_clause_count,f, "cnf/recover/" + out_file + ".out")

    else:
        print('Requires 3 arguments: g_file, h_file, k\n'
              'g_file: number of initial nodes\n'
              'h_file: average number of edges\n'
              'k: total nodes\n'
              'out_file: name of output file in graphs directory')
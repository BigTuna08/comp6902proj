import os
import tool_box as tb
from CliqueManager import IndManger

def verify_all():
    error_files = []
    locs = [("results/clique_sol/","c"), ("results/sat_sol/","s")]

    for loc in locs:
        print("Verifying Solutions in {}".format(loc[0]))
        directory = os.fsencode(loc[0])
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith(".out"):
                id = filename[:-4]
                s = tb.sol_from_file(id, loc[1])

                # print()

                if s.h_verts is None:
                    continue

                assert s.is_valid(id), "\nInvaild solution for {}".format(loc)
    print("all valid!")



def verify_all_cliques():
    directory = os.fsencode("cliques/")
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".mtx"):
            id = filename[:-4]
            verify_clique_reduction(id)



def verify_clique_reduction(id):
    print("verifying clique..")
    jfi = tb.JointFileID(id)

    g, _, _, n_g, _ = tb.load_graph_and_info("graphs/"+ jfi.g_file())
    h, _, _, n_h, _ = tb.load_graph_and_info("graphs/" + jfi.h_file())

    ind_mnger = IndManger(n_g, n_h)

    n = n_g*n_h + 1

    combo = [[0]*n for _ in range(n)]


    with open("cliques/"+id+".mtx") as f:
        f.readline()
        f.readline()
        for line in f.readlines():
            parts = line.split()  # targ_node, src_node (in graph product)
            s, t = int(parts[0]), int(parts[1])
            # src_g, src_h = ind_mnger.ind_to_combo(s)     # get indicies for g and h
            # targ_g, targ_h = ind_mnger.ind_to_combo(t)
            combo[s][t] = 1
            combo[t][s] = 1


    for s in range(1,n):
        for t in range(s+1,n):
            src_g, src_h = ind_mnger.ind_to_combo(s)  # get indicies for g and h
            targ_g, targ_h = ind_mnger.ind_to_combo(t)

            print(s,t)
            print(src_g, src_h)
            print(targ_g, targ_h)
            print(g[src_g][targ_g], h[src_h][targ_h], combo[s][t], "\n\n\n")

            if src_g == src_h or targ_g == src_h:
                assert combo[s][t] == 0, "Edge in wrong spot!"
            elif g[src_g][targ_g] == h[src_h][targ_h]:
                assert combo[s][t] == 1, "Missing edge in product graph!"
            else:
                assert combo[s][t] == 0, "Bad edge in product graph!"


    print("Reduction all good for: {}".format(id))



verify_all()
# verify_clique_reduction("g_2-8-0_5_h_1-8-0_5_k_6")
#verify_all_cliques()

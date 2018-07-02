import sys, os
from CliqueManager import IndManger, CliqueInfo
from tool_box import JointFileID



def print_common_induced_subgraph(instance_id, efs, out=sys.stdout):
    global errors_files
    a = CliqueInfo("cliques/results/" + instance_id + ".out")
    if a.clique_exists is None:
        efs.append(instance_id)
        return

    jfi = JointFileID(instance_id)

    ind_manager = IndManger(jfi.n_g, jfi.n_h)


    if a.clique_exists:
        print("in_g\tin_h", file=out)
        for vert in a.clique:
            g_vert, h_vert = ind_manager.ind_to_combo(vert)
            print(g_vert, h_vert, sep="\t", file=out)
    else:
        print(a, file=out)
        print("No Clique in ", jfi, "\n", a, "\n")

    with open("results/clique_times/" + instance_id + ".out", "w") as f:
        f.write(str(a.time))




def recover_all(loc):
    error_files = []
    directory = os.fsencode(loc)

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".out"):
            id = filename[:-4]
            with open("results/clique_sol/" + id + ".out", "w") as f:
                print("recovering ", id)
                print_common_induced_subgraph(id, error_files, out=f)

    print("errors in: ")
    for ef in error_files:
        print(ef)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        info_dir = sys.argv[1]
        # print_common_induced_subgraph(instance_id)
        recover_all(info_dir)
    else:
        print('Req')

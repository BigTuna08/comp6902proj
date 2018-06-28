import sys, os
from SatManager import AssignmentInfo, load_var_manger





def print_common_induced_subgraph(instance_id, out=sys.stdout):
    a = AssignmentInfo("cnf/assignments/" + instance_id + ".out")
    mnger = load_var_manger("cnf/recover/" + instance_id)

    if a.satisfiable:
        g_verts, h_verts = mnger.interpret_assignment(a)
        print("in_g\tin_h", file=out)
        for i in range(mnger.k):
            print(g_verts[i], h_verts[i], sep="\t", file=out)
    else:
        print(a, file=out)
        print(a)

    with open("results/sat_times/" + instance_id + ".out", "w") as f:
        f.write(str(a.cpu_time))


def recover_all(loc):
    directory = os.fsencode(loc)

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".out"):
            id = filename[:-4]
            with open("results/sat_sol/" + id + ".out", "w") as f:
                print("recovering ", id)
                print_common_induced_subgraph(id, out=f)



if __name__ == '__main__':
    if len(sys.argv) > 1:
        info_dir = sys.argv[1]
        recover_all(info_dir)
    else:
        print('Req')

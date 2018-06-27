import sys, os
from CNFVarManager import CNFVarManager, load_manger


class CliqueInfo:
    def __init__(self, file_name):
        self.clique_exists = None  # will be either true or false if file read sucessfully
        with open(file_name) as f:
            for line in f.readlines():
                if line == "-----------------------------------------------------------------------": # go past this
                    break

            for line in f.readlines():
                line = line.split()

                if len(line) > 3 and line[0] == "Time" and line[1] == "taken:":
                    self.time = float(line[2])

                elif line[0] is "Maximum" and line[1] is "clique:":
                    if line[2] == "1" and line[3] == "1":
                        self.clique_exists = False
                    else:
                        self.clique_exists = True
                        self.clique = [int(val) for val in line[2:]]

                elif line[0] is "Size" and line[1] is "(omega):": # has max clique size (not important to us)
                    pass


        assert self.clique_exists is not None, "Error loading assignment!"


    def __str__(self):
        s = "time= " + str(self.time)
        if not self.clique_exists:
            s += "\nNo clique!"
        else:
            s += "\nClique!\n"
            for val in self.clique:
                s += str(val) + " "
        return s


#g_1-12-1_5_h_4-12-1_5_k_7
#g_1 12 1_5_h_4 12 1_5_k_7
def parse_joint_id(id):
    info = id.split("-")

    n_g = int(info[0].split("_")[1])



def print_common_induced_subgraph(instance_id, out=sys.stdout):
    a = CliqueInfo("cliques/results/" + instance_id + ".out")
    mnger = load_manger("cnf/recover/" + instance_id)

    if a.clique_exists:
        g_verts, h_verts = mnger.interpret_assignment(a)
        print("in_g\tin_h", file=out)
        for i in range(mnger.k):
            print(g_verts[i], h_verts[i], sep="\t", file=out)
    else:
        print(a, file=out)
        print(a)


def recover_all(loc):
    directory = os.fsencode(loc)

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".out"):
            id = filename[:-4]
            with open("graphs/sat_sol/" + id + ".out", "w") as f:
                print("recovering ", id)
                print_common_induced_subgraph(id, out=f)



if __name__ == '__main__':
    if len(sys.argv) > 1:
        instance_id = sys.argv[1]
        # print_common_induced_subgraph(instance_id)
        recover_all(instance_id)
    else:
        print('Req')

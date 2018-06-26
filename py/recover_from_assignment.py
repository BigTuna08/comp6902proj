import sys, os
from CNFVarManager import CNFVarManager, load_manger


class AssignmentInfo:
    def __init__(self, file_name):
        self.satisfiable = None  # will be either true or false if file read sucessfully
        with open(file_name) as f:
            for line in f.readlines():
                line = line.split()
                if len(line) > 3 and line[1] == "cpu" and line[2] == "time":
                    self.cpu_time = float(line[4])
                elif line[0] is "s":
                    if line[1] == 'SATISFIABLE':
                        self.satisfiable = True
                    else:
                        self.satisfiable = False
                elif line[0] == "v":
                    self.assignment = [int(val) for val in line[1:] ]


        assert self.satisfiable is not None, "Error loading assignment!"


    def __str__(self):
        s = "cpu time= " + str(self.cpu_time)
        if not self.satisfiable:
            s += "\nNot satisfiable"
        else:
            s += "\nSatisfiable\n"
            for val in self.assignment:
                s += str(val) + " "
        return s



def print_common_induced_subgraph(instance_id, out=sys.stdout):
    a = AssignmentInfo("cnf/assignments/" + instance_id + ".out")
    mnger = load_manger("cnf/recover/" + instance_id)

    if a.satisfiable:
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

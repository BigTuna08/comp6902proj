

class CliqueInfo:
    def __init__(self, file_name):
        self.clique_exists = None  # will be either true or false if file read sucessfully
        in_info = False
        print("\n\nstarting")
        with open(file_name) as f:
            print("oped!")
            for line in f.readlines():
                if line.__contains__("---------------------------------------------------------------------"): # go past this
                    in_info = True
                    continue

                if not in_info:
                    continue

                line = line.split()
                print("split line", line)

                if len(line) > 3 and line[0] == "Time" and line[1] == "taken:":
                    self.time = float(line[2])
                    print("time")

                elif line[0] == "Maximum" and line[1] == "clique:":
                    print("clique")
                    if line[2] == "1" and line[3] == "1":
                        self.clique_exists = False
                    else:
                        self.clique_exists = True
                        self.clique = [int(val) for val in line[2:]]

                    print("cliqe eixists? ", self.clique_exists)

                elif line[0] is "Size" and line[1] is "(omega):": # has max clique size (not important to us)
                    print("size")
                    pass

                else:
                    print("else")

            print("done")


        # assert self.clique_exists is not None, "Error loading assignment for {}!".format(file_name)  # some outputs files are bad!


    def __str__(self):
        s = ""
        if not self.clique_exists:
            s += "Reject"
        else:
            for val in self.clique:
                s += str(val) + " "
        # s += "\ntime= " + str(self.time)
        return s



# Still not fully tested
class IndManger:
    def __init__(self, n_g, n_h):
        self.n_g = n_g #most significant
        self.n_h = n_h

    def get_combo_ind(self, g_i, h_i):
        return g_i*self.n_h + h_i + 1  # 1 indexed

    def ind_to_combo(self, ind):
        return ((ind-1)//self.n_h, (ind-1) % self.n_h)  # g, h




def ind_man_test():

    n = 3
    im = IndManger(n,n)


    for i in range(n):
        for j in range(n):
            com = im.get_combo_ind(i,j)

            new_i, new_j = im.ind_to_combo(com)
            print("from ", i, j,"got", com)
            print("got :", new_i, new_j)

            assert new_i == i
            assert new_j == j
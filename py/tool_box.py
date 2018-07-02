from sys import stdout



###                                 Graph related                                  ###

def count_edges(g_file):
    g = load_graph_and_info(g_file)
    print(g)
    s = sum([sum(row) for row in g])/2
    return s


def load_graph_and_info(file_name):
    g = []
    m0, m, n, alpha = None, None, None, None
    with open(file_name) as f:
        l = f.readline().split()
        m0, m, n, alpha = (int(l[0]), int(l[1]), int(l[2]), float(l[3]))
        for line in f.readlines():
            g.append([int(i) for i in line.strip().split()])

    return g, m0, m, n, alpha


def get_graph_info(file_name):
    with open(file_name) as f:
        l = f.readline().split()
        m0, m, n, alpha = (int(l[0]), int(l[1]), int(l[2]), float(l[3]))
        return m0, m, n, alpha



def adj_matrix_from_node_list(g):
    n = len(g)
    adj_mat = []
    for i in range(n):
        adj_mat.append([1 if j in g[i] else 0 for j in range(n)])
    return adj_mat



def create_subg_from_graph(g, nodes):
    n = len(g)
    assert n == len(g[0]), "Graph should be adj matrix here!"

    sub_g = []

    for i in range(n):
        if i not in nodes:
            sub_g.append([0]*n)  # empty row
        else:
            sub_g.append([1 if (j in nodes and g[i][j]==1) else 0 for j in range(n)])   #j in nodes and edge exists
    return sub_g





###          Graph printing     ###

# print graph as edge list
def print_el(g, out=stdout):
    print("source\ttarget", file=out)
    for i in range(len(g)):
        for j in g[i]:
            if i > j: # only print each edge once
                print("{}\t{}".format( i, j), file=out)


# print node-list graph as adjacency matrix
def print_adj_matrix(g):
    n = len(g)
    for i in range(n):
        for j in range(n):
            val = 1 if j in g[i] else 0
            print(val, end=" ")
        print()


# print graph as vertex list
def print_g(g):
    for i in range(len(g)):
        print(i, g[i])


# prints adj_matrix as adj_matrix
def print_adj_m(g, name = None):
    if name is not None:
        print(name, ":")
    for row in g:
        print(row)
    print()



###                                File management                                          ###

# add line to beginning of file
def line_prepender(filename, line):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)




class Solution:
    def __init__(self, g_verts =None, h_verts=None):
        self.exists = False if (g_verts is None or h_verts is None) else True
        self.g_verts = g_verts
        self.h_verts = h_verts

        if self.exists:
            self.k = len(self.g_verts)


    def __str__(self):
        if self.exists:
            pairs = ["{}\t{}".format(self.g_verts[i], self.h_verts[i]) for i in range(self.k)]
            return "in_g\tin_h\n" + "\n".join(pairs)
        else:
            return "Reject"


    def is_valid(self, instance_id):
        jfi = JointFileID(instance_id)
        g, _, _, _, _ = load_graph_and_info("graphs/"+jfi.g_file())
        h, _, _, _, _ = load_graph_and_info("graphs/" + jfi.h_file())

        # g = create_subg_from_graph(g, self.g_verts)
        # h = create_subg_from_graph(h, self.h_verts)
        # print("self g_verts: ", self.g_verts )
        # print("self h verts:", self.h_verts)
        #
        # print()
        # print_adj_m(g, "g")
        # print()
        # print_adj_m(h, "h")

        for sg_i in range(jfi.k):
            g_i = self.g_verts[sg_i]
            h_i = self.h_verts[sg_i]
            for sg_j in range(sg_i, jfi.k):
                g_j = self.g_verts[sg_j]
                h_j = self.h_verts[sg_j]

                assert g[g_i][g_j] == h[h_i][h_j], "Uh-oh it thinks an invalid solution is valid! \n" + \
                                                   "instance: {}\ng_i, g_j: {}, {}\nh_i, h_j: {}, {}" \
                                                   "\nsg_i, sg_j: {} {}".format(instance_id, g_i, g_j, h_i, h_j, sg_i, sg_j)

        return True









def sol_from_file(instance_id, sol_type):
    loc = None
    if sol_type == "c" or sol_type == "clique":
        loc = "clique_sol/"
    elif sol_type == "s" or sol_type == "sat":
        loc = "sat_sol/"
    else:
        raise "Invalid solution type, should be 'clique' ('c') or 'sat' ('s'). Was given {}".format(sol_type)

    with open("results/" + loc + instance_id + ".out") as f:
        # print("loc: ", loc)
        # print("reading f:", f)
        if f.readline().__contains__("Reject"):
            return Solution()
        else:
            gs = []
            hs = []
            for line in f.readlines():
                parts = line.split("\t")
                gs.append(int(parts[0]))
                hs.append(int(parts[1]))
            return Solution(gs, hs)



class SolveData:

    def __init__(self, instance_id):
        self.clique_time =float(open("results/clique_times/"+instance_id+".out").readline().strip())
        self.sat_time = None
        try:
            self.sat_time = float(open("results/sat_times/" + instance_id + ".out").readline().strip())
        except:
            pass

        self.id = JointFileID(instance_id)

        self.sol_exist, self.sol_agree = self.set_sol_exists(instance_id) # should only need exist




    def set_sol_exists(self, instance_id):
        sat_solved = "Reject" != open("results/sat_sol/" + instance_id + ".out").readline().strip()
        clique_solved = "Reject" != open("results/clique_sol/" + instance_id + ".out").readline().strip()

        # print(instance_id, sat_solved, clique_solved)

        # assert sat_solved == clique_solved, "Error, solvers do not agree, or error parsing files!" # trying to find error
        return sat_solved, sat_solved == clique_solved





class JointFileID:

    # eg id= g_1-12-1_5_h_4-12-1_5_k_7
    def __init__(self, id):
        info = id.split("-")  # g_1, 12, 1_5_h_4, 12,  1_5_k_7

        self.m_g = int(info[0].split("_")[1])  # 1
        self.n_g = int(info[1])  # 12
        self.alpha_g, self.m_h = parse_f_c_i(info[2], "h")
        self.n_h = int(info[3])
        self.alpha_h, self.k = parse_f_c_i(info[4], "k")


    def __str__(self):
        return "g_{}-{}-{}_h_{}-{}-{}_k_{}".format(self.m_g, self.n_g, str(self.alpha_g).replace(".", "_"),
                                                   self.m_h, self.n_h, str(self.alpha_h).replace(".", "_"), self.k)

    def g_file(self):
        return "g_{}-{}-{}".format(self.m_g, self.n_g, str(self.alpha_g).replace(".", "_"))

    def h_file(self):
        return "h_{}-{}-{}".format(self.m_h, self.n_h, str(self.alpha_h).replace(".", "_"))

    def m_diff(self):
        return abs(self.m_g-self.m_h)

    def m_ave(self):
        return (self.m_g + self.m_h)/2

    def alpha_diff(self):
        return abs(self.alpha_g - self.alpha_h)

    def alpha_ave(self):
        return (self.alpha_g - self.alpha_h)/2


# fci - float, char int (works with my filename convention)
# like 1_5_h_4 -> 1.5, 4  (c = "h")
def parse_f_c_i(fci, c):
    mid_info = fci.split(c)  # 1_5_ , _4
    left_mid = mid_info[0].split("_")  # 1, 5

    f = float(left_mid[0]) + 0.1 * float(left_mid[1])  # 1.5
    i = int(mid_info[1].split("_")[1])  # 4
    return f, i



###                                     Other                                            ###

# def verify_sol(instance_id, sol_type):
#     if sol_type == "c" or "clique":
#         pass
#     elif sol_type == "s" or "sat":
#         pass
#     else:
#         raise "Invalid solution type, should be 'clique' ('c') or 'sat' ('s'). Was given {}".format(sol_type)

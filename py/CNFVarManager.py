from collections import namedtuple

CNFVar = namedtuple('CNFVar', ['graph_name', 'node_i', 'subgraph_i'])

class CNFVarManager:
    '''
    Used to keep track of the numbers which represent variables
    '''
    def __init__(self, g, h, k):

        self.vars = [None] # index 0 is reserved, varibles begin at 1
        self.n_g = len(g) # nodes in g
        self.n_h = len(h) # nodes in h
        self.k = k

        for i in range(k):
            for j in range(self.n_g):
                self.vars.append(CNFVar('g', j, i))
        for i in range(k):
            for j in range(self.n_h):
                self.vars.append(CNFVar('h', j, i))

        assert len(self.vars) == self.k * (self.n_g + self.n_h) + 1,\
            "something wrong with initializing varibles"


    # get the number of the varible
    def var_index(self, graph_name, node_i, subgraph_i):
        # node_i, subgraph_i are 0 indexed, the variable indexes are 1 indexed
        if graph_name is "g":
            return subgraph_i*self.n_g + node_i + 1
        elif graph_name is "h":
            return self.k*self.n_g + subgraph_i*self.n_h + node_i + 1
        else:
            raise "I dont know that graph name " + str(graph_name)


    # run test to make sure indexing works right
    def test_indexing(self):
        for i in range(self.k):
            for j in range(self.n_g):
                ind = self.var_index('g', j, i)
                # print('g', j, i, ind)
                assert self.vars[ind] == CNFVar('g', j, i)
            for j in range(self.n_h):
                # print('g', j, i)
                assert self.vars[self.var_index('h', j, i)] == CNFVar('h', j, i)


    # returns number of varibles
    def n_vars(self):
        return len(self.vars) - 1 # index 0 not a var


    def write_to_file(self, f_name):
        with open(f_name, "w") as f:
            print(self.n_g, self.n_h, self.k, file=f)
            for v in self.vars:
                if v is not None:
                    print(v[0], v[1], v[2], file=f)



def load_manger(f_name):
    mnger = CNFVarManager([], [], 0)
    with open(f_name) as f:
        l = f.readline().split()
        mnger.n_g, mnger.n_h, mnger.k = int(l[0]), int(l[1]), int(l[2])
        mnger.vars = [None]
        for line in f.readlines():
            l = line.split()
            mnger.vars.append(CNFVar(l[0], int(l[1]), int(l[2])))


    mnger.write_to_file(f_name +".testcopy")
    return mnger


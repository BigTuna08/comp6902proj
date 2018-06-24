from collections import namedtuple

CNFVar = namedtuple('CNFVar', ['graph_name', 'node_i', 'subgraph_i'])

class CNFVarManager:
    '''

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

        # print(self.vars)

        assert len(self.vars) == self.k * (self.n_g + self.n_h) + 1,\
            "something wrong with initializing varibles"


    def var_index(self, graph_name, node_i, subgraph_i):
        # node_i, subgraph_i are 0 indexed, the variable indexes are 1 indexed
        if graph_name is "g":
            return subgraph_i*self.n_g + node_i + 1
        elif graph_name is "h":
            return self.k*self.n_g + subgraph_i*self.n_h + node_i + 1
        else:
            raise "I dont know that graph name " + str(graph_name)


    def test_indexing(self):
        for i in range(self.k):
            for j in range(self.n_g):
                ind = self.var_index('g', j, i)
                # print('g', j, i, ind)
                assert self.vars[ind] == CNFVar('g', j, i)
            for j in range(self.n_h):
                # print('g', j, i)
                assert self.vars[self.var_index('h', j, i)] == CNFVar('h', j, i)

    def n_vars(self):
        return len(self.vars) - 1 # index 0 not a var
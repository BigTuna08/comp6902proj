from tool_box import JointFileID, print_adj_m, SolveData
import os, sys


# assumes n_g = n_h
# If clique and SAT solver disagree (should never happen), will throw error on __init__
class TimeResultManager:
    def __init__(self):
        n_values = set()
        m_g_values = set()
        m_h_values = set()
        alpha_g_values = set()
        alpha_h_values = set()
        m_values_ave = set()
        m_values_diff = set()
        alpha_values_ave = set()
        alpha_values_diff = set()
        k_vaules = set()

       
        time_folder = "results/clique_times/"  # get all ids
        directory = os.fsencode(time_folder)

        time_results = []

        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith(".out"):
                
                id = filename[:-4]

                sol_data = SolveData(id)
                time_results.append(sol_data)

                n_values.add(sol_data.id.n_g)
                n_values.add(sol_data.id.n_h)
                m_g_values.add(sol_data.id.m_g)
                m_h_values.add(sol_data.id.m_h)
                alpha_g_values.add(sol_data.id.alpha_g)
                alpha_h_values.add(sol_data.id.alpha_h)
                m_values_ave.add(sol_data.id.m_ave())  # use average m
                m_values_diff.add(sol_data.id.m_diff())
                alpha_values_ave.add((sol_data.id.alpha_g + sol_data.id.alpha_h) / 2)
                alpha_values_diff.add(abs(sol_data.id.alpha_g - sol_data.id.alpha_h))
                k_vaules.add(sol_data.id.k)


        self.result_list = time_results


        self.n_values = list(n_values)
        self.n_values.sort()
        self.m_g_values = list(m_g_values)
        self.m_g_values.sort()
        self.m_h_values = list(m_h_values)
        self.m_h_values.sort()
        self.alpha_g_values = list(alpha_g_values)
        self.alpha_g_values.sort()
        self.alpha_h_values = list(alpha_h_values)
        self.alpha_h_values.sort()
        self.m_values_ave = list(m_values_ave)
        self.m_values_ave.sort()
        self.m_values_diff = list(m_values_diff)
        self.m_values_diff.sort()
        self.alpha_values_ave = list(alpha_values_ave)
        self.alpha_values_ave.sort()
        self.alpha_values_diff = list(alpha_values_diff)
        self.alpha_values_diff.sort()
        self.k_values = list(k_vaules)
        self.k_values.sort()



    def get_all_data(self, v1, v2):

        n1 = self.get_n_values(v1)  # number of values for varible 1
        n2 = self.get_n_values(v2)  # number of values for varible 2

        # all n1 rows by n2 cols
        res_matirx_clique_all = [[0] * n2 for _ in range(n1)]  # average times of clique solver on all instances
        res_matirx_sat_all = [[0] * n2 for _ in range(n1)]   # average times of sat solver on all instances
        res_matirx_clique_solved = [[0] * n2 for _ in range(n1)]   # average times of clique solver on solvable instances
        res_matirx_sat_solved = [[0] * n2 for _ in range(n1)]   # average times of sat solver on solvable instances
        res_matirx_clique_unsolved = [[0] * n2 for _ in range(n1)]   # average times of clique solver on unsolvable instances
        res_matirx_sat_unsolved = [[0] * n2 for _ in range(n1)]   # average times of sat solver on unsolvable instances
        res_matirx_solved = [[0] * n2 for _ in range(n1)]  #  proportion of instances solvable

        n_res = [[0] * n2 for _ in range(n1)]


        for res in self.result_list:
            i1 = self.get_ind(v1, res)
            i2 = self.get_ind(v2, res)

            res_matirx_clique_all[i1][i2] += res.clique_time
            res_matirx_sat_all[i1][i2] += res.sat_time
            n_res[i1][i2] += 1

            if res.sol_exist:
                res_matirx_clique_solved[i1][i2] += res.clique_time
                res_matirx_sat_solved[i1][i2] += res.sat_time
                res_matirx_solved[i1][i2] += 1
            else:
                res_matirx_clique_unsolved[i1][i2] += res.clique_time
                res_matirx_sat_unsolved[i1][i2] += res.sat_time


        for i in range(len(res_matirx_clique_all)):
            for j in range(len(res_matirx_clique_all[0])):

                if res_matirx_solved[i][j] > 0:  # at least one solved
                    res_matirx_clique_solved[i][j] /= res_matirx_solved[i][j]  # average
                    res_matirx_sat_solved[i][j] /= res_matirx_solved[i][j]  # average

                if (n_res[i][j]  - res_matirx_solved[i][j]) > 0: # at least one unsolved
                    res_matirx_clique_unsolved[i][j] /= (n_res[i][j] - res_matirx_solved[i][j])  # average
                    res_matirx_sat_unsolved[i][j] /= (n_res[i][j] - res_matirx_solved[i][j])  # average

                if  n_res[i][j] > 0: # at least one in this category
                    res_matirx_clique_all[i][j] /= n_res[i][j]  #average
                    res_matirx_sat_all[i][j] /= n_res[i][j]  # average

                    res_matirx_solved[i][j] /= n_res[i][j] # proportion solved


        results = {}  # dictionary with array of results for each solver (solver name is key)
        results["clique-all"] = res_matirx_clique_all
        results["sat-all"] = res_matirx_sat_all
        results["clique-solved"] = res_matirx_clique_solved
        results["sat-solved"] = res_matirx_sat_solved
        results["clique-un"] = res_matirx_clique_unsolved
        results["sat-un"] = res_matirx_sat_unsolved
        results["solved"] = res_matirx_solved


        return results
        
        
    
    def get_n_values(self, var):
        if var == "n":
            return len(self.n_values)
        elif var == "m_g":
            return len(self.m_g_values)
        elif var == "m_h":
            return len(self.m_h_values)
        elif var == "alpha_g":
            return len(self.alpha_g_values)
        elif var == "alpha_h":
            return len(self.alpha_h_values)
        elif var == "m_a":
            return len(self.m_values_ave)
        elif var == "m_d":
            return len(self.m_values_diff)
        elif var == "alpha_a":
            return len(self.alpha_values_ave)
        elif var == "alpha_d":
            return len(self.alpha_values_diff)
        elif var == "k":
            return len(self.k_values)
        raise "Invalid var- {}".format(var)
    


    def get_ind(self, var, info):
        if var == "n":
            n1 = info.id.n_g
            return self.n_values.index(n1)
        elif var == "m_g":
            n1 = info.id.m_g
            return self.m_g_values.index(n1)
        elif var == "m_h":
            n1 = info.id.m_h
            return self.m_h_values.index(n1)
        elif var == "alpha_g":
            n1 = info.id.alpha_g
            return self.alpha_g_values.index(n1)
        elif var == "alpha_h":
            n1 = info.id.alpha_h
            return self.alpha_h_values.index(n1)
        elif var == "m_a":
            n1 = info.id.m_ave()
            return self.m_values_ave.index(n1)
        elif var == "m_d":
            n1 = info.id.m_diff()
            return self.m_values_diff.index(n1)
        elif var == "alpha_a":
            n1 = info.id.alpha_ave()
            return self.alpha_values_ave.index(n1)
        elif var == "alpha_d":
            n1 = info.id.alpha_diff()
            return self.alpha_values_diff.index(n1)
        elif var == "k":
            n1 = info.id.k
            return self.k_values.index(n1)

        raise "Invalid var- {}".format(var)



    def get_seperate_1_var_time_compare(self, v1):
        solvers = ["clique", "sat"]
        two_v = self.get_seperate_2_var_time_compare(v1, v1)
        results = {}

        for solver in solvers:
            r = two_v.get(solver)
            one_v = [r[i][i] for i in range(len(r))]
            results[solver] = one_v

        return results


    def get_seperate_2_var_time_compare(self, v1, v2):
        results = {}  # dictionary with array of results for each solver (solver name is key)

        n1 = self.get_n_values(v1)
        n2 = self.get_n_values(v2)

        res_matirx_clique = [[0] * n2 for _ in range(n1)]  #n1 rows by n2 cols
        res_matirx_sat = [[0] * n2 for _ in range(n1)]  # n1 rows by n2 cols
        n_res = [[0] * n2 for _ in range(n1)]


        for res in self.result_list:
            i1 = self.get_ind(v1, res)
            i2 = self.get_ind(v2, res)

            res_matirx_clique[i1][i2] += res.clique_time
            res_matirx_sat[i1][i2] += res.sat_time
            n_res[i1][i2] += 1

        # print()
        # print_adj_m(res_matirx_clique)
        # print()
        # print_adj_m(n_res)


        for i in range(len(res_matirx_clique)):
            for j in range(len(res_matirx_clique[0])):
                if  n_res[i][j] > 0:
                    res_matirx_clique[i][j] /= n_res[i][j]  #average
                    res_matirx_sat[i][j] /= n_res[i][j]  # average

        results["clique"] = res_matirx_clique
        results["sat"] = res_matirx_sat

        return results



    def get_1_var_solve_compare(self, v1):
        two_v = self.get_2_var_solve_compare(v1, v1)
        return [two_v[i][i] for i in range(len(two_v))]



    def get_2_var_solve_compare(self, v1, v2):

        n1 = self.get_n_values(v1)
        n2 = self.get_n_values(v2)

        res_matirx = [[0] * n2 for _ in range(n1)]  # n1 rows by n2 cols
        n_res = [[0] * n2 for _ in range(n1)]

        for res in self.result_list:
            i1 = self.get_ind(v1, res)
            i2 = self.get_ind(v2, res)

            if res.sol_exist:
                res_matirx[i1][i2] += 1
            n_res[i1][i2] += 1

        for i in range(len(res_matirx)):
            for j in range(len(res_matirx[0])):
                if n_res[i][j] > 0:
                    res_matirx[i][j] /= n_res[i][j]  # % solved

        return res_matirx



    def check_for_invalids(self):
        n_inval = 0
        n = len(self.result_list)
        n_solved = 0
        n_not = 0
        inval_and_sovled = 0
        inval_and_no_sol = 0
        print("invalid list:")
        for res in self.result_list:
            if not res.sol_agree:
                print(res.id)
                n_inval += 1
            if res.sol_exist:
                n_solved += 1
            else:
                n_not += 1
            if res.sol_exist and not res.sol_agree:
                inval_and_sovled +=1
            if not res.sol_exist and not res.sol_agree:
                inval_and_no_sol +=1

        print("total invalid", n_inval, "out of total ", n)
        print("n_solved", n_solved, "not solved", n_not)
        print("n invalid and sol exists: ", inval_and_sovled, "(sat solved, clique did not)")
        print("n invalid and no sol exists: ", inval_and_no_sol, "(sat did not solve, clique did)")




def print_res_matrix(m):
    if type(m[0]) is float:  # not matrix, just row
        print_res_row(m)
    else:
        for row in m:
            print_res_row(row)


def print_res_row(row):
    for item in row:
        print("{:0.4f}".format(item), end="\t")
    print()




if __name__ == '__main__':
    if len(sys.argv) > 2:
        trm = TimeResultManager()

        res = trm.get_all_data(sys.argv[1], sys.argv[2])

        print("clique result- all")
        print_res_matrix(res.get("clique-all"))
        print("\nclique result- solved")
        print_res_matrix(res.get("clique-solved"))
        print("\nclique result- unsolved")
        print_res_matrix(res.get("clique-un"))


        if res.get("sat-all") is not None:
            print("\nsat result- all")
            print_res_matrix(res.get("sat-all"))
            print("\nsat result- solved")
            print_res_matrix(res.get("sat-solved"))
            print("\nsat result- unsolved")
            print_res_matrix(res.get("sat-un"))


        print("\nProportion solved")
        print_res_matrix(res.get("solved"))



    else:
        print('Requires args\n'
              '1) varible 1 to compare: n, m_a, m_d, alpha_a, alpha_d or k\n'
              '2) varible 2 (optional) same choices as above')




# trm = TimeResultManager()
#
# if len(sys.argv) == 2:
#     time_res = trm.get_seperate_1_var_time_compare(sys.argv[1])
#     solved_res = trm.get_1_var_solve_compare(sys.argv[1])
# else: # 2 var
#     time_res = trm.get_seperate_2_var_time_compare(sys.argv[1], sys.argv[2])
#     solved_res = trm.get_2_var_solve_compare(sys.argv[1], sys.argv[2])
#
#
# print("clique result with", sys.argv[1:])
# print_res_matrix(time_res.get("clique"))
# r = time_res.get("sat")
# if r is not None:
#     print("\nsat result with", sys.argv[1:])
#     print_res_matrix(r)
#
# print("\ncorrect result with", sys.argv[1:])
# print_res_matrix(solved_res)




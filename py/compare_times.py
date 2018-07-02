from tool_box import JointFileID, print_adj_m, SolveData
import os, sys


# assumes n_g = n_h
class TimeResultManager:
    def __init__(self):
        results = {}  # dictionary with array of results for each solver (solver name is key)

        n_values = set()
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
                m_values_ave.add(sol_data.id.m_ave()) # use average m
                m_values_diff.add(sol_data.id.m_diff())
                alpha_values_ave.add((sol_data.id.alpha_g+sol_data.id.alpha_h)/2)
                alpha_values_diff.add(abs(sol_data.id.alpha_g - sol_data.id.alpha_h))
                k_vaules.add(sol_data.id.k)



        self.result_list = time_results

        self.n_values = list(n_values)
        self.n_values.sort()
        self.m_values_ave = list(m_values_ave)
        self.m_values_ave.sort()
        self.m_values_diff = list(m_values_diff)
        self.m_values_diff.sort()
        self.alpha_values_ave = list(alpha_values_ave)
        self.alpha_values_ave.sort()
        # print("\n\n\nave alpha,", alpha_values_ave, "\n\n")
        self.alpha_values_diff = list(alpha_values_diff)
        self.alpha_values_diff.sort()
        # print("\n\n\nave alpha,", alpha_values_ave, "\n\n")
        self.k_values = list(k_vaules)
        self.k_values.sort()
        
        
    
    def get_n_values(self, var):
        if var == "n":
            return len(self.n_values)
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
            print("\n\nr was", r, "\n\none v", one_v, "\n\n")
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

        results["clique"] = res_matirx_clique
        results["sat"] = res_matirx_sat

        return results



    def get_seperate_1_var_solve_compare(self, v1):
        solvers = ["clique", "sat"]
        two_v = self.get_seperate_2_var_time_compare(v1, v1)
        results = {}

        for solver in solvers:
            r = two_v.get(solver)
            one_v = [r[i][i] for i in range(len(r))]
            print("\n\nr was", r, "\n\none v", one_v, "\n\n")
            results[solver] = one_v

        return results


    def get_seperate_2_var_solve_compare(self, v1, v2):

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



    def print_invalids(self):
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

        if len(sys.argv) == 3:
            if sys.argv[1] == "t":
                res = trm.get_seperate_1_var_time_compare(sys.argv[2])
            elif sys.argv[1] == "s":
                res = trm.get_seperate_1_var_solve_compare(sys.argv[2])
            else:
                raise "Invalid args {}".format(sys.argv)
        else: # 2 var
            if sys.argv[1] == "t":
                res = trm.get_seperate_2_var_time_compare(sys.argv[2], sys.argv[3])
            elif sys.argv[1] == "s":
                res = trm.get_seperate_2_var_solve_compare(sys.argv[2], sys.argv[3])
            else:
                raise "Invalid args {}".format(sys.argv)

        print("clique result with", sys.argv[1:])
        print_res_matrix(res.get("clique"))
        r = res.get("sat")
        if r is not None:
            print("sat result with", sys.argv[1:])
            print_res_matrix(r)

    else:
        print('Requires args 1) t/s (time or correct)\n'
              '2) varible 1 to compare: n, m_a, m_d, alpha_a, alpha_d or k\n'
              '3) varible 2 (optional) same choices as above')





# print("Sat\n")
# print_adj_m(res.get("sat"))

# print("\n\nSat\n")
# print_adj_m(res.get("clique"))





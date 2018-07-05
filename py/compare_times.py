import sys
from ResultsManager import ResultsManager


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
        trm = ResultsManager()

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




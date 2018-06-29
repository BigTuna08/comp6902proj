import graph_tools as gt
import CliqueManager as cm

f= "g_1-7-0_5_h_2-7-0_5_k_4"


s = gt.sol_from_file(f,"c")
print("sol is :\n", s, "\n")

print("valid? :\n", s.is_valid(f), "\n")

# cm.ind_man_test()
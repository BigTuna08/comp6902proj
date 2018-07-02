from graph_generator import make_graph
from reduce_to_clique import reduce_to_clique

# Good settings

# m_values = [1,2,3,4,5,6]
# alpha_values = [0.5, 1.0, 1.5, 2.0] # 0.0?
# n_values = [8,9,10,11]  # bigger than 7 aviods heuristic solving in clique solver
# k_values = [6,7,8,9]


m_values = [1,2,3,]
alpha_values = [0.5, 1.0, 1.5,2.0] # 0.0?
n_values = [10,12,14,16,18]  # bigger than 7 aviods heuristic solving in clique solver
k_values = [7, 10, 13]

if __name__ == '__main__':
    created_ids = []
    for n in n_values:
        for m in m_values:
            for alpha in alpha_values:
                id = str(m) + "-" + str(n) + "-" + str(alpha).replace(".", "_")
                make_graph(m, m, n, alpha, "g_" + id)
                make_graph(m, m, n, alpha, "h_" + id)
                created_ids.append(id)


    for g_id in created_ids:
        for h_id in created_ids:
            parts = g_id.split("-")
            n_g = int(parts[1])
            parts = h_id.split("-")
            n_h = int(parts[1])
            if n_g != n_h:  #only do for same n
                continue
            for k in k_values:
                if k > n_g or k > n_h:
                    continue
                joint_id = "g_" + g_id + "_h_" + h_id + "_k_" + str(k)
                reduce_to_clique("g_" + g_id, "h_" + h_id, k, joint_id)




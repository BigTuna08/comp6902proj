from graph_generator import make_graph
from reduce_to_clique import reduce_to_clique




# m_values = [1,2,3,4,5,6]
# alpha_values = [0.5, 1.0, 1.5,2.0] #
# n_values = [10,12,14,16,18]  #
# k_values = [8, 10, 12, 14, 16]

m_values = [1,2,3,4]
alpha_values = [i*.1 for i in range(5,16)] # 0.5, 0.6, ... 1.5
n_values = [14,15,16,17,18]
k_values = [12,13,14,15,16]


if __name__ == '__main__':
    created_ids = []
    for n in n_values:
        for m in m_values:
            for alpha in alpha_values:
                id = str(m) + "-" + str(n) + "-" + str(alpha).replace(".", "_")
                make_graph(m, m, n, alpha, "g_" + id)
                make_graph(m, m, n, alpha, "h_" + id)
                created_ids.append(id)


    for g_id in created_ids:  # create 2 graphs (g & h) for each combination of (n,alpha,m)
        for h_id in created_ids:
            parts = g_id.split("-")
            n_g = int(parts[1])
            parts = h_id.split("-")
            n_h = int(parts[1])
            if n_g != n_h:  #only do for same n
                continue
            for k in k_values:     # create an instance with each k value
                if k > n_g or k > n_h:
                    continue
                joint_id = "g_" + g_id + "_h_" + h_id + "_k_" + str(k)
                reduce_to_clique("g_" + g_id, "h_" + h_id, k, joint_id)




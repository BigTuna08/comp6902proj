from graph_generator import make_graph
from reduce_to_sat import reduce_to_sat
from reduce_to_clique import reduce_to_clique
from tool_box import format_alpha


m_values = [1,2,3,4]
alpha_values = [0.5, 1.0, 1.5]
n_values = [6,7,8,9,10]
#k_values = [5,6,7,8,9]


if __name__ == '__main__':
    created_ids = []
    for n in n_values:   # create 2 graphs (g & h) for each combination of (n,alpha,m)
        for m in m_values:
            for alpha in alpha_values:
                id = str(m) + "-" + str(n) + "-" + format_alpha(alpha)
                make_graph(m, m, n, alpha, "g_" + id)
                make_graph(m, m, n, alpha, "h_" + id)
                created_ids.append(id)


    for g_id in created_ids:     # pair every g with each h (if same size)
        for h_id in created_ids:
            parts = g_id.split("-")
            n_g = int(parts[1])
            parts = h_id.split("-")
            n_h = int(parts[1])
            if n_g != n_h:  # only do for same n
                continue
            for k in range(n_g-5,n_g-1):         # create an instance with each k value
                if k > n_g or k > n_h:
                    continue
                joint_id = "g_" + g_id + "_h_" + h_id + "_k_" + str(k)
                reduce_to_sat("g_" + g_id, "h_" + h_id, k, joint_id)
                reduce_to_clique("g_" + g_id, "h_" + h_id, k, joint_id)




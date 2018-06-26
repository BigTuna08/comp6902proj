from graph_generator import make_graph
from reduce_to_sat import reduce_to_sat


m_values = [1,2,4]
alpha_values = [0.5, 2.0]
n_values = [15]
k_values = [5, 13]


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
            for k in k_values:
                joint_id = "g_" + g_id + "_h_" + h_id
                reduce_to_sat("g_" + g_id, "h_" + h_id, k, joint_id)


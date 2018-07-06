from os import mkdir

# Create directory structure 
if __name__ == '__main__':
	mkdir('sat_solvers')
	mkdir('clique_solver')
    mkdir('archive_data')

	mkdir('cnf')
	mkdir('cnf/assignments')
	mkdir('cnf/recover')

	mkdir('graphs')
	mkdir('graphs/edge_list')

	mkdir('cliques')
	mkdir('cliques/results')

	mkdir('results')
	mkdir('results/sat_sol')
	mkdir('results/clique_sol')
	mkdir('results/clique_times')
	mkdir('results/sat_times')

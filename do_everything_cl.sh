#!/bin/sh

python3 py/clique_only_runner.py
wait
./scripts/solve_all_cliques.sh
wait
python3 py/recover_from_clique.py cliques/results
wait
echo Done

#!/bin/sh

python3 py/runner.py
wait
./scripts/solve_all_cliques.sh
wait
./scripts/solve_all_sats.sh
wait
python3 py/recover_from_assignment.py cnf/assignments
wait
echo Done

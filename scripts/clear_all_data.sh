#!/bin/sh

echo "Warning! About to erase all data files!!!"
echo "Press enter to continue, or kill this script to abort"

read ignore

rm -r cnf
mkdir cnf
mkdir cnf/assignments
mkdir cnf/recover

rm -r graphs
mkdir graphs
mkdir graphs/edge_list

rm -r cliques
mkdir cliques
mkdir cliques/results

rm -r results
mkdir results
mkdir results/sat_sol
mkdir results/clique_sol
mkdir results/clique_times
mkdir results/sat_times


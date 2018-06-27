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
mkdir graphs/sat_sol
mkdir graphs/edge_list
mkdir graphs/clique_sol

rm -r cliques
mkdir cliques
mkdir cliques/results


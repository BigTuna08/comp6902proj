#!/bin/sh

if [ "$#" -ne 1 ]; 
then
    echo "Illegal number of parameters"
else
    cat py/runner.py > runinfo.txt
    cat py/clique_only_runner.py > clique_runner_info.txt
    wait
    out_file="archive_data/$1.zip"
    zip -r $out_file graphs results cnf cliques runinfo.txt clique_runner_info.txt
    wait
    echo "Saved to $out_file"
    rm runinfo.txt
    rm clique_runner_info.txt
fi




#!/bin/sh

cd cliques
ls *.mtx | sed -e 's/\.mtx$//' > ../_f_names
cd ..

for f_name in $(cat _f_names)
do
    input_file="cliques/$f_name.mtx"
    out_file="cliques/results/$f_name.out"
    echo "Running solver on $input_file"
    ./clique_solver/fmc_package_v1.1/src/fmc -p $input_file > $out_file
    rm $input_file
done

rm _f_names



#!/bin/sh

cd cnf
ls *.cnf | sed -e 's/\.cnf$//' > ../_f_names
cd ..

for f_name in $(cat _f_names)
do
    input_file="cnf/$f_name.cnf"
    out_file="cnf/assignments/$f_name.out"
    echo "Running solver on $input_file"
    ./sat_solvers/syrup/bin/glucose-syrup -nthreads=4 -model -maxmemory=50000 -verb=0 $input_file > $out_file
    #rm $input_file
done

rm _f_names



#!/bin/sh

cd cliques
ls *.mtx | sed -e 's/\.mtx$//' > ../_f_names
cd ..

for f_name in $(cat _f_names)
do
    input_file="cliques/$f_name.mtx"
    out_file="cliques/results/$f_name.out"
    echo $f_name > _temp_f_name  # used to get k with cut
    k=$(cut -d "_" -f8 _temp_f_name)
    #echo "k is $k"
    rm _temp_f_name
    echo "Running solver on $input_file"
    #echo "f_name is $f_name"
    #./clique_solver/fmc_package_v1.1/src/fmc -p $input_file > $out_file
    ./clique_solver/pmc-master/pmc -a 0 -h 0 -f $input_file -k $k > $out_file
    #rm $input_file
done

rm _f_names



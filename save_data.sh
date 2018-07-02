#!/bin/sh

if [ "$#" -ne 1 ]; 
then
    echo "Illegal number of parameters"
else
    cat py/runner.py > runinfo.txt
    wait
    out_file="archive_data/$1.zip"
    zip -r $out_file graphs results runinfo.txt
    wait
    echo "Saved to $out_file"
    rm runinfo.txt
fi




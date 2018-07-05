#!/bin/sh

if [ "$#" -ne 1 ]; 
then
    echo "Illegal number of parameters"
else
    cat py/runner.py > runinfo.txt
    wait
    zip_file="archive_data/$1.zip"
    unzip $zip_file 
    wait
    echo "Extracted $out_file"
    rm runinfo.txt
fi




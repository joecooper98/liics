#!/bin/bash

# will convert .xyz file given as command line input to a .json file you should copy straight into your input file

geometry_file=$1

output_file=output.json

rm -f $output_file

for i in $(seq 3 `wc -l $geometry_file | cut -d ' ' -f1`)
do
    atom_type=`head -n $i $geometry_file| tail -n1 | awk '{print $1}'`
    xyz1=`head -n $i  $geometry_file | tail -n1 | awk '{print $2}'`
    xyz2=`head -n $i  $geometry_file | tail -n1 | awk '{print $3}'`
    xyz3=`head -n $i  $geometry_file | tail -n1 | awk '{print $4}'`
    echo "{ \"atom\"  : \"${atom_type}\" , \"xyz\"  : [ ${xyz1} , ${xyz2} , ${xyz3} ]}," >> $output_file
done

sed -i '$ s/.$//' $output_file

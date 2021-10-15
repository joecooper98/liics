#1/bin/bash
# Code to run pt2 calculations after a succesful casscf liic in bagel
# Just place the pt2.json file (standard input using a reference given
# in the liic_$i directory. Then grep the outputs
 

cwd=`pwd`

input_directory="${cwd}/input"

input_file=pt2.json

continuation_ref=cas.ref

no_of_points=`ls -d ${cwd}/CALCULATIONS/ | wc -l | cut -d ' ' -f1`

for i in $(seq 0 `echo "$no_of_points - 1" | bc`)
do
	cd ${cwd}/CALCULATIONS/liic_$i
	cp ${input_directory}/${input_file} pt2.json 
	nohup bagel pt2.json > pt2.out 
done

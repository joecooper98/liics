#1/bin/bash
# code to run liics in bagel. this makes use of bagel's ability to restart
# calculations from reference files. as this code was written at 3am, i just
# want it to work, and so the user must provide two files - a sample input
# for the calculation, and the referencee it must be restarted from. THe 
# script will create a directory for each pathway geometry, and then copy 
# the ref file into the first point. It will then create a bagel input from
# a sample calculation (i.e. can be whatever calculation you want), and run
# the calculation, again saving the reference. It then copies that reference
# into a new directory, recreates the input file, runs the calculation, etc.

# The bagel.json file should hava a line called "pointer" in the geometry 
# section. Also should load the reference as prev.ref, and save the ref as
# cas.ref

sourcebagel

cwd=`pwd`

input_directory="${cwd}/input"

input_file=bagel.json

input_ref=start.ref

pathway_directory="${cwd}/liic"

pathway_name=pathway

no_of_points=`ls ${pathway_directory} | wc -l | cut -d ' ' -f1`

mkdir $cwd/CALCULATIONS

cp ${input_directory}/$input_ref rolling.ref.archive


for i in $(seq 0 2 100)
#for i in $(seq 0 `echo "$no_of_points - 1" | bc`)
#for i in $(seq $nopm1 -1 0) # for reverse
do
	mkdir ${cwd}/CALCULATIONS/liic_$i
	cd ${cwd}/CALCULATIONS/liic_$i
	cp ${input_directory}/${input_file} .
	cp ${cwd}/rolling.ref.archive prev.ref.archive
	geo_iter="${pathway_name}_$i.xyz"
	cp ${pathway_directory}/${geo_iter} .
	cp ~/SCRIPTS/json_converter.sh .
	./json_converter.sh $geo_iter
	rm json_converter.sh
	sed -i -e '/pointer/r output.json' $input_file
	sed -i '/pointer/d' $input_file
	nohup bagel bagel.json > out.out 2> nohup.err
	cp cas.ref.archive ${cwd}/rolling.ref.archive
done
echo "liic done in `pwd`"

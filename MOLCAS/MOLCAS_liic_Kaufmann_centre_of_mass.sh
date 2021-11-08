#!/bin/bash

#Please define the input to a molcas calculation.
#Use the lumorb keyword to restart the orbitals propagated across the LIIC, which you will input into the calcution
#MOLCAS should load the 'geom' xyz file.

# To perform this calculation using Kaufmann functions, one should formulate the molcas script to perform these calulations automatically
# This would require first inputting the geometry, finding the centre of charge (using a quick scf calculation).
# Then, centre a zero charge 'X' atom at that centre of charge with your Rydberg/Kaufmann functions on it.
# Run the proper RASSCF calculation from there.

# add a ion_input_file, which performs a ion calculation using the geometry given. We then grep 'Center of charge' to find the centre of charge, and then append it on the X section (which is the Kaufmann section)
# Then we put the normal coordinates in, and move from there.


cwd=`pwd`

input_directory="${cwd}/input"

input_file=molcas.input

ion_input_file=ion.input

input_JobIph=start.JobIph

pathway_directory="${cwd}/liic"

pathway_name=pathway

JobIph_name=old.JobIph

mkdir $cwd/CALCULATIONS

JobIph_rolling="rolling_${JobIph_name}"

cp ${input_directory}/${input_JobIph} ${cwd}/${JobIph_rolling}

for i in $(seq 100 -2 0)
do
	mkdir ${cwd}/CALCULATIONS/liic_$i
	cd ${cwd}/CALCULATIONS/liic_$i
	cp ${input_directory}/${input_file} molcas.input
	geo_iter="${pathway_name}_$i.xyz"
	cp ${pathway_directory}/${geo_iter} geom
    cp ${cwd}/${JobIph_rolling} $JobIph_name
    rm -f JOBOLD
    ln -s $JobIph_name JOBOLD
    x_loc=`$input_directory/centre_of_mass.py geom`
    sed -i "s/X.*\/Angstrom/X $x_loc \/Angstrom/g" molcas.input	
    for j in $(seq 1 $((`wc -l geom | cut -d ' ' -f1`-2)) )
    do
            atom=`head -n$((j+2)) geom | tail -n1 | awk '{print $1}'`
            loc=`head -n$((j+2)) geom | tail -n1 | awk '{print "    ",$2,"    ",$3, "    ",$4, "    "}'`
            sed -i "s/$atom$j.*\/Angstrom/$atom$j $loc \/Angstrom/g" molcas.input
    done
	nohup pymolcas -f -b 1 $input_file 1>nohup.inp 2>nohup.err
    cp molcas.JobIph ${cwd}/${JobIph_rolling}
done

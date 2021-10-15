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

input_rasorb=start.RasOrb

pathway_directory="${cwd}/liic"

pathway_name=pathway

rasorb_name=old.RasOrb

mkdir $cwd/CALCULATIONS

rasorb_rolling="rolling_${rasorb_name}"

cp ${input_directory}/${input_rasorb} ${cwd}/${rasorb_rolling}

for i in $(seq 0 5 100)
do
	mkdir ${cwd}/CALCULATIONS/liic_$i
	cd ${cwd}/CALCULATIONS/liic_$i
	cp ${input_directory}/${input_file} molcas.input
	cp ${input_directory}/${ion_input_file} ion.input
	geo_iter="${pathway_name}_$i.xyz"
	cp ${pathway_directory}/${geo_iter} geom
    cp ${cwd}/${rasorb_rolling} $rasorb_name
    rm -f INPORB
    ln -s $rasorb_name INPORB
    nohup pymolcas -f -b1 $ion_input_file 1>nohup.out 2>nohup.err
    x_loc=`grep -A1 'Center of Charge' ion.log | tail -n1 | awk '{print "    ",$2, "    ",  $4, "    ", $6, "    "}'`
    sed -i "s/X.*\/Angstrom/X $x_loc \/Angstrom/g" molcas.input	
    for j in $(seq 1 $((`wc -l geom | cut -d ' ' -f1`-2)) )
    do
            atom=`head -n$((j+2)) geom | tail -n1 | awk '{print $1}'`
            loc=`head -n$((j+2)) geom | tail -n1 | awk '{print "    ",$2,"    ",$3, "    ",$4, "    "}'`
            sed -i "s/$atom$j.*\/Angstrom/$atom$j $loc \/Angstrom/g" molcas.input
    done
	nohup pymolcas -f -b 1 $input_file 1>nohup.inp 2>nohup.err
    cp molcas.RasOrb ${cwd}/${rasorb_rolling}
done

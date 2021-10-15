#!/bin/bash

#Please define the input to a pt2 calculation as pt2.input
# this will create a folder called pt2, and then cd into it, link the old RasOrb file and the old casscf file.
# this is as you need to calculate the scf wavefunction before calculating the pt2, but as you have the wavefunction, this should be pretty quick

# this should work with either the Kaufmann or the normal liic script.


cwd=`pwd`

input_directory="${cwd}/input"

pt2_input_file=pt2.input

for i in $(seq 0 2 100)
do
	cd ${cwd}/CALCULATIONS/liic_$i
    mkdir pt2 
    cd pt2
	cp ${input_directory}/${pt2_input_file} pt2.sec
	cp ../geom .
    rm -f INPORB
    ln -s ../molcas.RasOrb INPORB
    cat ../molcas.input pt2.sec > pt2.input
    nohup pymolcas -f -b1 pt2.input 1>nohup.out 2>nohup.err
done

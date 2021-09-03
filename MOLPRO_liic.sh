#!/bin/bash

#please define the .wfu directory as $WFU
#please setup a molpro calculation with the correct basis/active space/calculation 
#please change the FILE line in molpro example input file with " FILELINETOCHANGE "
#please change the geometry spectification with " GEOMETRYLINETOCHANGE "


cwd=`pwd`

WFU=/data/scratch/joe/wfu

input_directory="${cwd}/input"

input_file=molpro.inp

input_wfu=start.wfu

pathway_directory="${cwd}/liic"

pathway_name=pathway

wfu_name=liic

no_of_points=`ls ${pathway_directory} | wc -l`

mkdir $cwd/CALCULATIONS

wfu_rolling="${wfu_name}_rolling.wfu"

cp ${input_directory}/${input_wfu} ${WFU}/${wfu_rolling}

nopm1=`echo "$no_of_points -1" | bc`

#for i in {0..15}
for i in $(seq 0 $nopm1)
#for i in $(seq $nopm1 -1 0) # for reverse
do
	mkdir ${cwd}/CALCULATIONS/liic_$i
	cd ${cwd}/CALCULATIONS/liic_$i
	cp ${input_directory}/${input_file} molpro.inp
	cp ${WFU}/${wfu_rolling} init$i.wfu
	sed -i "s/FILELINETOCHANGE/FILE,2,$wfu_rolling/g" molpro.inp
	geo_iter="${pathway_name}_$i.xyz"
	cp ${pathway_directory}/${geo_iter} .
	sed -i "s/GEOMETRYLINETOCHANGE/geometry = $geo_iter/g" molpro.inp
	nohup molpro molpro.inp 
	cp ${WFU}/${wfu_rolling} final$i.wfu
done

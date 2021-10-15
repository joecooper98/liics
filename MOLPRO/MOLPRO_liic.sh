#!/bin/bash

#please define the .wfu directory as $WFU
#please setup a molpro calculation with the correct basis/active space/calculation 
#please change the FILE line in molpro example input file with " FILELINETOCHANGE "
#please change the geometry spectification with " GEOMETRYLINETOCHANGE "


cwd=`pwd`

input_directory="${cwd}/input"

input_file=molpro.inp

input_wfu=start.wfu

pathway_directory="${cwd}/liic"

pathway_name=pathway

wfu_name=liic1.wfu

mkdir $cwd/CALCULATIONS

wfu_rolling="rolling_${wfu_name}"

cp ${input_directory}/${input_wfu} ${cwd}/${wfu_rolling}

for i in $(seq 64 -4 0)
do
	mkdir ${cwd}/CALCULATIONS/liic_$i
	cd ${cwd}/CALCULATIONS/liic_$i
	cp ${input_directory}/${input_file} molpro.inp
	cp ${cwd}/${wfu_rolling} ${wfu_name}
	sed -i "/file/c\FILE,2,${wfu_name}" molpro.inp
	geo_iter="${pathway_name}_$i.xyz"
	cp ${pathway_directory}/${geo_iter} geom
	nohup molpro -W `pwd` -I `pwd` -d `pwd` molpro.inp 2> nohup.err
	cp ${wfu_name} ${cwd}/${wfu_rolling}
done

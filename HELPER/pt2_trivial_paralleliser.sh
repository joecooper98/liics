#!/bin/bash

largest_geoms_number=100
sample_rate=2
number_of_parallel_procs=7


number_of_points=$((largest_geoms_number/sample_rate))
points_per_run=$((number_of_points/number_of_parallel_procs +1))


number_of_iterations=$((number_of_points/points_per_run)) 


for i in $(seq 0 $number_of_iterations)
do
        s=$(( i*sample_rate*points_per_run))
        f=$(( s + points_per_run*sample_rate -sample_rate ))
        if [[ $f -gt $largest_geoms_number ]]
        then
                f=$largest_geoms_number
        fi
        sed  "s/for.*/for i in {$s..$f..$sample_rate}/" MOLCAS_liic_pt2.sh
  #      ./MOLCAS_liic_pt2.sh &
done


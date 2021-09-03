#!/bin/bash

states=`grep 'nstate' liic_*/out.out | head -1 | awk '{print $5}'`
sp1=`echo "$states + 1" | bc`

for i in $(seq 0 100)
do
        grep -b${sp1} "ci vector, state   0" liic_${i}/out.out | head -n${states} | awk '{print $5}' > int
        sed -i ':a;N;$!ba;s/\n/ /g' int 
        cat int >> energies
done



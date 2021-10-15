#!/bin/bash

for i in $(seq 0 100)
do
        grep "MS-CASPT2 energy" liic_${i}/pt2.out | awk '{print $7}' > int
        sed -i ':a;N;$!ba;s/\n/ /g' int 
        cat int >> pt2energies
done



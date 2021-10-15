#!/bin/bash

for i in liic_? liic_?? liic_??? liic_????
do
egrep 'CASPT2 Root' $i/pt2/pt2.log | awk '{print $7}' | tr -d ' ' | sed 'a ,' | tr -d '\n' | sed 's/,/ /g' 1>> pt2energies 
echo "" >> pt2energies
done

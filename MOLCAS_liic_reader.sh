#!/bin/bash

for i in liic_? liic_?? liic_??? liic_????
do
egrep 'RASSCF.*Total energy' $i/molcas.log | awk '{print $8}' | tr -d ' ' | sed 'a ,' | tr -d '\n' | sed 's/,/ /g' 1>> energies 
echo "" >> energies
done

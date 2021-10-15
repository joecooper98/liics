#!/bin/bash

input_file=molpro.out

for i in liic_? liic_?? liic_??? liic_????
do
grep '!MCSCF' ${i}/molpro.out | grep 'Energy' | cut -c36- | tr -d ' ' | sed 'a ,' | tr -d '\n' | sed 's/,/ /g' 1>> energies 
echo "" >> energies
done

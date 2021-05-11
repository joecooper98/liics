#!/usr/bin/env python

#####################################################
# This script takes a input .xyz geometry and then  #
# runs a HF/6-31g calculation and then prints the   #
# scf energy to the file energyout.txt              #
#####################################################

from pyscf import gto, scf
import numpy as np
import sys


# getting geometry

filename=sys.argv[1]

fin = open(filename, "r")

intgeometry = []

for line in fin:
    intgeometry.append(line.split())

del intgeometry[0:2]



geom=[]



for i in range(len(intgeometry)):
    intdata=intgeometry[i]
    data=[intdata[0],(intdata[1],intdata[2],intdata[3])]
    geom.append(data)

# load molecule and basis
    
mol = gto.M(atom=geom, basis='6-31g')
mol.verbose = 0

# run RHF - changes to UHF if needed...

mf=scf.RHF(mol)

# write energy to new line of file energyout.txt

outfile=open("energyout.txt",'a')

e = mf.kernel()

outfile.write(str(e)+"\n")



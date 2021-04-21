#!/usr/bin/env python

from pyscf import gto, scf
import numpy as np
import timeit
import sys



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

mol = gto.M(atom=geom, basis='ccpvdz')
mol.verbose = 0

mf=scf.RHF(mol)

outfile=open("energyout.txt",'a')

e = mf.kernel()

outfile.write(str(e)+"\n")



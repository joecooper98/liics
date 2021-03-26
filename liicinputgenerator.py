#!/usr/bin/env python3

# For this code, you input a gzmat file, and then a list of integers 
#corresponding to the desired order for the gzmat, it will change them

# i.e.,if you put in 11,4,2,1, it will change the zmatrix specification of atom
# 11 to X 4 r11 2 a11 1 d11, and then change r11, a11, and d11. For use with 
# liic.py

# Please ensure that the atoms are in the same order, i.e. using the ZMAT 
# editor of molden

import os
import sys
import re
import numpy as np



def distance(v1,v2):
    summing=0
    for i in range(len(v1)):
        summing+=(v1[i]-v2[i])**2
    dis = np.sqrt(summing)
    return dis

def angle(v1,v2,v3):
    lenvec1 = distance(v1,v2)
    lenvec2 = distance(v2,v3)
    total = 0 
    for i in range(len(v1)):
        total += (v2[i]-v1[i])*(v2[i]-v3[i])
    ang = np.degrees(np.arccos(total/(lenvec1*lenvec2)))
    return ang

def dihedral(v1,v2,v3,v4):
    p0=np.array(v1)
    p1=np.array(v2)
    p2=np.array(v3)
    p3=np.array(v4)
    
    b0 = -1.0*(p1 - p0)
    b1 = p2 - p1
    b2 = p3 - p2

    # normalize b1 so that it does not influence magnitude of vector
    # rejections that come next
    b1 /= np.linalg.norm(b1)

    # vector rejections
    # v = projection of b0 onto plane perpendicular to b1
    #   = b0 minus component that aligns with b1
    # w = projection of b2 onto plane perpendicular to b1
    #   = b2 minus component that aligns with b1
    v = b0 - np.dot(b0, b1)*b1
    w = b2 - np.dot(b2, b1)*b1

    # angle between v and w in a plane is the torsion angle
    # v and w may not be normalized but that's fine since tan is y/x
    x = np.dot(v, w)
    y = np.dot(np.cross(b1, v), w)
    ang = np.degrees(np.arctan2(y, x))
    if ang < 0:
        ang=ang+360
    return ang
    




filename = input("What .xyz file is to be changed?\n")
# filename="QC.xyz"
input_data = open(filename,"r")



init_geom = []
for line in input_data:
    sline=line.strip('\n')
    chunks=re.split(' +',sline)
    del chunks[0]
    for i in range(len(chunks)):
        chunks[i]=float(chunks[i].strip("'"))
    init_geom.append(chunks)
    
    
del init_geom[0:2]

copyfilename = input("Which file would you like to be copied? GZMAT form, can be handmade, needs 5 blank lines at top if so\n")
# copyfilename="NB.gzmat"
copy_file = open(copyfilename,"r")

copydata=[]
for line in copy_file:
    sline=line.strip('\n')
    chunks=re.split(' +',sline)
    copydata.append(chunks)
    
del copydata[0:5]

if copydata.index(['Variables:']) != len(init_geom):
    print("Different sized files!")
    sys.exit()



endfile = open("endfile","w")

endfile.write("\n\n\n\n0  1\n")
for i in range(copydata.index(['Variables:'])):
    for j in range(len(copydata[i])):
        if j < len(copydata[i])-1:
            endfile.write(copydata[i][j])
            endfile.write("  ")
        else:
            endfile.write(copydata[i][j])
    endfile.write("\n")
endfile.write('Variables:\n')

for i in range(len(init_geom)-1):
    if i == 0:
        endfile.write("r2= ")
        endfile.write(str(round(distance(init_geom[i+1],init_geom[int(copydata[i+1][1])-1]),4)))
        endfile.write("\n")
    elif i == 1:
        endfile.write("r3= ")
        endfile.write(str(round(distance(init_geom[i+1],init_geom[int(copydata[i+1][1])-1]),4)))
        endfile.write("\n")
        endfile.write("a3= ")
        endfile.write(str(round(angle(init_geom[i+1],init_geom[int(copydata[i+1][1])-1],init_geom[int(copydata[i+1][3])-1]),4)))
        endfile.write("\n")
    else:
        endfile.write("r"+str(i+2)+"= ")
        endfile.write(str(round(distance(init_geom[i+1],init_geom[int(copydata[i+1][1])-1]),4)))
        endfile.write("\n")
        endfile.write("a"+str(i+2)+"= ")
        endfile.write(str(round(angle(init_geom[i+1],init_geom[int(copydata[i+1][1])-1],init_geom[int(copydata[i+1][3])-1]),4)))
        endfile.write("\n")
        endfile.write("d"+str(i+2)+"= ")
        endfile.write(str(round(dihedral(init_geom[i+1],init_geom[int(copydata[i+1][1])-1],init_geom[int(copydata[i+1][3])-1],init_geom[int(copydata[i+1][5])-1]),4)))
        endfile.write("\n")





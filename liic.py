#!/usr/bin/env python
################################
#
# Hi there. This converts two gzmat files into a liic pathway of .xyz files (also gzmat files).
# You need to create to gzmat files (using obabel please), and then check that their definitions of internal coordinates are the same - i.e. they are the same Z-matrix (use vimdiff e.g.)
# If not, then change manually (e.g. using molden to measure bond lengths/angles). The first thing you should do is ensure that the initial files have the same ordering of atoms
# Also ensure that the periodicity of your angles is maintained (i.e., if the first geometry has a dihedral angle of 357 and the second of 3, then change the first to -3 or the second to 363.
#

import os
import sys

startfile = input("What is the starting geometry file? (GZMAT form from obabel please)\n") # start file initiation
start_file = open(startfile, "r") # input file

start_geom = [] # init a blank array for start file - this section gets the data
for line in start_file:
    line=line.strip('\n')
    start_geom.append(line) # gets data

endfile = input("What is the end geometry file? (GZMAT form from obabel please)\n")
end_file = open(endfile, "r") # same as above but for the end

end_geom = []
for line in end_file:
    line=line.strip('\n')
    end_geom.append(line)

pathwayname = input("What do you want the pathway files to be called?\n") # the name of the intermediate files

this_is_crap_but_it_works = [] # retrieve all variable names by splitting the lines. The bits after the line with "Variables:" are the variable names
for i in range(len(start_geom)):
    split=start_geom[i].split(" ")
    this_is_crap_but_it_works.append(split[0])


no_of_points = int(input("How many intermediate geometries would you like?\n")) #how many intermediate points. total path length will be this + 2

if end_geom.index("Variables:") != start_geom.index("Variables:"): # warning if molecules have different sizes
    print("Different sized molecules!")
    sys.exit()

for i in range(5,end_geom.index('Variables:')): # warning if molecules have different zmatrix definitions
    if end_geom[i] != start_geom[i]:
        print("Different internal coordinates!")
        sys.exit()

geoms = [] # init blank list for all the variables. will be an array of arrays for variables at each intermediate pathway point.
for i in range(no_of_points):
    geoms.append([]) # add a blank list to the list
    for j in range(end_geom.index('Variables:')+1,len(end_geom)): # only iterate over the variable section of the file
        difference=float(end_geom[j].split()[-1])-float(start_geom[j].split()[-1]) # find the difference between the start and end points variables
        increment = difference / (no_of_points+1) # create the increment, which is simply the difference divided by the number of points
        ithgeom = []
        ithgeom.append(float(start_geom[j].split()[-1])+increment*(i+1)) # add the increment onto the variables, and add the variables to the blank list at its index inside the list of geometries
        geoms[i].append(ithgeom)


for j in range(no_of_points):
    name=pathwayname+"_"+str(j+1); # create variable names
    f = open(name, "w") # open files with those names
    for i in range(len(start_geom)):
        if i <= start_geom.index("Variables:"): # copy start geom file up to the word Variables
            f.write(start_geom[i])
            f.write("\n")
        elif i < len(start_geom)-1: # write the variable name, then a space, then the variable (without []), and then a new line.
            f.write(this_is_crap_but_it_works[i]+" "+str(geoms[j][i-start_geom.index("Variables:")-1]).strip("[]")+"\n")
        else:
            f.write("\n") # end with new line
    f.close() #close file
    os.system("obabel -igzmat "+name+" -oxyz > "+name+".xyz") # convert files back into .xyz files

os.system("obabel -igzmat "+startfile+" -oxyz > "+pathwayname+"_0.xyz") # make start file an .xyz
os.system("obabel -igzmat "+startfile+" -oxyz > "+pathwayname+"_"+str(no_of_points+1)+".xyz") # make start file an .xyz

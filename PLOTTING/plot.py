#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import sys
import os.path

filename=sys.argv[-1]

plt.style.use("standard")

mults=[]
labels=[]

print("What should the title be?")
title = input("> ")

if len(sys.argv[:]) > 2:
    for i in range(int((len(sys.argv[:])-2)/2)):
        mults.append(int(sys.argv[i+1]))
        labels.append(str(sys.argv[int(0.5*len(sys.argv[:])+i)]))
else:
        mults.append(0)

def mult(x):
    if len(sys.argv[:])<3:
        return ['solid', "State", 0]
    elif x < mults[0]:
        return ['solid',labels[0],  0]
    elif x < sum(mults[0:2]):
        return ['dotted',labels[1],  sum(mults[0:1])-1]
    elif x < sum(mults[0:3]):
        return ['dashed',labels[2], sum(mults[0:2]) -1]
    elif x < sum(mults[0:4]):
        return ['dashdot',labels[3],sum(mults[0:3]) -1]
    elif x < sum(mults[0:5]):
        return [(0,(1,10)),labels[4],sum(mults[0:4])-1]
    elif x < sum(mults[0:6]):
        return [(0,(5,5)),labels[5], sum(mults[0:5])-1]

data=np.genfromtxt(filename)

if os.path.isfile('distances'):
    a=np.genfromtxt('distances')[0]
    x=np.genfromtxt('distances')[1:]
    if a == 0:
        print("Using non-mass-weighted distances from file 'distances'")
        lab='Distance / $\AA$'
    elif a == 1:
        print("Using square-root mass-weighted distances from file 'distances'")
        lab='Distance / $\AA$ amu$^{\frac{1}{2}}$'
    elif a == 2:
        print("Using mass-weighted distances from file 'distances'")
        lab='Distance / $\AA$ amu'
else:
    x=np.arange(np.shape(data)[0])
    lab='Pathway'
    print("Using standard indices for coordinate. Use LIIC_DISTANCE.py for distances")


if data[0,1] > -10:
    print("Looks like this is excitation energy based data! I will normalise the ground state, and then plot the excited states!")
    data[:,0] -= data[0,0]
    data[:,0] *= 27.2114
    for i in range(np.size(data)[1]-1):
        data[:,i+1] += data[:,0]
else:
    print("Looks like this is absolute energy based data! I will normalise all the data, and plot all at once")
    data -= data[0,0]
    data *= 27.2114

if data[0,-1] - data[0,0] > 10 :
    print("This looks like it could be data for multiple multiplicities. You can use the syntax './plot.py N_1 N_2 N_3.. S_1 S_2 S_3 inputdata', where N_n is the number of states of Multiplicity n (labelled by the string S_n)!")

if os.path.isfile('distances'):
    a=np.genfromtxt('distances')[0]
    x=np.genfromtxt('distances')[1:]
    if a == 0:
        print("Using non-mass-weighted distances from file 'distances'")
        lab='Distance / $\AA$'
    elif a == 1:
        print("Using square-root mass-weighted distances from file 'distances'")
        lab='Distance / $\AA$ amu$^{\frac{1}{2}}$'
    elif a == 2:
        print("Using mass-weighted distances from file 'distances'")
        lab='Distance / $\AA$ amu'
else:
    x=np.arange(np.shape(data)[0])
    lab='Pathway'
    print("Using standard indices for coordinate. Use LIIC_DISTANCE.py for distances")


fig, ax = plt.subplots(figsize=(5,5))

for i in range(np.shape(data)[1]):
    ax.plot(x, data[:,i], linestyle = mult(i)[0], label=mult(i)[1]+str(i - mult(i)[2] ))

ax.set_ylabel("Energy / eV")
ax.set_xlabel(lab)
ax.legend(ncol=4, loc="upper right",prop={'size': 8})
ax.set_xlim([0,x[-1]])
ax.set_title(title)
plt.savefig(filename+".png",dpi=1000)
plt.show()

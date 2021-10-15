#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import sys
import os.path

filename=sys.argv[-2]
filename2=sys.argv[-1]

plt.style.use("standard")

mults=[]
labels=[]

if len(sys.argv[:]) > 3:
    for i in range(int((len(sys.argv[:])-3)/2)):
        mults.append(int(sys.argv[i+1]))
        labels.append(str(sys.argv[int(0.5*len(sys.argv[:])+i)]))
else:
        mults.append(0)

def mult(x):
    if len(sys.argv[:])<4:
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
print("What should the title be?")

title = input("> ")

print("Label for first method?")

mlabel_1 = input("> ")

print("Label for second method?")

mlabel_2 = input("> ")

data=np.genfromtxt(filename)
data_2=np.genfromtxt(filename2)

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


if data_2[0,1] > -10:
    print("Looks like this is excitation energy based data! I will normalise the ground state, and then plot the excited states!")
    data_2[:,0] -= data_2[0,0]
    data_2[:,0] *= 27.2114
    for i in range(np.size(data_2)[1]-1):
        data_2[:,i+1] += data_2[:,0]
else:
    print("Looks like this is absolute energy based data! I will normalise all the data, and plot all at once")
    data_2 -= data_2[0,0]
    data_2 *= 27.2114



if os.path.isfile('distances') and os.path.isfile('distances2'):
    a=np.genfromtxt('distances')[0]
    x=np.genfromtxt('distances')[1:]
    a2=np.genfromtxt('distances2')[0]
    x2=np.genfromtxt('distances2')[1:]
    if a != a2:
        print("The distances must be the same type! e.g. use mass-weighted distance for both! I will use standard indices.")
        x=np.arange(np.shape(data)[0])
        lab='Pathway'
    elif a == 0:
        print("Using non-mass-weighted distances from file 'distances' and 'distances2'")
        lab='Distance / $\AA$'
    elif a == 1:
        print("Using square-root mass-weighted distances from file 'distances' and 'distances2'")
        lab='Distance / $\AA$ amu$^{\frac{1}{2}}$'
    elif a == 2:
        print("Using mass-weighted distances from file 'distances' and 'distances2'")
        lab='Distance / $\AA$ amu'
elif os.path.isfile('distances'):
    a=np.genfromtxt('distances')[0]
    x=np.genfromtxt('distances')[1:]
    x2=x
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
    x2=x
    lab='Pathway'
    print("Using standard indices for coordinate. Use LIIC_DISTANCE.py for distances")


fig, ax = plt.subplots(figsize=(5,5))

for i in range(np.shape(data)[1]):
    ax.plot(x, data[:,i], linestyle = mult(i)[0], label=mlabel_1+mult(i)[1]+str(i - mult(i)[2] ), color='#332288')

for i in range(np.shape(data_2)[1]):
    ax.plot(x2, data_2[:,i], linestyle = mult(i)[0], label=mlabel_2+mult(i)[1]+str(i - mult(i)[2] ), color='#88ccee')

ax.set_ylabel("Energy / eV")
ax.set_xlabel(lab)
ax.legend(ncol=4, loc="upper right",prop={'size': 8})
ax.set_xlim([0,max(x[-1],x2[-1])])
ax.set_title(title)
plt.savefig(filename+".png",dpi=1000)
plt.show()

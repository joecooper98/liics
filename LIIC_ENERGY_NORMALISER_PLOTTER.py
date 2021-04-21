#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt

data=np.genfromtxt("energyout.txt")

norm = data[0]

plotdata=np.zeros_like(data)

for i in range(len(data)):
    plotdata[i]=(data[i]-norm)*27.2114

print(plotdata)

fig, ax = plt.subplots()

ax.plot(np.arange(len(data)), plotdata)
ax.set_ylabel("Energy / eV")
ax.set_xlabel("Pathway")
ax.set_xticks([0,len(data)],["",""])
plt.show()

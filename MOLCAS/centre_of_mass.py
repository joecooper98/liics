#!/usr/bin/env python3

import numpy as np
import sys




U_TO_AMU = 1.            # conversion from g/mol to amu


# This table stolen from SHARC
# Atomic Weights of the most common isotopes
# From https://chemistry.sciences.ncsu.edu/msf/pdf/IsotopicMass_NaturalAbundance.pdf
MASSES = {'x' : 0.,
          'h' :   1.007825 * U_TO_AMU,
          'he':   4.002603 * U_TO_AMU,
          'li':   7.016004 * U_TO_AMU,
          'be':   9.012182 * U_TO_AMU,
          'b' :  11.009305 * U_TO_AMU,
          'c' :  12.000000 * U_TO_AMU,
          'n' :  14.003074 * U_TO_AMU,
          'o' :  15.994915 * U_TO_AMU,
          'f' :  18.998403 * U_TO_AMU,
          'ne':  19.992440 * U_TO_AMU,
          'na':  22.989770 * U_TO_AMU,
          'mg':  23.985042 * U_TO_AMU,
          'al':  26.981538 * U_TO_AMU,
          'si':  27.976927 * U_TO_AMU,
          'p' :  30.973762 * U_TO_AMU,
          's' :  31.972071 * U_TO_AMU,
          'cl':  34.968853 * U_TO_AMU,
          'ar':  39.962383 * U_TO_AMU,
          'k' :  38.963707 * U_TO_AMU,
          'ca':  39.962591 * U_TO_AMU,
          'sc':  44.955910 * U_TO_AMU,
          'ti':  47.947947 * U_TO_AMU,
          'v' :  50.943964 * U_TO_AMU,
          'cr':  51.940512 * U_TO_AMU,
          'mn':  54.938050 * U_TO_AMU,
          'fe':  55.934942 * U_TO_AMU,
          'co':  58.933200 * U_TO_AMU,
          'ni':  57.935348 * U_TO_AMU,
          'cu':  62.929601 * U_TO_AMU,
          'zn':  63.929147 * U_TO_AMU,
          'ga':  68.925581 * U_TO_AMU,
          'ge':  73.921178 * U_TO_AMU,
          'as':  74.921596 * U_TO_AMU,
          'se':  79.916522 * U_TO_AMU,
          'br':  78.918338 * U_TO_AMU,
          'kr':  83.911507 * U_TO_AMU,
          'rb':  84.911789 * U_TO_AMU,
          'sr':  87.905614 * U_TO_AMU,
          'y' :  88.905848 * U_TO_AMU,
          'zr':  89.904704 * U_TO_AMU,
          'nb':  92.906378 * U_TO_AMU,
          'mo':  97.905408 * U_TO_AMU,
          'tc':  98.907216 * U_TO_AMU,
          'ru': 101.904350 * U_TO_AMU,
          'rh': 102.905504 * U_TO_AMU,
          'pd': 105.903483 * U_TO_AMU,
          'ag': 106.905093 * U_TO_AMU,
          'cd': 113.903358 * U_TO_AMU,
          'in': 114.903878 * U_TO_AMU,
          'sn': 119.902197 * U_TO_AMU,
          'sb': 120.903818 * U_TO_AMU,
          'te': 129.906223 * U_TO_AMU,
          'i' : 126.904468 * U_TO_AMU,
          'xe': 131.904154 * U_TO_AMU,
          'cs': 132.905447 * U_TO_AMU,
          'ba': 137.905241 * U_TO_AMU,
          'la': 138.906348 * U_TO_AMU,
          'ce': 139.905435 * U_TO_AMU,
          'pr': 140.907648 * U_TO_AMU,
          'nd': 141.907719 * U_TO_AMU,
          'pm': 144.912744 * U_TO_AMU,
          'sm': 151.919729 * U_TO_AMU,
          'eu': 152.921227 * U_TO_AMU,
          'gd': 157.924101 * U_TO_AMU,
          'tb': 158.925343 * U_TO_AMU,
          'dy': 163.929171 * U_TO_AMU,
          'ho': 164.930319 * U_TO_AMU,
          'er': 165.930290 * U_TO_AMU,
          'tm': 168.934211 * U_TO_AMU,
          'yb': 173.938858 * U_TO_AMU,
          'lu': 174.940768 * U_TO_AMU,
          'hf': 179.946549 * U_TO_AMU,
          'ta': 180.947996 * U_TO_AMU,
          'w' : 183.950933 * U_TO_AMU,
          're': 186.955751 * U_TO_AMU,
          'os': 191.961479 * U_TO_AMU,
          'ir': 192.962924 * U_TO_AMU,
          'pt': 194.964774 * U_TO_AMU,
          'au': 196.966552 * U_TO_AMU,
          'hg': 201.970626 * U_TO_AMU,
          'tl': 204.974412 * U_TO_AMU,
          'pb': 207.976636 * U_TO_AMU,
          'bi': 208.980383 * U_TO_AMU,
          'po': 208.982416 * U_TO_AMU,
          'at': 209.987131 * U_TO_AMU,
          'rn': 222.017570 * U_TO_AMU,
          'fr': 223.019731 * U_TO_AMU,
          'ra': 226.025403 * U_TO_AMU,
          'ac': 227.027747 * U_TO_AMU,
          'th': 232.038050 * U_TO_AMU,
          'pa': 231.035879 * U_TO_AMU,
          'u' : 238.050783 * U_TO_AMU,
          'np': 237.048167 * U_TO_AMU,
          'pu': 244.064198 * U_TO_AMU,
          'am': 243.061373 * U_TO_AMU,
          'cm': 247.070347 * U_TO_AMU,
          'bk': 247.070299 * U_TO_AMU,
          'cf': 251.079580 * U_TO_AMU,
          'es': 252.082972 * U_TO_AMU,
          'fm': 257.095099 * U_TO_AMU,
          'md': 258.098425 * U_TO_AMU,
          'no': 259.101024 * U_TO_AMU,
          'lr': 262.109692 * U_TO_AMU,
          'rf': 267. * U_TO_AMU,
          'db': 268. * U_TO_AMU,
          'sg': 269. * U_TO_AMU,
          'bh': 270. * U_TO_AMU,
          'hs': 270. * U_TO_AMU,
          'mt': 278. * U_TO_AMU,
          'ds': 281. * U_TO_AMU,
          'rg': 282. * U_TO_AMU,
          'cn': 285. * U_TO_AMU,
          'nh': 286. * U_TO_AMU,
          'fl': 289. * U_TO_AMU,
          'mc': 290. * U_TO_AMU,
          'lv': 293. * U_TO_AMU,
          'ts': 294. * U_TO_AMU,
          'og': 294. * U_TO_AMU
}

with open(sys.argv[-1]) as f:
    mol1=f.readlines()

massindex = np.array([MASSES[mol1[x].split()[0].lower()] for x in range(len(mol1)) if x > 1])
masstot = sum(massindex)

f.close()

mol0 = np.genfromtxt(sys.argv[-1], skip_header=2, usecols=(1,2,3))

massscaled=massindex@mol0/masstot

print(massscaled[0],'   ',massscaled[1], '   ',massscaled[2])























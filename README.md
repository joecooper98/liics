# LIICS

These are the files needed to create and run linear interpolations in internal coordinates.

Broadly, it can be split into three sections

1) Creation
2) Calculation
3) Plotting

and the overall workflow is thus:

1) Perform initial calculations to get geometries, wavefunctions, etc.
2) Generate `pathway*.xyz` files using the creation suite, detailed in section 1
3) Create a new directory to calculate the LIIC in
4) Transfer the wavefunctions into a directory called `input`,
5) Put the `pathway*.xyz` files into the directory called `liic`
6) Run the `XXX_liic.sh` script, where `XXX` is the program to be used.

-----

## 1 - Creation

Everything needed here is in the `CREATION` directory.

You must first find two geometries in `.xyz` format to interpolate between - these are to be calculated by electronic structure packages.

The input requires a gaussian z-matrix file, which can be created from obabel using a command like

```
obabel -ixyz input.xyz -ogzmat > output.gzmat
```

By creating two of these files, we can linearly interpolate between the two geometries.

The files **MUST** have the same ordering of atoms, and the same definition of the internal coordinates - if not, the interpolation will produce nonsense.

Therefore create one gzmat file, and then then run 

```
./liicinputgenerator.py
```

which will lead you through the generation of a gzmat file using the same definitions of internal coordinates for a different geometry.

This file will be called `output.gzmat`.

Then run 

```
./liic.py
```
which should create a list of output files in `.xyz` and `.gzmat` format.

I recommend using the name pathway, which allows the directory to be cleaned using

```
rm pathway_? pathway_?? pathway_???
```

Before you move on, visualise the coordinate by using a command like

```
cat pathway_? pathway_?? pathway_??? > liic.xyz ; vmd liic.xyz
```

and check that the pathway is chemically viable (i.e. no nuclei passing through eachother).

If not, then try a different zmat form. If obabel does not produce correct definitions of coordinates, one should produce one manually (by editing the obabel generated one). 

Once you have done that, run  

```
./liicinputgenerator.py
```

on both input geometries, creating two `output.gzmat` files to use (make sure to change the name of `output.gzmat` inbetween the runs to avoid overwriting)

A recent update has fixed a phase issue with dihedrals, but this can cause some issues - visualise the results and check the interpolation looks correct.

Visualisation of the geometries can be easily accomplished with (using vmd as an example)
```
cat pathway_?.xyz pathway_??.xyz pathway_???.xyz > total.xyz ; vmd total.xyz
```

Sometimes you can see a large spinning of one of the dihedral angles. A quick way to check this is to see if the dihedral angles in the gzmat files (i.e. the dN values) for the two files are close to eachother. The code is written to minimise these errors (check this...), but they can still happen, especially if the motion is large.

The 2 `LIIC_ENERGY...` python scripts just run a simple set of HF calculations using pyscf in order to quickly check the pathway for viability - feel free to use or not. A good pathway should not have a large hump in the middle.

There is also the `LIIC_DISTANCE.py` script, which will perform a distance calculation. If one runs 
```
./LIIC_DISTANCE.py 0 pathway_?.xyz pathway_??.xyz pathway_???.xyz > distances
```
the file `distances` will contain a list of distances. If one changes `0` to `1`, the distances will be weighted by the square root of the masses of the nucleus, and `2` will weight them by the masses of the nuclei.

The file name `distances` can be used in the plotting scripts `plot.py` and `plotcomp.py` later.

## 2 - Calculation

There are currently scripts to run *MOLPRO*, *BAGEL* and *MOLCAS* calculations. The scripts for *TURBOMOLE* also exist, but need some work.

The general structure of these scripts is the same - it will generate a filesystem like this.

```
parent_directory  - liic          # you provide these using the previous sections
                    - pathway_0.xyz
                    - pathway_1.xyz
                    - ...
                  - input         # you provide these, which contain the details of the calculations you want to perform
                    - input files
                    - input wavefunctions
                  - CALCULATIONS  # these will be generated, and contain the inputs and results
                    - liic_0
                      - calculation inputs and results for geometry in pathway_0.xyz
                    - liic_1
                      - calculation inputs and results for geometry in pathway_1.xyz
```



The input does generally have to be slightly altered to perform the calculations:

### MOLPRO

`input` should contain  
- an input file, normally called `molpro.inp`
  - This should contain all the details for calculations to be performed, should have a `file` line, and a `geometry=geom` line
- an input wavefunction with the name `start.wfu`

### MOLCAS

`input` should contain  
- an input file, normally called `molcas.input`
  - for Kaufmann functions, you should use the `MOLCAS..` script, and define the ..
                        - an input wavefunction with the name `start.RasOrb`

### BAGEL

`input` should contain  - an input file, normally called `molcas.input`
                        - an input wavefunction with the name `start.wfu`
                        

If one wants to calculate CASPT2 afterwards, one can use the `*pt2*` scripts. These use a input file in `input` called `pt2.inp`, `pt2.json`, or `pt2.input` for MOLPRO, BAGEL and MOLCAS respectively. These do not normally require an input wavefunction, and they run in the original `CALCULATIONS` directory.

Afterwards, the scripts MOLPRO_liic_reader.sh and BAGEL_liic_reader.sh will read the liics and output as a space separated energy file, which can be plotted with

```
./plot.py energies
```
.

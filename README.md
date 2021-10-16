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
## Theory

Interpolating in cartesian coordinates can often lead to nonsense coordinates. Bonds drastically shortening and lengthening, atoms moving through other atoms, etc. A simple way to get around this is to simply interpolate in a set of internal coordinates.

In essence, we are putting in our knowledge of chemical systems. Bonds do lengthen and shorten in chemical dynamics, but not not much. Atoms don't generally move through eachother, etc.

In chemical theory, we always want to check that our electronic structure methods give reasonable results for the critical points of our system - minima, crossing points, transition states - but we also want to check that the regions in between these regions are described well.

These linear interpolations provide pseudo-reaction pathways to follow, and check the potential energy descriptions of the systems we are calculating.


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

----
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

Run using the script `MOLPRO_liic.sh`, and can be read using `MOLPRO_liic_`

`input` should contain  
- An input file, normally called `molpro.inp`
  - This should contain all the details for calculations to be performed, should have a `file,2,liic.wfu` line, and a `geometry=geom` line
  - This file will be the main input file, and will be altered to use the correct geometry and wavefunction
  - The calculation will be performed locally, so all of the permanent files are in the calculation directory
- *Optional*An input wavefunction with the name `start.wfu`
  - This should be a good initial wavefunction for the first geometry to be calculated - this is crucial for CASSCF.
  - This will be copied and propagated across the LIIC. The intermediate file will be in the parent directory and called `rolling.wfu`
- *Optional* a CASPT2/MRCI input file, normally called `pt2.inp`
  - This should contain all the details for a CASPT2/MRCI calculation, and will load the wavefunction from the wavefunction of the CASSCF calculation

#### PT2

If one wants to perform CASPT2 after the LIIC is finished, one can use the `MOLPRO_LIIC_pt2.sh` script. This will copy a new file into the `CALCULATIONS/liic_X` trajectory, and then run a CASPT2 calculation from the wavefunction of the CASSCF calculation.

This is generally preferable over performing CASPT2 in the CASSCF calculation, as only a converged CASSCF calculation is needed to propagate the wavefunctions, not a full CASPT2 one. This allows the 'trivial parallelisation' of the calculation with a simple altering of the script, or a downsampling of the LIIC by only performing a few calculations.

### MOLCAS

`input` should contain  
- An input file, normally called `molcas.input`
  - The `RASSCF` section should have the `lumorb` keyword to load the old orbitals.
  - If Kaufmann functions are not required, then one should define the geometry/basis in `GATEWAY`, defining the geometry from the file `geom`.
  - for Kaufmann functions, you should use the `MOLCAS_liic_Kaufmann.sh` script, and define the basis set as seen in the example. This will perform an cation calculation using a file called `ion.input`, and centre the Kaufmann functions on a dummy atom `X` the centre of charge.
- *Optional* An input wavefunction with the name `start.RasOrb`
  - This should be a good initial wavefunction for the start geometry - this is crucial for CASSCF.
- *Optional* A CASPT2 input fule, normally called `pt2.input` 
  - This should contain all of the details for the `&CASPT2` module in `MOLCAS` - it will be concatenated onto the original input file.

#### CASPT2

Similar to the way one can do this in `MOLPRO`, one can perform a CASPT2 calculation after the CASSCF calculation. The main points are:

- The file name should be `pt2.input` or similar
- The script will run the calculations in a `liic_X/pt2` subdirectory, to ensure the wavefunctions are kept for analysis
- The file will be concatenated with the initial calculation to rerun the CASSCF. This is slower than in MOLPRO or BAGEL, but I am unaware of any workaround. This shouldn't be a huge slowdown, as the wavefunction should be already converged (and will be loaded from the `molcas.RasOrb` file of the old calculation.

### BAGEL

`input` should contain  
- an input file, normally called `bagel.json`
  - This should have the loading of the basis set, the `"angstrom" : true` keyphrase, and no geometry defined, just the word `pointer` (the script will look for this, and this will be fixed soon...)
  - The file should load a reference file called `prev.ref.archive` (or similar, making sure to use the `"continue_geom" : false` keyphrase) and save to one called `cas.ref.archive`
  - It is preferable to print the orbitals to a molden file for analysis of the wavefunction over the coordinate
- *Optional* An input wavefunction with the name `start.ref`
  - This should be a good initial wavefunction for the start geometry - this is crucial for CASSCF.
- *Optional* A CASPT2 input fule, normally called `pt2.json` 
  - This should load the wavefunction/geometries in `cas.ref.archive` - seem more details below or in the examples.
                        
#### CASPT2

Similar to the way one can do this in `MOLPRO`, one can perform a CASPT2 calculation after the CASSCF calculation. The main points are:

- The file name should be `pt2.json` or similar
- The file should load the `cas.ref.archive` file (one should use the default `"continue_geom" : true` keyphrase)
                        
### Other Codes

Other codes exist, and I eventually want to get around to writing something for all of the codes I use (TURBOMOLE, ORCA, GAUSSIAN, Q-CHEM).


## 3 - Plotting

After the calculation, we need to retrieve the energies of the individual calculations, and visualise them.

### Energy retrieval

For each interface, a script has been provided which will find and retrieve the energies from the calculations. It will generally put them into a file called `energies` as a space-separated variable file.

Each of the columns represents the nth adiabatic energy of the system, and each row respresents a geometry.

For all of the CASPT2 interfaces, a separate script is provided to retrieve the pt2 energies into the file `pt2energies`.

### Plotting

There are also plotting scripts `plot.py` and `plotcomp.py`, which use `numpy` and `matplotlib`. These allow quick visualisation and saving of the figures.

These are called by using 
```
./plot.py energies
```
If the file `distances` exists in the directory, the script will display the interpolation with the distance (either mass-weighted or not) on the x-axis.

If one has calculations of differing multiplicities, one can use (for 5 singlets (labelled 'S') and 4 triplets (labelled 'T'))
```
./plot.py 5 4 S T energies
```
This can of course be generalised to any number of multiplicities or symmetries.

If one wants to compare the energies of two differing methods by plotting on the same axes, one can use
```
./plotcomp.py energies1 energies2
```
If the files `distances` and `distances2` exists, each pathway will be plotted with each of the respective distances as the x axis. If only `distances` exists, it will plot both on the same distance x axis.



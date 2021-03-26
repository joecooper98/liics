These are the files needed to create linear interpolations in internal coordinates.

The input requires a gaussian z-matrix file, which can be created from obabel using a command like

$ obabel -ixyz input.xyz -ogzmat > output.gzmat

By creating two of these files, we can linearly interpolate between the two geometries.

The files MUST have the same ordering of atoms.

Before we linearly interpolate, we must first check that the definitions of 
the geometries are the same, using vimdiff for example.

If not, then run ./liicinputgenerator.py, which will lead you through the 
generation of a gzmat file using the same definitions of internal coordinates.

Then run ./liic.py, which should create a list of output files in .xyz and .gzmat format.

I recommend using the name pathway, which allows the directory to be cleaned using

$ rm pathway_? pathway_?? pathway_???

Before you move on, visualise the coordinate by using a command like

$ cat pathway_? pathway_?? pathway_??? > liic.xyz ; vmd liic.xyz

and check that the pathway is chemically viable (i.e. no nuclei passing through eachother).
If not, then try a different zmat form. This can be created manually, and then using 
./liicinputgenerator.py twice, we can create two .gzmat files to use.


A recent update has fixed a phase issue with dihedrals, but this can cause 
some issues - visualise the results and check the interpolation looks 
correct.



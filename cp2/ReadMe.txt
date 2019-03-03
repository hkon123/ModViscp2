Run im.exe for full functionality of recompile GoL.c

it can be run with multiple flags:
no flags runs a countour plot with dimensions 20x20 for 1000 sweeps

-b : sets dimension of countourplot to 50x50
-s : sets dimension of countourplot to 10x10
-l : sets the sweeps to 10000
-c : lets the user set a custoum dimension and number of sweeps
-i : runs the simulation with varying imunity fraction

output:
newFraction.txt
newVariance.txt

to display results use python script GoL.py

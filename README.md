# Formula 1 Automated Parametric Sweep Analysis

# Table of Contents
1. [Description](#Description)
2. [Getting Started](#Getting-Started)
3. [Help](#Help)


## Description

The CFD simulation was built in openFOAM with the goal of creating an automated parametric sweep analysis of the aerodynamics of a Formula 1 vehicle and then ranking the best performing model.

## Getting Started

### Installing

* Install openFOAM, if required can follow the guide on openFOAM website.
* Ensure Python3, matplotlib, and Numpy are installed on your linux system/sub-system.
* Install, and place this folder into your chooice of location within a Linux directory.

### Executing program

* Enter your linux terminal.
* CD into case directory.
* execute the parametric_sweep.py code.
```
python3 parametric_sweep.py
```
* Once it has finished running, you will then be output in the terminal ranking scores of each case, furthermore you can type "explorer.exe ." into the terminal and navigate through the cases and output graphs produced.
```
explorer.exe .
```

## Help
There are multiple further script files that you can utilise aswell.
  
* Runs the simulation in parallel, and produces output graphs.
```
python3 parametric_sweep.py
```
* Cleans the simulation directories of previous results.
```
Allclean_scipt.py
```
* CD into [x] case directory and type ./Allrun into terminal to run a single case.
```
./Allrun
```
* CD into [x] case directory and type ./Allclean into terminal to clean a single case.
```
./Allclean
```
* These are the following commands to enter if you would like to run the case file completely manually.
```
blockMesh
```
```
snappyHexMesh -overwrite
```
```
decomposePar
```
```
mpirun -np 6 simpleFoam -parallel
```
```
ReconstructPar
```
```
touch results.foam
```

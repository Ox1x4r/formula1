# Formula 1 Automated Parametric Sweep Analysis

An OpenFOAM CFD study that sweeps through several Formula 1 aerodynamic
configurations, runs each case in parallel, and ranks them by performance.

## Contents

- [Overview](#overview)
- [Cases](#cases)
- [Requirements](#requirements)
- [Installation](#installation)
- [Running the sweep](#running-the-sweep)
- [Running a single case](#running-a-single-case)
- [Running a case manually](#running-a-case-manually)
- [Cleaning up](#cleaning-up)
- [Repository layout](#repository-layout)

## Overview

The simulation is built in OpenFOAM and driven by a Python wrapper. Rather than
setting up and solving each geometry by hand, `parametric_sweep.py` meshes and
solves every case in the repository, plots the results, and prints a ranked
score for each configuration so the variants can be compared directly.

## Cases

Each case is a variation on the same base vehicle, isolating the contribution of
the front and rear wings:

| Directory  | Configuration                |
| ---------- | ---------------------------- |
| `fullF1`   | Full car, both wings fitted  |
| `noFWF1`   | Front wing removed           |
| `noRWF1`   | Rear wing removed            |
| `noFWRWF1` | Both wings removed           |

## Requirements

- Linux, or Windows with WSL
- OpenFOAM — see the [installation guide](https://openfoam.org/download/) on the
  OpenFOAM website
- Python 3, with NumPy and Matplotlib

Install the Python dependencies with:

```bash
pip3 install numpy matplotlib
```

## Installation

Clone the repository somewhere inside your Linux filesystem:

```bash
git clone https://github.com/Ox1x4r/formula1.git
cd formula1
```

Source your OpenFOAM environment before running anything, for example:

```bash
source /opt/openfoam*/etc/bashrc
```

## Running the sweep

From the repository root:

```bash
python3 parametric_sweep.py
```

The script meshes and solves each case in parallel, generates the output graphs,
and prints the ranking scores to the terminal when it finishes.

To browse the case folders and the graphs afterwards from WSL, open the current
directory in Windows Explorer:

```bash
explorer.exe .
```

On a native Linux desktop, use `xdg-open .` instead.

## Running a single case

Change into the case directory you want, then:

```bash
./Allrun
```

## Running a case manually

If you would rather drive a case step by step, run these in the case directory:

```bash
blockMesh
snappyHexMesh -overwrite
decomposePar
mpirun -np 6 simpleFoam -parallel
reconstructPar
touch results.foam
```

`results.foam` is an empty marker file that lets ParaView open the reconstructed
results. The `-np 6` argument must match `numberOfSubdomains` in the case's
`system/decomposeParDict`; change both together if you want a different core
count.

## Cleaning up

To clear previous results from every case:

```bash
python3 Allclean_script.py
```

To clear a single case, run this from inside that case directory:

```bash
./Allclean
```

## Repository layout

```
formula1/
├── fullF1/               # Full car
├── noFWF1/               # No front wing
├── noRWF1/               # No rear wing
├── noFWRWF1/             # No front or rear wing
├── parametric_sweep.py   # Runs every case, plots results, ranks them
├── Allclean_script.py    # Clears results from every case
└── README.md
```

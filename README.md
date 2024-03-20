may need to create postProcessing folder

blockMesh
snappyHexMesh
decomposePar
mpirun -np 6 simpleFoam -parallel
ReconstructPar
touch results.foam

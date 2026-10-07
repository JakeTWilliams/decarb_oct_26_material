#!/bin/bash -l
#SBATCH --account=<account_name>
#SBATCH --partition=cpu
#SBATCH --qos=default
#SBATCH --time=00:10:00
#SBATCH --nodes=1

module load GCC MPICH

mpirun -n 1 ./ideal_example
mpirun -n 2 ./ideal_example
mpirun -n 4 ./ideal_example
mpirun -n 8 ./ideal_example
mpirun -n 16 ./ideal_example
mpirun -n 32 ./ideal_example
mpirun -n 64 ./ideal_example

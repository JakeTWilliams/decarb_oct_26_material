#!/bin/bash -l
#SBATCH --account=<account_name>
#SBATCH --partition=cpu
#SBATCH --qos=default
#SBATCH --time=00:10:00
#SBATCH --nodes=1

module load GCC MPICH

mpicc -o non_ideal_example amdahl_non_ideal.c

mpirun -n 1 ./non_ideal_example
mpirun -n 2 ./non_ideal_example
mpirun -n 4 ./non_ideal_example
mpirun -n 8 ./non_ideal_example
mpirun -n 16 ./non_ideal_example
mpirun -n 32 ./non_ideal_example
mpirun -n 64 ./non_ideal_example

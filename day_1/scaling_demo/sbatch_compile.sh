#!/bin/bash -l
#SBATCH --account=<account_name>
#SBATCH --partition=cpu
#SBATCH --qos=default
#SBATCH --time=00:02:00
#SBATCH --nodes=1

module load GCC MPICH

mpicc -o ideal_example amdahl_ideal.c
mpicc -o non_ideal_example amdahl_non_ideal.c

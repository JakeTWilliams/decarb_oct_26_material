#!/bin/bash -l
#SBATCH --job-name=digits-mlp
#SBATCH --account=p201580            # workshop training project
#SBATCH --partition=gpu
#SBATCH --qos=default
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --time=00:15:00
#SBATCH --output=digits-%j.out

# Hyperparameter search for a small neural network (Practical 3).
# Submit from this folder with:  sbatch train_digits.slurm

module load env/release/2025.1
module load scikit-learn/1.7.0-gfbf-2025a

# One thread per worker process, so 16 parallel fits use exactly 16 cores
export OMP_NUM_THREADS=1

python train_digits.py --n-jobs "${SLURM_CPUS_PER_TASK}"

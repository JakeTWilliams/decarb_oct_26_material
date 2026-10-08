#!/bin/bash -l
#SBATCH --job-name=jupyter
#SBATCH --account=p201580            # workshop training project
#SBATCH --partition=gpu
#SBATCH --qos=short
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --time=00:30:00              # covers 11:30 to 15:00, including lunch
#SBATCH --output=jupyter-%j.out

# Starts JupyterLab on a MeluXina compute node for the practicals.
# Submit from this folder with:  sbatch jupyter.slurm
# then follow the instructions printed at the top of jupyter-<jobid>.out

module load env/release/2025.1
module load JupyterLab/4.4.4-GCCcore-14.2.0 \
            scikit-learn/1.7.0-gfbf-2025a \
            matplotlib/3.10.3-gfbf-2025a

# The matplotlib module sets MPLBACKEND=Agg, which hides plots in notebooks
unset MPLBACKEND
# The practical datasets are tiny: one BLAS thread per process avoids oversubscription
# when scikit-learn runs several fits in parallel (n_jobs)
export OMP_NUM_THREADS=1

NODE=$(hostname)
# Ask the OS for a free port, so several users on one node don't collide
PORT=$(python -c 'import socket; s = socket.socket(); s.bind(("", 0)); print(s.getsockname()[1])')

cat <<INFO
====================================================================
 JupyterLab is starting on ${NODE}, port ${PORT}.

 1. On YOUR LAPTOP, open a new terminal and run (leave it open):

      ssh -p 8822 -N -L ${PORT}:${NODE}:${PORT} ${USER}@login.lxp.lu

 2. In your browser, open the URL below that starts with
    http://127.0.0.1:${PORT}/lab?token=...

 3. When you are done: File > Shut Down in JupyterLab, or
      scancel ${SLURM_JOB_ID}
====================================================================
INFO

jupyter lab --no-browser --ip="${NODE}" --port="${PORT}" --ServerApp.port_retries=0

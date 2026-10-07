---
# You can also start simply with 'default'
theme: academic
addons:
  - slidev-addon-ichec
# random image from a curated Unsplash collection by Anthony
# like them? see https://unsplash.com/collections/94734566/slidev
background: https://cdn.jsdelivr.net/gh/slidevjs/slidev-covers@main/static/3GmudSL84n4.webp

# some information about your slides (markdown enabled)
info: |
  ## Slidev Starter Template 
  Presentation slides for developers.

  Learn more at [Sli.dev](https://sli.dev)
# apply unocss classes to the current slide
class: text-center
# https://sli.dev/features/drawing
drawings:
  persist: false
# slide transition: https://sli.dev/guide/animations.html#slide-transitions
transition: slide-left
# enable MDC Syntax: https://sli.dev/features/mdc
mdc: true
# open graph
# seoMeta:
#  ogImage: https://cover.sli.dev
---

# Strong Scaling Demo 

Katie O'Connor, ICHEC

---

# Introduction

In this exercise we will produce our own strong scaling tables and graphs. There are two programs two be compiled and run, one can be entirely parallelised, the other has a serial section. For both cases, you will run the compile and run the code with 1, 2, 4, 8, 16, 32, 64 cores and plot the results. For plotting, you are encouraged to use Python, but you are also welcome to use any software you are familiar with or plot them by hand. 

---

# Ideal case- and running a job interactively

While there is a script that can run all our jobs for us, this is a good chance to practise running jobs interactively on the compute nodes. The workflow is: 
- Request a compute node 
`salloc -A <account_name> -t 00:20:00 -q default -N 1 -p cpu`
- Load required modules 
`module load GCC MPICH`
- Compile 
`mpicc -o ideal_example amdahl_ideal.c`
- Run 
`mpirun -n <num_cores> ./ideal_example`

The single core example can take around 1 minute. 

In this example, you should see good strong scaling, where the execution time halves as the number of cores is doubled. It is not perfect, and it will fall off as at a certain point, but this is as good a strong scaling curve as one would expect in a realistic problem. 

---

# Non ideal case- and using Slurm scripts 

For the non ideal case, we will use a Slurm script to complete this workload for us. This has been provided in `sbatch_non_ideal.sh`. To submit your job use: 
`sbatch sbatch_run_ideal.sh`

You will be provided with a job ID as a response. In order to check where your job is in the queue, use `squeue --me`. When your job is no longer listed in the queue, it has completed. 

To see the results, the terminal output from the compute node is saved in `slurm-<job_ID>.out`. 

I this case, the execution time will be reduced as the number of cores is increased, but we do not see ideal scaling as we did before. As the number of cores is increased, the execution time tends towards the execution time of the serial section (which has been set to 10 seconds in this case). 
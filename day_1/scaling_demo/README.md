To run the jobs interactively: 

On the login node, request a compute node using salloc

`salloc -A <account_name> -t 00:20:00 -q default -N 1 -p cpu`

This will automatically redirect you to the compute node when it is ready 

Then load the modules you will need

`module load GCC MPICH`

And then compile the program 

`mpicc -o ideal_example amdahl_ideal.c`

And finally run for different sizes of simulation

```bash
mpirun -n 1 ./ideal_example
mpirun -n 2 ./ideal_example
mpirun -n 4 ./ideal_example
mpirun -n 8 ./ideal_example
mpirun -n 16 ./ideal_example
mpirun -n 32 ./ideal_example
mpirun -n 64 ./ideal_example
```
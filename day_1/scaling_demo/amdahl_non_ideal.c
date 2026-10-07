#include <stdio.h>
#include <mpi.h>
#include <unistd.h>
#include <stdlib.h>
#include <time.h>

int main(int argc, char** argv){
    MPI_Init(&argc, &argv);
    time_t start; 
    start = time(NULL);

    sleep(10);

    long n_global=1000000000;
    unsigned int seed = 28;  
    int size, rank;
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    int n = n_global/size;  //I know I should calculate remainders
    long sum=0;
    srand(seed + rank);
    for(int i=0; i<n; i++){
        double x = (double)rand()/(double)RAND_MAX;
        double y = (double)rand()/(double)RAND_MAX;
        double r2 = x*x+y*y;
        if(r2<1){
            sum++;
        }
    }
    
    long total;	
    MPI_Reduce(&sum, &total, 1, MPI_LONG, MPI_SUM, 0, MPI_COMM_WORLD); 
    
    if(rank ==0){
        double pi = 4*((double) total/(double) n_global);
        printf("Estimate of pi is: %lf \n", pi);
    }
    time_t finish; 
    finish = time(NULL);
    time_t time = finish - start;
    if(rank ==0){
	   printf("Cores used: %d \n", size);
	   printf("Time taken in seconds: %d \n", time);
    } 
    MPI_Finalize();
    return 0;
}
    

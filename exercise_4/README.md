# Exercise 4: Parallel K-Means Clustering (MPI + Covertype Dataset)

Distributed implementation of the K-Means algorithm using MPI (mpi4py) with performance comparison against a serial baseline. Runs inside Docker.

## Setup

Build the Docker image:

``` bash
docker build -t proyecto-hpc
```

## Usage

Run all experiments:

``` bash
python exercise_4/run_all.py
```

This will:

-Load and preprocess the dataset
-Run K-Means (serial)
-Run K-Means (MPI) with multiple processes
-Evaluate performance across configurations

## Data

Dataset: Covertype (Forest Cover Type)

~580,000 samples
54 features
7 classes (forest cover types)


Performance

| K  | Mode    | Iterations | Total Time (s) | Time/Iter (s) | Speedup |
| -- | ------- | ---------- | -------------- | ------------- | ------- |
| 7  | Serial  | 50         | 245.38         | 4.90          | 1.00x   |
| 7  | MPI (1) | 8          | 48.17          | 6.02          | 5.09x*  |
| 7  | MPI (2) | 4          | 18.41          | 4.60          | 13.32x* |
| 7  | MPI (4) | 11         | 74.85          | 6.80          | 3.27x   |
| 10 | MPI (1) | 15         | 134.93         | 8.99          | 1.81x   |
| 10 | MPI (4) | 18         | 131.50         | 7.30          | 1.86x   |


## Key Concepts
1. Distributed clustering (MPI)
2. Data partitioning (Scatterv / Gatherv)
3. Collective communication (Allreduce, bcast)
4. Convergence in parallel algorithms
5. Scalability and speedup analysis
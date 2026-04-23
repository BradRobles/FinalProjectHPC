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


Performance (Example)
| Mode | Processes | K | Time (s) | Speedup |
|:----|:------|:----|:-----|:-----|
|Serial|1|7|12.5|1.00|
|MPI|2|7|7.1|1.76|
|MPI|4|7|4.3|2.90|
|MPI|4|10|5.0|2.50|

## Key Concepts
1. Distributed clustering (MPI)
2. Data partitioning (Scatterv / Gatherv)
3. Collective communication (Allreduce, bcast)
4. Convergence in parallel algorithms
5. Scalability and speedup analysis
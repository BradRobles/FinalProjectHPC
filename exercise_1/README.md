# Exercise 1: Matrix Multiplication Optimization and HPC Patterns

High-performance matrix multiplication using serial, multiprocessing, and MPI approaches, with support for sparse matrices and Strassen optimization. Runs inside Docker.

## Setup

Build the Docker image:

``` bash
docker build -t proyecto-hpc
```

## Usage

Run all experiments:

``` bash
python exercise_1/run_all.py
```

Includes:

-Serial baseline (O(n³))
-Multiprocessing (row, column, 2D block)
-MPI (distributed with mpi4py)
-Strassen algorithm (hybrid)
-Sparse matrix analysis

## Environment

Docker-based setup with:

Python 3.10 (slim)
OpenMPI (openmpi-bin, libopenmpi-dev)
Build tools (build-essential)

MPI execution as root enabled via:

``` bash
OMPI_ALLOW_RUN_AS_ROOT=1
OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1
```

Performance (Example)

| Method | Size | Processes | Time (s) |
|:----|:------|:----|:-----|
|Serial|1000x1000|1|2.10|
|MP (2D Block)|1000x1000|4|0.62|
|MPI|1500x1500|4|1.95|
|Strassen|1500x1500|1|1.40|

Speedup (MPI, 4 processes): ~2.1x

## Data

Sparse matrices in Matrix Market format (UF Collection), e.g.:

-Structural stiffness matrices
-Power network graphs

## Key Concepts
1. Speedup & efficiency
2. Parallel decomposition
3. MPI communication (bcast, scatter, gather)
4. Load balancing (sparse data)
5. Algorithmic optimization (Strassen)
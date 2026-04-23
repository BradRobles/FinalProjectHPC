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

Performance


### Baseline Serial Multiplication
| Size (n × n) | Execution Time (s) | Correctness |
| ------------ | ------------------ | ----------- |
| 64           | 0.0563             | True        |
| 128          | 0.3238             | True        |
| 256          | 2.5880             | True        |

### Multiprocessing Performance (512 × 512)
| Partition Method | Workers | Execution Time (s) |
| ---------------- | ------- | ------------------ |
| Rows             | 10      | 0.2102             |
| Columns          | 10      | 0.1425             |
| Blocks (2D)      | 9       | 0.2075             |

### Distributed Memory (MPI)
| Size      | Workers | Execution Time (s) |
| --------- | ------- | ------------------ |
| 512 × 512 | 4       | 0.0041             |

### Strassen vs Baseline (512 × 512)
| Method          | Threshold | Time (s) |
| --------------- | --------- | -------- |
| Pure Strassen   | 16        | 0.0927   |
| Hybrid Strassen | 128       | 0.0034   |
| NumPy Baseline  | N/A       | 0.0013   |

### Sparse Matrix Analysis
| Matrix   | Source         | Sparsity (%) | Time (s) |
| -------- | -------------- | ------------ | -------- |
| bcspwr08 | Power Network  | 99.77        | 0.0004   |
| bcsstk18 | Structural Eng | 99.90        | 0.0131   |


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
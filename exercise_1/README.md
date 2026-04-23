# Exercise 1: Matrix Multiplication Optimization and HPC Patterns

This project explores various strategies for matrix multiplication, ranging from basic serial implementations to advanced algorithms and high-performance computing (HPC) parallelization techniques using Shared Memory (Multiprocessing) and Distributed Memory (MPI).

---

## 📂 Project Structure

```text
exercise_1/
├── README.md             # Summary of the exercise
├── data/                 # Sparse matrix files (.mtx)
├── src/
│   ├── baseline.py       # Serial triple-loop implementation O(n³)
│   ├── parallel_mp.py    # Row and Column partitioning (Multiprocessing)
│   ├── parallel_mp2.py   # 2D Block partitioning (Multiprocessing)
│   ├── parallel_mpi.py   # Distributed memory implementation (mpi4py)
│   ├── sparse_experiments.py # Analysis of sparse matrices and load balancing
│   ├── strassen.py       # Strassen’s Algorithm (Pure vs. Hybrid)
│   └── utils.py          # Helper functions (loading, validation, generation)
└── run_all.py            # Orchestrator script to run all tests via Docker

```

# Module Descriptions
1. Serial Baseline (baseline.py)

Implements the standard $O(n^3)$ matrix multiplication using a nested triple-loop.

-Serves as the Ground Truth and performance benchmark.
-Used to calculate speedup.
-Validation: Uses numpy.dot to ensure numerical correctness.

2. Shared Memory Parallelism (parallel_mp.py & parallel_mp2.py)

Utilizes the Python multiprocessing library to bypass the GIL and leverage multiple CPU cores.

Strategies:

-Row-wise partitioning: Splits Matrix A into horizontal chunks.
-Column-wise partitioning: Splits Matrix B into vertical chunks.
-2D Block Partitioning: Divides both matrices into sub-blocks, improving cache locality.

3. Distributed Memory (parallel_mpi.py)

Designed for cluster environments where memory is not shared between nodes. Uses MPI via mpi4py.

Mechanism:

-Rank 0 performs:
   -bcast → Broadcasts Matrix B to all processes.
   -scatter → Distributes rows of Matrix A.
-Each process computes its partial result.
-gather reconstructs the final matrix.

4. Strassen’s Algorithm (strassen.py)

A divide-and-conquer algorithm that reduces complexity from:

$O(n^3)$ → $O(n^{2.81})$

Hybrid Approach:

-Uses recursion for large matrices.
-Switches to NumPy (BLAS) when matrices are small to reduce overhead.

5. Sparse Matrix Analysis (sparse_experiments.py)

Analyzes real-world sparse matrices (e.g., Power Grid, Structural Engineering).

-Format: CSR (Compressed Sparse Row)
-Focus:
   -Load imbalance
   -Distribution of non-zero elements
-Impact on parallel performance

6. Utilities (utils.py)

Centralized helper functions for:

-Dense matrix generation (with fixed seeds)
-Matrix Market (.mtx) file loading
-Accuracy validation using np.allclose

# How to Run

The project is containerized using Docker to ensure all dependencies are available.

**Prerequisites**
1. Docker installed and running
2. Docker image built and tagged as: proyecto-hpc
3. Execution

Run the full experimental suite:

``` bash
python run_all.py
```

This script:

-Detects the OS
-Mounts the current directory into the container
-Executes all tests
-Reports execution time and correctness

# Key HPC Concepts Evaluated
1. Speedup: Ratio between serial and parallel execution time
2. Efficiency: Performance gain per processor used
3. Communication Overhead: Cost of data transfer (MPI)
4. Load Balancing: Distribution of work across processes
# <img src="https://slackmojis.com/emojis/55973-digital_rain_matrix/download" width="25"/> Exercise 1 — Matrix Multiplication

Implements and benchmarks serial and parallel strategies for dense matrix multiplication, plus a sparse matrix analysis module. All experiments run inside a Docker container (`proyecto-hpc`) for full reproducibility.

The serial baseline uses a naive O(n³) triple loop. Parallel variants partition the work using row, column, or block decomposition (Python `multiprocessing`), distributed computation via MPI, and the Strassen divide-and-conquer algorithm. A separate script (`sparse_experiments.py`) analyzes real-world sparse matrices in CSR format, examining load imbalance across row partitions.

## Results

### Baseline — Serial (dense, O(n³))

| Size | Time (s) |
|---|---|
| 64 × 64 | 0.0563 |
| 128 × 128 | 0.3238 |
| 256 × 256 | 2.5880 |

### Multiprocessing — Partition Strategies (512 × 512)

| Partition Method | Workers | Time (s) |
|---|---|---|
| Rows | 10 | 0.2102 |
| Columns | 10 | 0.1425 |
| Blocks (2D) | 9 | 0.2075 |

Column partitioning outperforms rows due to better cache locality — sequential memory access maximizes cache hit rate and reduces costly RAM reads.

### MPI Distributed (512 × 512, 4 processes)

| Time (s) |
|---|
| 0.0041 |

The low time reflects MPI's use of shared memory (`/dev/shm`) when all processes run on the same node, bypassing network overhead entirely.

### Strassen vs. NumPy Baseline (512 × 512)

| Method | Recursive Threshold | Time (s) |
|---|---|---|
| Pure Strassen | 16 | 0.0927 |
| Hybrid Strassen | 128 | 0.0034 |
| NumPy Baseline | — | 0.0013 |

The hybrid variant is ~27x faster than pure Strassen by stopping recursion at 128×128 blocks, avoiding Python call stack overhead. Even so, it cannot match NumPy's native C/BLAS implementation.

### Sparse Matrix Analysis (CSR format, 4 workers)

| Matrix | Domain | Sparsity (%) | CSR Time (s) |
|---|---|---|---|
| `bcspwr08` | Power network | 99.77 | 0.0004 |
| `bcsstk18` | Structural engineering | 99.90 | 0.0131 |

Static row-based load division exposes significant imbalance: Worker 0 receives ~20.9% of non-zero operations while Worker 2 carries ~26.8%, a ~6% gap that bottlenecks the entire parallel execution.

---

For further details, see the full report at `docs/report.pdf`.
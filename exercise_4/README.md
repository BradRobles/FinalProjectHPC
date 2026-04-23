# <img src="https://slackmojis.com/emojis/28601-laptop/download" width="25"/> Exercise 4 — Distributed K-Means

Implements K-Means clustering on the **Covertype dataset** (581,012 samples, 54 features) in both serial and MPI-distributed variants. Features are normalized with `StandardScaler` before clustering to prevent high-range dimensions from dominating Euclidean distance calculations.

The parallel version distributes samples across processes using `Scatterv` (handling uneven splits gracefully), performs local distance computations on each partition, and synchronizes cluster centroids globally via `Allreduce` at every iteration — avoiding the idle time of a centralized `Gather + Bcast` approach. Final labels are collected on rank 0 via `Gatherv`.

## ▷ Results

### K = 7

| Implementation | Processes | Iterations | Total Time (s) | Time / Iter (s) | Speedup |
|---|---|---|---|---|---|
| Serial | 1 | 50 | 245.38 | 4.90 | 1.00x |
| MPI | 1 | 8 | 48.17 | 6.02 | 5.09x* |
| MPI | 2 | 4 | 18.41 | 4.60 | 13.32x* |
| MPI | 4 | 11 | 74.85 | 6.80 | 3.27x |

### K = 10

| Implementation | Processes | Iterations | Total Time (s) | Time / Iter (s) | Speedup |
|---|---|---|---|---|---|
| Serial | 1 | 50 | 245.38 | 4.90 | 1.00x |
| MPI | 1 | 15 | 134.93 | 8.99 | 1.81x |
| MPI | 4 | 18 | 131.50 | 7.30 | 1.86x |

> \* Speedup is sensitive to random centroid initialization, which affects the number of iterations needed to converge. The 4-process run for K=7 converges in more iterations, offsetting the per-iteration gain. Increasing K to 10 grows the `Allreduce` message payload by ~42%, increasing communication overhead and limiting scalability.

---

For further details, see the full report at `docs/report.pdf`.
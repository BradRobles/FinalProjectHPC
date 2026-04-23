# Evaluating Activity 3 — Parallel Programming Applications


## ▷ Objective

This assignment implements and evaluates serial and parallel computational strategies across four distinct workloads. The goal is to measure the real-world impact of parallelism on execution time, speedup, and scalability using two paradigms:

- **Shared memory** — Python `multiprocessing`
- **Distributed memory** — OpenMPI with `mpi4py`

Each exercise provides a serial baseline and one or more parallel implementations so both approaches can be directly compared under the same conditions.

## ▷ Repository Structure

```
FinalProjectHPC/
├── exercise_1/                   # Matrix Multiplication
│   ├── data/
│   │   ├── bcspwr08.mtx          # Sparse matrix — power network
│   │   └── bcsstk18.mtx          # Sparse matrix — structural engineering
│   ├── src/
│   │   ├── baseline.py           # Serial baseline — O(n³)
│   │   ├── parallel_mp.py        # Multiprocessing (row partition)
│   │   ├── parallel_mp2.py       # Multiprocessing (block partition)
│   │   ├── parallel_mpi.py       # MPI distributed
│   │   ├── strassen.py           # Strassen algorithm
│   │   ├── sparse_experiments.py # Sparse matrix analysis & load imbalance
│   │   └── utils.py
│   ├── run_all.py
│   └── README.md
│
├── exercise_2/                   # Cell Morphology Analysis
│   ├── results/
│   │   └── morphology_summary.csv
│   ├── src/
│   │   ├── segmentation.py       # Serial baseline
│   │   ├── parallel.py           # Multiprocessing parallel
│   │   └── utils.py
│   ├── download_data.py
│   ├── run_analysis.py
│   ├── run_all.py
│   └── README.md
│
├── exercise_3/                   # Forest Fire Simulation
│   ├── results/
│   │   ├── frames/
│   │   ├── final_map.png
│   │   └── fire_simulation.gif
│   ├── src/
│   │   ├── automaton_serial.py   # Serial baseline
│   │   ├── automaton_parallel.py # MPI parallel
│   │   ├── firms_loader.py
│   │   ├── utils.py
│   │   └── visualization.py
│   ├── .env                      # NASA FIRMS API key (not committed)
│   ├── run_all.py
│   └── README.md
│
├── exercise_4/                   # Distributed K-Means
│   ├── kmeans_serial.py          # Serial baseline
│   ├── kmeans_parallel.py        # MPI parallel
│   ├── data_loader.py
│   ├── run_all.py
│   └── README.md
│
├── docs/
│   └── report.pdf
├── .gitignore
├── Dockerfile
├── requirements.txt
└── README.md
```

## ▷ How to Compare Serial vs Parallel

Each exercise follows the same structure: a serial baseline file and one or more parallel implementations, all runnable through a single `run_all.py` that executes both versions and prints timing results side by side.

| Exercise | Baseline file | Parallel file(s) | Strategy |
|---|---|---|---|
| 1 — Matrix Multiplication | `src/baseline.py` | `src/parallel_mp.py`, `src/parallel_mp2.py`, `src/parallel_mpi.py`, `src/strassen.py` | Multiprocessing + MPI + Strassen |
| 2 — Cell Morphology | `src/segmentation.py` | `src/parallel.py` | Multiprocessing |
| 3 — Forest Fire | `src/automaton_serial.py` | `src/automaton_parallel.py` | MPI |
| 4 — K-Means | `kmeans_serial.py` | `kmeans_parallel.py` | MPI |

To reproduce all performance experiments for any exercise:

```bash
python exercise_X/run_all.py   # replace X with 1, 2, 3, or 4
```

This runs the serial baseline first, then each parallel variant, and outputs execution times and speedup for direct comparison.

## ▷ Requirements & Setup

**Required:** Docker Desktop

```bash
# 1. Clone the repo
git clone https://github.com/your-org/FinalProjectHPC.git
cd FinalProjectHPC

# 2. Build the image (installs MPI, mpi4py, numpy, scikit-learn, scikit-image, scipy)
docker build -t proyecto-hpc .
```

Exercise 3 additionally requires a NASA FIRMS API key. Add it to the `.env` file inside `exercise_3/`:

```
FIRMS_API_KEY=your_key_here
```

Exercise 2 requires downloading the dataset first:

```bash
python exercise_2/download_data.py
```

##  <img src="https://slackmojis.com/emojis/55973-digital_rain_matrix/download" width="25"/> Exercise 1 — Matrix Multiplication

**Baseline:** `exercise_1/src/baseline.py` — naive O(n³) triple loop  
**Parallel:** `src/parallel_mp.py`, `src/parallel_mp2.py` (Multiprocessing) · `src/parallel_mpi.py` (MPI) · `src/strassen.py` (Strassen)  
**Additional:** `src/sparse_experiments.py` — standalone analysis of sparse matrices (CSR format via scipy) and load imbalance across row partitions; run independently with `python exercise_1/src/sparse_experiments.py`  

```bash
python exercise_1/run_all.py
```

| Implementation | Size | Workers | Time (s) |
|---|---|---|---|
| Serial | 256 × 256 | 1 | 2.5880 |
| Multiprocessing — rows | 512 × 512 | 10 | 0.2102 |
| Multiprocessing — columns | 512 × 512 | 10 | 0.1425 |
| Multiprocessing — blocks | 512 × 512 | 9 | 0.2075 |
| MPI | 512 × 512 | 4 | 0.0041 |
| Hybrid Strassen | 512 × 512 | — | 0.0034 |


## <img src="https://slackmojis.com/emojis/52843-bacteria/download" width="25"/> Exercise 2 — Cell Morphology Analysis

**Baseline:** `exercise_2/src/segmentation.py`  
**Parallel:** `exercise_2/src/parallel.py` — Python Multiprocessing over image frames

```bash
python exercise_2/run_all.py
```

| Implementation | Workers | Time (s) | Speedup |
|---|---|---|---|
| Serial | 1 | 246.28 | 1.00x |
| Parallel | 2 | 298.58 | 0.82x |

> Speedup < 1 is expected here: frame loading is I/O-bound and worker spawn overhead dominates at this dataset size.


## <img src="https://slackmojis.com/emojis/49-fireball/download" width="25"/> Exercise 3 — Forest Fire Simulation

**Baseline:** `exercise_3/src/automaton_serial.py`  
**Parallel:** `exercise_3/src/automaton_parallel.py` — domain decomposition via MPI

```bash
python exercise_3/run_all.py
```

| Implementation | Grid | Processes | Time (s) | Speedup |
|---|---|---|---|---|
| Serial | 1500 × 1500 | 1 | 4.46 | 1.00x |
| MPI | 1500 × 1500 | 4 | 2.04 | 2.19x |


## <img src="https://slackmojis.com/emojis/28601-laptop/download" width="25"/> Exercise 4 — Distributed K-Means

**Baseline:** `exercise_4/kmeans_serial.py`  
**Parallel:** `exercise_4/kmeans_parallel.py` — MPI with `Scatterv`, `Gatherv`, `Allreduce`, `Broadcast`

```bash
python exercise_4/run_all.py
```

| Implementation | Processes | K | Iterations | Time (s) | Speedup |
|---|---|---|---|---|---|
| Serial | 1 | 7 | 50 | 245.38 | 1.00x |
| MPI | 1 | 7 | 8 | 48.17 | 5.09x |
| MPI | 2 | 7 | 4 | 18.41 | 13.32x |
| MPI | 4 | 7 | 11 | 74.85 | 3.27x |


## ▷ Full Report

Methodology, analysis, and conclusions: `docs/report.pdf`
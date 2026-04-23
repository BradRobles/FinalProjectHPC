# High-Performance Computing: Final Project

## Objective

This repository contains the final project for the High-Performance Computing (HPC) course. The objective is to implement, evaluate, and compare serial and parallel computational strategies across data engineering and machine learning workloads.

*The project explores:*

-Shared memory parallelism (Python Multiprocessing)
-Distributed memory (OpenMPI with mpi4py)

with a focus on performance, scalability, and efficiency.

Team Members:

1. *KAREN CARDIEL OLEA 2209039*
2. *JORGE RAMIRO CHAY KOYOC 2309052*
3. *ANGELES ALEJANDRA CRUZ LEGORRETA 2309064*
4. *DIEGO JESUS LORIA CAMPOS 2309140*
5. *BRAD ROBLES GARCIA 2309198*
6. *ELISABET ARELLY SULU VELA 2309212*

Institution: Universidad Politécnica de Yucatán (UPY)


```bash
FinalProjectHPC/
├── exercise_1/             # Matrix Multiplication & Strassen
│   ├── data/               # Sparse matrices (.mtx)
│   ├── src/                # Implementations (serial, MP, MPI, Strassen)
│   ├── run_all.py
│   └── README.md
│
├── exercise_2/             # Cell Morphology Analysis
│   ├── data/               # DIC-C2DH-HeLa dataset
│   ├── results/            # CSV outputs
│   ├── src/                # Segmentation + parallel logic
│   ├── download_data.py
│   ├── run_analysis.py
│   ├── run_all.py
│   └── README.md
│
├── exercise_3/             # Forest Fire Cellular Automaton (MPI)
│   ├── results/            # Simulation outputs
│   ├── src/
│   ├── run_all.py
│   └── README.md
│
├── exercise_4/             # Distributed K-Means (MPI)
│   ├── data_loader.py
│   ├── kmeans_serial.py
│   ├── kmeans_parallel.py
│   ├── run_all.py
│   └── README.md
│
├── docs/
│   ├── assets/             # Figures, plots, logs
│   └── report.pdf          # Final report
│
├── Dockerfile
├── requirements.txt
└── README.md
```

## Environment

This project is fully containerized to ensure reproducibility.

*Requirements*
-Docker Desktop
-Python 3.x (optional, for running scripts locally)
-Build Image
-```docker build -t proyecto-hpc .```
-Execution

Each exercise includes a ```run_all.py``` orchestrator.

Example:

```bash
python exercise_X/run_all.py
```

This will:

-Launch a Docker container
-Mount the project directory
-Execute all experiments automatically
-Exercises Overview

## *Exercise 1: Matrix Multiplication Optimization*

Efficient matrix multiplication using:

*Serial baseline (O(n³))
*Multiprocessing (row, column, 2D block)
*MPI (distributed)
*Strassen algorithm
*Performance (Example)

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


## *Exercise 2: Parallel Cell Morphology Analysis*

Bioimage processing pipeline using microscopy data.

-Dataset: DIC-C2DH-HeLa
-Extracts:
-Cell count
-Area
-Morphological features
-Performance

| Mode | Workers | Time (s) | Speedup|
|:----|:------|:----|:-----|
|Serial|1|246.28|1.00x|
|Parallel|2|298.58|0.82x|

## *Exercise 3: Forest Fire Simulation (MPI)*

Cellular automaton simulating wildfire spread using NASA FIRMS data.

### Setup

```bash
docker build -t proyecto-hpc .
```

Add API key:

```bash
FIRMS_API_KEY=your_key_here
```

### Usage
```bash
python exercise_3/run_all.py
```

### Performance

| Method | Grid | Processes | Time (s) |
|:----|:------|:----|:-----|
|Serial|1500x1500|1|4.46|
|MPI|1500x1500|4|2.04|

Speedup: 2.19x

## *Exercise 4: Distributed K-Means (MPI)*

Clustering using Covertype dataset (~580k samples, 54 features).

-Serial K-Means baseline
-Parallel K-Means using MPI:
-Scatterv / Gatherv
-Allreduce
-Broadcast
-Performance (Example)

| K  | Mode    | Iterations | Total Time (s) | Time/Iter (s) | Speedup |
| -- | ------- | ---------- | -------------- | ------------- | ------- |
| 7  | Serial  | 50         | 245.38         | 4.90          | 1.00x   |
| 7  | MPI (1) | 8          | 48.17          | 6.02          | 5.09x*  |
| 7  | MPI (2) | 4          | 18.41          | 4.60          | 13.32x* |
| 7  | MPI (4) | 11         | 74.85          | 6.80          | 3.27x   |
| 10 | MPI (1) | 15         | 134.93         | 8.99          | 1.81x   |
| 10 | MPI (4) | 18         | 131.50         | 7.30          | 1.86x   |

# Key HPC Concepts
1. Speedup & efficiency
2. Load balancing
3. Communication overhead (MPI)
4. Data partitioning strategies
5. Algorithmic optimization
6. Scalability analysis
7. Documentation

A full technical report including:

1. Methodology
2. Experimental results
3. Performance analysis
4. Bottlenecks and conclusions

is available at:

```bash
docs/report.pdf
```
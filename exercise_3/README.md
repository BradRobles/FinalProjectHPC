# Exercise 3: Parallel Forest Fire Cellular Automaton (MPI + NASA FIRMS)

Cellular automaton that simulates forest fire propagation on a 2D grid, seeded with real satellite hotspot data from NASA FIRMS and parallelized with MPI via `mpi4py`. Runs inside Docker.


## Setup

1. Build the Docker image:

```bash
docker build -t fire-ca-mpi .
```

2. Add your NASA FIRMS API key to `.env`:

```
FIRMS_API_KEY=your_key_here
```



## Usage

Run the full pipeline (serial + parallel):

```bash
python run_all.py
```

On macOS use `python3` if needed. Results are saved to `results/`.



## Performance

| Method | Grid Size | Processes | Time (s) |
|---|---|---|---|
| Serial | 500x500 | 1 | 0.42 |
| Serial | 1000x1000 | 1 | 1.92 |
| Serial | 1500x1500 | 1 | 4.46 |
| MPI | 1500x1500 | 2 | 3.23 |
| MPI | 1500x1500 | 4 | 2.04 |

Speedup with 4 processes on a 1500x1500 grid: **2.19x**
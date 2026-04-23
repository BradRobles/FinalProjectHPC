from mpi4py import MPI
import numpy as np

from utils import setup_project
from firms_loader import FirmsLoader
from visualization import plot_fire_grid, create_gif


# -----------------------------
# RULES (COMPUTATION ONLY)
# -----------------------------
def apply_rules(grid, p):
    rows, cols = grid.shape
    new_grid = grid.copy()

    burning = grid == 2
    new_grid[burning] = 3

    neighbors = np.zeros((rows, cols), dtype=int)

    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            neighbors += np.roll(np.roll(burning, dr, 0), dc, 1)

    ignite = (
        (grid == 1)
        & (neighbors > 0)
        & (np.random.rand(rows, cols) < p)
    )

    new_grid[ignite] = 2
    return new_grid


# -----------------------------
# MPI SIMULATION
# -----------------------------
def run_simulation():

    VISUAL = False  # False para benchmarking, True para imagen final y gif

    api_key = setup_project()

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    N = 1500
    steps = 150
    p_spread = 0.45
    bbox = [18, -14, 28, -4]

    full_grid = None

    # -----------------------------
    # LOAD DATA (ONLY RANK 0)
    # -----------------------------
    if rank == 0:
        print("Loading NASA FIRMS data...")
        loader = FirmsLoader(api_key, bbox, (N, N))
        df = loader.get_data(day_range=2)
        full_grid = loader.create_grid(df)
        print("Initial fire cells:", np.sum(full_grid == 2))

    # -----------------------------
    # DISTRIBUTE GRID
    # -----------------------------
    chunks = np.array_split(full_grid, size, axis=0) if rank == 0 else None
    local = comm.scatter(chunks, root=0)

    rows = local.shape[0]
    local_grid = np.zeros((rows + 2, N), dtype=int)
    local_grid[1:-1] = local

    # -----------------------------
    # TIMING ONLY COMPUTATION
    # -----------------------------
    comm.Barrier()
    start = MPI.Wtime()

    for t in range(steps):

        # exchange ghost rows
        comm.Sendrecv(
            local_grid[-2], (rank + 1) % size, 0,
            local_grid[0], (rank - 1) % size, 0
        )

        comm.Sendrecv(
            local_grid[1], (rank - 1) % size, 1,
            local_grid[-1], (rank + 1) % size, 1
        )

        updated = apply_rules(local_grid, p_spread)
        local_grid[1:-1] = updated[1:-1]

    # -----------------------------
    # FINAL GATHER
    # -----------------------------
    final = comm.gather(local_grid[1:-1], root=0)

    comm.Barrier()
    end = MPI.Wtime()

    # -----------------------------
    # VISUALIZATION (ONLY IF ENABLED)
    # -----------------------------
    if rank == 0:

        total_grid = np.vstack(final)

        if VISUAL:
            plot_fire_grid(
                total_grid,
                steps,
                save_path="results/final_map.png"
            )

            create_gif(
                "results",
                "results/fire_simulation.gif"
            )

        print(f"Execution time: {end - start:.3f} sec")
        print("Simulation finished.")


if __name__ == "__main__":
    run_simulation()
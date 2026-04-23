import numpy as np
import time

from utils import setup_project
from firms_loader import FirmsLoader
from visualization import plot_fire_grid, create_gif


class ForestFireCA:
    def __init__(self, grid, p_spread=0.3):
        self.grid = grid.copy()
        self.p_spread = p_spread

    def step(self):
        rows, cols = self.grid.shape
        new_grid = self.grid.copy()

        burning = self.grid == 2
        new_grid[burning] = 3

        neighbors = np.zeros((rows, cols), dtype=int)

        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                neighbors += np.roll(np.roll(burning, dr, 0), dc, 1)

        ignite = (
            (self.grid == 1)
            & (neighbors > 0)
            & (np.random.rand(rows, cols) < self.p_spread)
        )

        new_grid[ignite] = 2
        self.grid = new_grid
        return self.grid


def run_serial():

    VISUAL = False   # cambiar a False para benchmarking

    api_key = setup_project()

    N = 1500 # 800 visual | 1500 benchmarking
    steps = 150 # 140 visual | 150 benchmarking
    p_spread = 0.45
    bbox = [18, -14, 28, -4]

    print("Loading NASA FIRMS data...")

    loader = FirmsLoader(api_key, bbox, (N, N))
    df = loader.get_data(day_range=2)
    grid = loader.create_grid(df)

    print("Initial fire cells:", np.sum(grid == 2))

    model = ForestFireCA(grid, p_spread)

    start = time.time()

    for t in range(steps):
        model.step()

        if VISUAL and t % 5 == 0:
            plot_fire_grid(
                model.grid,
                t,
                save_path=f"results/frames/frame_{t:03d}.png"
            )

    end = time.time()

    if VISUAL:
        plot_fire_grid(
            model.grid,
            steps,
            save_path="results/final_map.png"
        )

        create_gif(
            "results",
            "results/fire_simulation.gif"
        )

    print(f"Serial runtime: {end - start:.4f} sec")


if __name__ == "__main__":
    run_serial()
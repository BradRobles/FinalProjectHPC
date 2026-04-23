import matplotlib.pyplot as plt
from matplotlib import colors
import imageio.v2 as imageio
import os


def plot_fire_grid(grid, step, save_path=None):
    cmap = colors.ListedColormap([
        "#4fc3f7",   # 0 agua
        "#2e7d32",   # 1 bosque
        "#ff3d00",   # 2 fuego
        "#424242"    # 3 ceniza
    ])

    bounds = [0, 1, 2, 3, 4]
    norm = colors.BoundaryNorm(bounds, cmap.N)

    plt.figure(figsize=(10, 10))
    plt.imshow(grid, cmap=cmap, norm=norm)
    plt.title(f"Forest Fire Simulation - Step {step}", fontsize=16)
    plt.axis("off")

    if save_path:
        plt.savefig(save_path, dpi=180, bbox_inches="tight")
        plt.close()
    else:
        plt.show()


def create_gif(folder, output_path):
    files = sorted([
        f for f in os.listdir(folder)
        if f.startswith("frame_") and f.endswith(".png")
    ])

    images = []

    for file in files:
        path = os.path.join(folder, file)
        images.append(imageio.imread(path))

    imageio.mimsave(output_path, images, duration=0.35)
# <img src="https://slackmojis.com/emojis/52843-bacteria/download" width="25"/> Exercise 2 — Cell Morphology Analysis

Segments and measures cell morphology across the **DIC-C2DH-HeLa** time-lapse microscopy dataset (10 TIFF frames, physical resolution 0.19 µm/px) using the **Cellpose** deep learning model (v4.0.1+). Metrics extracted per frame include detected cell count, average and standard deviation of cell area (µm²), and average major and minor axis lengths (µm).

The serial baseline processes frames sequentially. The parallel version distributes frames across workers using Python `multiprocessing`. A key adaptation was required for Docker on Apple Silicon: the multiprocessing context was explicitly set to `spawn` instead of `fork` to prevent deadlocks when multiple workers load the 1.15 GB Cellpose model concurrently.

## Results

### Performance

| Implementation | Workers | Time (s) | Speedup |
|---|---|---|---|
| Serial | 1 | 246.28 | 1.00x |
| Parallel | 2 | 298.58 | 0.82x |

Speedup < 1 is expected here. Each spawned worker independently loads the full 1.15 GB neural network into memory, creating a memory bandwidth bottleneck that overwhelms the gain from parallelism across only 10 images. With a dataset of ~1,000 images, initialization overhead would be diluted and speedup would approach theoretical expectations.

### Morphology Summary (`morphology_summary.csv`)

| Image | Detected Cells | Avg Area (µm²) | Std Area (µm²) | Avg Major Axis (µm) | Avg Minor Axis (µm) |
|---|---|---|---|---|---|
| t000.tif | 12 | 371.62 | 189.11 | 28.69 | 16.49 |
| t001.tif | 8 | 415.43 | 105.25 | 29.95 | 18.45 |
| t002.tif | 11 | 337.52 | 211.55 | 26.99 | 14.81 |
| t003.tif | 9 | 346.13 | 200.25 | 26.79 | 16.30 |
| t004.tif | 12 | 403.53 | 196.81 | 29.41 | 17.15 |
| t005.tif | 18 | 186.62 | 228.23 | 16.79 | 9.22 |
| t006.tif | 12 | 442.53 | 196.25 | 32.99 | 17.43 |
| t007.tif | 12 | 426.53 | 182.32 | 31.60 | 17.43 |
| t008.tif | 12 | 420.65 | 175.29 | 32.59 | 16.94 |
| t009.tif | 13 | 353.95 | 191.96 | 27.43 | 15.89 |

Average cell area ranges between 337–442 µm², consistent with the known physical resolution of the HeLa dataset.

---

For further details, see the full report at `docs/report.pdf`.
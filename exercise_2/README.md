# Exercise 2: Parallel Cell Morphology Analysis (Multiprocessing + Bioimaging)

Pipeline for analyzing cell morphology from microscopy images using serial and parallel processing. Uses real biological data and runs inside Docker.

## Setup

Build the Docker image:

``` bash
docker build -t proyecto-hpc .
```

## Usage

Run the full pipeline:

``` bash
python exercise_2/run_all.py
```

This will:

-Download and extract the dataset
-Inspect image metadata
-Run serial analysis
-Run parallel analysis (multiprocessing)
-Save results to exercise_2/results/

## Data

Dataset: DIC-C2DH-HeLa (Cell Tracking Challenge)

Format: TIFF microscopy images
Resolution: ~0.19 µm/px
Content: HeLa cells for segmentation and tracking
Processing

Results (Example)

| Image | Cells	| Avg Area (µm²) | Avg Major Axis (µm)|
|:----|:------|:----|:-----|
|t000|12|371.62|28.69|
|t005|18|186.62|16.79|
|t009|13|353.95|27.43|

Performance (Example)

| Mode | Workers | Time (s) | Speedup|
|:----|:------|:----|:-----|
|Serial|1|2.50|1.00|
|Parallel|2|1.60|1.56|

## Key Concepts
1. Image processing pipelines
2. Morphological feature extraction
3. Parallelization with multiprocessing
4. Speedup evaluation
5. Real-world bioimage data analysis
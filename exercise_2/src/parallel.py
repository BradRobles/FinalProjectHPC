import multiprocessing as mp
from multiprocessing import Pool
from src.segmentation import CellAnalyzer

def worker_task(path):
    # Cada worker carga su propio modelo de forma aislada y limpia
    analyzer = CellAnalyzer()
    return analyzer.process_image(path)

def process_parallel(image_paths, n_workers):
    context = mp.get_context('spawn')
    with context.Pool(processes=n_workers) as pool:
        results = pool.map(worker_task, image_paths)
    return results
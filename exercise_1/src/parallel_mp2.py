import numpy as np
import pandas as pd
import multiprocessing as mp
import time
import math
from utils import generate_dense_matrices, validate_result

# ==========================================
# Funciones Worker
# ==========================================

def multiply_row_chunk(chunk_A, B):
    return np.dot(chunk_A, B)

def multiply_col_chunk(A, chunk_B):
    return np.dot(A, chunk_B)

def multiply_block(block_A, block_B):
    return np.dot(block_A, block_B)

# ==========================================
# Lógica de Partición
# ==========================================

def parallel_multiply_rows(A, B, num_workers):
    chunks_A = np.array_split(A, num_workers, axis=0)
    args = [(chunk, B) for chunk in chunks_A]
    with mp.Pool(processes=num_workers) as pool:
        results = pool.starmap(multiply_row_chunk, args)
    return np.vstack(results)

def parallel_multiply_cols(A, B, num_workers):
    chunks_B = np.array_split(B, num_workers, axis=1)
    args = [(A, chunk) for chunk in chunks_B]
    with mp.Pool(processes=num_workers) as pool:
        results = pool.starmap(multiply_col_chunk, args)
    return np.hstack(results)


def parallel_multiply_blocks(A, B, num_workers):
    grid_size = int(math.sqrt(num_workers))
    workers_to_use = grid_size * grid_size
    
    A_rows = np.array_split(A, grid_size, axis=0)
    B_cols = np.array_split(B, grid_size, axis=1)
    
    args = []
    for i in range(grid_size):
        for j in range(grid_size):
            args.append((A_rows[i], B_cols[j]))
            
    with mp.Pool(processes=workers_to_use) as pool:
        results = pool.starmap(multiply_block, args)
        
    C_blocks = []
    for i in range(grid_size):
        row_blocks = results[i*grid_size : (i+1)*grid_size]
        C_blocks.append(np.hstack(row_blocks))
        
    return np.vstack(C_blocks)

# ==========================================
# Ejecución y Pruebas
# ==========================================

if __name__ == '__main__':
    size = 512
    num_workers = mp.cpu_count()
    
    print(f"Generando matrices de {size}x{size}...")
    A, B = generate_dense_matrices(size)
    C_true = np.dot(A, B)
    
    results = []
    
    # 1. Filas
    start_time = time.time()
    C_rows = parallel_multiply_rows(A, B, num_workers)
    results.append({'Method': 'Rows', 'Size': size, 'Workers': num_workers, 'Time_s': time.time() - start_time})
    
    # 2. Columnas
    start_time = time.time()
    C_cols = parallel_multiply_cols(A, B, num_workers)
    results.append({'Method': 'Cols', 'Size': size, 'Workers': num_workers, 'Time_s': time.time() - start_time})
    
    # 3. Bloques
    start_time = time.time()
    C_blocks = parallel_multiply_blocks(A, B, num_workers)
    workers_used = int(math.sqrt(num_workers))**2
    results.append({'Method': 'Blocks (2D)', 'Size': size, 'Workers': workers_used, 'Time_s': time.time() - start_time})
    
    df_results = pd.DataFrame(results)
    print("\nResumen de resultados (Multiprocessing):")
    print(df_results)

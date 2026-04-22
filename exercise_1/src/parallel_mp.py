import numpy as np
import pandas as pd
import multiprocessing as mp
import time
from utils import generate_dense_matrices, validate_result

# ==========================================
# Funciones Worker
# ==========================================

def multiply_row_chunk(chunk_A, B):
    return np.dot(chunk_A, B)

def multiply_col_chunk(A, chunk_B):
    return np.dot(A, chunk_B)

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

# ==========================================
# Ejecución y Pruebas
# ==========================================

if __name__ == '__main__':
    size = 256 
    num_workers = mp.cpu_count()
    
    print(f"Generando matrices de {size}x{size}...")
    A, B = generate_dense_matrices(size)
    C_true = np.dot(A, B)
    
    results = []
    
    # Prueba 1: Por Filas
    print(f"\nEjecutando partición por FILAS con {num_workers} workers...")
    start_time = time.time()
    C_rows = parallel_multiply_rows(A, B, num_workers)
    time_rows = time.time() - start_time
    is_correct_rows = validate_result(C_rows, C_true)
    
    results.append({
        'Method': 'Parallel_Rows',
        'Matrix_Size': size,
        'Workers': num_workers,
        'Execution_Time_s': time_rows,
        'Correct': is_correct_rows
    })
    
    # Prueba 2: Por Columnas
    print(f"Ejecutando partición por COLUMNAS con {num_workers} workers...")
    start_time = time.time()
    C_cols = parallel_multiply_cols(A, B, num_workers)
    time_cols = time.time() - start_time
    is_correct_cols = validate_result(C_cols, C_true)
    
    results.append({
        'Method': 'Parallel_Cols',
        'Matrix_Size': size,
        'Workers': num_workers,
        'Execution_Time_s': time_cols,
        'Correct': is_correct_cols
    })
    
    df_results = pd.DataFrame(results)
    print("\nResumen de resultados paralelos:")
    print(df_results)

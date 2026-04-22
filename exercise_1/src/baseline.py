import numpy as np
import pandas as pd
import time
from utils import generate_dense_matrices, validate_result

def serial_matrix_multiply(A, B):
    n = A.shape[0]
    C = np.zeros((n, n))
    
    for i in range(n):
        for k in range(n):
            for j in range(n):
                C[i, j] += A[i, k] * B[k, j]
    return C

def run_serial_experiments(sizes):
    results = []
    
    print("Iniciando experimentos seriales...")
    for size in sizes:
        A, B = generate_dense_matrices(size)
        
        start_time = time.time()
        C_serial = serial_matrix_multiply(A, B)
        end_time = time.time()
        
        exec_time = end_time - start_time
        
        C_true = np.dot(A, B)
        is_correct = validate_result(C_serial, C_true)
        
        results.append({
            'Method': 'Serial',
            'Matrix_Size': size,
            'Execution_Time_s': exec_time,
            'Correct': is_correct
        })
        print(f"Tamaño: {size}x{size} | Tiempo: {exec_time:.4f}s | Correcto: {is_correct}")
        
    return pd.DataFrame(results)

if __name__ == '__main__':

    # BLOQUE DE PRUEBA	
    test_sizes = [64, 128, 256] 
    df_results = run_serial_experiments(test_sizes)
    
    print("\nResumen de resultados:")
    print(df_results)

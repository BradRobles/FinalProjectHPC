import numpy as np
import pandas as pd
import time
from utils import generate_dense_matrices, validate_result

def strassen_multiply(A, B, threshold=64):
    n = A.shape[0]
    
    if n <= threshold:
        return np.dot(A, B)

    mid = n // 2
    A11, A12 = A[:mid, :mid], A[:mid, mid:]
    A21, A22 = A[mid:, :mid], A[mid:, mid:]
    
    B11, B12 = B[:mid, :mid], B[:mid, mid:]
    B21, B22 = B[mid:, :mid], B[mid:, mid:]

    P1 = strassen_multiply(A11 + A22, B11 + B22, threshold)
    P2 = strassen_multiply(A21 + A22, B11, threshold)
    P3 = strassen_multiply(A11, B12 - B22, threshold)
    P4 = strassen_multiply(A22, B21 - B11, threshold)
    P5 = strassen_multiply(A11 + A12, B22, threshold)
    P6 = strassen_multiply(A21 - A11, B11 + B12, threshold)
    P7 = strassen_multiply(A12 - A22, B21 + B22, threshold)

    C11 = P1 + P4 - P5 + P7
    C12 = P3 + P5
    C21 = P2 + P4
    C22 = P1 - P2 + P3 + P6

    C = np.vstack((np.hstack((C11, C12)), np.hstack((C21, C22))))
    return C

if __name__ == '__main__':
    size = 512 
    
    print(f"Generando matrices densas de {size}x{size} para prueba Strassen...")
    A, B = generate_dense_matrices(size)
    C_true = np.dot(A, B)
    
    results = []
    
    # 1. Prueba: Baseline NumPy
    start_time = time.time()
    C_numpy = np.dot(A, B)
    time_numpy = time.time() - start_time
    results.append({'Method': 'NumPy Baseline', 'Time_s': time_numpy})
    
    # 2. Prueba: Strassen Puro (Umbral de 1, fuerza recursión hasta bloques de 1x1)
    print("\nEjecutando Strassen Puro (Esto tomará unos segundos por el overhead)...")
    start_time = time.time()
    # Usamos un umbral bajo pero no 1 para no congelar tu Mac, 16 es suficiente para ver la lentitud
    C_strassen_pure = strassen_multiply(A, B, threshold=16) 
    time_strassen_pure = time.time() - start_time
    is_correct_pure = validate_result(C_strassen_pure, C_true)
    results.append({'Method': 'Strassen Puro (th=16)', 'Time_s': time_strassen_pure})
    
    # 3. Prueba: Strassen Híbrido (Umbral de 128)
    print("Ejecutando Strassen Híbrido...")
    start_time = time.time()
    C_strassen_hybrid = strassen_multiply(A, B, threshold=128)
    time_strassen_hybrid = time.time() - start_time
    is_correct_hybrid = validate_result(C_strassen_hybrid, C_true)
    results.append({'Method': 'Strassen Híbrido (th=128)', 'Time_s': time_strassen_hybrid})
    
    df_results = pd.DataFrame(results)
    print("\n=== Resumen de Resultados (Strassen) ===")
    print(df_results)
    print(f"\nExactitud de los cálculos: {is_correct_pure and is_correct_hybrid}")

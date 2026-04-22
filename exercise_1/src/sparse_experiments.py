import numpy as np
import time
from scipy import sparse
from utils import load_sparse_matrix

def run_sparse_analysis(matrix_path, num_workers=4):
    print(f"\n{'='*50}")
    print(f"Analizando Matriz: {matrix_path.split('/')[-1]}")
    print(f"{'='*50}")
    
    start_load = time.time()
    A_sparse = load_sparse_matrix(matrix_path)
    print(f"(Tiempo de carga: {time.time() - start_load:.4f}s)")
    
    n = A_sparse.shape[0]
    
    non_zeros = A_sparse.nnz
    total_elements = n * n
    sparsity = 100 * (1 - (non_zeros / total_elements))
    
    print(f"\n[Metadatos de la Matriz]")
    print(f"Tamaño                  : {n}x{n}")
    print(f"Elementos Totales       : {total_elements}")
    print(f"Elementos No Cero (nnz) : {non_zeros}")
    print(f"Porcentaje de ceros     : {sparsity:.2f}% (Sparsity)")
    
    B_sparse = A_sparse.copy()
    start_mul = time.time()
    C_sparse = A_sparse.dot(B_sparse) 
    time_sparse = time.time() - start_mul
    
    print(f"\n[Rendimiento]")
    print(f"Tiempo Multiplicación Dispersa (CSR) : {time_sparse:.6f}s")
    
    print("\n[Análisis de Desequilibrio de Carga - Partición por 4 Filas]")
    chunk_size = n // num_workers
    
    for i in range(num_workers):
        start_row = i * chunk_size
        end_row = (i + 1) * chunk_size if i != num_workers - 1 else n 
        
        row_chunk = A_sparse[start_row:end_row, :]
        nnz_in_chunk = row_chunk.nnz
        porcentaje_trabajo = (nnz_in_chunk / non_zeros) * 100
        
        print(f"Worker {i} (Filas {start_row}-{end_row-1:4d}) : Recibe {nnz_in_chunk:5d} operaciones ({porcentaje_trabajo:.1f}% de la carga total)")

if __name__ == '__main__':
    try:
        # 1. Matriz de Red Eléctrica
        run_sparse_analysis("data/bcspwr08.mtx")
        
        # 2. Matriz Estructural
        run_sparse_analysis("data/bcsstk18.mtx")
        
        print("\n" + "="*50)
        print("Conclusión para el reporte:")
        print("Si el porcentaje de carga (% de operaciones) varía mucho entre workers,")
        print("sufrimos de 'Load Imbalance'. El worker con más carga será el cuello de botella,")
        print("mientras los demás se quedan ociosos esperando a que termine.")
        print("="*50 + "\n")
        
    except FileNotFoundError as e:
        print(f"\n[ERROR] No se encontró el archivo: {e}")
        print("Asegúrate de que 'bcspwr08.mtx' y 'bcsstk18.mtx' estén dentro de la carpeta 'data/'.")

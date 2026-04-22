import numpy as np
import time
from mpi4py import MPI
from utils import generate_dense_matrices, validate_result

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    matrix_size = 512
    
    if rank == 0:
        print(f"[Rank 0] Generando matrices de {matrix_size}x{matrix_size} para {size} procesos...")
        A, B = generate_dense_matrices(matrix_size)
        
        # Nota: np.array_split devuelve una lista de sub-arreglos
        chunks_A = np.array_split(A, size, axis=0)
        C_true = np.dot(A, B)
    else:
        chunks_A = None
        B = None

    # Sincronizamos el tiempo de inicio
    comm.Barrier()
    start_time = MPI.Wtime()

    # 1. BROADCAST: El maestro envía la matriz B completa a TODOS los procesos
    B = comm.bcast(B, root=0)

    # 2. SCATTER: El maestro reparte un pedazo de A (chunk_A) a cada proceso
    local_A = comm.scatter(chunks_A, root=0)

    # 3. COMPUTACIÓN: Cada trabajador (incluido el maestro) hace su parte
    local_C = np.dot(local_A, B)

    # 4. GATHER: El maestro recolecta los resultados parciales de todos los trabajadores
    gathered_C = comm.gather(local_C, root=0)

    comm.Barrier()
    end_time = MPI.Wtime()

    if rank == 0:
        C_final = np.vstack(gathered_C)
        exec_time = end_time - start_time
        is_correct = validate_result(C_final, C_true)
        
        print("\n=== Resumen de Resultados (MPI) ===")
        print(f"Método      : MPI (Distributed Memory)")
        print(f"Workers     : {size}")
        print(f"Tiempo (s)  : {exec_time:.6f}")
        print(f"Correcto    : {is_correct}")
        
        print("\nNota para el reporte: Este tiempo incluye el overhead de serializar")
        print("y enviar/recibir mensajes a través de MPI (bcast, scatter, gather).")

if __name__ == '__main__':
    main()

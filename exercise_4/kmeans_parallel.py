import numpy as np
import time
import sys
from mpi4py import MPI
from data_loader import load_and_preprocess_covertype # Importamos la función de carga de datos

def kmeans_parallel(X_global, n_clusters, comm, rank, size, max_iters=100, tol=1e-4):
    """
    Implementación paralela del algoritmo K-Means utilizando mpi4py.

    Args:
        X_global (np.array): El dataset completo (solo es relevante en el proceso raíz).
        n_clusters (int): Número de clusters (K).
        comm (MPI.Comm): Objeto comunicador de MPI.
        rank (int): Rango del proceso actual.
        size (int): Número total de procesos.
        max_iters (int): Número máximo de iteraciones para el algoritmo.
        tol (float): Tolerancia para la condición de convergencia de los centroides.

    Returns:
        tuple:
            - centroids (np.array): Los centroides finales de los clusters (solo en el proceso raíz).
            - global_labels (np.array): Las etiquetas de cluster asignadas a cada punto de datos (solo en el proceso raíz).
    """
    # Obtener el número de características. Solo el proceso raíz lo sabe inicialmente.
    n_features = X_global.shape[1] if rank == 0 else 0
    # Broadcast del número de características a todos los procesos.
    n_features = comm.bcast(n_features, root=0)

    # 1. Distribución de datos (Scatterv):
    # El proceso raíz divide el dataset global en bloques y los distribuye a todos los procesos.
    # Se usa Scatterv para manejar bloques de datos de tamaño potencialmente variable.
    local_X = None
    if rank == 0:
        # Asegurarse de que X_global sea un array de numpy para Scatterv
        if not isinstance(X_global, np.ndarray):
            X_global = np.array(X_global)
        
        # Calcular el tamaño de cada chunk para cada proceso
        avg_chunk_size = X_global.shape[0] // size
        remainder = X_global.shape[0] % size
        
        sendcounts = [avg_chunk_size + 1 if i < remainder else avg_chunk_size for i in range(size)]
        displs = [sum(sendcounts[:i]) for i in range(size)]
        
        # Crear el buffer de recepción para el proceso raíz
        local_X = np.empty((sendcounts[rank], n_features), dtype=X_global.dtype)
    else:
        # Los procesos no raíz reciben sendcounts y displs del root
        sendcounts = None
        displs = None
        # Se inicializa local_X con un tamaño temporal, el tamaño real se ajustará con Scatterv
        local_X = np.empty((0, n_features), dtype=np.float64) 

    # Broadcast de sendcounts y displs para que todos los procesos conozcan la distribución
    sendcounts = comm.bcast(sendcounts, root=0)
    displs = comm.bcast(displs, root=0)

    # Ajustar el tamaño de local_X para los procesos no raíz antes de Scatterv
    if rank != 0:
        local_X = np.empty((sendcounts[rank], n_features), dtype=np.float64)

    # Realizar la distribución de datos
    comm.Scatterv([X_global, sendcounts, displs, MPI.DOUBLE], local_X, root=0)
    
    n_local_samples = local_X.shape[0]
    
    # 2. Inicialización de centroides (solo en el proceso raíz, luego Broadcast):
    centroids = None
    if rank == 0:
        # Inicialización aleatoria de centroides en el proceso raíz a partir del dataset global.
        random_indices = np.random.choice(X_global.shape[0], n_clusters, replace=False)
        centroids = X_global[random_indices].astype(np.float64)
        print(f"Proceso {rank}: Centroides iniciales generados.")
    
    # Broadcast de los centroides iniciales a todos los procesos.
    # Todos los procesos necesitan los mismos centroides para el paso E.
    centroids = comm.bcast(centroids, root=0)
    
    if rank == 0:
        print(f"\n--- Iniciando K-Means paralelo con {n_clusters} clusters ---")
        print(f"Máximo de iteraciones: {max_iters}, Tolerancia de convergencia: {tol}")

    # Bucle principal de K-Means
    for i in range(max_iters):
        # 3. Paso de Asignación (E-step) - Local:
        # Cada proceso calcula las distancias y asigna etiquetas solo para su bloque de datos local.
        distances = np.sqrt(((local_X - centroids[:, np.newaxis])**2).sum(axis=2))
        local_labels = np.argmin(distances, axis=0)

        # 4. Paso de Actualización (M-step) - Local:
        # Cada proceso calcula la suma local de puntos y el conteo de puntos
        # para cada cluster dentro de su bloque de datos.
        local_sums = np.zeros((n_clusters, n_features), dtype=np.float64)
        local_counts = np.zeros(n_clusters, dtype=int)

        for k in range(n_clusters):
            points_in_cluster = local_X[local_labels == k]
            if len(points_in_cluster) > 0:
                local_sums[k] = points_in_cluster.sum(axis=0)
                local_counts[k] = len(points_in_cluster)
        
        # 5. Agregación global de sumas y conteos (Allreduce):
        # Se utiliza Allreduce para sumar las contribuciones locales de todos los procesos.
        # Esto permite que cada proceso obtenga las sumas y conteos globales para calcular
        # los nuevos centroides sin necesidad de una comunicación adicional.
        global_sums = np.zeros((n_clusters, n_features), dtype=np.float64)
        global_counts = np.zeros(n_clusters, dtype=int)

        comm.Allreduce(local_sums, global_sums, op=MPI.SUM)
        comm.Allreduce(local_counts, global_counts, op=MPI.SUM)

        # Calcular nuevos centroides globales
        new_centroids = np.zeros((n_clusters, n_features), dtype=np.float64)
        for k in range(n_clusters):
            if global_counts[k] > 0:
                new_centroids[k] = global_sums[k] / global_counts[k]
            else:
                # Si un cluster está vacío globalmente, se mantiene el centroide anterior
                # para evitar divisiones por cero o centroides erráticos.
                new_centroids[k] = centroids[k]

        # 6. Comprobación de Convergencia (Broadcast):
        # Solo el proceso raíz verifica la convergencia y luego difunde el resultado.
        converged = False
        if rank == 0:
            if np.all(np.abs(new_centroids - centroids) < tol):
                converged = True
                print(f"Proceso {rank}: K-Means paralelo convergió en la iteración {i+1}.")
            # else:
            #     print(f"Proceso {rank}: Iteración {i+1}, no ha convergido.")
        
        # Broadcast del estado de convergencia a todos los procesos.
        converged = comm.bcast(converged, root=0)

        centroids = new_centroids # Actualizar centroides para la próxima iteración

        if converged:
            break
    else:
        if rank == 0:
            print(f"Proceso {rank}: K-Means paralelo alcanzó el número máximo de iteraciones ({max_iters}) sin converger.")


    # 7. Recolección de etiquetas globales (Gatherv):
    # Forzamos el uso de np.int32 para que coincida exactamente con el estándar MPI.INT
    local_labels_32 = local_labels.astype(np.int32)
    local_labels_count = len(local_labels_32)
    
    # Todos los procesos envían su conteo local al root (rank 0)
    all_labels_counts = comm.gather(local_labels_count, root=0)

    global_labels = None
    if rank == 0:
        total_samples = sum(all_labels_counts)
        # El buffer global debe tener el tamaño total exacto y ser int32
        global_labels = np.empty(total_samples, dtype=np.int32)
        
        # Calcular los desplazamientos (offsets) exactos para cada bloque en el buffer global
        displs_labels = [sum(all_labels_counts[:i]) for i in range(size)]
        
        # Recolección con tipos de datos emparejados (np.int32 <-> MPI.INT)
        comm.Gatherv(sendbuf=local_labels_32, 
                     recvbuf=[global_labels, all_labels_counts, displs_labels, MPI.INT], 
                     root=0)
    else:
        # Los procesos que no son raíz envían su parte al root
        comm.Gatherv(sendbuf=local_labels_32, recvbuf=None, root=0)

    return centroids, global_labels


if __name__ == "__main__":
    # Añade esta importación al inicio o aquí
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # Tarea 5: Permitir cambiar K desde la terminal
    # Uso: mpirun -n 4 python kmeans_parallel.py 10
    n_clusters = int(sys.argv[1]) if len(sys.argv) > 1 else 7

    X_data = None
    if rank == 0:
        X_data, _ = load_and_preprocess_covertype()

    comm.Barrier() 
    start_time_parallel = time.time()
    final_centroids, _ = kmeans_parallel(X_data, n_clusters, comm, rank, size)
    end_time_parallel = time.time()
    comm.Barrier() 

    if rank == 0:
        print(f"\nRESULTADO_BENCHMARK: Procesos={size}, Clusters={n_clusters}, Tiempo={end_time_parallel - start_time_parallel:.4f}")
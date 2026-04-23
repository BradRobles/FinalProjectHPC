import numpy as np
import time
from data_loader import load_and_preprocess_covertype # Importamos la función de carga de datos

def kmeans_serial(X, n_clusters, max_iters=100, tol=1e-4):
    """
    Implementación serial del algoritmo K-Means.

    Args:
        X (np.array): El dataset de entrada (características).
        n_clusters (int): Número de clusters (K).
        max_iters (int): Número máximo de iteraciones para el algoritmo.
        tol (float): Tolerancia para la condición de convergencia de los centroides.

    Returns:
        tuple:
            - centroids (np.array): Los centroides finales de los clusters.
            - labels (np.array): Las etiquetas de cluster asignadas a cada punto de datos.
    """
    n_samples, n_features = X.shape

    # 1. Inicialización de centroides:
    # Se seleccionan 'n_clusters' puntos de datos aleatorios del dataset
    # como los centroides iniciales. Esto es una estrategia común y sencilla.
    random_indices = np.random.choice(n_samples, n_clusters, replace=False)
    centroids = X[random_indices].astype(np.float64) # Aseguramos el tipo de dato float64

    print(f"\n--- Iniciando K-Means serial con {n_clusters} clusters ---")
    print(f"Máximo de iteraciones: {max_iters}, Tolerancia de convergencia: {tol}")

    for i in range(max_iters):
        # 2. Paso de Asignación (E-step - Expectation):
        # Para cada punto de datos, se calcula la distancia euclidiana a cada centroide.
        # np.newaxis se usa para permitir el broadcasting y calcular distancias eficientemente.
        distances = np.sqrt(((X - centroids[:, np.newaxis])**2).sum(axis=2))
        # Cada punto se asigna al centroide más cercano.
        labels = np.argmin(distances, axis=0)

        # 3. Paso de Actualización (M-step - Maximization):
        # Se calculan los nuevos centroides como la media de todos los puntos
        # asignados a cada cluster.
        new_centroids = np.array([X[labels == k].mean(axis=0) if np.any(labels == k) else centroids[k]
                                  for k in range(n_clusters)])
        
        # Manejo de clusters vacíos: Si un cluster no tiene puntos asignados,
        # su centroide se mantiene igual que en la iteración anterior para evitar NaN.
        # La condición `if np.any(labels == k)` ya lo maneja, pero se puede añadir
        # una verificación explícita si se desea.

        # 4. Comprobación de Convergencia:
        # El algoritmo converge si la posición de los centroides no cambia
        # significativamente entre iteraciones (cambio menor que 'tol').
        if np.all(np.abs(new_centroids - centroids) < tol):
            print(f"K-Means serial convergió en la iteración {i+1}.")
            centroids = new_centroids
            break
        
        centroids = new_centroids # Actualizar centroides para la próxima iteración
    else:
        print(f"K-Means serial alcanzó el número máximo de iteraciones ({max_iters}) sin converger.")

    return centroids, labels

if __name__ == "__main__":
    # Bloque principal para ejecutar el K-Means serial
    # Se carga y preprocesan el dataset Covertype.
    X_data, y_labels_true = load_and_preprocess_covertype()

    # Parámetros para el algoritmo K-Means
    n_clusters = 7 # El dataset Covertype tiene 7 clases, un buen punto de partida.

    print("\n--- Ejecutando K-Means Serial ---")
    start_time = time.time() # Inicio de la medición de tiempo
    final_centroids_serial, assigned_labels_serial = kmeans_serial(X_data, n_clusters)
    end_time = time.time() # Fin de la medición de tiempo

    execution_time = end_time - start_time
    print(f"\nK-Means serial completado en {execution_time:.4f} segundos.")
    print(f"Forma de los centroides finales: {final_centroids_serial.shape}")
    # print(f"Primeras 10 etiquetas asignadas: {assigned_labels_serial[:10]}") # Opcional para inspección

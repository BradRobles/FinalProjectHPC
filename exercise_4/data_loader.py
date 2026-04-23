import pandas as pd
from sklearn.datasets import fetch_covtype
from sklearn.preprocessing import StandardScaler
import numpy as np

def load_and_preprocess_covertype():
    """
    Carga el dataset Covertype, realiza un escalado de características
    y describe sus propiedades principales.

    Returns:
        tuple: Un numpy array (X_scaled) con las características escaladas
               y un numpy array (y) con las etiquetas del dataset.
    """
    print("--- Iniciando carga y preprocesamiento del dataset Covertype ---")

    # Carga del dataset Covertype
    # fetch_covtype descarga y carga el dataset de forma eficiente.
    # Retorna un objeto Bunch similar a un diccionario.
    covtype = fetch_covtype()
    X = covtype.data  # Características del dataset
    y = covtype.target # Etiquetas de clase (tipo de cubierta forestal)

    print(f"Dimensiones originales del dataset: {X.shape}")
    print(f"Número de características (features): {X.shape[1]}")
    print(f"Número de muestras (observaciones): {X.shape[0]}")
    print(f"Clases de etiquetas únicas: {np.unique(y)}")
    # Opcional: Mostrar las primeras filas para inspección
    # print(f"Descripción de las características (primeras 5 filas):\n{pd.DataFrame(X).head()}")

    print("\n--- Realizando escalado de características (StandardScaler) ---")
    # Escalado de características: K-Means es sensible a la escala de los datos.
    # StandardScaler normaliza las características para que tengan media 0 y varianza 1.
    # Esto asegura que todas las características contribuyan por igual a la distancia euclidiana.
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    print(f"Dimensiones del dataset escalado: {X_scaled.shape}")
    # Opcional: Mostrar las primeras filas del dataset escalado
    # print(f"Descripción de las características escaladas (primeras 5 filas):\n{pd.DataFrame(X_scaled).head()}")

    print("--- Carga y preprocesamiento completados ---")
    return X_scaled, y

if __name__ == "__main__":
    # Este bloque se ejecuta solo si el script se corre directamente.
    # Permite una inspección rápida de la función de carga.
    X_data, y_labels = load_and_preprocess_covertype()
    print(f"\nDataset listo para K-Means: X_data.shape={X_data.shape}, y_labels.shape={y_labels.shape}")

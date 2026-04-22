import os
import subprocess
import platform

def run_command(command, description):
    print(f"\n{'-'*60}")
    print(f"-> {description}")
    print(f"{'-'*60}\n")
    
    # subprocess.run ejecuta el comando en la terminal nativa del usuario
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError:
        print(f"\n[ERROR] Falló la ejecución de: {description}")
        print("Continuando con la siguiente prueba...\n")

def main():
    # Detectamos el sistema operativo para limpiar la pantalla correctamente
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

    print("========================================================")
    print("   EJECUTANDO TODAS LAS PRUEBAS DEL EJERCICIO 1")
    print("========================================================\n")

    current_dir = os.getcwd()
    image = "proyecto-hpc"

    # Definimos la base del comando Docker asegurando la compatibilidad de rutas
    docker_base = f'docker run --rm -v "{current_dir}:/app" {image}'

    # 1. Baseline
    run_command(f"{docker_base} python src/baseline.py", 
                "1. Ejecutando Baseline Serial O(n^3)...")

    # 2. Multiprocessing
    run_command(f"{docker_base} python src/parallel_mp.py", 
                "2. Ejecutando Multiprocessing (Filas, Columnas, Bloques)...")

    # 3. Multiprocessing Actualizado
    run_command(f"{docker_base} python src/parallel_mp2.py", 
                "2. Ejecutando Multiprocessing Actualizado (Filas, Columnas, Bloques)...")

    # 4. MPI
    run_command(f"{docker_base} mpirun -n 4 python src/parallel_mpi.py", 
                "3. Ejecutando Memoria Distribuida (MPI - 4 Workers)...")

    # 5. Sparse Matrices
    run_command(f"{docker_base} python src/sparse_experiments.py", 
                "4. Ejecutando Análisis de Matrices Dispersas (Sparsity)...")

    # 6. Strassen
    run_command(f"{docker_base} python src/strassen.py", 
                "5. Ejecutando Algoritmo Híbrido de Strassen...")

    print("\n========================================================")
    print("   PRUEBAS FINALIZADAS CON ÉXITO")
    print("========================================================")

if __name__ == "__main__":
    main()

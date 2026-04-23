import os
import subprocess
import platform

def run_command(command, description):
    print(f"\n{'-'*60}")
    print(f"-> {description}")
    print(f"{'-'*60}\n")
    
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError:
        print(f"\n[ERROR] Falló la ejecución de: {description}")
        print("Revisa los logs de Docker para más detalles.\n")

def main():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

    print("========================================================")
    print("   EJECUTANDO BARRIDO DE PRUEBAS DEL EJERCICIO 4")
    print("========================================================\n")

    current_dir = os.getcwd()
    project_root = os.path.abspath(os.path.join(current_dir, ".."))
    image = "proyecto-hpc"

    # Base del comando Docker
    docker_base = f'docker run --rm -v "{project_root}:/app" -w /app {image}'

    # --- PASO 1: Preparación de Datos ---
    run_command(f"{docker_base} python exercise_4/data_loader.py", 
                "1. Generando / Cargando el dataset para K-Means...")

    # Valores para nuestras pruebas
    k_values = [7, 10]
    n_processes = [1, 2, 4]

    # --- PASO 2: Ejecución Serial ---
    # Asumo que el serial también recibe el número de clusters 'k' como argumento.
    # Si no es así y el k está fijo por dentro, solo quítale el "{k}" al comando.
    for k in k_values:
        run_command(f"{docker_base} python -u exercise_4/kmeans_serial.py {k}", 
                    f"2. Ejecutando K-Means en modo Serial (Baseline) con k={k}...")

    # --- PASO 3: Ejecución Paralela Distribuida (MPI) ---
    # Aquí se ejecutarán las 6 pruebas automáticamente (3 configuraciones de n * 2 valores de k)
    for n in n_processes:
        for k in k_values:
            mpi_command = f"mpiexec --allow-run-as-root -n {n} python -u exercise_4/kmeans_parallel.py {k}"
            
            run_command(f"{docker_base} {mpi_command}", 
                        f"3. Ejecutando K-Means (MPI) con n={n} workers y k={k}...")

    print("\n========================================================")
    print("   BARRIDO DE PRUEBAS FINALIZADO")
    print("========================================================\n")

if __name__ == "__main__":
    main()
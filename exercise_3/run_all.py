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
        print(f"\n[ERROR] Falló: {description}\n")

def main():

    # limpiar pantalla
    os.system("cls" if platform.system() == "Windows" else "clear")

    print("========================================================")
    print("   PIPELINE - EXERCISE 3: MPI FOREST FIRE SIMULATION")
    print("========================================================\n")

    # carpeta del proyecto (exercise_3)
    current_dir = os.getcwd()
    project_root = os.path.abspath(current_dir)

    image = "fire-ca-mpi"

    docker_base = f'docker run --rm -v "{project_root}:/app" -w /app {image}'

    # ---------------- SERIAL ----------------
    run_command(
        f"{docker_base} python src/automaton_serial.py",
        "1. Ejecutando simulación SERIAL (baseline)"
    )
    # Cambiar a python3, si usas mac.
    # ---------------- MPI ----------------
    run_command(
        f"{docker_base} mpirun -n 4 python src/automaton_parallel.py",
        "2. Ejecutando simulación PARALELA (MPI)"
    )

    print("\n========================================================")
    print("   PIPELINE COMPLETADO")
    print("   Outputs:")
    print("   - results/frame_*.png")
    print("   - results/final_map.png")
    print("   - results/fire_simulation.gif")
    print("========================================================\n")


if __name__ == "__main__":
    main()
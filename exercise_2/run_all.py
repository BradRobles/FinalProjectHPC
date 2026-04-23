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
        print("Revisa los logs de Docker arriba.\n")

def main():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

    print("========================================================")
    print("   EJECUTANDO EL PIPELINE DEL EJERCICIO 2)")
    print("========================================================\n")

    current_dir = os.getcwd()
    project_root = os.path.abspath(os.path.join(current_dir, ".."))
    
    image = "proyecto-hpc"

    docker_base = f'docker run --rm -v "{project_root}:/app" -w /app {image}'

    run_command(f"{docker_base} python exercise_2/download_data.py", 
                "1. Descargando y preparando el dataset DIC-C2DH-HeLa...")

    run_command(f"{docker_base} python exercise_2/run_analysis.py", 
                "2. Ejecutando Análisis Morfológico (Serial vs Paralelo)...")

    print("\n========================================================")
    print("   PROCESAMIENTO FINALIZADO")
    print(f"   Resultados disponibles en la carpeta 'results'")
    print("========================================================\n")

if __name__ == "__main__":
    main()
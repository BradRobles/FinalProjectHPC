import os
import time
import glob
import pandas as pd
from src.segmentation import CellAnalyzer
from src.parallel import process_parallel
from src.utils import summarize_results

def get_image_paths(data_dir, limit=10):
    pattern = os.path.join(data_dir, "DIC-C2DH-HeLa", "01", "*.tif")
    return sorted(glob.glob(pattern))[:limit]

def main():
    os.makedirs("exercise_2/results", exist_ok=True)
    
    image_paths = get_image_paths("exercise_2/data", limit=10)
    if not image_paths:
        print("No hay imágenes. Ejecuta 'python exercise_2/download_data.py' primero.")
        return

    print(f"Iniciando análisis morfológico de {len(image_paths)} imágenes...\n")

    # === TAREA 2 Y 7: PIPELINE SERIAL ===
    print("--- 1. Ejecutando Pipeline Serial ---")
    analyzer = CellAnalyzer()
    
    start_time = time.time()
    serial_data = []
    for path in image_paths:
        data = analyzer.process_image(path)
        serial_data.append((path, data))
        
    serial_time = time.time() - start_time
    print(f"Tiempo Serial: {serial_time:.2f} segundos\n")

    # Guardar métricas biológicas
    summaries = []
    for path, data in serial_data:
        img_name = os.path.basename(path)
        summary = summarize_results(img_name, data)
        if summary:
            summaries.append(summary)
            
    df_summary = pd.DataFrame(summaries)
    df_summary.to_csv("exercise_2/results/morphology_summary.csv", index=False)
    print("Métricas biológicas guardadas en: results/morphology_summary.csv\n")

    # === TAREA 6 Y 8: PIPELINE PARALELO ===
    print("--- 2. Ejecutando Pipeline Paralelo (Evaluación de Speedup) ---")
    worker_counts = [2] 
    performance_records = []
    
    for w in worker_counts:
        print(f"Lanzando {w} workers...")
        start_time_par = time.time()
        
        _ = process_parallel(image_paths, w)
        
        elapsed = time.time() - start_time_par
        performance_records.append((w, elapsed))
        print(f"Tiempo Paralelo con {w} workers: {elapsed:.2f} segundos")

    # === RESUMEN DE RENDIMIENTO COMPUTACIONAL ===
    print("\n=== RESUMEN DE RENDIMIENTO COMPUTACIONAL ===")
    results_list = [("Serial", 1, serial_time)]
    for w, t in performance_records:
        results_list.append(("Parallel", w, t))
        
    df_times = pd.DataFrame(results_list, columns=["Execution_Mode", "Workers", "Time_Seconds"])
    df_times['Speedup'] = serial_time / df_times['Time_Seconds']
    
    print(df_times.to_string(index=False))

if __name__ == "__main__":
    main()
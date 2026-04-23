import os
import zipfile
import requests
import tifffile

def download_dataset():
    url = "http://data.celltrackingchallenge.net/training-datasets/DIC-C2DH-HeLa.zip"
    zip_path = "exercise_2/data/DIC-C2DH-HeLa.zip"
    extract_path = "exercise_2/data/"

    if not os.path.exists(os.path.join(extract_path, "DIC-C2DH-HeLa")):
        print("--> Descargando dataset DIC-C2DH-HeLa (aprox. 30MB)...")
        response = requests.get(url, stream=True)
        with open(zip_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print("--> Extrayendo archivos...")
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_path)
        os.remove(zip_path)
        print("--> Descarga completada.")
    else:
        print("--> El dataset ya existe localmente.")

def inspect_metadata():
    img_path = "exercise_2/data/DIC-C2DH-HeLa/01/t000.tif"
    if not os.path.exists(img_path):
        return
        
    with tifffile.TiffFile(img_path) as tif:
        image = tif.asarray()
        print("\n=== METADATOS DE LA IMAGEN (Tarea 1) ===")
        print(f"Formato: TIFF")
        print(f"Dimensiones (XY): {image.shape[1]} x {image.shape[0]} px")
        print(f"Tipo de dato: {image.dtype}")
        print(f"Resolución física: 0.19 µm/px (según documentación oficial DIC-C2DH-HeLa)")

if __name__ == "__main__":
    download_dataset()
    inspect_metadata()
import numpy as np
import cv2
import tifffile
from cellpose import models
from skimage.measure import regionprops
import warnings

# Suprimimos warnings molestos de lectura de TIFFs
warnings.filterwarnings("ignore")

class CellAnalyzer:
    def __init__(self, model_type='cyto', gpu=False):
        # FIX: En Cellpose v4+ la clase se renombró a CellposeModel
        self.model = models.CellposeModel(model_type=model_type, gpu=gpu)
        
    def process_image(self, image_path):
        img = tifffile.imread(image_path)
        
        # FIX: En v4, eval() puede devolver diferente cantidad de valores. 
        # Guardamos todo el resultado y extraemos solo la máscara (índice 0).
        resultado = self.model.eval(img, diameter=None, channels=[0,0])
        masks = resultado[0] 
        
        # Tarea 4: Extraer Bounding Box, Área y Ejes
        props = regionprops(masks)
        object_data = []
                
        for prop in props:
            # Tarea 5: Rotated Bounding Box
            # Aislamos la máscara de esta célula específica
            obj_mask = (masks == prop.label).astype(np.uint8)
            contours, _ = cv2.findContours(obj_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            rotated_bbox = None
            if contours:
                # cv2.minAreaRect encuentra el rectángulo más pequeño que envuelve el contorno, 
                # permitiendo rotación, a diferencia del BBox tradicional que es axis-aligned.
                rect = cv2.minAreaRect(contours[0])
                rotated_bbox = cv2.boxPoints(rect).tolist() 
            
            data = {
                'label': prop.label,
                'area': prop.area,
                'bbox': prop.bbox,
                'major_axis': prop.major_axis_length,
                'minor_axis': prop.minor_axis_length,
                'rotated_bbox': rotated_bbox
            }
            object_data.append(data)
            
        return object_data

import pandas as pd

# Resolución estándar del dataset (Micrómetros por píxel)
UM_PER_PX = 0.19 

def convert_to_microns(pixel_value, is_area=False):
    if pd.isna(pixel_value):
        return 0.0
    if is_area:
        return pixel_value * (UM_PER_PX ** 2)
    return pixel_value * UM_PER_PX

def summarize_results(image_id, object_data):
    df = pd.DataFrame(object_data)
    if df.empty:
        return None
        
    return {
        'Image_ID': image_id,
        'Detected_Cells': len(df),
        'Avg_Area_um2': round(convert_to_microns(df['area'].mean(), is_area=True), 2),
        'Std_Area_um2': round(convert_to_microns(df['area'].std(), is_area=True), 2),
        'Avg_Major_Axis_um': round(convert_to_microns(df['major_axis'].mean()), 2),
        'Avg_Minor_Axis_um': round(convert_to_microns(df['minor_axis'].mean()), 2)
    }

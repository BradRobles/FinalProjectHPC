import pandas as pd
import numpy as np
import requests
from io import StringIO

class FirmsLoader:
    def __init__(self, map_key, bbox, grid_size=(400, 400)):
        self.map_key = map_key
        self.bbox = bbox
        self.grid_size = grid_size

    def get_data(self, day_range=1):
        sensors = [
            "VIIRS_NOAA20_NRT",
            "VIIRS_SNPP_NRT",
            "MODIS_NRT"
        ]

        west, south, east, north = self.bbox

        for sensor in sensors:
            url = (
                f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/"
                f"{self.map_key}/{sensor}/"
                f"{west},{south},{east},{north}/{day_range}"
            )

            try:
                response = requests.get(url, timeout=20)

                if response.status_code == 200:
                    df = pd.read_csv(StringIO(response.text))
                    print(f"{sensor}: {len(df)} hotspots")
                    return df

            except:
                pass

        return None

    def create_grid(self, df):
        grid = np.ones(self.grid_size, dtype=int)

        if df is None or df.empty:
            return grid

        west, south, east, north = self.bbox
        rows, cols = self.grid_size

        for _, r in df.iterrows():
            col = int((r["longitude"] - west) / (east - west) * (cols - 1))
            row = int((north - r["latitude"]) / (north - south) * (rows - 1))

            if 0 <= row < rows and 0 <= col < cols:
                grid[row, col] = 2

        return grid
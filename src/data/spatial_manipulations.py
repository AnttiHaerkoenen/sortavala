from pathlib import Path

import pandas as pd
import geopandas as gpd
import numpy as np
import folium

from src.visualization.map import make_web_map

if __name__ == '__main__':
    input_dir = Path('../../data') / 'raw'
    output_dir = Path('../../data') / 'interim'
    map_dir = Path('../../reports/figures')

    map = make_web_map()
    map.save(str(map_dir / 'map.html'))

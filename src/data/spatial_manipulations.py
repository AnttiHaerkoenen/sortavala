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

    layers = [
        'water',
        'blocks',
        'fields',
        'plots',
        'buildings',
        'sheds',
    ]

    for l in layers:
        layer = gpd.read_file(input_dir / f'{l}.shp')
        layer = layer.rotate(-9, origin=(3416357, 8789352)).translate(xoff=50, yoff=-70)
        layer.set_crs(epsg=3857, allow_override=True, inplace=True)
        layer = layer.to_crs(epsg=4326)
        layer.to_file(output_dir / f'{l}.shp')

    map = make_web_map(layers=layers, input_dir=output_dir)
    map.save(str(map_dir / 'map.html'))

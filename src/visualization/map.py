from pathlib import Path

import pandas as pd
import geopandas as gpd
import numpy as np
import folium


def make_web_map(
        *,
        layers=None,
        input_dir,
):
    if not layers:
        layers = []

    map = folium.Map(
        location=(61.703, 30.695),
        zoom_start=15,
    )

    for layer_name in layers:
        layer = gpd.read_file(input_dir / f'{layer_name}.shp')
        layer = layer.to_json()
        folium.GeoJson(
            layer,
            name=layer_name,
        ).add_to(map)

    folium.LayerControl().add_to(map)

    return map


if __name__ == '__main__':
    data_dir = Path('../../data')
    map_dir = Path('../../reports/figures')

    layers = [
        'water',
        'blocks',
        'fields',
        'plots',
        'buildings',
        'sheds'
    ]

    map = make_web_map(layers=layers, input_dir=data_dir / 'interim')
    map.save(str(map_dir / 'map.html'))

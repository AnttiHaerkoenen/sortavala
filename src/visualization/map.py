from pathlib import Path

import pandas as pd
import geopandas as gpd
import numpy as np
import folium


def make_web_map(
        layers=None,
):
    if not layers:
        layers = []

    map = folium.Map(
        location=(61.703, 30.695),
        zoom_start=15,
    )
    for layer_name in layers:
        layer = gpd.read_file(input_dir / f'{layer_name}.shp')
        layer.set_crs(epsg=3857, allow_override=True, inplace=True)
        layer.to_crs(epsg=4326, inplace=True)
        layer = layer.to_json()
        folium.GeoJson(
            layer,
            name=layer_name,
        ).add_to(map)

    folium.LayerControl().add_to(map)

    return map


if __name__ == '__main__':
    input_dir = Path('../../data') / 'raw'
    map_dir = Path('../../reports/figures')

    layers = [
        'water',
        'blocks',
        'fields',
        'plots',
        'buildings',
        'sheds'
    ]

    map = make_web_map(layers)
    map.save(str(map_dir / 'map.html'))

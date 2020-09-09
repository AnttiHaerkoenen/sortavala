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


def make_choropleth(
        *,
        layers=None,
        choropleth_layer,
        input_dir,
        numerical_data,
        key_on,
        **kwargs
):
    if not layers:
        layers = []

    geo_data = gpd.read_file(input_dir / f'{choropleth_layer}.shp')
    geo_data.set_index(key_on, inplace=True, drop=True)
    geo_data = geo_data.to_json()

    map = folium.Map(
        location=(61.703, 30.695),
        zoom_start=15,
    )
    folium.Choropleth(
        geo_data=geo_data,
        data=numerical_data,
        **kwargs
    ).add_to(map)

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

    # data = pd.read_csv(data_dir / 'processed' / 'plots_status.csv')

    # map = make_choropleth(
    #     layers=layers,
    #     input_dir=data_dir / 'interim',
    #     numerical_data=data,
    #     choropleth_layer='plots',
    #     name='choropleth',
    #     columns=['plot_number', 'quartile'],
    #     key_on='number',
    #     bins=[1, 2, 3, 4],
    # )
    # map.save(str(map_dir / 'choropleth.html'))

    map = make_web_map(layers=layers, input_dir=data_dir / 'interim')
    map.save(str(map_dir / 'map.html'))

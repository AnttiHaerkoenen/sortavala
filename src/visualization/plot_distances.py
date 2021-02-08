from pathlib import Path

import pandas as pd
import numpy as np
import geopandas as gpd
from shapely.geometry import Point, LineString
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style="ticks", palette="pastel")


def distances(data, locations):
    distance_data = []
    for k, v in locations.items():
        d = data.copy()
        d['landmark'] = k
        d['distance'] = d.geometry.centroid.distance(v)
        distance_data.append(d)
    data = pd.concat(distance_data)
    return data


if __name__ == '__main__':
    fig_dir = Path('../../reports/figures')
    data_dir = Path('../../data') / 'processed'
    square = Point(695_240, 6_846_340)
    church_street = LineString([(695_000, 6_846_450), (695_300, 6_846_450)])

    plots = gpd.read_file(data_dir / 'plots.shp', index_col=0).set_index('number', drop=True)
    plots = plots.to_crs(epsg=3067)
    plots.quartile.fillna('NA', inplace=True)
    plots['quartile'] = plots.quartile.apply(lambda c: int(c) if not isinstance(c, str) else c)
    gentry = plots.status == 'g'
    plots.loc[gentry, 'quartile'] = 'gentry'
    plots = distances(plots, {'Market square': square, 'Church street': church_street})
    order = ['gentry', 1, 2, 3, 4, 'NA']
    plt.rc('legend', loc='upper center')
    plot_1 = sns.boxplot(
        y='distance',
        x='quartile',
        hue='landmark',
        data=plots,
        order=order,
        palette=["m", "g"],
    )
    plot_1.get_legend().set_title('Distance to')
    plt.show()
    fig = plot_1.get_figure()
    fig.savefig(fig_dir / 'dist_plot.png')

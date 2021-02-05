from pathlib import Path

import pandas as pd
import numpy as np
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt


color_mapper = {
    1.0: "grey",
    2.0: "green",
    3.0: "blue",
    4.0: "red",
}


if __name__ == '__main__':
    fig_dir = Path('../../reports/figures')
    data_dir = Path('../../data') / 'processed'
    square = Point(695_240, 6_846_340)

    plots = gpd.read_file(data_dir / 'plots.shp', index_col=0).set_index('number', drop=True)
    plots = plots.to_crs(epsg=3067)
    plots['distance'] = plots.geometry.centroid.distance(square)
    plots = pd.DataFrame(plots)
    plots.quartile.fillna(0, inplace=True)
    plots['quartile'] = plots.quartile.apply(lambda c: int(c))
    plots.plot(
        x='distance',
        y='tax',
        kind='scatter',
        c='quartile',
        colormap=plt.get_cmap('Set2', 4),
        colorbar=False,
    )
    plt.savefig(fig_dir / 'dist_plot.png')
    plt.show()

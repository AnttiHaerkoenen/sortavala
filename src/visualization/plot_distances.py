from pathlib import Path

import pandas as pd
import numpy as np
import geopandas as gpd
from shapely.geometry import Point, LineString
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
    church_street = LineString([(695_000, 6_846_450), (695_300, 6_846_450)])

    plots = gpd.read_file(data_dir / 'plots.shp', index_col=0).set_index('number', drop=True)
    plots = plots.to_crs(epsg=3067)
    plots['distance'] = plots.geometry.centroid.distance(square)
    plots = pd.DataFrame(plots)
    plots.quartile.fillna('NA', inplace=True)
    plots['quartile'] = plots.quartile.apply(lambda c: int(c) if not isinstance(c, str) else c)
    gentry = plots.status == 'g'
    plots.loc[gentry, 'quartile'] = 'gentry'
    # plots.plot(
    #     x='distance',
    #     y='tax',
    #     kind='scatter',
    #     c='quartile',
    #     colormap=plt.get_cmap('Set2', 4),
    #     colorbar=False,
    # )
    plots.boxplot(
        column='distance',
        by='quartile',
    )
    plt.savefig(fig_dir / 'dist_plot.png')
    plt.show()

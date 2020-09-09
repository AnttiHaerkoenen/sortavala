from pathlib import Path
from typing import Sequence

import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import MultiPoint
from scipy import stats


def simulate_centroids(
        locations: gpd.GeoDataFrame,
        n: int,
        repeats: int,
) -> gpd.GeoSeries:
    actual_points = locations.geometry.centroid
    results = {}

    for i in range(repeats):
        sample = actual_points.sample(n=n)
        center = MultiPoint(list(sample)).centroid
        results[i] = center

    results = gpd.GeoSeries(results)
    return results


def kde_surface(
        points: gpd.GeoSeries,
):
    x, y = zip(*points.geometry.apply(lambda p: p.coords[0]))
    x_min, x_max = min(x), max(x)
    y_min, y_max = min(y), max(y)

    X, Y = np.mgrid[x_min:x_max:100j, y_min:y_max:100j]
    X = np.flipud(X)
    Y = np.flipud(Y)

    XY = np.vstack([X.ravel(), Y.ravel()])
    values = np.vstack([x, y])
    kernel = stats.gaussian_kde(values)
    Z = np.reshape(kernel(XY).T, X.shape)

    return X, Y, Z, [x_min, x_max, y_min, y_max]


def contour_levels(
        density,
        proportions,
):
    levels = []
    ordered = np.sort(density, axis=None)
    cumsum = np.cumsum(ordered) / ordered.sum()

    for p in proportions:
        p = 1 - p
        closest = np.min(np.abs(cumsum - p))
        closest_i = np.where(np.abs(cumsum - p) == closest)[0]
        level = list(ordered[closest_i])[0]

        levels.append(level)

    return levels


def plot_significance(
        locations: gpd.GeoDataFrame,
        actual_locations: Sequence,
        proportions: Sequence,
        contour_colors: Sequence,
        n: int,
        title: str,
):
    proportions = sorted(proportions, reverse=True)
    plots = locations[locations['number'].isin(actual_locations)]
    actual_centroid = MultiPoint(list(plots.geometry.centroid)).centroid

    simulated_centroids = simulate_centroids(locations, len(actual_locations), n)
    X, Y, Z, extent = kde_surface(simulated_centroids)

    fig = locations.plot(
        color='none',
        edgecolor='black',
        figsize=(10, 10),
    )
    fig.set_title(title.capitalize())

    levels = contour_levels(Z, proportions)
    contours = fig.contour(
        X,
        Y,
        Z,
        levels,
        colors=contour_colors,
    )
    fmt = {k: str(v) for k, v in zip(contours.levels, proportions)}
    fig.clabel(
        contours,
        contours.levels,
        use_clabeltext=levels,
        inline=True,
        fmt=fmt,
        fontsize=10,
    )

    fig.plot(
        actual_centroid.x,
        actual_centroid.y,
        marker='o',
        markersize=5,
        color='red',
    )

    return fig


if __name__ == '__main__':
    input_dir = Path('../../data/interim')

    locations = gpd.read_file(input_dir / 'plots.shp').to_crs(epsg=3067).astype({'number': 'int'})
    status_data = pd.read_csv(Path('../../data/processed') / 'plots_status.csv')

    data = {
        'q1': status_data[status_data['quartile'] == 1]['plot_number'].to_list(),
        'q2': status_data[status_data['quartile'] == 2]['plot_number'].to_list(),
        'q3': status_data[status_data['quartile'] == 3]['plot_number'].to_list(),
        'q4': status_data[status_data['quartile'] == 4]['plot_number'].to_list(),
        'gentry': status_data[status_data['status'] == 'g']['plot_number'].to_list(),
        'councillors': status_data[status_data['status'] == 'c']['plot_number'].to_list(),
        'status_elites': status_data[status_data['status'].isin(list('gc'))]['plot_number'].to_list(),
    }
    data['elites'] = data['q4'] + data['status_elites']

    proportions = [0.8, 0.85, 0.9, 0.95]
    # proportions = [0.01, 0.02, 0.05, 0.1]
    contour_colors = ['green', 'blue', 'black', 'violet']

    for k, v in data.items():
        fig = plot_significance(
            locations=locations,
            actual_locations=v,
            proportions=proportions,
            contour_colors=contour_colors,
            n=10000,
            title=k,
        )

    # plt.imshow(Z, extent=extent)
    # base.set_xlim([695000, 695350])
    # base.set_ylim([6846270, 6846600])
    # simulated_centroids.plot(
    #     ax=base,
    #     color='blue',
    # )
    plt.show()

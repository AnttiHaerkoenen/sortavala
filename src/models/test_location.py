from pathlib import Path

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
    proportions = sorted(proportions, reverse=True)
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


if __name__ == '__main__':
    input_dir = Path('../../data/interim')

    locations = gpd.read_file(input_dir / 'plots.shp').to_crs(epsg=3067)

    simulated_centroids = simulate_centroids(locations, 12, 1000)
    X, Y, Z, extent = kde_surface(simulated_centroids)

    base = locations.plot(
        color='none',
        edgecolor='black',
        figsize=(10, 10),
    )
    proportions = [0.9, 0.95]
    contour_colors = ['green', 'blue']

    levels = contour_levels(Z, proportions)
    contours = base.contour(
        X,
        Y,
        Z,
        levels,
        colors=contour_colors,
    )
    fmt = {k: f'{v}' for k, v in zip(contours.levels, proportions)}

    base.clabel(
        contours,
        contours.levels,
        use_clabeltext=levels,
        inline=True,
        fmt=fmt,
        fontsize=10,
    )

    # plt.imshow(Z, extent=extent)
    # base.set_xlim([695000, 695350])
    # base.set_ylim([6846270, 6846600])
    # simulated_centroids.plot(
    #     ax=base,
    #     color='blue',
    # )
    plt.show()

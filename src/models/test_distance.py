from pathlib import Path
from typing import Sequence

import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point, LineString
import statsmodels.formula.api as smf


if __name__ == '__main__':
    input_dir = Path('../../data/processed')
    common_owner = [('37', '3'), ('4', '11'), ('5', '29')]

    data = gpd.read_file(input_dir / 'plots.shp').to_crs(epsg=3067)
    square = Point(695_240, 6_846_340)
    center = Point(695_200, 6_846_450)
    church_street = LineString([(695_000, 6_846_450), (695_300, 6_846_450)])
    data['d'] = data.geometry.centroid.distance(church_street)
    data = pd.DataFrame(data).set_index('number', drop=True)

    for p1, p2 in common_owner:
        mid = (data.at[p1, 'd'] + data.at[p2, 'd']) / 2
        data.at[p1, 'd'] = mid
        data.drop(labels=[p2], inplace=True)

    ols_log_model = smf.ols('d ~ np.log(tax)', data=data).fit()
    print(ols_log_model.summary())

    ols_model = smf.ols('d ~ tax', data=data).fit()
    print(ols_model.summary())

    data.plot(x='d', y='tax', kind='scatter', logy=True)
    data.plot(x='d', y='tax', kind='scatter', logy=False)

    plt.show()

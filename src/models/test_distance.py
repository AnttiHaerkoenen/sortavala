from pathlib import Path
from typing import Sequence

import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point
from scipy import stats


if __name__ == '__main__':
    input_dir = Path('../../data/processed')

    data = gpd.read_file(input_dir / 'plots.shp').to_crs(epsg=3067)
    square = Point(695_240, 6_846_340)
    data['d'] = data.geometry.centroid.distance(square)
    data = pd.DataFrame(data)
    data.plot(x='d', y='tax', kind='scatter')

    plt.show()

from pathlib import Path

import pandas as pd
import geopandas as gpd


if __name__ == '__main__':
    data_dir = Path('../../data')
    plots = gpd.read_file(data_dir / 'interim' / 'plots.shp')
    plots.set_index('number', drop=True, inplace=True)
    data = pd.read_csv(data_dir / 'processed' / 'plots_status.csv')
    data.rename({'plot_number': 'number'}, axis=1, inplace=True)
    data = data.astype({'number': 'str'})
    data.set_index('number', drop=True, inplace=True)
    plots = plots.join(data, on='number')
    plots.drop(columns=['id'], inplace=True)
    plots.to_file(data_dir / 'processed' / 'plots.shp')

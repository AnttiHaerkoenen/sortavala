from pathlib import Path

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt


if __name__ == '__main__':
    data_dir = Path('../../data')
    map_dir = Path('../../reports/figures')

    plots = gpd.read_file(data_dir / 'interim' / 'plots.shp')
    plots.set_index('number', drop=True, inplace=True)
    data = pd.read_csv(data_dir / 'processed' / 'plots_status.csv')
    data.rename({'plot_number': 'number'}, axis=1, inplace=True)
    data = data.astype({'number': 'str'})
    data.set_index('number', drop=True, inplace=True)
    plots = plots.join(data, on='number')
    map = plots.plot(
        column='quartile',
        edgecolor='black',
        figsize=(8, 8),
        missing_kwds={
            'color': 'lightgrey',
            'edgecolor': 'black',
            'label': 'missing data',
        }
    )
    map.get_xaxis().set_visible(False)
    map.get_yaxis().set_visible(False)
    plt.show()
    plt.savefig(str(map_dir / 'choropleth.png'))

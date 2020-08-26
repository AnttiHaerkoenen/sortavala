from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


if __name__ == '__main__':
    data_dir = Path('../../data/') / 'interim'

    year = 1681
    data = pd.read_csv(data_dir / f'contribution_tax_{year}.csv')
    quartiles = pd.qcut(data.tax, 4)
    print(quartiles)

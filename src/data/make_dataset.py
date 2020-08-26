from pathlib import Path

import pandas as pd


if __name__ == '__main__':
    data_dir = Path('../../data')

    years = 1681, 1682, 1683, 1685
    old_columns = 'numerot KMt status'.split()
    new_columns = 'plot_numbers tax status'.split()

    for year in years:
        data = pd.read_excel(
            data_dir / 'raw' / 'porvarit_kontribuutiot.xlsx',
            sheet_name=f'{year}',
        )
        data.drop(
            columns=set(data.columns).difference(old_columns),
            inplace=True,
        )
        data.columns = new_columns
        data.tax = data.tax.apply(
            lambda c: float(c.replace(',', '.')) if isinstance(c, str) else c
        )
        data.to_csv(data_dir / 'interim' / f'contribution_tax_{year}.csv')

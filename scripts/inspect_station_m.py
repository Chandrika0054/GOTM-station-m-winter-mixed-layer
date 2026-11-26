import xarray as xr, numpy as np, pandas as pd
raw = '/home/chandrika/gotm/station_m/data/raw/'
for f in ['OS_STATION-M-1_194810_D_CTD.nc', 'OS_STATION-M-1_195304_D_OCTD.nc']:
    ds = xr.open_dataset(raw + f)
    t = pd.to_datetime(ds.TIME.values).round('min')
    print('\n==', f)
    print('records:', ds.sizes['TIME'])
    print('first:', t.min(), ' last:', t.max())
    n = pd.Series(1, index=t).groupby(level=0).size()
    print('profiles (unique times):', len(n), ' median records per profile:', int(n.median()))
    for v in ['DEPH', 'TEMP', 'PSAL']:
        if v in ds:
            x = ds[v].values.ravel()
            print(v, 'min', np.nanmin(x), 'max', np.nanmax(x), ds[v].attrs.get('units'))
    for q in ['TEMP_QC', 'PSAL_QC']:
        if q in ds:
            x = ds[q].values.ravel()
            print(q, 'flags:', np.unique(x[~np.isnan(x)]))
    print('profiles per decade:', n.groupby((n.index.year // 10) * 10).size().to_dict())

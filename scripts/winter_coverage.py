import sys, xarray as xr, numpy as np, pandas as pd
f = sys.argv[1] if len(sys.argv) > 1 else '/home/chandrika/gotm/station_m/data/raw/OS_STATION-M-1_194810_D_CTD.nc'
ds = xr.open_dataset(f)
df = pd.DataFrame({'time': pd.to_datetime(ds.TIME.values).round('min'),
                   'z': ds.DEPH.values.ravel(), 'T': ds.TEMP.values.ravel(), 'S': ds.PSAL.values.ravel(),
                   'tq': ds.TEMP_QC.values.ravel(), 'sq': ds.PSAL_QC.values.ravel()})
good = df[(df.tq == 1) & (df.sq == 1)].dropna(subset=['z', 'T', 'S'])
print('good records (both flags = 1):', len(good), 'of', len(df))
print('20 most common depths (m):', sorted(good.z.value_counts().head(20).index.tolist()))
p = good.groupby('time').agg(zmin=('z', 'min'), zmax=('z', 'max'), lev500=('z', lambda s: int((s <= 500).sum())))
p = p[p.index.month.isin([9, 10, 11, 12, 1, 2, 3, 4, 5])]
p['winter'] = np.where(p.index.month >= 9, p.index.year, p.index.year - 1)
u = p[(p.zmin <= 10) & (p.zmax >= 1000)].reset_index()
w = u.groupby('winter').agg(profiles=('time', 'size'), levels_top500m=('lev500', 'median'))
w['longest_gap_days'] = u.groupby('winter')['time'].apply(lambda s: s.sort_values().diff().dt.days.max())
print('\nUsable Sep-May profiles per winter (surface to at least 1000 m, good flags):')
print(w.to_string())

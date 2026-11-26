# Observed mixed-layer depth at Station M (TEOS-10, 0.03 kg/m3 above the 10 m value)
import os, sys
import numpy as np, pandas as pd, xarray as xr, gsw
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

base = os.path.expanduser('~/gotm/station_m')
f = sys.argv[1] if len(sys.argv) > 1 else base + '/data/raw/OS_STATION-M-1_194810_D_CTD.nc'
LAT, LON = 66.0, 2.0          # nominal station position
ZREF, DSIG = 10.0, 0.03       # reference depth (m) and density threshold (kg/m3)
BASELINE = 2002               # baseline winter: Sep 2002 to May 2003
WINTERS = [2000, 2001, 2002, 2003]

ds = xr.open_dataset(f)
df = pd.DataFrame({'time': pd.to_datetime(ds.TIME.values).round('min'),
                   'z': ds.DEPH.values.ravel(), 'T': ds.TEMP.values.ravel(), 'S': ds.PSAL.values.ravel(),
                   'tq': ds.TEMP_QC.values.ravel(), 'sq': ds.PSAL_QC.values.ravel()})
df = df[(df.tq == 1) & (df.sq == 1)].dropna(subset=['z', 'T', 'S'])

p = gsw.p_from_z(-df.z.values, LAT)
SA = gsw.SA_from_SP(df.S.values, p, LON, LAT)
CT = gsw.CT_from_t(SA, df['T'].values, p)
df['sigma0'] = gsw.sigma0(SA, CT)

rows = []
for t, g in df.groupby('time'):
    g = g.groupby('z', as_index=False)['sigma0'].mean().sort_values('z')
    z, s = g.z.values, g.sigma0.values
    if len(z) < 3 or z[0] > ZREF or z[-1] <= ZREF:
        continue
    s_ref = np.interp(ZREF, z, s)
    below = np.where((z > ZREF) & (s >= s_ref + DSIG))[0]
    if len(below) == 0:
        rows.append((t, np.nan, z[-1], True, len(z)))      # mixed to the bottom of the profile
        continue
    i = below[0]
    z0, s0 = (ZREF, s_ref) if z[i - 1] < ZREF else (z[i - 1], s[i - 1])
    mld = z0 + (s_ref + DSIG - s0) * (z[i] - z0) / (s[i] - s0)
    rows.append((t, mld, z[-1], False, len(z)))

m = pd.DataFrame(rows, columns=['time', 'mld_m', 'profile_max_depth_m', 'mixed_to_bottom', 'n_levels'])
m['winter'] = np.where(m.time.dt.month >= 9, m.time.dt.year, m.time.dt.year - 1)
os.makedirs(base + '/data/processed', exist_ok=True)
m.to_csv(base + '/data/processed/station_m_observed_mld.csv', index=False)
print('profiles with an MLD:', int(m.mld_m.notna().sum()), ' mixed to profile bottom:', int(m.mixed_to_bottom.sum()))

print('\nWinter (Sep-May) summary:')
for w in WINTERS:
    s = m[(m.winter == w) & m.time.dt.month.isin([9, 10, 11, 12, 1, 2, 3, 4, 5])].dropna(subset=['mld_m'])
    if len(s) == 0:
        print(w, 'no profiles'); continue
    k = s.mld_m.idxmax()
    print(f"{w}/{str(w + 1)[2:]}: profiles {len(s):3d}  max MLD {s.mld_m.max():6.0f} m on {s.time[k].date()}"
          f"  median Feb-Mar MLD {s[s.time.dt.month.isin([2, 3])].mld_m.median():6.0f} m")

fig, ax = plt.subplots(figsize=(9, 5))
others = [w for w in WINTERS if w != BASELINE]
for w in WINTERS:
    s = m[(m.winter == w)].dropna(subset=['mld_m'])
    s = s[(s.time >= pd.Timestamp(w, 9, 1)) & (s.time < pd.Timestamp(w + 1, 6, 1))].sort_values('time')
    d = (s.time - pd.Timestamp(w, 9, 1)).dt.days
    med = s.set_index('time').mld_m.rolling('15D', center=True, min_periods=3).median()
    lab = f'{w}/{str(w + 1)[2:]}'
    if w == BASELINE:
        ax.scatter(d, s.mld_m, s=14, color='#1f5fa8', alpha=0.45, lw=0, zorder=3)
        ax.plot(d, med.values, color='#1f5fa8', lw=2.5, label=lab + ' (baseline), 15-day running median', zorder=4)
    else:
        ax.scatter(d, s.mld_m, s=8, color='0.75', alpha=0.6, lw=0, zorder=1)
        lab = 'Other winters (' + ', '.join(f'{o}/{str(o + 1)[2:]}' for o in others) + ')' if w == others[0] else None
        ax.plot(d, med.values, color='0.6', lw=1.2, label=lab, zorder=2)
ticks = [(pd.Timestamp(2001 if mo < 9 else 2000, mo, 1) - pd.Timestamp(2000, 9, 1)).days for mo in [9, 10, 11, 12, 1, 2, 3, 4, 5]]
ax.set_xticks(ticks, ['Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May'])
ax.invert_yaxis()
ax.set_ylabel('Mixed-layer depth (m)')
ax.set_title('Observed mixed-layer depth at Station M (66 N, 2 E)\nDots: individual profiles. Lines: 15-day running median')
ax.grid(alpha=0.3, lw=0.5)
for sp in ['top', 'right']:
    ax.spines[sp].set_visible(False)
ax.legend(frameon=False, loc='lower left', fontsize=9)
fig.text(0.99, 0.01, 'TEOS-10 potential density; MLD where density exceeds the 10 m value by 0.03 kg m$^{-3}$',
         ha='right', va='bottom', fontsize=7, color='0.4')
os.makedirs(base + '/figures', exist_ok=True)
fig.tight_layout(rect=(0, 0.02, 1, 1))
fig.savefig(base + '/figures/observed_mld_winters.png', dpi=200)
print('\nSaved figures/observed_mld_winters.png and data/processed/station_m_observed_mld.csv')

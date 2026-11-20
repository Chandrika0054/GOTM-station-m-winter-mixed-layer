# General Ocean Turbulence Model - Winter mixed-layer deepening at Ocean Weather Station M

An independent single-column modelling study of winter mixed-layer deepening at Ocean Weather Station M in the Norwegian Sea, using the General Ocean Turbulence Model (GOTM). The study compares four turbulence closures against observations, with verification, validation and error estimation.

**Status:** in preparation. Work begins in November 2026, and results will be added here as each stage is completed.

## Scientific question

How well does a one-dimensional ocean turbulence model reproduce winter mixed-layer deepening at Station M, and how much does the answer depend on the choice of turbulence closure?

## Motivation

Winter mixing in the Nordic Seas links air-sea heat loss to the formation of dense water, which feeds the deep circulation of the North Atlantic. Weather and climate models represent this vertical mixing through parameterisations, and different closures can give different mixed-layer depths under the same surface forcing. Station M offers a long observational record at a single location, which makes it a suitable site for testing these closures against measurements.

## Study design

| Item | Choice |
|---|---|
| Site | Ocean Weather Station M, 66°N, 2°E, Norwegian Sea |
| Model | GOTM v6.0.8, built with CVMix |
| Turbulence closures | k-ε, k-ω, Mellor-Yamada 2.5, KPP |
| Surface forcing | ERA5 hourly heat, freshwater and momentum fluxes, prescribed |
| Observations | OceanSITES Station M temperature and salinity profiles (1948 to 2009) |
| Period | One baseline winter, September to May, chosen from the observations |
| Mixed-layer depth criterion | Density increase of 0.03 kg m⁻³ from the 10 m value |
| Density | TEOS-10 (`gsw` package), applied identically to model output and observations |

## Plan and progress

- [ ] 1. Set up this repository
- [ ] 2. Build GOTM v6.0.8 with CVMix
- [ ] 3. Run the GOTM test cases and compare the four closures at Ocean Weather Station Papa
- [ ] 4. Download the Station M observations
- [ ] 5. Calculate the observed winter mixed-layer depth and choose the baseline winter
- [ ] 6. Run GOTM at Station M with ERA5 forcing (Figure 1: model against observations)
- [ ] 7. Grid convergence test (Figure 2)
- [ ] 8. Verify the KPP and k-ω configurations
- [ ] 9. Run the experiments: four closures across a range of forcing strengths
- [ ] 10. Write the report

## Planned repository structure

```
README.md            this file
SETUP.md             build instructions and configuration notes
scripts/
  run_closures.py    runs a GOTM case with each of the four closures
  mld.py             mixed-layer depth, same criterion for model and observations
  plot_closures.py   plots mixed-layer depth for each closure
  era5_download.py   downloads ERA5 hourly fluxes at 66°N, 2°E for one winter
  era5_to_gotm.py    converts ERA5 output into GOTM flux files
config/              GOTM configuration for Station M
figures/             figures produced by the study
data/raw/            observations and forcing (not tracked; see SETUP.md)
```

## How to reproduce

1. Build GOTM and install the Python packages as described in `SETUP.md`.
2. Download the Station M observations into `data/raw/`.
3. Download and convert the ERA5 forcing with the two `era5_` scripts.
4. Run the closures with `scripts/run_closures.py` and plot them with `scripts/plot_closures.py`.

Raw data files are not stored in this repository. They are downloaded from their original providers.

## Known limitations

- A single-column model has no lateral advection, so heat and salt carried by currents are missing.
- The surface forcing comes from a reanalysis and carries its own uncertainty.
- Results at one site and for one winter may not hold elsewhere.

## Use of AI assistance

The initial study plan and starter scripts were drafted with the help of an AI assistant (Claude, Anthropic). I run, test, adapt and document all code and results in this repository myself, and each script records any changes I make to it.

## Credits and references

- GOTM: https://gotm.net and https://github.com/gotm-model/code
- Station M observations: OceanSITES, https://www.ncei.noaa.gov/data/oceans/ndbc/oceansites/DATA/STATION-M/
- ERA5: Hersbach, H. et al. (2020). The ERA5 global reanalysis. *Quarterly Journal of the Royal Meteorological Society*, 146, 1999–2049.
- Umlauf, L. and Burchard, H. (2005). Second-order turbulence closure models for geophysical boundary layers. *Continental Shelf Research*, 25, 795–827.
- Umlauf, L., Burchard, H. and Hutter, K. (2003). Extending the k–ω turbulence model towards oceanic applications. *Ocean Modelling*, 5, 195–218.
- Mellor, G. L. and Yamada, T. (1982). Development of a turbulence closure model for geophysical fluid problems. *Reviews of Geophysics and Space Physics*, 20, 851–875.
- Large, W. G., McWilliams, J. C. and Doney, S. C. (1994). Oceanic vertical mixing: a review and a model with a nonlocal boundary layer parameterization. *Reviews of Geophysics*, 32, 363–403.
- TEOS-10: IOC, SCOR and IAPSO (2010). *The international thermodynamic equation of seawater 2010*. https://www.teos-10.org

## Author

Baby Chandrika Shanmugam

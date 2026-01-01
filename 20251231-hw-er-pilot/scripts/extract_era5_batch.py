"""
Efficient ERA5 extraction for HW-ER compound events analysis.

Uses precomputed grid indices for ~140× speedup over xarray.sel().
Extracts 1 year of data for 882 cities in ~10 min (6 variables).

Default variables for HW-ER:
  - 2t: 2m temperature (heatwave detection)
  - 2d: 2m dewpoint (humidity, heat stress)
  - 10u, 10v: 10m wind (heat stress)
  - msl: mean sea level pressure (WRF forcing)
  - tp: total precipitation (extreme rainfall)

Usage:
    # Default HW-ER variables
    uv run python scripts/extract_era5_batch.py --years 2020-2023

    # Custom variables
    uv run python scripts/extract_era5_batch.py --years 2020 --variables 2t tp

Note: On CEDA/JASMIN, only an_sfc variables are hourly instantaneous.
      Precipitation (tp) and radiation (ssrd, strd) are NOT in CEDA ERA5 archive.
      These must be downloaded from CDS to GWS if needed.
"""

import argparse
from pathlib import Path
from calendar import monthrange
from datetime import datetime
import numpy as np
import pandas as pd
import netCDF4 as nc
import xarray as xr

ERA5_SFC = Path("/badc/ecmwf-era5/data/oper/an_sfc")

# ERA5 variable mapping: CLI arg -> netCDF variable name
# For HW-ER compound events analysis
VAR_MAP = {
    # Temperature (heatwave detection)
    "2t": "t2m",      # 2m temperature (K) - primary HW indicator
    "2d": "d2m",      # 2m dewpoint (K) - humidity/heat stress
    "skt": "skt",     # Skin temperature (K) - surface heat
    # Wind (heat stress, circulation)
    "10u": "u10",     # 10m u-wind (m/s)
    "10v": "v10",     # 10m v-wind (m/s)
    # Pressure (WRF forcing, heat stress calcs)
    # "sp": "sp",     # Surface pressure (Pa) - NOT ON CEDA an_sfc
    "msl": "msl",     # Mean sea level pressure (Pa)
    # Precipitation (extreme rainfall) - NOT ON CEDA, download from CDS
    # "tp": "tp",     # Total precipitation (m) - requires CDS download
    # Radiation (heat stress indices) - NOT ON CEDA, download from CDS
    # "ssrd": "ssrd", # Surface solar radiation down (J/m²) - requires CDS download
    # "strd": "strd", # Surface thermal radiation down (J/m²) - requires CDS download
    # Moisture (atmospheric water)
    "tcwv": "tcwv",   # Total column water vapour (kg/m²)
}

# Default variables for HW-ER analysis (available on CEDA)
# Note: tp (precipitation) requires separate CDS download
HWER_VARIABLES = ["2t", "2d", "10u", "10v", "msl"]


def load_cities(csv_path: Path) -> pd.DataFrame:
    """Load city list and prepare coordinates."""
    df = pd.read_csv(csv_path)
    df.columns = [c.strip().replace('\ufeff', '') for c in df.columns]
    df['lon_360'] = df['lon'] % 360
    return df


def precompute_indices(cities: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    """Precompute grid indices for all cities (one-time cost)."""
    # Get grid from reference file
    ref_file = ERA5_SFC / "2020/01/01/ecmwf-era5_oper_an_sfc_202001010000.2t.nc"
    ds = nc.Dataset(ref_file)
    grid_lats = ds.variables['latitude'][:]
    grid_lons = ds.variables['longitude'][:]
    ds.close()

    city_lats = cities['lat'].values
    city_lons = cities['lon_360'].values

    # Find nearest grid indices
    lat_idx = np.array([np.abs(grid_lats - lat).argmin() for lat in city_lats])
    lon_idx = np.array([np.abs(grid_lons - lon).argmin() for lon in city_lons])

    return lat_idx, lon_idx


def extract_year(
    year: int,
    cities: pd.DataFrame,
    lat_idx: np.ndarray,
    lon_idx: np.ndarray,
    variables: list[str],
    output_dir: Path,
) -> None:
    """Extract ERA5 data for all cities for one year."""

    n_cities = len(cities)
    city_ids = cities['ID_UC_G0'].values

    # Build timestamp index for the year
    timestamps = []
    for month in range(1, 13):
        n_days = monthrange(year, month)[1]
        for day in range(1, n_days + 1):
            for hour in range(24):
                timestamps.append(datetime(year, month, day, hour))

    n_times = len(timestamps)
    print(f"  {n_times} timesteps × {n_cities} cities × {len(variables)} variables", flush=True)

    # Initialize arrays
    data = {var: np.zeros((n_times, n_cities), dtype=np.float32) for var in variables}

    # Extract all data
    t_idx = 0
    start_time = datetime.now()

    for month in range(1, 13):
        n_days = monthrange(year, month)[1]
        month_start = datetime.now()

        for day in range(1, n_days + 1):
            for hour in range(24):
                for var in variables:
                    fpath = (ERA5_SFC / f"{year}/{month:02d}/{day:02d}/"
                             f"ecmwf-era5_oper_an_sfc_{year}{month:02d}{day:02d}{hour:02d}00.{var}.nc")

                    if not fpath.exists():
                        data[var][t_idx, :] = np.nan
                        continue

                    ds = nc.Dataset(fpath)
                    grid = ds.variables[VAR_MAP.get(var, var)][0, :, :]
                    data[var][t_idx, :] = grid[lat_idx, lon_idx]
                    ds.close()

                t_idx += 1

        month_elapsed = (datetime.now() - month_start).total_seconds()
        total_elapsed = (datetime.now() - start_time).total_seconds()
        print(f"    {year}-{month:02d}: {month_elapsed:.1f}s (total: {total_elapsed:.0f}s)", flush=True)

    # Save per-city files
    print(f"  Saving {n_cities} city files...")
    output_dir.mkdir(parents=True, exist_ok=True)
    time_coord = pd.DatetimeIndex(timestamps)

    for i, city_id in enumerate(city_ids):
        city_row = cities.iloc[i]
        city_name = city_row['city'].strip().replace('\ufeff', '').replace(' ', '_')

        data_vars = {}
        for var in variables:
            var_name = VAR_MAP.get(var, var)
            data_vars[var_name] = (['time'], data[var][:, i])

        ds = xr.Dataset(
            data_vars,
            coords={'time': time_coord},
            attrs={
                'city_id': int(city_id),
                'city_name': city_name,
                'lat': float(city_row['lat']),
                'lon': float(city_row['lon']),
            }
        )

        out_file = output_dir / f"era5_{year}_{city_id}_{city_name}.nc"
        ds.to_netcdf(out_file)

    print(f"  Done: {output_dir}")


def main():
    parser = argparse.ArgumentParser(description="Efficient ERA5 batch extraction")
    parser.add_argument("--city-list", type=Path,
                        default=Path("20251231-hw-er-pilot/data/cities.csv"))
    parser.add_argument("--years", default="2020", help="Year or range (e.g., 2020-2023)")
    parser.add_argument("--variables", nargs="+", default=HWER_VARIABLES,
                        help="Variables to extract (default: HW-ER set)")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/era5"))
    args = parser.parse_args()

    # Parse years
    if "-" in args.years:
        start, end = map(int, args.years.split("-"))
        years = list(range(start, end + 1))
    else:
        years = [int(args.years)]

    print(f"ERA5 Batch Extraction (netCDF4 + numpy)")
    print(f"  Years: {years}")
    print(f"  Variables: {args.variables}")

    cities = load_cities(args.city_list)
    print(f"  Cities: {len(cities)}")

    print("Precomputing grid indices...")
    lat_idx, lon_idx = precompute_indices(cities)

    for year in years:
        print(f"\nProcessing {year}...")
        start = datetime.now()
        extract_year(year, cities, lat_idx, lon_idx, args.variables, args.output_dir)
        elapsed = (datetime.now() - start).total_seconds()
        print(f"  Year complete: {elapsed/60:.1f} min")

    print("\nAll done!")


if __name__ == "__main__":
    main()

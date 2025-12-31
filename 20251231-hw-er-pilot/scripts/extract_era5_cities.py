"""
Extract ERA5 data for 882 global cities.

Usage:
    uv run python scripts/extract_era5_cities.py --city-list data/cities.csv --output-dir outputs/era5

For a single city test:
    uv run python scripts/extract_era5_cities.py --city-id 47 --years 2020-2023
"""

import argparse
from pathlib import Path
import pandas as pd
import xarray as xr
import numpy as np
from datetime import datetime

# ERA5 paths on JASMIN CEDA
ERA5_SFC = Path("/badc/ecmwf-era5/data/oper/an_sfc")
ERA5_LAND = Path("/badc/ecmwf-era5-land/data")

# Variables for HW-ER analysis
VARIABLES = {
    "2t": "2m temperature (K)",
    "2d": "2m dewpoint (K)",
    "tp": "total precipitation (m)",
    "10u": "10m u-wind (m/s)",
    "10v": "10m v-wind (m/s)",
}


def load_city_list(csv_path: Path) -> pd.DataFrame:
    """Load city list with bounding boxes."""
    df = pd.read_csv(csv_path)
    # Clean BOM from column names
    df.columns = [c.strip().replace('\ufeff', '') for c in df.columns]
    return df


def get_era5_files(year: int, month: int, variable: str = "2t") -> list[Path]:
    """Get list of ERA5 files for a given year/month/variable.

    Structure: /badc/ecmwf-era5/data/oper/an_sfc/YYYY/MM/DD/*.nc
    """
    month_dir = ERA5_SFC / str(year) / f"{month:02d}"
    if not month_dir.exists():
        return []

    # Iterate over all day directories
    files = []
    for day_dir in sorted(month_dir.iterdir()):
        if day_dir.is_dir():
            pattern = f"ecmwf-era5_oper_an_sfc_*.{variable}.nc"
            files.extend(sorted(day_dir.glob(pattern)))

    return files


def lon_to_360(lon: float) -> float:
    """Convert longitude from -180/180 to 0-360 convention (ERA5 uses 0-360)."""
    return lon % 360


def extract_city_data(
    city_row: pd.Series,
    years: list[int],
    variables: list[str] = ["2t"],
    output_dir: Path = None
) -> xr.Dataset:
    """Extract ERA5 data for a single city bounding box."""

    city_id = city_row["ID_UC_G0"]
    city_name = city_row["city"].strip()
    # Convert longitudes to ERA5 convention (0-360)
    min_lon = lon_to_360(city_row["min_lon"])
    max_lon = lon_to_360(city_row["max_lon"])
    min_lat, max_lat = city_row["min_lat"], city_row["max_lat"]

    print(f"Extracting {city_name} (ID={city_id})")
    print(f"  Bbox: [{min_lon:.2f}, {min_lat:.2f}] to [{max_lon:.2f}, {max_lat:.2f}] (0-360)")

    datasets = []

    for year in years:
        for month in range(1, 13):
            for var in variables:
                files = get_era5_files(year, month, var)
                if not files:
                    print(f"  No files for {year}/{month:02d}/{var}")
                    continue

                # Process files one at a time to avoid dask segfaults on JASMIN
                for f in files:
                    ds = xr.open_dataset(f)

                    # Extract bounding box (ERA5 lat is descending)
                    ds_city = ds.sel(
                        latitude=slice(max_lat, min_lat),
                        longitude=slice(min_lon, max_lon)
                    )

                    datasets.append(ds_city.load())  # Load into memory
                    ds.close()

    if not datasets:
        return None

    # Combine all data
    combined = xr.concat(datasets, dim="time")

    # Save if output dir specified
    if output_dir:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / f"era5_{city_id}_{city_name.replace(' ', '_')}.nc"
        combined.to_netcdf(output_file)
        print(f"  Saved: {output_file}")

    return combined


def main():
    parser = argparse.ArgumentParser(description="Extract ERA5 for cities")
    parser.add_argument("--city-list", type=Path, help="City list CSV")
    parser.add_argument("--city-id", type=int, help="Single city ID to extract")
    parser.add_argument("--years", default="2020-2023", help="Year range (e.g., 2020-2023)")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/era5"))
    parser.add_argument("--variables", nargs="+", default=["2t"], help="Variables to extract")
    args = parser.parse_args()

    # Parse years
    if "-" in args.years:
        start, end = map(int, args.years.split("-"))
        years = list(range(start, end + 1))
    else:
        years = [int(args.years)]

    print(f"Years: {years}")
    print(f"Variables: {args.variables}")

    # Load cities
    if args.city_list:
        cities = load_city_list(args.city_list)
    else:
        # Default path in Fu's repo
        cities = load_city_list(Path("data/selected_cities_ucdb_bbox.csv"))

    print(f"Loaded {len(cities)} cities")

    # Extract
    if args.city_id:
        # Single city
        city = cities[cities["ID_UC_G0"] == args.city_id].iloc[0]
        extract_city_data(city, years, args.variables, args.output_dir)
    else:
        # All cities
        for idx, city in cities.iterrows():
            try:
                extract_city_data(city, years, args.variables, args.output_dir)
            except Exception as e:
                print(f"  Error: {e}")
                continue


if __name__ == "__main__":
    main()

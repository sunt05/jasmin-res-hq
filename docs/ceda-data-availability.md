# CEDA Data Availability Guide

**Created**: 2026-01-01
**Issue**: [[PER-393]]

## Key Principle

> **Always check CEDA catalogue BEFORE designing JASMIN-based research workflows.**

CEDA mirrors only a **limited subset** (~20%) of ERA5 variables. Designing workflows assuming full ERA5 availability will fail.

## How to Check Data Availability

### 1. CEDA Catalogue (Primary)

Browse the catalogue to see what's actually available:

| Dataset | Catalogue URL | JASMIN Path |
|---------|---------------|-------------|
| ERA5 Surface Analysis | [catalogue.ceda.ac.uk/uuid/c1145ccc4b6d4310a4fc7cce61041b63](https://catalogue.ceda.ac.uk/uuid/c1145ccc4b6d4310a4fc7cce61041b63/) | `/badc/ecmwf-era5/data/oper/an_sfc/` |
| ERA5 Surface Forecast | [catalogue.ceda.ac.uk/uuid/3e7ad71f09c244318f9bddf92e5fcc4b](https://catalogue.ceda.ac.uk/uuid/3e7ad71f09c244318f9bddf92e5fcc4b/) | `/badc/ecmwf-era5/data/oper/fc_sfc/` |
| ERA5 Pressure Levels | [catalogue.ceda.ac.uk/uuid/f809e61a61ee4eb9a64d4957c3e5bfac](https://catalogue.ceda.ac.uk/uuid/f809e61a61ee4eb9a64d4957c3e5bfac/) | `/badc/ecmwf-era5/data/oper/an_pl/` |
| ERA5-Land | [catalogue.ceda.ac.uk](https://catalogue.ceda.ac.uk/) (search "ERA5-Land") | `/badc/ecmwf-era5-land/data/` |

### 2. Verify on JASMIN Filesystem

Before writing extraction code, verify files exist:

```bash
# Check what variables exist for a sample date
ls /badc/ecmwf-era5/data/oper/an_sfc/2020/01/01/*.nc | head -20

# Check specific variable
ls /badc/ecmwf-era5/data/oper/an_sfc/2020/01/01/*.2t.nc
ls /badc/ecmwf-era5/data/oper/an_sfc/2020/01/01/*.tp.nc  # Will fail - tp not on CEDA!
```

### 3. CEDA Web Download Service

Browse interactively: [data.ceda.ac.uk/badc/ecmwf-era5/](http://data.ceda.ac.uk/badc/ecmwf-era5/)

## ERA5 Variables on CEDA

### Available (an_sfc - Analysis Surface)

| Variable | Short Name | Description |
|----------|------------|-------------|
| 2t | t2m | 2 metre temperature |
| 2d | d2m | 2 metre dewpoint |
| 10u | u10 | 10 metre U wind |
| 10v | v10 | 10 metre V wind |
| msl | msl | Mean sea level pressure |
| skt | skt | Skin temperature |
| cape | cape | Convective available potential energy |
| tcc | tcc | Total cloud cover |
| tcwv | tcwv | Total column water vapour |
| sd | sd | Snow depth |
| sst | sst | Sea surface temperature |
| asn | asn | Snow albedo |
| ci | siconc | Sea ice area fraction |

### Available (fc_sfc - Forecast Surface) - LIMITED

Only 6 variables:
- metss, mntss (turbulent stress)
- mslhf, msshf (heat fluxes)
- msnlwrf, msnswrf (radiation fluxes)

### NOT Available on CEDA (Use CDS API)

| Variable | Description | Alternative |
|----------|-------------|-------------|
| **tp** | Total precipitation | CDS API download required |
| **sp** | Surface pressure | Use `msl` or derive from altitude |
| **ssrd** | Surface solar radiation down | CDS API |
| **strd** | Surface thermal radiation down | CDS API |
| **mx2t** | Maximum 2m temperature | CDS API |
| **mn2t** | Minimum 2m temperature | CDS API |

## Workflow for New Research Tasks

### Step 1: Identify Required Variables

List all variables needed for your analysis. For HW-ER compound events:
- Temperature: 2t, 2d ✓ (on CEDA)
- Wind: 10u, 10v ✓ (on CEDA)
- Pressure: msl ✓ (on CEDA), sp ✗ (not on CEDA)
- Precipitation: tp ✗ (not on CEDA)
- Radiation: ssrd, strd ✗ (not on CEDA)

### Step 2: Check CEDA Availability

```bash
# On JASMIN, verify each variable
for var in 2t 2d 10u 10v msl tp sp ssrd; do
    if ls /badc/ecmwf-era5/data/oper/an_sfc/2020/01/01/*.${var}.nc &>/dev/null; then
        echo "$var: ✓ Available"
    else
        echo "$var: ✗ Not on CEDA"
    fi
done
```

### Step 3: Plan Data Acquisition

| Source | Variables | Method |
|--------|-----------|--------|
| CEDA/JASMIN | 2t, 2d, 10u, 10v, msl | Direct file access |
| CDS API | tp, sp, ssrd, strd | Download via API |
| ERA5-Land | Higher-res surface vars | CEDA or CDS |

### Step 4: Document in Data Catalogue

Update `data/catalogue.yaml` with:
- Which variables from which source
- Access method used
- Any substitutions (e.g., msl for sp)

## CDS API Setup

For variables not on CEDA, use Copernicus Climate Data Store:

1. Register: [cds.climate.copernicus.eu](https://cds.climate.copernicus.eu/)
2. Get API key from profile page
3. Configure on JASMIN:
   ```bash
   echo "url: https://cds.climate.copernicus.eu/api/v2
   key: YOUR_UID:YOUR_API_KEY" > ~/.cdsapirc
   ```
4. Use `cdsapi` Python package for downloads

## References

- [CEDA Archive on JASMIN](https://help.jasmin.ac.uk/docs/long-term-archive-storage/ceda-archive/)
- [CEDA ERA5 Support](https://www.ceda.ac.uk/news/updates/2018/2018-07-23-ceda-archive-support-for-era5-use/)
- [Copernicus CDS](https://cds.climate.copernicus.eu/)

## Lessons Learned

1. **CEDA capacity is ~2PB** - cannot hold full ERA5 (~5PB)
2. **Variable selection is curated** - based on common use cases
3. **Some variables require CDS download** - plan for this in workflows
4. **ERA5t (near-real-time)** - 6-month rolling archive only
5. **Check before coding** - verify file existence before writing extraction scripts

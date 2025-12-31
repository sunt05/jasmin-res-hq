# HW-ER Compound Events Pilot Study

**Issue**: [[PER-394]] (sub-issue of [[PER-393]])
**Status**: Planning
**Started**: 2025-12-31

## Research Question

How do urban climate effects modulate compound heatwave-extreme rainfall (HW-ER) events in the Pearl River Delta, and can we prepare JASMIN-based forcing data for WRF-SUEWS simulations?

## Context

Pilot study supporting [[Fu Luo]]'s PhD research:
- **Repo**: `~/LOCAL/supervision/fuluo/` ([UrbanClimateRisk-UCL/FuLuo-PhD](https://github.com/UrbanClimateRisk-UCL/FuLuo-PhD))
- **Focus**: Compound HW-ER in urbanised Pearl River Delta
- **Method**: WRF-SUEWS coupled simulations
- **Key findings** (from literature): Urbanisation contributes ~50% of HW frequency increase in South China

## Objectives

1. **Data access**: Extract ERA5 data for PRD region on JASMIN
2. **Event identification**: Apply HW-ER compound event criteria from Fu's literature review
3. **Forcing preparation**: Prepare ERA5-based forcing for WRF boundary conditions
4. **Validation data**: Extract MIDAS/observational data for model validation

## Data Sources

See `../data/catalogue.yaml` for JASMIN paths.

**Primary**:
- ERA5 reanalysis (temperature, precipitation, pressure levels)
- ERA5-Land for surface variables

**Secondary**:
- MIDAS UK observations (method validation)
- China Meteorological Administration data (via Fu's access)

## PRD Study Domain

- **Latitude**: 21.5°N - 24.0°N
- **Longitude**: 112.0°E - 115.5°E
- **Key cities**: Guangzhou, Shenzhen, Hong Kong, Dongguan

## Tasks

- [ ] Set up Python/xarray environment on JASMIN
- [ ] Extract ERA5 data for PRD domain (2010-2023)
- [ ] Apply HW-ER detection criteria from `HW-ER_results/gba_hw_hr_metrics.md`
- [ ] Calculate climatological statistics
- [ ] Document ERA5 data access workflow for Fu

## Linked GitHub Issues (FuLuo-PhD)

| Issue | Task | JASMIN Relevance |
|-------|------|------------------|
| [#44](https://github.com/UrbanClimateRisk-UCL/FuLuo-PhD/issues/44) | Download ERA5-Land data | Direct CEDA access vs CDS API |
| [#42](https://github.com/UrbanClimateRisk-UCL/FuLuo-PhD/issues/42) | Global cities (882) analysis | ERA5 extraction for all cities |
| [#43](https://github.com/UrbanClimateRisk-UCL/FuLuo-PhD/issues/43) | Data redownload for HW-ER | JASMIN can speed up |
| [#45](https://github.com/UrbanClimateRisk-UCL/FuLuo-PhD/issues/45) | ERA5-Land vs IMERG | Both on CEDA |

**Note**: Fu currently downloads via CDS API to IRDR server (~5.5 days for 30yr temp).
JASMIN has ERA5 on `/badc/ecmwf-era5/` - direct disk access, much faster.

## Related

- [[Fu Luo]] - PhD researcher
- [[Yuanjian Yang]] - Co-supervisor at NUIST
- [[knowledge/pages/Urban climate and compound HW-ER extremes]]
- Fu's repo: `~/LOCAL/supervision/fuluo/HW-ER_results/`

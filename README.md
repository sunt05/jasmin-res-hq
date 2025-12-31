# JASMIN Research HQ

**Issue**: `[[PER-393]]`
**Status**: Active

Meta-repository for JASMIN-based research tasks using Claude Code hybrid workflow.

## Locations

| Location | Path | Purpose |
|----------|------|---------|
| **Local** | `~/LOCAL/personal-notes/projects/jasmin-res-hq/` | Vault context |
| **JASMIN** | `/gws/nopw/j04/landsurf_rdg/sunt05/jasmin-res-hq/` | Data-proximate prototyping |
| **UCL** | `~/jasmin-res-hq/` | Heavy compute (96 cores, 754GB) |

## Structure

```
jasmin-res-hq/
├── CLAUDE.md                    # Agent protocol
├── README.md                    # This file
├── data/catalogue.yaml          # Shared JASMIN data catalogue
├── YYYYMMDD-task-name/          # Research task directories
│   ├── README.md                # Task-specific goals
│   ├── src/                     # Scripts
│   └── notebooks/               # Analysis
└── ...
```

## Research Tasks

<!-- Add dated task directories as sub-issues of [[PER-393]] -->

| Directory | Description | Status |
|-----------|-------------|--------|
| [[20251231-hw-er-pilot]] | HW-ER compound events pilot study ([[Fu Luo]]) | Planning |

## Data Catalogue

See `data/catalogue.yaml` for JASMIN datasets accessed across all tasks.

## Quick Start

```bash
# JASMIN
ssh jasmin-sci && tmc && crh && scc

# UCL
ssh ucl && tmc && crh && scc

# Local - pull changes
git subtree pull --prefix=projects/jasmin-res-hq \
    git@github.com:sunt05/jasmin-res-hq.git main --squash
```

## Related

- [[diary/2025-12-31]] - Setup session

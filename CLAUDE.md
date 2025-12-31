# JASMIN Research HQ - Agent Protocol

Multi-location Claude Code coordination for JASMIN-based research.

**Master Issue**: [[PER-393]]

## Locations

| Location | Path | Purpose |
|----------|------|---------|
| **JASMIN** | `/gws/nopw/j04/landsurf_rdg/sunt05/jasmin-res-hq/` | Data access, prototyping |
| **Local** | `~/LOCAL/personal-notes/projects/jasmin-res-hq/` | Vault context, orchestration |
| **UCL** | `~/jasmin-res-hq/` | Heavy compute (96 cores, 754GB) |

## Monorepo Structure

This is a meta-repository containing multiple research tasks:

```
jasmin-res-hq/
├── CLAUDE.md                    # This file
├── README.md                    # Overview, task list
├── data/catalogue.yaml          # Shared JASMIN data catalogue
├── handoff/                     # Cross-location handoff notes
├── YYYYMMDD-task-name/          # Research task directory
│   ├── README.md                # Task goals, linked to sub-issue
│   ├── src/
│   └── notebooks/
└── ...
```

Each task directory should:
- Be date-prefixed: `YYYYMMDD-task-name/`
- Have its own README.md with goals
- Link to a sub-issue of [[PER-393]]

## Slash Commands

| Command | Purpose |
|---------|---------|
| `/pickup` | Pull latest and read pending handoff notes from other locations |
| `/handoff` | Create handoff note and push for next location |

See `.claude/commands/` for full documentation.

## Before Starting Work

Run `/pickup` to:
1. Pull latest changes
2. Read handoff notes from other locations
3. See pending tasks

## After Finishing Work

Run `/handoff` to:
1. Create handoff note with progress and next steps
2. Commit and push for other locations

## Commit Prefixes

- `JASMIN:` - Work done on JASMIN sci servers
- `LOCAL:` - Work done in vault (wikilinks, context)
- `UCL:` - Work done on UCL compute

## Handoff Note Template

```markdown
# Session: YYYY-MM-DD (<location>)

**Issue**: [[PER-393]] / [[PER-XXX]] (sub-issue)

## Completed
- [x] Task description

## In Progress
- [ ] Partial work
- State: <where left off>

## Next Steps
1. Recommended action

## Data/Files Changed
- `YYYYMMDD-task/src/file.py` - Description
- `outputs/result.nc` - Size, not in git
```

## Data Handling

| Type | Location | Sync Method |
|------|----------|-------------|
| Code/notebooks | Git | push/pull |
| Large outputs (>50MB) | JASMIN only | rclone to local/UCL |
| Processed results | Git (if <50MB) | push/pull |
| Raw CEDA data | JASMIN only | Reference in catalogue.yaml |

## Data Catalogue

Update `data/catalogue.yaml` when accessing new JASMIN datasets.
Shared across all tasks in this monorepo.

## Quick Reference

```bash
# On JASMIN
ssh jasmin-sci && tmc && crh
git pull && scc

# On UCL
ssh ucl && tmc && crh
git pull && scc

# On Local - pull remote changes
cd ~/LOCAL/personal-notes
git subtree pull --prefix=projects/jasmin-res-hq \
    git@github.com:sunt05/jasmin-res-hq.git main --squash
```

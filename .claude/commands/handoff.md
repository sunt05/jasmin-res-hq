---
description: Create handoff note for next location (git-based)
---

# Handoff - Cross-Location Handoff Note

## Workflow

1. **Detect location** from hostname:
   - `sci-vm-*` or `xfer-vm-*` → JASMIN
   - `*ucl*` → UCL
   - Otherwise → LOCAL

2. **Create handoff note**: `handoff/YYYY-MM-DD-<location>.md`

3. **Use template**:
```markdown
# Session: YYYY-MM-DD (<LOCATION>)

**Issue**: [[PER-393]] / [[PER-XXX]]

## Completed
- [x] What was done

## In Progress
- [ ] Partial work
- State: where left off

## For Next Session
Instructions or commands for the next location.

## Files Changed
- `path/to/file.py` - Description
```

4. **Commit and push**:
```bash
git add handoff/
git commit -m "<LOCATION>: handoff note"
git push origin main
```

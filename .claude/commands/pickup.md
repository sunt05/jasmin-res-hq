---
description: Pull pending handoffs from other locations (git-based)
---

# Pickup - Resume from Cross-Location Handoff

## Workflow

1. **Pull latest**:
```bash
git pull origin main
```

2. **Detect current location** from hostname:
   - `sci-vm-*` or `xfer-vm-*` → JASMIN
   - `*ucl*` → UCL
   - Otherwise → LOCAL

3. **Read handoff notes** from `handoff/` directory (excluding current location)

4. **Summarise** pending tasks from other sessions

## Output

Show what other locations have completed and what this session should do.

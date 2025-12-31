# Claude Code on JASMIN Setup Guide

## Prerequisites

- JASMIN account with `jasmin-login` access
- SSH key uploaded to JASMIN accounts portal
- Anthropic API key

## One-Time Setup

### 1. SSH to JASMIN sci server

```bash
# From local machine
ssh jasmin-sci

# First time: accept host keys for login.jasmin.ac.uk and sci-vm-01.jasmin.ac.uk
```

### 2. Install Claude Code

**Option A: npm (if Node.js available)**
```bash
# Check if npm is available
which npm

# Install to user directory
npm install -g @anthropic-ai/claude-code --prefix ~/.local
```

**Option B: Standalone binary (recommended)**
```bash
# Download and install
curl -fsSL https://claude.ai/install.sh | sh

# Or manual download
curl -L -o ~/.local/bin/claude https://github.com/anthropics/claude-code/releases/latest/download/claude-linux-x64
chmod +x ~/.local/bin/claude
```

### 3. Configure PATH and API Key

Add to `~/.bashrc`:
```bash
# Claude Code
export PATH="$HOME/.local/bin:$PATH"
export ANTHROPIC_API_KEY="sk-ant-api03-..."
```

Reload:
```bash
source ~/.bashrc
```

### 4. Verify Installation

```bash
claude --version
claude --help
```

### 5. Set Up tmux for Persistent Sessions

```bash
# Start named session
tmux new -s claude

# Detach: Ctrl-b d
# List sessions: tmux ls
# Reattach: tmux attach -t claude
```

## Daily Workflow

```bash
# 1. Connect to JASMIN
ssh jasmin-sci

# 2. Attach to existing session or create new
tmux attach -t claude || tmux new -s claude

# 3. Navigate to project
cd /gws/nopw/j04/<gws>/<project>

# 4. Pull latest changes
git pull origin main

# 5. Start Claude Code
claude

# 6. When done, create handoff note and push
git add . && git commit -m "JASMIN: <description>"
git push origin main
```

## Constraints

| Constraint | Limit | Workaround |
|------------|-------|------------|
| Execution time | 1 hour | Use tmux, chunk work |
| Outbound SSH | Blocked | Use HTTPS for git |
| sudo/su | Blocked | Install to ~/.local |
| Memory (VM) | 512MB | Use sci-ph for more |
| Memory (Physical) | 20GB | Good for most work |

## Troubleshooting

### Host key verification failed
```bash
# First-time connection - accept the key
ssh -o StrictHostKeyChecking=accept-new jasmin-sci
```

### API connection issues
```bash
# Check outbound HTTPS works
curl -I https://api.anthropic.com

# Verify API key is set
echo $ANTHROPIC_API_KEY | head -c 20
```

### tmux session lost
```bash
# List all sessions
tmux ls

# Create new if needed
tmux new -s claude
```

### Git push fails (SSH blocked)
```bash
# Use HTTPS remote instead
git remote set-url origin https://github.com/sunt05/<project>.git

# Configure credential caching
git config --global credential.helper cache
```

## Best Practices

1. **Always use tmux** - SSH sessions can drop
2. **Commit frequently** - Small, focused commits
3. **Create handoff notes** - Help future sessions understand state
4. **Update data catalogue** - Document new datasets accessed
5. **Use HTTPS for git** - SSH outbound is blocked on sci servers

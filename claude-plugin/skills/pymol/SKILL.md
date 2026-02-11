---
name: pymol
description: Use when user runs /pymol command to launch PyMOL and establish a controllable session
version: 0.1.0
---

# Launch / Connect to PyMOL

Establish a connection to PyMOL for molecular visualization work.

## Connection Flow

### Step 1: Check existing connection

The SessionStart hook runs `claudemol status` automatically. Read its output:
- **"Socket connection: OK"** → PyMOL is already running. Skip to Step 3.
- **"Socket connection: Not available"** → Installed but not running. Go to Step 2.
- **"claudemol: not configured"** → Run `/pymol-setup` first.

### Step 2: Launch PyMOL

```bash
~/.claudemol/bin/claudemol launch
```

This connects to an existing PyMOL if running, or launches a new instance.

### Step 3: Verify connection

```bash
~/.claudemol/bin/claudemol exec "print('connected')"
```

## Sending Commands

All commands go through `~/.claudemol/bin/claudemol exec`:

```bash
# Fetch a structure
~/.claudemol/bin/claudemol exec "cmd.fetch('1ubq')"

# Multiple commands via heredoc
~/.claudemol/bin/claudemol exec "$(cat <<'PYMOL'
cmd.hide('everything')
cmd.show('cartoon')
cmd.color('spectrum')
cmd.orient()
PYMOL
)"

# Get object names
~/.claudemol/bin/claudemol exec "print(cmd.get_names())"
```

## Image Capture

Always use `cmd.ray()` then `cmd.png()` separately:

```bash
~/.claudemol/bin/claudemol exec "$(cat <<'PYMOL'
cmd.ray(1200, 900)
cmd.png('/tmp/figure.png')
PYMOL
)"
```

**Never** use `cmd.png(path, width, height)` — causes view corruption.

## Rules

- **Never call `cmd.reinitialize()`** unless the user explicitly asks.
- **If PyMOL crashes**, tell the user and offer to relaunch with `~/.claudemol/bin/claudemol launch`.
- **exec does NOT auto-launch.** If exec fails with "Cannot connect", run `launch` first.

## Related Skills

- @pymol-fundamentals - selections, representations, colors
- @pymol-setup - first-time configuration
- @binding-site-visualization - ligand binding sites
- @publication-figures - high-quality figures
- @structure-alignment-analysis - comparing structures

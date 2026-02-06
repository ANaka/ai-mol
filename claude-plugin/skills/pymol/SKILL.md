---
name: pymol
description: Use when user runs /pymol command to launch PyMOL and establish a controllable session
---

# Launch / Connect to PyMOL

Establish a connection to PyMOL for molecular visualization work.

## Connection Flow

### Step 1: Check existing connection

The SessionStart hook runs `claudemol status` automatically. Read its output:
- **"Socket connection: OK"** → PyMOL is already running. Skip to Step 3.
- **"Socket connection: Not available"** → Installed but not running. Go to Step 2.
- **"claudemol not installed or PyMOL not running"** → Go to Step 2.

### Step 2: Connect or launch

```python
from claudemol import connect_or_launch

conn, process = connect_or_launch()
print("Connected to PyMOL")
```

This tries connecting to an existing PyMOL first, and only launches a new instance if needed.

**If the import fails** (ModuleNotFoundError), claudemol may be in a project venv. Check the persisted config:

```python
import json
from pathlib import Path

config_file = Path.home() / ".claudemol" / "config.json"
if config_file.exists():
    config = json.loads(config_file.read_text())
    python_path = config.get("python_path")
    print(f"claudemol Python: {python_path}")
    # Use this python to run: {python_path} -c "from claudemol import connect_or_launch; ..."
```

If no config exists, suggest running `/pymol-setup`.

### Step 3: Verify connection

```python
result = conn.execute("print('connected')")
```

**Reuse this `conn` object for all subsequent commands.** Do not create a new connection each time.

## Sending Commands

```python
# Fetch a structure
conn.execute("cmd.fetch('1ubq')")

# Multiple commands
conn.execute("""
cmd.hide('everything')
cmd.show('cartoon')
cmd.color('spectrum')
cmd.orient()
""")

# Get object names
result = conn.execute("print(cmd.get_names())")
```

## Rules

- **Never use `PyMOLSession`** — its recovery mode kills existing PyMOL sessions.
- **Never call `cmd.reinitialize()`** unless the user explicitly asks.
- **If connection drops mid-session**, `conn.execute()` auto-reconnects. Do not create a new connection or relaunch PyMOL.
- **If PyMOL crashes**, tell the user and offer to relaunch.

## Related Skills

- @pymol-fundamentals - selections, representations, colors
- @pymol-setup - first-time configuration
- @binding-site-visualization - ligand binding sites
- @publication-figures - high-quality figures
- @structure-alignment-analysis - comparing structures

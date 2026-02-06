---
name: pymol-connect
description: Use when launching PyMOL or connecting to an existing PyMOL session for molecular visualization work
---

# PyMOL Connect

Establish a connection to PyMOL for molecular visualization work.

## Connection Flow

Follow these steps in order. Stop as soon as you're connected.

### Step 1: Check the SessionStart hook output

The hook runs `claudemol status` automatically. Read its output:
- **"Socket connection: OK"** → PyMOL is running. Go to Step 3.
- **"Socket connection: Not available"** → PyMOL is installed but not running. Go to Step 2.
- **"PyMOL not found"** → PyMOL is not installed. Tell the user to run `pip install claudemol && claudemol setup`, then start PyMOL manually.

### Step 2: Launch PyMOL

Only if no existing PyMOL is running:

```python
from claudemol import launch_pymol
process = launch_pymol()
```

This launches PyMOL with the socket plugin and waits for it to be ready.

### Step 3: Connect and verify

```python
from claudemol import PyMOLConnection
conn = PyMOLConnection()
conn.connect()
result = conn.execute("print('connected')")
```

**Reuse this `conn` object for all subsequent commands.** Do not create a new connection each time.

## Rules

- **Never use `PyMOLSession`** — its recovery mode kills existing PyMOL sessions.
- **Never call `cmd.reinitialize()`** unless the user explicitly asks.
- **If connection drops mid-session**, `conn.execute()` auto-reconnects. Do not create a new connection or relaunch PyMOL.
- **If PyMOL crashes**, tell the user and offer to relaunch.

## Refer to Other Skills

For specific visualization tasks, use:
- @pymol-fundamentals - selections, representations, colors
- @binding-site-visualization - ligand binding sites
- @publication-figures - high-quality figures
- @structure-alignment-analysis - comparing structures

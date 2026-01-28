---
name: pymol-connect
description: Use when launching PyMOL or connecting to an existing PyMOL session for molecular visualization work
---

# PyMOL Connect

Connect to PyMOL for molecular visualization work.

## Quick Start

When user wants to work with PyMOL (e.g., "open PyMOL", "load 1abc.pdb", "show me this structure"):

### 1. Try Connecting to Existing Instance

```python
import sys
sys.path.insert(0, '/path/to/pymol-mcp')  # Use actual repo path
from pymol_connection import PyMOLConnection

conn = PyMOLConnection()
try:
    conn.connect(timeout=1.0)
    print("Connected to existing PyMOL session")
except:
    print("No existing PyMOL session")
```

### 2. Launch PyMOL if Needed

```python
from pymol_connection import launch_pymol, PyMOLConnection

process = launch_pymol()  # or launch_pymol("file.pdb")
conn = PyMOLConnection()
conn.connect()
print("PyMOL launched and connected")
```

### 3. Send Commands

```python
# Simple command
conn.execute("fetch 1abc")

# Multiple commands
conn.execute("""
fetch 1abc
hide everything
show cartoon
color spectrum, chain A
""")

# Get information back
result = conn.execute("""
_result = cmd.get_names()
""")
print(result)  # List of object names
```

## Session Management

**Check connection:**
```python
if conn.is_connected():
    # Good to go
else:
    conn.connect()  # Will auto-reconnect
```

**Connection drops:** The connection module auto-reconnects on failure (up to 3 attempts).

**Close session:** Just close PyMOL normally. No special handling needed.

## Common Patterns

**Load structure from PDB:**
```python
conn.execute("fetch 4HHB")
```

**Load local file:**
```python
conn.execute("load /path/to/structure.pdb")
```

**Basic visualization:**
```python
conn.execute("""
hide everything
show cartoon
color spectrum
orient
""")
```

**Save image:**
```python
conn.execute("""
ray 1920, 1080
png /path/to/output.png
""")
```

## Refer to Other Skills

For specific visualization tasks, use:
- @pymol-fundamentals - selections, representations, colors
- @binding-site-visualization - ligand binding sites
- @publication-figures - high-quality figures
- @structure-alignment-analysis - comparing structures

---
name: pymol-setup
description: Use when connecting Claude to PyMOL, troubleshooting socket errors, or setting up the PyMOL integration for the first time
---

# PyMOL Setup

Set up Claude Code to work with PyMOL.

## What This Does

1. Verifies PyMOL is installed
2. Configures pymolrc to auto-load the socket plugin
3. Tests the connection

## Steps

### 1. Check PyMOL Installation

Run this command to verify PyMOL is available:

```bash
which pymol && pymol --version
```

If not found, tell the user to install PyMOL first.

### 2. Find pymolrc Location

PyMOL looks for startup scripts in these locations (in order):
- `~/.pymolrc.py` (Python script)
- `~/.pymolrc` (PyMOL commands)

Check if either exists:

```bash
ls -la ~/.pymolrc.py ~/.pymolrc 2>/dev/null || echo "No pymolrc found"
```

### 3. Configure Auto-Load

Add the plugin to pymolrc. The plugin path is:
`<repo-root>/claude_socket_plugin.py`

If `~/.pymolrc.py` exists, add this line:
```python
import subprocess; subprocess.Popen(['python', '-c', 'pass'])  # dummy to avoid import issues
run /path/to/pymol-mcp/claude_socket_plugin.py
```

If no pymolrc exists, create `~/.pymolrc` with:
```
run /path/to/pymol-mcp/claude_socket_plugin.py
```

Use the actual absolute path to the plugin.

### 4. Test Connection

Launch PyMOL and verify connection:

```bash
pymol &
sleep 3
```

Then use the connection module to test:

```python
from pymol_connection import PyMOLConnection
conn = PyMOLConnection()
conn.connect()
result = conn.execute("print('Setup successful!')")
print(result)
```

### 5. Report Success

Tell the user:
- Setup complete
- PyMOL will auto-connect when launched
- They can say "open PyMOL" or "load <file>" to start working

## Troubleshooting

**"Connection refused"**: PyMOL isn't running or plugin didn't load. Check:
- Is PyMOL running?
- Run `claude_status` in PyMOL console
- Check for errors in PyMOL console

**"pymol: command not found"**: PyMOL not in PATH. User needs to:
- Install PyMOL, or
- Add PyMOL to PATH, or
- Create alias in shell config

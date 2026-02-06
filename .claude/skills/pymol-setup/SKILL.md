---
name: pymol-setup
description: Use when connecting Claude to PyMOL, troubleshooting socket errors, or setting up the PyMOL integration for the first time
---

# PyMOL Setup

Set up Claude Code to work with PyMOL.

## Quick Setup (Recommended)

```bash
pip install claudemol
claudemol setup
```

If claudemol is already installed in a project venv:
```bash
.venv/bin/claudemol setup
```

This:
1. Installs the claudemol package (if needed)
2. Configures `~/.pymolrc` to auto-load the socket plugin
3. Saves the Python path to `~/.claudemol/config.json` for future sessions
4. Reports status

## What This Does

1. Checks if claudemol is already installed (project venv, config, or system)
2. Detects platform and checks if PyMOL is installed
3. Installs open-source PyMOL if not found (with user consent)
4. Configures pymolrc to auto-load the socket plugin
5. Tests the connection

## Step 1: Check for Existing claudemol Installation

Before installing anything, check if claudemol is already available.

**Check the project venv first** (most common case):
```bash
.venv/bin/python -c "import claudemol; print(claudemol.__file__)" 2>/dev/null
```

**Check saved config** from a previous setup:
```bash
cat ~/.claudemol/config.json 2>/dev/null
```
If `config.json` exists, it contains `{"python_path": "/path/to/python"}` -- use that Python to run claudemol.

**Check system install** as fallback:
```bash
python3 -c "import claudemol; print(claudemol.__file__)" 2>/dev/null
```

If claudemol is found in any of these locations, skip to Step 3 using the discovered Python path. Do NOT run `pip install claudemol` if it is already installed somewhere.

## Step 2: Check Platform & Install PyMOL

Detect the operating system:
```bash
uname -s  # Returns: Linux, Darwin (macOS), or MINGW*/CYGWIN* (Windows)
```

Check if PyMOL is available:
```bash
which pymol 2>/dev/null && pymol --version
```

If PyMOL is found, skip to Step 3.

If PyMOL is not found, **ask the user how they want to install it**. Common options:
- `pip install pymol-open-source-whl` (pre-built wheels, works on Linux/macOS/Windows)
- `conda install -c conda-forge pymol-open-source` (if user has conda/mamba)
- System package manager (`apt install pymol`, `brew install pymol`, etc.)
- User may already have PyMOL installed elsewhere (e.g., Schrodinger PyMOL) -- ask first

Do not assume an installation method. Let the user choose.

After installation, verify:
```bash
pymol --version
# or if installed via pip:
python3 -m pymol --version
```

## Step 3: Configure pymolrc

Run `claudemol setup` using whichever Python has claudemol installed:

```bash
# If claudemol is in the project venv:
.venv/bin/python -m claudemol.cli setup

# If claudemol is installed globally:
claudemol setup

# If you have a python_path from ~/.claudemol/config.json:
/path/to/python -m claudemol.cli setup
```

`claudemol setup` now also saves the Python path to `~/.claudemol/config.json` so future sessions can find claudemol automatically.

### Manual Configuration (only if claudemol CLI is unavailable)

PyMOL looks for startup scripts in these locations:
- `~/.pymolrc.py` (Python script - takes precedence)
- `~/.pymolrc` (PyMOL commands)

Check existing config:
```bash
ls -la ~/.pymolrc.py ~/.pymolrc 2>/dev/null || echo "No pymolrc found"
```

Find the plugin path:
```python
from claudemol.connection import get_plugin_path
print(get_plugin_path())
```

Add to `~/.pymolrc`:
```
# claudemol: Claude Code socket plugin
run /path/to/plugin.py
```

**Important:** Use the actual absolute path from `get_plugin_path()`.

## Step 4: Test Connection

Launch PyMOL:
```bash
pymol &
# or: python3 -m pymol &
```

Wait a few seconds for startup, then test connection:

```python
from claudemol import connect_or_launch
conn, process = connect_or_launch()
result = conn.execute("print('Claude connection successful!')")
print("Setup complete!" if "successful" in result else f"Connection issue: {result}")
```

## Step 5: Configure Permissions (Optional)

Ask the user if they want seamless PyMOL commands without per-command approval. If yes, add to the project's `.claude/settings.json`:

```json
{
  "permissions": {
    "allow": [
      "Bash(claudemol*)",
      "Bash(*python*claudemol*)",
      "Bash(pymol*)"
    ]
  }
}
```

This allows: claudemol CLI commands, Python scripts that use claudemol, and PyMOL launches. If the file already exists, merge the `allow` entries.

## Step 6: Report Results

On success, tell the user:
- PyMOL is installed and configured
- The socket plugin will auto-load when PyMOL starts
- They can say "open PyMOL" or "load <structure>" to start working
- PyMOL console commands: `claude_status`, `claude_stop`, `claude_start`

## Troubleshooting

### "Connection refused"
PyMOL isn't running or plugin didn't load:
1. Check if PyMOL is running
2. In PyMOL console, run `claude_status`
3. Look for errors in PyMOL console about the plugin

### "pymol: command not found" after pip install
The pymol-open-source-whl package doesn't install a `pymol` command. Solutions:
- Use `python -m pymol` (or `python3 -m pymol`)
- Create an alias in `~/.bashrc` or `~/.zshrc`:
  ```bash
  alias pymol='python3 -m pymol'
  ```

### "No module named 'pymol'" with pip
- Ensure you used the correct pip: `python3 -m pip install pymol-open-source-whl`
- Check Python version is 3.10+

### "ModuleNotFoundError: No module named 'claudemol'"
claudemol is likely installed in a project venv, not globally. Check:
1. `cat ~/.claudemol/config.json` for the saved Python path
2. `.venv/bin/python -c "import claudemol"` for the project venv
3. Use the discovered Python path instead of the system Python

### pymolrc not loading
- Ensure the path in pymolrc is absolute, not relative
- Check file permissions on the plugin
- Run `claudemol setup` to auto-configure

### PyQt5/GUI issues
If PyMOL launches but GUI is broken:
```bash
pip install pyqt5
```

### Conda environment not activated
If using conda, ensure the environment is active:
```bash
conda activate <your-pymol-env>
pymol
```

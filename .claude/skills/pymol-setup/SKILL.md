---
name: pymol-setup
description: Use when connecting Claude to PyMOL, troubleshooting socket errors, or setting up the PyMOL integration for the first time
---

# PyMOL Setup

Set up Claude Code to work with PyMOL, including installing open-source PyMOL if needed.

## What This Does

1. Detects platform and checks if PyMOL is installed
2. Installs open-source PyMOL if not found (with user consent)
3. Configures pymolrc to auto-load the socket plugin
4. Tests the connection

## Step 1: Check Platform & PyMOL Installation

Detect the operating system:

```bash
uname -s  # Returns: Linux, Darwin (macOS), or MINGW*/CYGWIN* (Windows)
```

Check if PyMOL is available:

```bash
which pymol 2>/dev/null && pymol --version
```

If found, skip to Step 3. If not found, proceed to Step 2.

## Step 2: Install Open-Source PyMOL

**Ask the user** which installation method they prefer before proceeding.

### Option A: uv (Recommended - fast, works on all platforms)

Check if uv is installed:
```bash
which uv && uv --version
```

If not installed, install uv first:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Create a dedicated environment and install PyMOL:
```bash
uv venv ~/.pymol-env --python 3.12
source ~/.pymol-env/bin/activate  # Linux/macOS
# or: .pymol-env\Scripts\activate  # Windows
uv pip install pymol-open-source-whl
```

Launch PyMOL:
```bash
python -m pymol
```

**Tip:** Create an alias for convenience (add to `~/.bashrc` or `~/.zshrc`):
```bash
alias pymol='~/.pymol-env/bin/python -m pymol'
```

### Option B: pip (if uv not available)

Requires Python 3.10+. Check Python version first:

```bash
python3 --version
```

Install with pip:

```bash
pip install pymol-open-source-whl
```

This installs pre-built wheels for Linux, macOS (Intel & ARM), and Windows.

After pip install, PyMOL is launched via Python module:
```bash
python3 -m pymol
```

### Option C: Conda/Mamba (if user has conda)

```bash
conda install -c conda-forge pymol-open-source
# or with mamba:
mamba install -c conda-forge pymol-open-source
```

### Option D: System Package Manager (Linux only)

**Ubuntu/Debian (22.04+):**
```bash
sudo apt install pymol
```

**Fedora:**
```bash
sudo dnf install pymol
```

**Arch:**
```bash
sudo pacman -S pymol
```

### Verify Installation

After installation, verify it works:

```bash
pymol --version
# or if installed via pip:
python3 -m pymol --version
```

## Step 3: Configure pymolrc

PyMOL looks for startup scripts in these locations:
- `~/.pymolrc.py` (Python script - takes precedence)
- `~/.pymolrc` (PyMOL commands)

Check existing config:

```bash
ls -la ~/.pymolrc.py ~/.pymolrc 2>/dev/null || echo "No pymolrc found"
```

The plugin path is: `<this-repo>/claude_socket_plugin.py`

### If ~/.pymolrc.py exists

Append to the file:
```python
# Claude Code socket plugin
run /absolute/path/to/pymol-mcp/claude_socket_plugin.py
```

### If no pymolrc exists (or only ~/.pymolrc)

Create or append to `~/.pymolrc`:
```
# Claude Code socket plugin
run /absolute/path/to/pymol-mcp/claude_socket_plugin.py
```

**Important:** Use the actual absolute path to `claude_socket_plugin.py` in this repository.

## Step 4: Test Connection

Launch PyMOL:

```bash
# If using uv environment:
~/.pymol-env/bin/python -m pymol &

# If using system/pip install:
python3 -m pymol &

# If alias is configured:
pymol &
```

Wait a few seconds for startup, then test connection using the Python module in this repo:

```python
import sys
sys.path.insert(0, '/path/to/pymol-mcp')
from pymol_connection import PyMOLConnection

conn = PyMOLConnection()
if conn.connect():
    result = conn.execute("print('Claude connection successful!')")
    print("✓ Setup complete!" if "successful" in result else f"Connection issue: {result}")
else:
    print("✗ Could not connect. Check if PyMOL is running and plugin loaded.")
```

## Step 5: Report Results

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

### "pymol: command not found" after pip/uv install
The pymol-open-source-whl package doesn't install a `pymol` command. Solutions:
- Use `python -m pymol` (or `python3 -m pymol`)
- Create an alias in `~/.bashrc` or `~/.zshrc`:
  ```bash
  # If using uv environment:
  alias pymol='~/.pymol-env/bin/python -m pymol'
  # If using system Python:
  alias pymol='python3 -m pymol'
  ```

### "No module named 'pymol'" with pip
- Ensure you used the correct pip: `python3 -m pip install pymol-open-source-whl`
- Check Python version is 3.10+

### pymolrc not loading
- Ensure the path in pymolrc is absolute, not relative
- Check file permissions on the plugin
- Try running the plugin manually in PyMOL console: `run /path/to/claude_socket_plugin.py`

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

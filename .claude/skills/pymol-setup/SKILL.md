---
name: pymol-setup
description: Use when connecting Claude to PyMOL, troubleshooting socket errors, or setting up the PyMOL integration for the first time
---

# PyMOL Setup

Set up Claude Code to work with PyMOL.

## IMPORTANT: Run This First

**Before doing ANYTHING else**, run this single command to discover existing installations:

```bash
echo "=== Project venv ===" && .venv/bin/python -c "import claudemol; print(claudemol.__file__)" 2>/dev/null || echo "not found"; echo "=== Config ===" && cat ~/.claudemol/config.json 2>/dev/null || echo "not found"; echo "=== System ===" && python3 -c "import claudemol; print(claudemol.__file__)" 2>/dev/null || echo "not found"; echo "=== PyMOL ===" && which pymol 2>/dev/null && pymol --version 2>/dev/null || echo "not found"; echo "=== pymolrc ===" && cat ~/.pymolrc 2>/dev/null || echo "not found"
```

Read the output carefully. **Do NOT install claudemol if it already exists in any location.**

Based on the results:
- **claudemol found in project venv** → Use `.venv/bin/python -m claudemol.cli` for all commands. Go to Step 2.
- **claudemol found in config.json** → Use the `python_path` from config. Go to Step 2.
- **claudemol found in system** → Use `claudemol` directly. Go to Step 2.
- **claudemol not found anywhere** → Go to Step 1.
- **PyMOL not found** → Ask user how they want to install it (see Step 1b).

## Step 1: Install (Only If Not Found Above)

### Step 1a: Install claudemol (only if not found in ANY location)

```bash
uv pip install claudemol   # if using uv
pip install claudemol       # otherwise
```

### Step 1b: Install PyMOL (only if not found)

**Ask the user** which method they prefer. Common options:
- `brew install pymol` (macOS)
- `pip install pymol-open-source-whl` (pre-built wheels)
- `conda install -c conda-forge pymol-open-source`
- System package manager (`apt install pymol`, etc.)
- User may already have PyMOL installed elsewhere -- ask first

Do not assume an installation method.

## Step 2: Run claudemol setup

Run `claudemol setup` using whichever Python has claudemol. This configures `~/.pymolrc` and saves the Python path to `~/.claudemol/config.json` for future sessions.

```bash
# If claudemol is in the project venv:
.venv/bin/python -m claudemol.cli setup

# If claudemol is installed globally:
claudemol setup

# If you have a python_path from ~/.claudemol/config.json:
/path/to/python -m claudemol.cli setup
```

## Step 3: Test Connection

Launch PyMOL and test:

```bash
pymol &
```

Wait a few seconds, then:

```python
from claudemol import connect_or_launch
conn, process = connect_or_launch()
result = conn.execute("print('Claude connection successful!')")
print("Setup complete!" if "successful" in result else f"Connection issue: {result}")
```

## Step 4: Configure Permissions (Optional)

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

If the file already exists, merge the `allow` entries.

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

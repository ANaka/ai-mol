---
name: pymol-setup
description: Use when connecting Claude to PyMOL, troubleshooting socket errors, or setting up the PyMOL integration for the first time
version: 0.1.0
---

# PyMOL Setup

Set up Claude Code to work with PyMOL.

## Step 1: Check Existing Installation

```bash
~/.claudemol/bin/claudemol info 2>/dev/null || echo "NOT CONFIGURED"
```

Read the output carefully:
- **If info prints successfully** → claudemol is already installed. Go to Step 3.
- **If "NOT CONFIGURED"** → Go to Step 2.

## Step 2: Install (Only If Not Configured)

### Step 2a: Install claudemol (only if not found)

```bash
uv pip install claudemol   # if using uv
pip install claudemol       # otherwise
```

### Step 2b: Install PyMOL (only if not found)

**Ask the user** which method they prefer. Common options:
- `brew install pymol` (macOS)
- `pip install pymol-open-source-whl` (pre-built wheels)
- `conda install -c conda-forge pymol-open-source`
- System package manager (`apt install pymol`, etc.)
- User may already have PyMOL installed elsewhere — ask first

Do not assume an installation method.

### Step 2c: Run claudemol setup

Run `claudemol setup` using whichever Python has claudemol installed. This configures `~/.pymolrc`, saves the Python path, and creates the wrapper script at `~/.claudemol/bin/claudemol`.

```bash
# If claudemol is in the project venv:
.venv/bin/python -m claudemol.cli setup

# If claudemol is installed globally:
claudemol setup
```

## Step 3: Test Connection

```bash
~/.claudemol/bin/claudemol launch
~/.claudemol/bin/claudemol exec "print('Claude connection successful!')"
```

## Step 4: Configure Permissions (Optional)

Ask the user if they want seamless PyMOL commands without per-command approval. If yes, add to the project's `.claude/settings.json`:

```json
{
  "permissions": {
    "allow": [
      "Bash(*/.claudemol/bin/claudemol*)",
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
- All commands go through `~/.claudemol/bin/claudemol exec`

## Troubleshooting

### "Cannot connect to PyMOL. Is it running?"
PyMOL isn't running or plugin didn't load:
1. Run `~/.claudemol/bin/claudemol launch`
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

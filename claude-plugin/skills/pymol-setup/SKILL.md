---
name: pymol-setup
description: Use when connecting Claude to PyMOL, troubleshooting socket errors, or setting up the PyMOL integration for the first time
version: 0.2.0
---

# PyMOL Setup

Set up Claude Code to work with PyMOL. This skill installs `pymol-agent-bridge` (the Python library that lets Claude talk to PyMOL over a local socket) and configures the connection.

**Guiding principles:**
- **Explain before acting.** Tell the user what you're about to do and why before running any command that installs packages or modifies config files.
- **Always ask permission.** Never install packages, create environments, or modify files like `~/.pymolrc` without the user's explicit go-ahead.
- **Prefer virtual environments.** `pymol-agent-bridge` should be installed in a virtual environment, not globally. Help the user choose the right one.

---

## Step 1: Check for an Existing Installation

Tell the user: "Let me check if `pymol-agent-bridge` is already configured on your system."

```bash
~/.pymol-agent-bridge/bin/pymol-agent-bridge info --json 2>/dev/null || echo "NOT_CONFIGURED"
```

Read the output:
- **If valid JSON** (has `version`, `plugin_path`, `wrapper_path`) → already installed. Tell the user what version is configured and skip to **Step 4** (Test Connection).
- **If "NOT_CONFIGURED"** → continue to Step 2.

---

## Step 2: Discover the User's Environment

Before installing anything, understand the user's setup. Run these checks:

```bash
# Check for existing virtual environments and package managers
ls -d .venv venv env .env 2>/dev/null          # common venv dirs in cwd
ls pyproject.toml setup.py setup.cfg 2>/dev/null # project files
which uv 2>/dev/null                             # uv available?
which conda 2>/dev/null                          # conda available?
which poetry 2>/dev/null                         # poetry available?
which pymol 2>/dev/null                          # pymol already on PATH?
python3 -c "import pymol; print(pymol.__file__)" 2>/dev/null  # pymol importable?
```

**Present your findings to the user.** Summarize what you found — e.g., "I see you have a `.venv/` in this project and `uv` is installed. PyMOL appears to be installed via conda at `/path/to/pymol`."

### Step 2a: Choose Where to Install pymol-agent-bridge

**You must ask the user where they want `pymol-agent-bridge` installed.** Do not assume. Present options based on what you discovered, in this preference order:

1. **Existing project venv** (if one exists in cwd): "I found a virtual environment at `.venv/`. Would you like to install `pymol-agent-bridge` there?"
2. **Create a new venv** (if no venv exists): "There's no virtual environment here. I'd recommend creating one — would you like me to create a `.venv/` using `uv venv` / `python3 -m venv`?"
3. **Existing conda env** (if conda is active or user mentions one): "You have conda available. Would you like to install into a specific conda environment?"
4. **Global install** (discourage): "I can also install globally, but I'd strongly recommend using a virtual environment to avoid conflicts with other packages."

**Wait for the user's response before proceeding.**

### Step 2b: Install `pymol-agent-bridge`

Once the user has chosen an environment, tell them what you're about to do:

"I'm going to install `pymol-agent-bridge` into [chosen environment]. This is the Python library that creates a socket connection between Claude and PyMOL."

Then install using the appropriate method:

```bash
# If using uv with a project venv:
uv pip install pymol-agent-bridge --python .venv/bin/python

# If using uv to create a new venv first:
uv venv .venv && uv pip install pymol-agent-bridge --python .venv/bin/python

# If using plain venv:
python3 -m venv .venv && .venv/bin/pip install pymol-agent-bridge

# If using conda:
conda install -n <env-name> pip && conda run -n <env-name> pip install pymol-agent-bridge

# If using poetry:
poetry add pymol-agent-bridge
```

### Step 2c: Install PyMOL (only if not found)

If Step 2's discovery did not find PyMOL, tell the user: "I couldn't find a PyMOL installation on your system. You'll need PyMOL to use these skills."

**Ask the user** which method they prefer. Common options:
- `brew install pymol` (macOS, easiest)
- `conda install -c conda-forge pymol-open-source` (conda users)
- `pip install pymol-open-source-whl` (pre-built wheels, note: no `pymol` CLI command — use `python -m pymol`)
- System package manager (`apt install pymol`, etc.)
- User may already have PyMOL installed elsewhere — ask first

**Do not install PyMOL without the user's explicit choice.**

---

## Step 3: Run `pymol-agent-bridge setup`

Tell the user: "Now I'll run `pymol-agent-bridge setup`. This does three things:
1. Adds a socket plugin to your `~/.pymolrc` so PyMOL can receive commands from Claude
2. Saves the Python path so the wrapper knows which interpreter to use
3. Creates a wrapper script at `~/.pymol-agent-bridge/bin/pymol-agent-bridge`"

**Ask the user if it's OK to proceed** (since this modifies `~/.pymolrc`).

Then run setup using the Python where `pymol-agent-bridge` was installed:

```bash
# If pymol-agent-bridge is in a project venv:
.venv/bin/pymol-agent-bridge setup

# If in a conda env:
conda run -n <env-name> pymol-agent-bridge setup

# If installed globally (not recommended):
pymol-agent-bridge setup
```

---

## Step 4: Test Connection

Tell the user: "Let me verify the connection works. I'll launch PyMOL and send a test command."

```bash
~/.pymol-agent-bridge/bin/pymol-agent-bridge launch
```

Wait a moment for PyMOL to start, then:

```bash
~/.pymol-agent-bridge/bin/pymol-agent-bridge exec "print('Claude connection successful!')"
```

If this succeeds, tell the user the connection is working. If it fails, go to **Troubleshooting**.

---

## Step 5: Configure Permissions (Optional)

Tell the user: "By default, Claude will ask your permission each time it runs a PyMOL command. If you'd like seamless operation, I can add permission rules to your project's `.claude/settings.json` so PyMOL commands run without prompts."

**Ask if they want this.** If yes, add to the project's `.claude/settings.json`:

```json
{
  "permissions": {
    "allow": [
      "Bash(*/.pymol-agent-bridge/bin/pymol-agent-bridge*)",
      "Bash(pymol*)"
    ]
  }
}
```

If the file already exists, merge the `allow` entries — do not overwrite existing permissions.

---

## Step 6: Report Results

Summarize what was done:
- Where `pymol-agent-bridge` was installed (which environment)
- That `~/.pymolrc` was configured with the socket plugin
- That the wrapper script is at `~/.pymol-agent-bridge/bin/pymol-agent-bridge`
- Whether permissions were configured

Tell the user:
- The socket plugin auto-loads when PyMOL starts
- They can say "open PyMOL" or "load structure 1UBQ" to start working
- All commands go through `~/.pymol-agent-bridge/bin/pymol-agent-bridge exec`

---

## Troubleshooting

### "Cannot connect to PyMOL. Is it running?"
PyMOL isn't running or the socket plugin didn't load:
1. Run `~/.pymol-agent-bridge/bin/pymol-agent-bridge launch`
2. In the PyMOL console, run `bridge_status`
3. Look for errors in the PyMOL console about the plugin

### "pymol: command not found" after pip install
The `pymol-open-source-whl` package doesn't install a `pymol` CLI command. Solutions:
- Use `python -m pymol` (or `python3 -m pymol`)
- Create an alias in `~/.bashrc` or `~/.zshrc`:
  ```bash
  alias pymol='python3 -m pymol'
  ```

### "No module named 'pymol'" with pip
- Ensure you used the correct pip: `python3 -m pip install pymol-open-source-whl`
- Check Python version is 3.10+

### pymolrc not loading
- Ensure the path in `~/.pymolrc` is absolute, not relative
- Check file permissions on the plugin
- Re-run `pymol-agent-bridge setup` to auto-configure

### PyQt5/GUI issues
If PyMOL launches but the GUI is broken:
```bash
pip install pyqt5
```

### Conda environment not activated
If using conda, ensure the environment is active:
```bash
conda activate <your-pymol-env>
pymol
```

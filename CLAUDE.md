# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

claudemol integrates PyMOL (molecular visualization software) with Claude Code. It enables Claude to control PyMOL via natural language commands for structural biology and molecular visualization tasks.

## Repository Structure

```
claudemol/
├── src/claudemol/        # pip package
│   ├── connection.py     # PyMOLConnection class
│   ├── session.py        # Session management
│   ├── view.py           # Visual feedback helpers
│   ├── plugin.py         # Socket plugin (runs in PyMOL)
│   └── cli.py            # CLI: claudemol setup|status|test|info|launch|exec
├── claude-plugin/        # Claude Code plugin
│   ├── .claude-plugin/
│   │   └── plugin.json
│   └── skills/           # All visualization skills
└── .claude/skills/       # Local skills (for development)
```

## Architecture

```
Claude Code → ~/.claudemol/bin/claudemol exec → TCP Socket (port 9880) → PyMOL Plugin → cmd.* execution
```

**Key components:**

1. **PyMOL Plugin** (`src/claudemol/plugin.py`) - Socket listener that runs inside PyMOL
   - Auto-loads via `~/.pymolrc` after `claudemol setup`
   - Accepts TCP connections on localhost:9880
   - Executes received Python code via `exec()` with output capture
   - Commands: `claude_status`, `claude_stop`, `claude_start`

2. **Connection Module** (`src/claudemol/connection.py`) - Python module for socket communication
   - `PyMOLConnection` class handles TCP socket communication
   - Used by CLI commands to send commands to PyMOL

3. **CLI** (`src/claudemol/cli.py`) - Command-line interface
   - `setup` - Configures `~/.pymolrc` and creates `~/.claudemol/bin/claudemol` wrapper
   - `status` - Checks if PyMOL is running and connected
   - `test` - Tests connection with a simple command
   - `info` - Shows installation info
   - `launch` - Launches PyMOL or connects to existing instance
   - `exec` - Executes code in PyMOL (positional arg or stdin)

4. **Wrapper Script** (`~/.claudemol/bin/claudemol`) - Created by `claudemol setup`
   - Bash script with baked Python path from the venv where claudemol is installed
   - Works from any environment without import issues

5. **Skills** (`claude-plugin/skills/`) - Workflow guidance for visualization tasks
   - Distributed as Claude Code plugin separately from pip package

## Distribution

**pip package:**
```bash
pip install claudemol
claudemol setup  # Configures PyMOL + creates wrapper script
```

**Claude Code skills:**
```bash
/plugin marketplace add ANaka/claudemol?path=claude-plugin
/plugin install claudemol-skills
```

## Known Issues

**View Inflation Bug (FIXED):** When using `cmd.png(path, width, height)` with explicit dimensions, PyMOL's view matrix can become corrupted after multiple reinitialize cycles. Always use `cmd.ray(width, height)` followed by `cmd.png(path)` without dimensions to prevent this.

## Development Commands

```bash
# Install locally for development
pip install -e .

# Linting (ruff configured for E, F, I rules)
ruff check src/
ruff format src/

# Type checking
pyright

# Run tests
pytest tests/
```

## Key Code Patterns

- `~/.claudemol/bin/claudemol exec "cmd.fetch('1ubq')"` - Send commands to PyMOL
- `~/.claudemol/bin/claudemol launch` - Launch or connect to PyMOL
- `from claudemol import PyMOLConnection, PyMOLSession` - Python API (used internally by CLI)
- Global session via `get_session()` with auto-reconnect
- Plugin handles multiple clients but only one active connection at a time
- Local skills in `.claude/skills/` for development, `claude-plugin/skills/` for distribution

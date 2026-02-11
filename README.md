# claudemol: Control PyMOL with Claude Code

Control PyMOL through natural language using Claude Code. This integration enables conversational structural biology, molecular visualization, and analysis.

## Features

- **Natural language control**: Tell Claude what you want to visualize and it executes PyMOL commands
- **Direct socket communication**: Claude Code talks directly to PyMOL (no intermediary server)
- **Full PyMOL access**: Manipulate representations, colors, views, perform measurements, alignments, and more
- **Skill-based workflows**: Built-in skills for common tasks like binding site visualization and publication figures
- **Connect to anything**: Because Claude is the bridge, it can pull in data from online databases (UniProt, PDB, OPM), literature, protein language model annotations, or local analysis scripts and map them directly onto your structure

## Architecture

```
Claude Code → ~/.claudemol/bin/claudemol exec → TCP Socket (port 9880) → PyMOL Plugin → cmd.* execution
```

## Quick Start

### Prerequisites

- PyMOL installed on your system
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) CLI installed
- Python 3.10+

### 1. Install claudemol

```bash
pip install claudemol
claudemol setup
```

This configures `~/.pymolrc` to auto-load the socket plugin, saves your Python path to `~/.claudemol/config.json`, and creates the `~/.claudemol/bin/claudemol` wrapper script so future Claude Code sessions can find it automatically.

### 2. Install the Claude Code plugin

```
/plugin marketplace add ANaka/claudemol?path=claude-plugin
/plugin install claudemol-skills
```

This gives Claude the skills and hooks to work with PyMOL.

### 3. Start using it

Open Claude Code and say:

> "Open PyMOL and load structure 1UBQ"

Claude will launch PyMOL, connect via socket, and load the structure.

### Optional: Seamless permissions

By default, Claude asks for approval before running each command. To auto-approve PyMOL-related commands, add to your project's `.claude/settings.json`:

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

## Usage

### Starting a Session

Simply ask Claude to open PyMOL or load a structure:

- "Open PyMOL"
- "Load PDB 4HHB and show as cartoon"
- "Fetch 1UBQ from the PDB"

Claude connects to an existing PyMOL if one is running, or launches a new instance.

### Example Commands

- "Color the protein by secondary structure"
- "Show the binding site residues within 5A of the ligand as sticks"
- "Align these two structures and calculate RMSD"
- "Create a publication-quality figure with ray tracing"
- "Make a 360 degree rotation movie"

### PyMOL Console Commands

Check or control the socket listener from PyMOL's command line:

```
claude_status   # Check if listener is running
claude_stop     # Stop the listener
claude_start    # Start the listener
```

### Available Skills

The plugin includes skills for common workflows:

- **pymol-fundamentals** - Basic visualization, selections, coloring
- **protein-structure-basics** - Secondary structure, B-factor, representations
- **binding-site-visualization** - Protein-ligand interactions
- **structure-alignment-analysis** - Comparing and aligning structures
- **antibody-visualization** - CDR loops, epitopes, Fab structures
- **publication-figures** - High-quality figure export
- **movie-creation** - Animations and rotations
- **miscellaneous** - Additional patterns and utility commands

## How It Works

### Connection Lifecycle

1. On session start, a hook runs `claudemol status` to check if PyMOL is reachable
2. When you ask Claude to work with PyMOL, it uses `claudemol launch` — connecting to an existing instance or starting a new one
3. Commands are sent as Python code over TCP and executed inside PyMOL via the socket plugin
4. If the connection drops, `conn.execute()` auto-reconnects (up to 3 attempts)

### Venv Support

`claudemol setup` saves your Python interpreter path to `~/.claudemol/config.json`. This means claudemol works even when installed in a project virtualenv — the SessionStart hook and skills read the config to find the right Python.

## Troubleshooting

### Connection Issues

- **"Could not connect to PyMOL"**: Make sure PyMOL is running and the plugin is loaded
- **Check listener status**: Run `claude_status` in PyMOL's command line
- **Restart listener**: Run `claude_stop` then `claude_start` in PyMOL

### Plugin Not Loading

- Run `claudemol setup` to configure PyMOL
- Check PyMOL's output for any error messages on startup

### claudemol Not Found

If Claude reports `ModuleNotFoundError`, claudemol may be installed in a venv that isn't active. Fix:

```bash
# Re-run setup from the venv that has claudemol
.venv/bin/claudemol setup
```

This updates `~/.claudemol/config.json` so future sessions find it.

### First-Time Setup Help

Run `/pymol-setup` in Claude Code for guided setup assistance.

## Configuration

The default socket port is **9880**. Both the plugin and connection module use this port.

Key files:
- `~/.pymolrc` - PyMOL startup script (loads the socket plugin)
- `~/.claudemol/config.json` - Persisted Python path for venv discovery
- `src/claudemol/plugin.py` - Socket listener plugin (runs inside PyMOL)
- `src/claudemol/connection.py` - Python module for socket communication

## Limitations

- PyMOL and Claude Code must run on the same machine (localhost connection)
- One active connection at a time
- Some complex multi-step operations may need guidance

## Contributing

Contributions welcome! This project aims to build comprehensive skills for Claude-PyMOL interaction. If you discover useful patterns or workflows, consider adding them as skills.

## License

MIT License - see LICENSE file for details.

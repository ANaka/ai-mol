# PyMOL-MCP: Control PyMOL with Claude Code

Control PyMOL through natural language using Claude Code. This integration enables conversational structural biology, molecular visualization, and analysis.

https://github.com/user-attachments/assets/687f43dc-d45e-477e-ac2b-7438e175cb36

## Features

- **Natural language control**: Tell Claude what you want to visualize and it executes PyMOL commands
- **Direct socket communication**: Claude Code talks directly to PyMOL (no intermediary server)
- **Full PyMOL access**: Manipulate representations, colors, views, perform measurements, alignments, and more
- **Skill-based workflows**: Built-in skills for common tasks like binding site visualization and publication figures

## Architecture

```
Claude Code → TCP Socket (port 9876) → PyMOL Plugin → cmd.* execution
```

## Quick Start

### Prerequisites

- PyMOL installed on your system
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) CLI installed
- Python 3.10+

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/ANaka/pymol-mcp
   cd pymol-mcp
   ```

2. **Set up the PyMOL plugin:**

   Add this line to your `~/.pymolrc` (create it if it doesn't exist):

   ```python
   run /path/to/pymol-mcp/claude_socket_plugin.py
   ```

   Replace `/path/to/pymol-mcp` with the actual path where you cloned the repository.

3. **Start using it:**

   Open Claude Code in the `pymol-mcp` directory and say:

   > "Open PyMOL and load structure 1UBQ"

   Claude will launch PyMOL (with the socket listener active) and load the structure.

## Usage

### Starting a Session

Simply ask Claude to open PyMOL or load a structure:

- "Open PyMOL"
- "Load PDB 4HHB and show as cartoon"
- "Fetch 1UBQ from the PDB"

Claude will launch PyMOL if it's not already running.

### Example Commands

- "Color the protein by secondary structure"
- "Show the binding site residues within 5Å of the ligand as sticks"
- "Align these two structures and calculate RMSD"
- "Create a publication-quality figure with ray tracing"
- "Make a 360° rotation movie"

### PyMOL Console Commands

Check or control the socket listener from PyMOL's command line:

```
claude_status   # Check if listener is running
claude_stop     # Stop the listener
claude_start    # Start the listener
```

### Available Skills

Claude Code has built-in skills for common workflows:

- **pymol-fundamentals** - Basic visualization, selections, coloring
- **binding-site-visualization** - Protein-ligand interactions
- **structure-alignment-analysis** - Comparing and aligning structures
- **publication-figures** - High-quality figure export
- **movie-creation** - Animations and rotations

## Troubleshooting

### Connection Issues

- **"Could not connect to PyMOL"**: Make sure PyMOL is running and the plugin is loaded
- **Check listener status**: Run `claude_status` in PyMOL's command line
- **Restart listener**: Run `claude_stop` then `claude_start` in PyMOL

### Plugin Not Loading

- Verify the path in your `~/.pymolrc` is correct
- Check PyMOL's output for any error messages on startup
- Try running `run /path/to/claude_socket_plugin.py` manually in PyMOL

### First-Time Setup Help

Run the `/pymol-setup` skill in Claude Code for guided setup assistance.

## Configuration

The default socket port is **9876**. Both the plugin and Claude Code connection module use this port.

Key files:
- `claude_socket_plugin.py` - PyMOL plugin (headless, auto-loads via pymolrc)
- `pymol_connection.py` - Python module for socket communication
- `.claude/skills/` - Claude Code skills for PyMOL workflows

## Limitations

- PyMOL and Claude Code must run on the same machine (localhost connection)
- One active connection at a time
- Some complex multi-step operations may need guidance

## Contributing

Contributions welcome! This project aims to build comprehensive skills for Claude-PyMOL interaction. If you discover useful patterns or workflows, consider adding them as skills.

## Community

Join the Bio-MCP Community for support and discussion: https://join.slack.com/t/bio-mcpslack/shared_invite/zt-31z4pho39-K5tb6sZ1hUvrFyoPmKihAA

## License

MIT License - see LICENSE file for details.

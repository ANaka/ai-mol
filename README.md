# claudemol: PyMOL Skills for Claude Code

`claudemol` is a collection of specialized structural biology and molecular visualization skills for [Claude Code](https://docs.anthropic.com/en/docs/claude-code). 

It provides Claude with the expertise to perform complex PyMOL workflows—from binding site analysis and antibody visualization to publication-quality figure generation—using natural language.

## 🚀 Powered by `pymol-agent-bridge`

This repository is now **skills-only**. All core infrastructure (socket communication, session management, and CLI) has been moved to the [pymol-agent-bridge](https://github.com/ANaka/pymol-agent-bridge) project— a lightweight, agent-agnostic bridge for PyMOL.

## 🛠️ Installation

### 1. Install the Plugin

In Claude Code, install this plugin to give Claude its structural biology expertise:

```
/plugin marketplace add ANaka/claudemol
/plugin install claudemol-skills
```

### 2. Run Setup

Ask Claude to run `/pymol-setup`. It will walk you through everything:

- **Install `pymol-agent-bridge`** — the Python library that connects Claude to PyMOL over a local socket
- **Configure `~/.pymolrc`** — adds the bridge plugin so PyMOL listens for commands on startup
- **Install open-source PyMOL** — if you don't already have PyMOL installed, it can help you set it up (via Homebrew, pip, conda, etc.)
- **Verify the connection** — confirms Claude can send commands to PyMOL

## 🧬 Available Skills

The plugin includes specialized skills for common structural biology workflows:

- **pymol-fundamentals** - Basic visualization, selections, coloring
- **protein-structure-basics** - Secondary structure, B-factor, representations
- **binding-site-visualization** - Protein-ligand interactions
- **structure-alignment-analysis** - Comparing and aligning structures
- **antibody-visualization** - CDR loops, epitopes, Fab structures
- **publication-figures** - High-quality figure export
- **movie-creation** - Animations and rotations
- **miscellaneous** - Additional patterns and utility commands
- **pymol-setup** - Guided configuration and troubleshooting

## 🏗️ Architecture

```
Claude Code → claudemol-skills (Expertise) → pymol-agent-bridge (Plumbing) → PyMOL
```

- **Expertise**: These skills define *how* to perform structural biology tasks.
- **Plumbing**: `pymol-agent-bridge` handles the TCP socket connection and command execution.

## 🔄 Migrating from claudemol < 0.5.0

If you previously used the unified `claudemol` package:

1. Uninstall the old package: `pip uninstall claudemol`
2. Install the new bridge: `pip install pymol-agent-bridge`
3. Run setup to update `~/.pymolrc` and create the new wrapper: `pymol-agent-bridge setup`
4. Update your Claude Code plugin: `/plugin install claudemol-skills` (it will update to the latest version)
5. Update your `.claude/settings.json` permissions to allow the new bridge path:

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

## 🙏 Acknowledgments

This project was originally forked from [pymol-mcp](https://github.com/vrtejus/pymol-mcp) by [vrtejus](https://github.com/vrtejus), which provided PyMOL integration via the Model Context Protocol (MCP). Also inspired by [ChatMol](https://github.com/ChatMol/ChatMol). `claudemol` has since been substantially rewritten to use a CLI-based architecture (`pymol-agent-bridge`) and restructured as a skills-only plugin for Claude Code.

## 📜 License

MIT License - see [LICENSE](LICENSE) file for details.

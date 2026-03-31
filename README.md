# claudemol: PyMOL Skills for Claude Code

`claudemol` is a collection of specialized structural biology and molecular visualization skills for [Claude Code](https://docs.anthropic.com/en/docs/claude-code). 

It provides Claude with the expertise to perform complex PyMOL workflows—from binding site analysis and antibody visualization to publication-quality figure generation—using natural language.

## 🚀 Powered by `pymol-agent-bridge`

This repository is **skills-only**. To talk to pymol it depends on a lightweight python library/CLI, [pymol-agent-bridge](https://github.com/ANaka/pymol-agent-bridge).

## 🛠️ Installation

### 1. Install the Bridge (Prerequisite)

The bridge provides the underlying connection between Claude and PyMOL.

```bash
pip install pymol-agent-bridge
pymol-agent-bridge setup
```

### 2. Install the claudemol Skills

In Claude Code, install this plugin to give Claude its structural biology expertise:

```
/plugin marketplace add ANaka/claudemol
/plugin install claudemol-skills
```

### 3. Verify Connection

Open PyMOL and run `/pymol-setup` in Claude Code to verify everything is working.

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

This project was originally forked from [pymol-mcp](https://github.com/colorifix/pymol-mcp) by [Colorifix](https://github.com/colorifix). The original project provided PyMOL integration via the Model Context Protocol (MCP). `claudemol` has since been substantially rewritten to use a CLI-based architecture (`pymol-agent-bridge`) and restructured as a skills-only plugin for Claude Code.

## 📜 License

MIT License - see [LICENSE](LICENSE) file for details.

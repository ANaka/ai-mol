# pymol-agent-bridge Skills for Claude Code

PyMOL visualization skills for Claude Code.

## Installation

```bash
/plugin marketplace add ANaka/claudemol
/plugin install claudemol-skills
```

Then restart Claude Code.

## Prerequisites

You need the `pymol-agent-bridge` pip package installed:

```bash
pip install pymol-agent-bridge
pymol-agent-bridge setup
```

## Available Skills

- **pymol-fundamentals** - Basic PyMOL operations: loading structures, selections, representations
- **protein-structure-basics** - Visualizing protein secondary structure, B-factors, surfaces
- **binding-site-visualization** - Protein-ligand binding pockets and active sites
- **antibody-visualization** - Antibody structures, CDR loops, epitopes
- **structure-alignment-analysis** - Comparing and aligning protein structures
- **publication-figures** - Creating publication-quality molecular figures
- **movie-creation** - Animations, rotations, and morphing sequences
- **pymol-setup** - First-time PyMOL configuration
- **pymol-connect** - Connecting to PyMOL sessions

## Usage

Once installed, just describe what you want to visualize:

- "Load 1ubq and show it as a cartoon"
- "Visualize the binding site of 1hsg"
- "Create a publication figure of this protein"
- "Align these two structures and show the differences"

Claude will use the appropriate skill automatically.

# PyMOL + Claude Cookbook

A task-oriented guide to what Claude can do with PyMOL through the MCP integration.

## Quick Start

### Connecting PyMOL to Claude

1. Install the PyMOL plugin from `pymol-mcp-socket-plugin/`
2. In PyMOL, start the MCP listener (Plugin menu → MCP Socket → Start)
3. Configure Claude Desktop with the MCP server path
4. You're ready to go!

### Your First Visualization

> "Fetch 1ubq and show it as cartoon colored by secondary structure"

This loads ubiquitin from the PDB and displays it with helices, sheets, and loops in different colors.

---

## Viewing Structures

### Loading a Structure

> "Fetch structure 1ubq from PDB"

> "Load the structure 4HHB (hemoglobin)"

PyMOL downloads the structure from RCSB PDB and displays it.

### Changing Representations

> "Show 1ubq as cartoon"

> "Show residues 1-20 as sticks"

> "Hide the lines representation"

> "Show the surface of chain A"

Available representations: cartoon, sticks, spheres, surface, mesh, lines, ribbon, dots.

### Coloring

> "Color the protein cyan"

> "Color helices red and sheets yellow"

> "Color by secondary structure"

> "Apply rainbow coloring from N to C terminus"

> "Color by B-factor using blue-white-red spectrum"

### Selecting Parts of the Structure

> "Select chain A"

> "Select residues 45 to 60"

> "Select all alanines"

> "Select atoms within 5 angstroms of residue 50"

---

## Comparing Structures

### Loading Multiple Structures

> "Fetch 1ubq and 1ubi"

### Aligning Structures

> "Align 1ubi to 1ubq"

Claude will perform the alignment and report the RMSD. Example output:
```
Alignment RMSD: 0.10 Å over 520 atoms
```

### Superposition (Structure-Based)

> "Superimpose 1ubi onto 1ubq"

Use `super` instead of `align` when comparing structures with different sequences.

### Visualizing Differences

> "Color 1ubq green and 1ubi cyan"

> "Show both structures as cartoon"

---

## Binding Sites & Ligands

### Identifying the Ligand

> "Select the ligand" (uses `organic` selection)

> "How many atoms are in the ligand?"

### Viewing Binding Site Residues

> "Select residues within 5 angstroms of the ligand"

> "Show the binding site as sticks"

> "Color binding site residues yellow"

### Showing Interactions

> "Show polar contacts between ligand and protein"

> "Show hydrogen bonds in the binding site"

This uses distance measurement with `mode=2` to detect and display polar contacts.

### Complete Binding Site Workflow

> "Fetch 1hsg, then show the ligand in sticks with the binding site residues, and display the polar contacts"

This produces a publication-ready view with:
- Protein in cartoon
- Ligand in sticks colored by atom
- Binding site residues in sticks
- Dashed lines showing hydrogen bonds

---

## Analysis

### Measuring Distances

> "Measure the distance between CA of residue 10 and CA of residue 50"

> "What is the distance between the two active site residues?"

### Detecting Hydrogen Bonds

> "Show hydrogen bonds in the structure"

> "Show polar contacts between chains A and B"

### Counting Atoms

> "How many atoms are in chain A?"

> "How many residues are in the ligand?"

---

## Publication Figures

### Setting Up the View

> "Center on the binding site"

> "Zoom to fit the ligand with some buffer"

> "Orient the view along the principal axes"

### Background and Style

> "Set a white background"

> "Enable fancy helices"

> "Make the cartoon look publication-ready"

### Ray Tracing

> "Ray trace at 1200x900 resolution"

Note: Ray tracing takes several seconds depending on complexity.

### Saving Images

> "Save a PNG of the current view"

### Saving Scenes

> "Store this view as scene F1"

> "Recall scene F1"

Scenes remember the camera position, representations, and colors.

---

## Movies & Animations

### Creating a Simple Rotation Movie

> "Set up a 90-frame movie"

> "Create keyframes at the start, middle, and end"

### Scene-Based Movies

> "Store scene F1 for the overview"

> "Store scene F2 for the ligand close-up"

> "Create a movie that transitions between scenes"

### Playing and Exporting

> "Play the movie"

> "Stop the movie"

Note: Movie export to video files requires additional setup in PyMOL.

---

## Selection Reference

Quick reference for selection syntax you can use in your requests:

| What to Select | How to Ask |
| -------------- | ---------- |
| Everything | "all" or "the whole structure" |
| Specific chain | "chain A" |
| Residue range | "residues 10-50" |
| Specific residue | "residue 42" or "resi 42" |
| By residue name | "all alanines" or "resn ALA" |
| Alpha carbons | "CA atoms" or "name CA" |
| Ligand/drug | "the ligand" or "organic molecules" |
| Protein only | "the protein" or "polymer.protein" |
| Water | "water molecules" or "solvent" |
| Secondary structure | "helices" (ss h), "sheets" (ss s), "loops" (ss l+) |
| Nearby atoms | "within 5 angstroms of X" |
| Complete residues | "residues within 5 angstroms of X" |

---

## Tips & Tricks

### Verified Working Patterns

- **Rainbow coloring**: `spectrum count, rainbow, selection`
- **B-factor coloring**: `spectrum b, blue_white_red, selection`
- **Polar contacts**: `distance name, sel1, sel2, mode=2`
- **Binding site selection**: `byres (protein within 5 of organic)`

### Deprecated Commands

- `util.ss` → Use `dss` for secondary structure assignment

### Common Issues

- **"Selection not found"**: Check that the object is loaded with the expected name
- **Empty selection**: Verify selection syntax with atom count
- **Ray tracing slow**: Use `draw` for quick previews, `ray` for final output

### Best Practices

1. Always verify structures loaded: "What objects are loaded?"
2. Hide lines for cleaner views: "Hide lines, show cartoon"
3. Use white background for figures: "Set white background"
4. Store important views as scenes for easy recall

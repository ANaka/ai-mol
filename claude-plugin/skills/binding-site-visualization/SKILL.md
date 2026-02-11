---
name: binding-site-visualization
description: Use when visualizing protein-ligand binding sites, drug binding pockets, active sites, or protein-small molecule interactions through PyMOL.
version: 0.1.0
---

# Binding Site Visualization

Workflows for visualizing and analyzing protein-ligand interactions.

> **Send all `cmd.*` code via:** `~/.claudemol/bin/claudemol exec "..."` (or heredoc for multi-line). See @pymol-fundamentals for details.

## Identifying the Ligand

### Common Selection Patterns

```python
# Select organic small molecules (excludes water, ions)
cmd.select("ligand", "organic")

# More specific: exclude solvent
cmd.select("ligand", "organic and not solvent")

# By residue name if known
cmd.select("ligand", "resn ATP")
cmd.select("ligand", "resn NAD")

# All heteroatoms (includes cofactors, metals, water)
cmd.select("het", "hetatm")
```

### Verification

```python
# Check atom count
count = cmd.count_atoms("ligand")
print("Ligand atoms: " + str(count))

# List all residue names in selection
cmd.iterate("ligand", "print(resn)", quiet=0)
```

## Defining the Binding Pocket

### Distance-Based Selection

```python
# Residues within 4 Angstroms of ligand
cmd.select("pocket", "byres (polymer.protein within 4 of ligand)")

# Wider pocket (5 Angstroms)
cmd.select("pocket_wide", "byres (polymer.protein within 5 of ligand)")

# Just the atoms, not full residues
cmd.select("contact_atoms", "polymer.protein within 3.5 of ligand")
```

### Counting Pocket Residues

```python
# Count CA atoms = number of residues
count = cmd.count_atoms("pocket and name CA")
print("Pocket residues: " + str(count))
```

## Standard Visualization

### Basic Binding Site View

```python
# Protein as gray cartoon
cmd.show("cartoon", "polymer.protein")
cmd.color("gray80", "polymer.protein")
cmd.hide("lines")

# Ligand as sticks, colored by atom with green carbons
cmd.show("sticks", "ligand")
cmd.util.cbag("ligand")

# Pocket residues as sticks, colored by atom with white carbons
cmd.show("sticks", "pocket")
cmd.util.cbaw("pocket")

# Center on binding site
cmd.zoom("ligand", 8)
```

### With Surface

```python
# Semi-transparent surface on protein
cmd.show("surface", "polymer.protein")
cmd.set("transparency", 0.7)
cmd.set("surface_color", "white", "polymer.protein")

# Or surface just around binding site
cmd.show("surface", "pocket")
cmd.set("transparency", 0.5, "pocket")
```

### With Labels

```python
# Label pocket residues
cmd.label("pocket and name CA", "resn+resi")
cmd.set("label_size", 14)
cmd.set("label_color", "black", "pocket")
```

## Showing Interactions

### Polar Contacts (Hydrogen Bonds)

```python
# H-bonds between ligand and pocket
cmd.distance("hbonds", "ligand", "pocket", mode=2)

# Style the dashes
cmd.set("dash_color", "yellow", "hbonds")
cmd.set("dash_gap", 0.2)
cmd.set("dash_length", 0.4)
```

### All Contacts

```python
# Show all close contacts
cmd.distance("contacts", "ligand", "pocket", cutoff=4.0, mode=0)
```

## Coloring Strategies

### By Interaction Type

```python
# Ligand: green carbons
cmd.util.cbag("ligand")

# Key residues: different colors
cmd.color("cyan", "pocket and resn ARG+LYS")  # Basic
cmd.color("salmon", "pocket and resn ASP+GLU")  # Acidic
cmd.color("yellow", "pocket and resn PHE+TYR+TRP")  # Aromatic
```

### By Distance from Ligand

```python
# Gradient based on distance
cmd.spectrum("pc", "blue_white_red", "pocket", byres=1)
```

## Complete Workflow

### Standard Binding Site Figure

```python
# 1. Setup
cmd.delete("all")
cmd.fetch("1hsg")  # HIV protease with inhibitor

# 2. Identify components
cmd.select("lig", "organic")
cmd.select("prot", "polymer.protein")
cmd.select("pocket", "byres (prot within 4 of lig)")

# 3. Style protein
cmd.show("cartoon", "prot")
cmd.color("gray80", "prot")
cmd.hide("lines")

# 4. Style ligand
cmd.show("sticks", "lig")
cmd.util.cbag("lig")

# 5. Style pocket
cmd.show("sticks", "pocket")
cmd.util.cbaw("pocket")

# 6. Show interactions
cmd.distance("hbonds", "lig", "pocket", mode=2)
cmd.set("dash_color", "yellow", "hbonds")

# 7. Camera
cmd.zoom("lig", 6)
cmd.bg_color("white")
```

## Publication-Quality Figures

### Settings for Print/Publication

```python
# Anti-aliasing
cmd.set("antialias", 2)

# Clean ray-trace mode
cmd.set("ray_trace_mode", 1)
cmd.set("ray_shadows", 0)
cmd.set("depth_cue", 0)
cmd.set("spec_reflect", 0.2)
cmd.set("ambient", 0.5)

# Transparent protein cartoon
cmd.set("cartoon_transparency", 0.3)

# White background
cmd.bg_color("white")
```

### Two-Figure Strategy

Always create BOTH overview and detail figures:

**Overview Figure** - Shows binding site in protein context:
```python
cmd.center("ligand")
cmd.zoom("ligand", buffer=12)
cmd.ray(1200, 900)
cmd.png("binding_overview.png")
```

**Detail Figure** - Close-up of interactions:
```python
cmd.zoom("ligand", buffer=5)
cmd.ray(1200, 900)
cmd.png("binding_detail.png")
```

### Key Residue Highlighting

Highlight biologically important residues with distinct colors:

```python
# Example: kinase inhibitor binding
cmd.select("gatekeeper", "resi 529")  # Gatekeeper residue
cmd.color("tv_blue", "gatekeeper and elem C")

cmd.select("mutation", "resi 600")  # V600E mutation site
cmd.color("salmon", "mutation and elem C")
```

### H-Bond Styling for Figures

```python
cmd.distance("hbonds", "ligand", "pocket", mode=2)
cmd.set("dash_color", "yellow", "hbonds")
cmd.set("dash_gap", 0.3, "hbonds")
cmd.set("dash_width", 2.0, "hbonds")
cmd.hide("labels", "hbonds")  # Remove distance labels for cleaner figure
```

## Tips

- `organic` is the reliable selector for ligands
- Use `byres` to expand selections to complete residues
- 4 Angstroms is typical for binding pocket definition
- `mode=2` in distance shows polar contacts only
- White carbons (`util.cbaw`) for pocket, colored carbons for ligand helps distinguish
- Gray protein cartoon keeps focus on binding site
- **Always ray-trace for publication** - OpenGL is for exploration only
- **Multiple views tell a complete story** - don't settle for just one angle

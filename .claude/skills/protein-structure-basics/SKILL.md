---
name: protein-structure-basics
description: Use when visualizing protein structures, showing secondary structure, coloring by B-factor, creating surface representations, or generating basic structural figures through PyMOL.
version: 0.1.0
---

# Protein Structure Basics

Fundamental workflows for visualizing protein structures.

> **Send all `cmd.*` code via:** `~/.claudemol/bin/claudemol exec "..."` (or heredoc for multi-line). See @pymol-fundamentals for details.

## Representations

### Cartoon (Most Common)

```python
cmd.hide("everything")
cmd.show("cartoon")
```

### Surface

```python
cmd.show("surface")
cmd.set("transparency", 0.5)  # Semi-transparent
```

### Sticks (Sidechains)

```python
# Show sticks for specific residues
cmd.show("sticks", "resi 50-60")

# Show all sidechains with cartoon backbone
cmd.show("cartoon")
cmd.show("sticks", "sidechain")
```

### Spheres (CPK)

```python
cmd.show("spheres")
cmd.set("sphere_scale", 0.3)  # Smaller spheres
```

### Ribbon

```python
cmd.show("ribbon")
```

## Coloring

### By Secondary Structure

```python
cmd.color("marine", "ss h")      # Helices - blue
cmd.color("tv_orange", "ss s")   # Sheets - orange
cmd.color("gray70", "ss l+")     # Loops - gray
```

### By Chain

```python
cmd.util.cbc()  # Color by chain (automatic)
# Or manually:
cmd.color("green", "chain A")
cmd.color("cyan", "chain B")
```

### By B-factor (Flexibility/Disorder)

```python
cmd.spectrum("b", "blue_white_red", "all")
# Blue = low B-factor (rigid)
# Red = high B-factor (flexible)
```

### By Residue Type

```python
# Hydrophobic
cmd.color("yellow", "resn ALA+VAL+LEU+ILE+MET+PHE+TRP+PRO")
# Polar
cmd.color("cyan", "resn SER+THR+ASN+GLN+TYR+CYS")
# Positive
cmd.color("blue", "resn ARG+LYS+HIS")
# Negative
cmd.color("red", "resn ASP+GLU")
```

### Rainbow (N to C terminus)

```python
cmd.spectrum("count", "rainbow", "polymer.protein")
```

## Structure Analysis

### Count Residues by Secondary Structure

```python
total = cmd.count_atoms("name CA")
helix = cmd.count_atoms("name CA and ss h")
sheet = cmd.count_atoms("name CA and ss s")
loop = cmd.count_atoms("name CA and ss l+")
print(f"Total: {total}")
print(f"Helix: {helix} ({100*helix/total:.1f}%)")
print(f"Sheet: {sheet} ({100*sheet/total:.1f}%)")
print(f"Loop: {loop} ({100*loop/total:.1f}%)")
```

### List Chains

```python
chains = cmd.get_chains()
for chain in chains:
    count = cmd.count_atoms(f"chain {chain} and name CA")
    print(f"Chain {chain}: {count} residues")
```

## Publication Settings

```python
cmd.bg_color("white")
cmd.set("ray_shadows", 0)
cmd.set("spec_reflect", 0.2)
cmd.set("ambient", 0.5)
cmd.set("antialias", 2)
cmd.set("ray_trace_mode", 1)
cmd.set("cartoon_fancy_helices", 1)
cmd.set("cartoon_smooth_loops", 1)
```

## Complete Workflow

### Standard Protein Figure Set

```python
# 1. Load and clean
cmd.delete("all")
cmd.fetch("1ema")  # GFP
cmd.remove("solvent")

# 2. Basic cartoon with secondary structure colors
cmd.hide("everything")
cmd.show("cartoon")
cmd.color("marine", "ss h")
cmd.color("tv_orange", "ss s")
cmd.color("gray70", "ss l+")

# 3. Publication settings
cmd.bg_color("white")
cmd.set("ray_shadows", 0)
cmd.set("spec_reflect", 0.2)
cmd.set("ambient", 0.5)
cmd.set("antialias", 2)
cmd.set("ray_trace_mode", 1)
cmd.set("cartoon_fancy_helices", 1)

# 4. Overview figure
cmd.orient()
cmd.ray(1200, 900)
cmd.png("protein_overview.png")

# 5. B-factor figure
cmd.spectrum("b", "blue_white_red", "all")
cmd.ray(1200, 900)
cmd.png("protein_bfactor.png")

# 6. Side view
cmd.color("marine", "ss h")  # Reset colors
cmd.color("tv_orange", "ss s")
cmd.color("gray70", "ss l+")
cmd.turn("y", 90)
cmd.ray(1200, 900)
cmd.png("protein_side.png")
```

## Tips

- Always use `cmd.ray(w, h)` then `cmd.png(path)` without dimensions
- `ss h` = helix, `ss s` = sheet/strand, `ss l+` = loop/coil
- B-factor visualization helps identify flexible regions and potential disorder
- Multiple views (front, side, top) tell a more complete story
- Consider showing key functional residues as sticks on top of cartoon

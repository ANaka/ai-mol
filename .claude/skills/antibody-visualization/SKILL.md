---
name: antibody-visualization
description: Use when visualizing antibodies, Fab fragments, CDR loops, epitopes, paratopes, or antibody-antigen complexes through PyMOL.
version: 0.1.0
---

# Antibody Visualization

Workflows for visualizing antibodies, their binding regions, and interactions with antigens.

> **Send all `cmd.*` code via:** `~/.claudemol/bin/claudemol exec "..."` (or heredoc for multi-line). See @pymol-fundamentals for details.

## CDR Loop Identification

### Kabat Numbering (Most Common)

CDR boundaries vary slightly by structure. These are typical ranges:

```python
# Light chain CDRs (Kabat)
cmd.select("CDR_L1", "chain L and resi 24-34")
cmd.select("CDR_L2", "chain L and resi 50-56")
cmd.select("CDR_L3", "chain L and resi 89-97")

# Heavy chain CDRs (Kabat)
cmd.select("CDR_H1", "chain H and resi 26-35")
cmd.select("CDR_H2", "chain H and resi 50-65")
cmd.select("CDR_H3", "chain H and resi 95-102")

# All CDRs combined
cmd.select("all_CDRs", "CDR_L1 or CDR_L2 or CDR_L3 or CDR_H1 or CDR_H2 or CDR_H3")
cmd.select("framework", "(chain L or chain H) and not all_CDRs")
```

### Chain Identification

Check actual chain IDs in the structure:
```python
# List all chains
chains = cmd.get_chains()
print("Chains:", chains)

# Count residues per chain
for chain in chains:
    count = cmd.count_atoms(f"chain {chain} and name CA")
    print(f"Chain {chain}: {count} residues")
```

## Color Schemes

### CDR Loop Coloring

Standard color scheme (warm for light chain, cool for heavy chain):

```python
# Framework regions
cmd.color("gray70", "chain L and not all_CDRs")  # Light chain framework
cmd.color("gray50", "chain H and not all_CDRs")  # Heavy chain framework

# Light chain CDRs (warm colors)
cmd.color("tv_red", "CDR_L1")
cmd.color("salmon", "CDR_L2")
cmd.color("lightorange", "CDR_L3")

# Heavy chain CDRs (cool colors)
cmd.color("marine", "CDR_H1")
cmd.color("slate", "CDR_H2")
cmd.color("deepblue", "CDR_H3")

# Make CDRs visually prominent
cmd.set("cartoon_loop_radius", 0.4, "all_CDRs")
```

### Antigen Coloring

```python
cmd.select("antigen", "not (chain L or chain H)")
cmd.color("palegreen", "antigen")
```

## Epitope/Paratope Analysis

### Identify Interface Residues

```python
# Paratope (antibody residues contacting antigen)
cmd.select("paratope", "(chain L or chain H) within 4 of antigen")

# Epitope (antigen residues contacting antibody)
cmd.select("epitope", "antigen within 4 of (chain L or chain H)")

# Count interface residues
para_count = cmd.count_atoms("paratope and name CA")
epi_count = cmd.count_atoms("epitope and name CA")
print(f"Paratope: {para_count} residues")
print(f"Epitope: {epi_count} residues")
```

### Show Interface Detail

```python
cmd.show("sticks", "paratope or epitope")
cmd.util.cbaw("paratope")  # white carbons for antibody
cmd.util.cbag("epitope")   # green carbons for antigen

# Show H-bonds at interface
cmd.distance("interface_hbonds", "paratope", "epitope", mode=2)
cmd.set("dash_color", "yellow", "interface_hbonds")
cmd.hide("labels", "interface_hbonds")
```

## Standard Views

### Overview (Full Complex)

```python
cmd.orient()
cmd.ray(1200, 900)
cmd.png("antibody_overview.png")
```

### Paratope View (Looking at Binding Surface)

```python
cmd.center("all_CDRs")
cmd.rotate("x", 90)  # Look down at CDRs from antigen side
cmd.zoom("all_CDRs", buffer=8)
cmd.ray(1200, 900)
cmd.png("antibody_paratope.png")
```

### Interface Detail

```python
cmd.zoom("epitope or paratope", buffer=3)
cmd.ray(1200, 900)
cmd.png("antibody_interface.png")
```

## Complete Workflow

### Fab-Antigen Complex Figure Set

```python
# 1. Load and clean
cmd.delete("all")
cmd.fetch("1n8z")  # Trastuzumab Fab bound to HER2
cmd.remove("solvent")

# 2. Identify chains (check with cmd.get_chains() first)
cmd.select("light_chain", "chain A")
cmd.select("heavy_chain", "chain B")
cmd.select("antigen", "chain C or chain D")

# 3. Define CDR loops (adjust residue numbers for specific structure)
cmd.select("CDR_L1", "chain A and resi 24-34")
cmd.select("CDR_L2", "chain A and resi 50-56")
cmd.select("CDR_L3", "chain A and resi 89-97")
cmd.select("CDR_H1", "chain B and resi 26-35")
cmd.select("CDR_H2", "chain B and resi 50-65")
cmd.select("CDR_H3", "chain B and resi 95-102")
cmd.select("all_CDRs", "CDR_L1 or CDR_L2 or CDR_L3 or CDR_H1 or CDR_H2 or CDR_H3")

# 4. Style
cmd.hide("everything")
cmd.show("cartoon", "all")

cmd.color("gray70", "light_chain")
cmd.color("gray50", "heavy_chain")
cmd.color("palegreen", "antigen")

cmd.color("tv_red", "CDR_L1")
cmd.color("salmon", "CDR_L2")
cmd.color("lightorange", "CDR_L3")
cmd.color("marine", "CDR_H1")
cmd.color("slate", "CDR_H2")
cmd.color("deepblue", "CDR_H3")

# 5. Publication settings
cmd.bg_color("white")
cmd.set("ray_shadows", 0)
cmd.set("spec_reflect", 0.2)
cmd.set("ambient", 0.5)
cmd.set("antialias", 2)
cmd.set("ray_trace_mode", 1)

# 6. Generate figures
cmd.orient()
cmd.ray(1200, 900)
cmd.png("fab_antigen_overview.png")

cmd.center("all_CDRs")
cmd.zoom("all_CDRs", buffer=8)
cmd.ray(1200, 900)
cmd.png("fab_antigen_paratope.png")
```

## Tips

- CDR numbering varies - always verify residue ranges for each structure
- Chain letters vary between structures (A/B, L/H, etc.)
- CDR-H3 is the most variable and often makes key antigen contacts
- Use warm colors for light chain, cool colors for heavy chain
- **IMPORTANT**: Always use `cmd.ray(w, h)` then `cmd.png(path)` without dimensions

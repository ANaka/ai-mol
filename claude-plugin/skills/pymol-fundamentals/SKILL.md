---
name: pymol-fundamentals
description: Use when working with PyMOL for molecular visualization tasks including loading structures, creating representations, coloring, selections, and basic analysis.
version: 0.1.0
---

# PyMOL Fundamentals

Core operations for molecular visualization through PyMOL.

## Sending Commands

All commands go through the CLI wrapper. **Never use raw sockets.**

```bash
# Single command
~/.claudemol/bin/claudemol exec "cmd.fetch('1ubq')"

# Multiple commands via heredoc
~/.claudemol/bin/claudemol exec "$(cat <<'PYMOL'
cmd.hide('everything')
cmd.show('cartoon')
cmd.color('spectrum')
PYMOL
)"

# Get values back via print()
~/.claudemol/bin/claudemol exec "print(cmd.get_names())"
```

All `cmd.*` examples below should be sent this way.

## Loading Structures

### Fetch from PDB

```python
cmd.fetch("1ubq")  # Downloads and loads structure
cmd.fetch("1ubq", name="my_protein")  # Custom object name
```

### Load Local File

```python
cmd.load("/path/to/file.pdb")
cmd.load("/path/to/file.pdb", "object_name")
```

### Check Loaded Objects

```python
cmd.get_names()  # Returns list of all objects
cmd.get_names("objects")  # Only objects
cmd.get_names("selections")  # Only selections
```

## Representations

### Show/Hide Representations

Available representations: `cartoon`, `sticks`, `spheres`, `surface`, `mesh`, `lines`, `ribbon`, `dots`

```python
cmd.show("cartoon", "all")
cmd.hide("lines", "all")
cmd.show("sticks", "resi 1-10")
```

### Representation as Exclusive

```python
cmd.as_("cartoon", "all")  # Shows cartoon, hides all others
```

### Cartoon Styles

```python
cmd.set("cartoon_fancy_helices", 1)
cmd.set("cartoon_smooth_loops", 1)
cmd.cartoon("oval", "ss h")  # Oval helices
cmd.cartoon("tube", "ss l+")  # Tube loops
```

## Selection Syntax

### Basic Selections

| Selection | Meaning |
| --------- | ------- |
| `all` | Everything |
| `1ubq` | Object named 1ubq |
| `chain A` | Chain A |
| `resi 1-50` | Residues 1-50 |
| `resn ALA` | All alanines |
| `name CA` | Alpha carbons |
| `elem C` | Carbon atoms |

### Property-Based Selections

| Selection | Meaning |
| --------- | ------- |
| `ss h` | Alpha helices |
| `ss s` | Beta sheets |
| `ss l+` | Loops |
| `organic` | Ligands/small molecules |
| `polymer.protein` | Protein chains |
| `solvent` | Water molecules |

### Proximity Selections

```python
# Atoms within 5 Angstroms
cmd.select("nearby", "all within 5 of ligand")

# Expand to complete residues
cmd.select("binding_site", "byres (protein within 5 of ligand)")
```

### Boolean Operations

```python
cmd.select("pocket", "resi 45-48 and chain A")
cmd.select("not_water", "all and not solvent")
cmd.select("interface", "chain A within 4 of chain B")
```

## Coloring

### Named Colors

```python
cmd.color("red", "ss h")
cmd.color("yellow", "ss s")
cmd.color("green", "ss l+")
cmd.color("cyan", "chain A")
```

### Utility Coloring

```python
cmd.util.cbc()  # Color by chain
cmd.util.cbag("ligand")  # By atom, green carbons
cmd.util.rainbow("all")  # N-to-C rainbow
```

### Spectrum Coloring

```python
cmd.spectrum("count", "rainbow", "all")  # Rainbow by residue
cmd.spectrum("b", "blue_white_red", "all")  # By B-factor
cmd.spectrum("pc", "rainbow", "all")  # By partial charge
```

### Secondary Structure Coloring

```python
cmd.dss()  # Assign secondary structure (replaces deprecated util.ss)
cmd.color("red", "ss h")
cmd.color("yellow", "ss s")
cmd.color("green", "ss l+")
```

## Camera Control

### View Manipulation

```python
cmd.center("selection")  # Center on selection
cmd.zoom("selection")  # Zoom to fit selection
cmd.zoom("selection", 5)  # Zoom with 5 Angstrom buffer
cmd.orient("selection")  # Align to principal axes
cmd.reset()  # Reset view
```

### Rotation and Movement

```python
cmd.turn("y", 90)  # Rotate 90 degrees around Y
cmd.move("z", 10)  # Move camera along Z
cmd.rock()  # Toggle rocking animation
```

## Measurements

### Distance

```python
cmd.distance("dist1", "resi 10 and name CA", "resi 20 and name CA")
```

### Polar Contacts (Hydrogen Bonds)

```python
cmd.distance("hbonds", "ligand", "protein", mode=2)
cmd.distance("polar", "selection1", "selection2", mode=2)
```

### Angles and Dihedrals

```python
cmd.angle("ang1", "atom1", "atom2", "atom3")
cmd.dihedral("dih1", "atom1", "atom2", "atom3", "atom4")
```

## Object Management

### Create and Extract

```python
cmd.create("new_obj", "selection")  # Copy selection to new object
cmd.extract("extracted", "selection")  # Move selection to new object
```

### Delete and Remove

```python
cmd.delete("object_name")  # Delete entire object
cmd.remove("selection")  # Remove atoms from object
cmd.delete("all")  # Clear everything
```

## Common Workflows

### Basic Protein Visualization

```python
cmd.fetch("1ubq")
cmd.show("cartoon", "1ubq")
cmd.hide("lines", "1ubq")
cmd.dss()
cmd.color("green", "ss h")
cmd.color("yellow", "ss s")
cmd.color("cyan", "ss l+")
cmd.center("1ubq")
```

### Ligand-Binding Site View

```python
cmd.fetch("1hsg")
cmd.select("lig", "organic")
cmd.select("prot", "polymer.protein")
cmd.select("site", "byres (prot within 5 of lig)")
cmd.show("cartoon", "prot")
cmd.hide("lines")
cmd.show("sticks", "lig")
cmd.show("sticks", "site")
cmd.util.cbag("lig")
cmd.color("yellow", "site and elem C")
cmd.distance("contacts", "lig", "site", mode=2)
cmd.zoom("lig", 8)
```

### Multi-Structure Comparison

```python
cmd.fetch("1ubq")
cmd.fetch("1ubi")
result = cmd.align("1ubi", "1ubq")
print(f"RMSD: {result[0]:.2f} A over {result[1]} atoms")
cmd.color("green", "1ubq")
cmd.color("cyan", "1ubi")
cmd.show("cartoon", "all")
cmd.hide("lines")
```

## Tips

- Use `cmd.get_names()` to verify objects loaded correctly
- Use `cmd.count_atoms("selection")` to verify selection syntax
- `organic` selects ligands; `polymer.protein` selects protein
- `byres` expands atom selections to complete residues
- `mode=2` in distance shows polar contacts (H-bonds)
- `cmd.dss()` assigns secondary structure (newer than util.ss)
- Use `cmd.remove("solvent")` after loading to remove water molecules (cleaner visualizations)
- Use `cmd.util.cnc()` after showing sticks to color by element (N blue, O red, S yellow)
- Use `cmd.rebuild()` after `cmd.show("surface")` to ensure surface is generated before saving images
- For charge-colored surfaces: color atoms by residue type first, then show surface (surface inherits atom colors)

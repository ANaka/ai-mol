---
name: pymol-miscellaneous
description: Collection of useful PyMOL patterns and commands that don't fit into specific workflow skills. Use as reference for edge cases and less common operations.
version: 0.1.0
---

# Miscellaneous PyMOL Patterns

Useful commands and patterns that don't fit neatly into other skills.

## Object and State Information

### List Objects

```python
cmd.get_names()                    # All objects
cmd.get_names("objects")           # Only objects
cmd.get_names("selections")        # Only selections
```

### Count Atoms

```python
cmd.count_atoms("all")
cmd.count_atoms("polymer.protein")
cmd.count_atoms("organic")
```

### Count States (for NMR/MD)

```python
n = cmd.count_states("object_name")
```

### Get Object Properties

```python
# Get all residue names
resnames = []
cmd.iterate("all", "resnames.append(resn)", space={"resnames": resnames})
unique_resnames = list(set(resnames))
```

## Session Management

### Save Session

```python
cmd.save("session.pse")
```

### Load Session

```python
cmd.load("session.pse")
```

### Clear Everything

```python
cmd.delete("all")
cmd.reset()
```

## Working with Chains

### Get Chain IDs

```python
chains = []
cmd.iterate("all", "chains.append(chain)", space={"chains": chains})
unique_chains = list(set(chains))
```

### Split by Chain

```python
cmd.split_chains("object_name")
```

### Rename Chain

```python
cmd.alter("chain A", "chain='X'")
```

## Modifying Structures

### Remove Water

```python
cmd.remove("solvent")
```

### Remove Hydrogens

```python
cmd.remove("hydro")
```

### Add Hydrogens

```python
cmd.h_add("all")
```

### Keep Only Protein

```python
cmd.remove("not polymer.protein")
```

## Selection Tricks

### Expand Selection

```python
# Atoms within distance
cmd.select("expanded", "all within 5 of ligand")

# Complete residues
cmd.select("expanded", "byres (all within 5 of ligand)")

# Complete chains
cmd.select("expanded", "bychain (all within 5 of ligand)")
```

### Invert Selection

```python
cmd.select("inverse", "not current_selection")
```

### Around vs Within

```python
# "within" includes the reference
cmd.select("s1", "all within 5 of ligand")  # Includes ligand atoms

# "around" excludes the reference
cmd.select("s2", "all around 5 of ligand")  # Excludes ligand atoms
```

## Special Representations

### Ball and Stick

```python
cmd.show("sticks", "selection")
cmd.set("stick_ball", 1)
cmd.set("stick_ball_ratio", 1.5)
```

### Putty (B-factor Tube)

```python
cmd.show("cartoon", "selection")
cmd.cartoon("putty", "selection")
```

### Dots for Surface Points

```python
cmd.show("dots", "selection")
cmd.set("dot_density", 3)
```

## Label Formatting

### Custom Labels

```python
cmd.label("name CA", "resn")           # Just residue name
cmd.label("name CA", "resi")           # Just residue number
cmd.label("name CA", "resn+resi")      # Combined: ALA45
cmd.label("name CA", "'%s%s'%(resn,resi)")  # Same result
```

### Label Styling

```python
cmd.set("label_size", 14)
cmd.set("label_font_id", 7)            # Bold font
cmd.set("label_color", "black", "all")
cmd.set("label_position", (0, 0, 2))   # Offset from atom
```

### Clear Labels

```python
cmd.label("all", "")
```

## Symmetry Operations

### Show Unit Cell

```python
cmd.show("cell")
```

### Generate Symmetry Mates

```python
cmd.symexp("sym", "object", "object", 10)  # Within 10 Angstroms
```

## File Formats

### Export Formats

```python
cmd.save("output.pdb", "selection")     # PDB
cmd.save("output.cif", "selection")     # mmCIF
cmd.save("output.mol2", "selection")    # MOL2
cmd.save("output.sdf", "selection")     # SDF
```

### Image Formats

```python
cmd.png("image.png", width, height, dpi=300, ray=1)
cmd.save("image.pse")  # PyMOL session
```

## Performance Tips

### Disable Updates During Batch Operations

```python
cmd.set("defer_updates", 1)
# ... batch operations ...
cmd.set("defer_updates", 0)
cmd.rebuild()
```

### Reduce Quality for Large Systems

```python
cmd.set("cartoon_sampling", 5)      # Lower = faster
cmd.set("surface_quality", 0)       # Lower = faster
cmd.set("hash_max", 200)            # For large structures
```

## Debugging

### Print Command Output

```python
# Capture output
output = cmd.get("ray_trace_mode")
print("Current setting: " + str(output))
```

### Check Selection Syntax

```python
count = cmd.count_atoms("your_selection_here")
print("Matched atoms: " + str(count))
```

---

## TODO: Patterns to Add

- Electrostatic surface mapping
- Map fitting and isosurface
- Custom CGO objects
- Plugins and scripts

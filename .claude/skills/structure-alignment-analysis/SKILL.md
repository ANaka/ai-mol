---
name: structure-alignment-analysis
description: Use when comparing protein structures, aligning molecules, calculating RMSD, or visualizing structural differences through PyMOL.
version: 0.1.0
---

# Structure Alignment & Analysis

Workflows for structural comparison of proteins and other molecules.

> **Send all `cmd.*` code via:** `~/.claudemol/bin/claudemol exec "..."` (or heredoc for multi-line). See @pymol-fundamentals for details.

## Alignment Methods

### align - Sequence + Structure

Best for: Homologous proteins with similar sequences.

```python
# Basic alignment (mobile moves to target)
result = cmd.align("mobile", "target")

# Result tuple: (RMSD, aligned_atoms, cycles, RMSD_pre, aligned_pairs, raw_score, align_length)
print("RMSD: " + str(round(result[0], 2)) + " A")
print("Atoms aligned: " + str(result[1]))
print("Refinement cycles: " + str(result[2]))
```

### super - Structure Only

Best for: Proteins with low sequence identity but structural similarity.

```python
result = cmd.super("mobile", "target")
print("RMSD: " + str(round(result[0], 2)) + " A")
print("Atoms aligned: " + str(result[1]))
```

### cealign - Combinatorial Extension

Best for: Detecting distant structural homology.

```python
result = cmd.cealign("target", "mobile")
print("RMSD: " + str(round(result["RMSD"], 2)) + " A")
print("Aligned length: " + str(result["alignment_length"]))
```

Note: `cealign` argument order is `(target, mobile)`, opposite of `align`/`super`.

## RMSD Calculations

### After Alignment

```python
# All atoms
rms = cmd.rms_cur("mobile", "target")

# CA atoms only (standard for backbone comparison)
rms = cmd.rms_cur("mobile and name CA", "target and name CA")
print("CA RMSD: " + str(round(rms, 2)) + " A")
```

### Without Moving Structures

```python
# Calculate RMSD without transformation
rms = cmd.rms("mobile", "target", matchmaker=4)
```

## Loading Multiple Structures

### From PDB

```python
cmd.fetch("1tim")
cmd.fetch("8tim")
print("Loaded: " + str(cmd.get_names()))
```

### Naming Convention

```python
cmd.fetch("1tim", name="reference")
cmd.fetch("8tim", name="variant")
```

## Visualization

### Color by Structure

```python
cmd.color("green", "reference")
cmd.color("cyan", "variant")
cmd.show("cartoon")
cmd.hide("lines")
```

### Show Alignment

```python
# Create alignment object for visualization
cmd.align("variant", "reference", object="alignment")
cmd.show("cgo", "alignment")  # Shows aligned residue connections
```

### Highlight Differences

```python
# Color by RMSD (requires script)
# Simpler approach: color conserved vs variable regions
cmd.select("core", "variant within 1 of reference")
cmd.select("variable", "variant and not core")
cmd.color("white", "core")
cmd.color("red", "variable")
```

## Partial Alignment

### Align Specific Regions

```python
# Align only chain A
result = cmd.align("mobile and chain A", "target and chain A")

# Align specific domain
result = cmd.align("mobile and resi 1-100", "target and resi 1-100")

# Align only CA atoms
result = cmd.align("mobile and name CA", "target and name CA")
```

### Exclude Flexible Regions

```python
# Exclude loops from alignment
result = cmd.align(
    "mobile and ss h+s",  # Only helices and sheets
    "target and ss h+s"
)
```

## Multi-Structure Comparison

### Sequential Alignment

```python
# Align all to reference
cmd.fetch("1tim", name="ref")
cmd.fetch("2tim", name="var1")
cmd.fetch("3tim", name="var2")

for structure in ["var1", "var2"]:
    result = cmd.align(structure, "ref")
    print(structure + " RMSD: " + str(round(result[0], 2)))
```

### Color Scheme

```python
colors = ["green", "cyan", "magenta", "yellow", "orange"]
structures = ["ref", "var1", "var2"]
for i, struct in enumerate(structures):
    cmd.color(colors[i], struct)
```

## Complete Workflow

### Standard Structure Comparison

```python
# 1. Load structures
cmd.delete("all")
cmd.fetch("1tim", name="reference")
cmd.fetch("8tim", name="variant")

# 2. Align
result = cmd.align("variant", "reference")
print("RMSD: " + str(round(result[0], 2)) + " A")
print("Atoms: " + str(result[1]))

# 3. Style
cmd.show("cartoon")
cmd.hide("lines")
cmd.color("green", "reference")
cmd.color("cyan", "variant")

# 4. Calculate backbone RMSD
ca_rms = cmd.rms_cur("variant and name CA", "reference and name CA")
print("CA RMSD: " + str(round(ca_rms, 2)) + " A")

# 5. View
cmd.center("all")
cmd.zoom("all")
cmd.bg_color("white")
```

## Interpretation

| RMSD (CA) | Interpretation |
| --------- | -------------- |
| < 0.5 A | Nearly identical |
| 0.5-1.0 A | Very similar (same fold, minor differences) |
| 1.0-2.0 A | Similar fold, some conformational differences |
| 2.0-3.0 A | Same fold family, significant differences |
| > 3.0 A | Different conformations or distant homologs |

## Publication-Quality Figures

### Settings for Print

```python
cmd.bg_color("white")
cmd.set("ray_shadows", 0)
cmd.set("spec_reflect", 0.2)
cmd.set("ambient", 0.5)
cmd.set("antialias", 2)
cmd.set("ray_trace_mode", 1)
cmd.set("cartoon_fancy_helices", 1)
```

### Multi-View Strategy

Always create multiple views to tell the complete story:

**Overview** - Shows full aligned structures:
```python
cmd.orient()
cmd.ray(1200, 900)
cmd.png("comparison_overview.png")
```

**Side View** - Rotated 90° to show depth:
```python
cmd.turn("y", 90)
cmd.ray(1200, 900)
cmd.png("comparison_side.png")
```

**Detail View** - Focus on key difference regions:
```python
cmd.center("mobile and resi 65-85")  # Hinge region, mutation site, etc.
cmd.zoom("all and resi 60-90", buffer=8)
cmd.ray(1200, 900)
cmd.png("comparison_detail.png")
```

### Color Schemes for Comparison

Standard two-structure comparison:
- Structure 1: marine (blue)
- Structure 2: salmon (pink/orange)

Multi-structure comparison:
- Reference: green
- Variants: cyan, magenta, yellow, orange

**IMPORTANT**: Always use `cmd.ray(w, h)` then `cmd.png(path)` without dimensions.
Using `cmd.png(path, w, h)` causes a view inflation bug.

## Tips

- Use `align` for closely related proteins
- Use `super` when sequence identity is low
- Use `cealign` for detecting distant relationships
- Always report CA RMSD for standardization
- Color structures distinctly for clarity
- `rms_cur` calculates RMSD of current positions (after alignment)
- Multiple views tell a more complete story than a single image

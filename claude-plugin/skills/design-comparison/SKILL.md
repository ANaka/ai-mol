---
name: design-comparison
description: Use when comparing multiple protein designs, ranking design candidates, tracking design iterations, overlaying before/after structures, or performing batch visual QC through PyMOL.
version: 0.1.0
---

# Design Comparison

Workflows for comparing, ranking, and screening protein design candidates in PyMOL. Composes with any design tool skill (@rfdiffusion-viz, @proteinmpnn-viz, @alphafold-validation).

> **Send all `cmd.*` code via:** `~/.pymol-agent-bridge/bin/pymol-agent-bridge exec "..."` (or heredoc for multi-line). See @pymol-fundamentals for details.

## Batch Loading

### Load All Designs from a Directory

```python
import glob, os
design_dir = "/path/to/designs"
for f in sorted(glob.glob(os.path.join(design_dir, "*.pdb"))):
    name = os.path.splitext(os.path.basename(f))[0]
    cmd.load(f, name)
print("Loaded %d designs" % len(cmd.get_object_list()))
```

### Load with Naming Convention

```python
# Load designs with a prefix for easy selection
import glob, os
for f in sorted(glob.glob("/path/to/designs/*.pdb")):
    name = "d_" + os.path.splitext(os.path.basename(f))[0]
    cmd.load(f, name)
```

## Grid View (Batch Visual QC)

### Tile All Designs

```python
cmd.set("grid_mode", 1)
cmd.show("cartoon")

# Color each design uniformly
for obj in cmd.get_object_list():
    cmd.do("util.cbc %s" % obj)
```

### Grid with pLDDT Coloring

```python
cmd.set("grid_mode", 1)
for obj in cmd.get_object_list():
    cmd.spectrum("b", "red_yellow_green_cyan_blue", obj, minimum=50, maximum=90)
cmd.show("cartoon")
```

### Exit Grid Mode

```python
cmd.set("grid_mode", 0)
```

## Before/After Overlay

### Design vs. Template

```python
cmd.load("template.pdb", "template")
cmd.load("design.pdb", "design")

cmd.align("design", "template")
cmd.color("gray70", "template")
cmd.color("marine", "design")
cmd.show("cartoon")

rms = cmd.rms_cur("design and name CA", "template and name CA")
print("Template-design RMSD: %.2f A" % rms)
```

### Design vs. AF2 Prediction

```python
cmd.load("rfdiffusion_output.pdb", "backbone")
cmd.load("af2_prediction.pdb", "af2")

cmd.align("af2 and name CA", "backbone and name CA")
rms = cmd.rms_cur("af2 and name CA", "backbone and name CA")
print("Self-consistency RMSD: %.2f A" % rms)

cmd.color("cyan", "backbone")
cmd.color("green", "af2")
```

### Color by Deviation

```python
# After alignment, highlight regions with large deviations
# Select well-matching and poorly-matching regions
cmd.select("good_match", "af2 within 1.0 of backbone")
cmd.select("poor_match", "af2 and not (af2 within 2.0 of backbone)")
cmd.color("green", "good_match")
cmd.color("red", "poor_match")
```

## Ranking by Metrics

### Score and Rank Designs

```python
import glob, os

results = []
for obj in cmd.get_object_list():
    # Mean pLDDT
    stored.bfactors = []
    cmd.iterate("%s and name CA" % obj, "stored.bfactors.append(b)")
    mean_plddt = sum(stored.bfactors) / len(stored.bfactors) if stored.bfactors else 0

    # Length
    n_res = cmd.count_atoms("%s and name CA" % obj)

    results.append((obj, mean_plddt, n_res))

# Sort by pLDDT descending
results.sort(key=lambda x: -x[1])
print("\nDesign Rankings:")
print("%-30s  pLDDT  Length" % "Name")
print("-" * 50)
for name, plddt, n in results:
    print("%-30s  %5.1f  %5d" % (name, plddt, n))
```

### Rank with RMSD (Self-Consistency)

```python
import glob, os

design_dir = "/path/to/designs"
pred_dir = "/path/to/af2_predictions"

results = []
for f in sorted(glob.glob(os.path.join(pred_dir, "*.pdb"))):
    pred_name = os.path.splitext(os.path.basename(f))[0]
    cmd.load(f, pred_name)

    # Find corresponding design
    design_name = pred_name.replace("_pred", "")
    design_file = os.path.join(design_dir, design_name + ".pdb")
    if os.path.exists(design_file):
        cmd.load(design_file, "tmp_design")
        rms = cmd.align("%s and name CA" % pred_name, "tmp_design and name CA")
        rmsd = rms[0]
        cmd.delete("tmp_design")
    else:
        rmsd = -1

    stored.bfactors = []
    cmd.iterate("%s and name CA" % pred_name, "stored.bfactors.append(b)")
    mean_plddt = sum(stored.bfactors) / len(stored.bfactors) if stored.bfactors else 0

    results.append((pred_name, mean_plddt, rmsd))

# Sort by combined score (high pLDDT, low RMSD)
results.sort(key=lambda x: (-x[1], x[2]))
print("\nDesign Rankings (pLDDT + self-consistency):")
print("%-30s  pLDDT   RMSD  Pass?" % "Name")
print("-" * 60)
for name, plddt, rmsd in results:
    passed = "Y" if plddt > 80 and 0 < rmsd < 1.5 else "N"
    print("%-30s  %5.1f  %5.2f  %s" % (name, plddt, rmsd, passed))
```

## Iteration Tracking

### Compare Design Rounds

```python
# Load designs from different rounds
cmd.load("round1/best_design.pdb", "round1")
cmd.load("round2/best_design.pdb", "round2")
cmd.load("round3/best_design.pdb", "round3")

# Align all to round 1
cmd.align("round2", "round1")
cmd.align("round3", "round1")

# Color by round
cmd.color("gray70", "round1")
cmd.color("marine", "round2")
cmd.color("green", "round3")
cmd.show("cartoon")
```

### Track Improvement

```python
rounds = ["round1", "round2", "round3"]
print("\nIteration Progress:")
print("%-10s  pLDDT  RMSD_vs_r1" % "Round")
print("-" * 35)
for r in rounds:
    stored.bfactors = []
    cmd.iterate("%s and name CA" % r, "stored.bfactors.append(b)")
    mean_plddt = sum(stored.bfactors) / len(stored.bfactors) if stored.bfactors else 0

    if r == "round1":
        rmsd = 0.0
    else:
        rms = cmd.align("%s and name CA" % r, "round1 and name CA")
        rmsd = rms[0]

    print("%-10s  %5.1f  %5.2f" % (r, mean_plddt, rmsd))
```

## Multi-Chain Design Comparison

### Compare Designed Binders Against Same Target

```python
# Load target + multiple binder designs
cmd.load("target.pdb", "target")
cmd.color("gray80", "target")
cmd.show("surface", "target")
cmd.set("transparency", 0.7, "target")

binder_colors = ["marine", "green", "salmon", "orange", "cyan"]
for i, f in enumerate(sorted(glob.glob("/path/to/binders/*.pdb"))):
    name = "binder_%d" % i
    cmd.load(f, name)
    cmd.align(name, "target")
    cmd.color(binder_colors[i % len(binder_colors)], name)
    cmd.show("cartoon", name)
```

## Motif Fidelity Comparison

For motif scaffolding: compare how well each scaffold preserves the motif geometry.

```python
cmd.load("original_motif.pdb", "motif_ref")

motif_resi = "10-30"  # residue range of motif in scaffolds

for obj in cmd.get_object_list():
    if obj == "motif_ref":
        continue
    rms = cmd.align(
        "%s and resi %s and name CA" % (obj, motif_resi),
        "motif_ref and name CA"
    )
    print("%s motif RMSD: %.2f A" % (obj, rms[0]))
```

### Motif Fidelity Table

| RMSD | Interpretation |
|------|---------------|
| < 0.5 A | Excellent — motif geometry preserved |
| 0.5-1.0 A | Good — minor backbone deviations |
| 1.0-2.0 A | Marginal — check functional contacts |
| > 2.0 A | Poor — motif likely non-functional |

## Publication Comparison Figures

### Side-by-Side Panels

```python
import os
output_dir = os.path.expanduser("~/Desktop/design_comparison")
os.makedirs(output_dir, exist_ok=True)

# Store views for each design
designs = cmd.get_object_list()[:4]  # top 4
for d in designs:
    cmd.disable("all")
    cmd.enable(d)
    cmd.orient(d)
    cmd.spectrum("b", "red_yellow_green_cyan_blue", d, minimum=50, maximum=90)
    cmd.ray(1200, 900)
    cmd.png(os.path.join(output_dir, d + ".png"), dpi=300)
    print("Saved %s.png" % d)

cmd.enable("all")
```

### Grid Export

```python
cmd.set("grid_mode", 1)
cmd.show("cartoon")
for obj in cmd.get_object_list():
    cmd.spectrum("b", "red_yellow_green_cyan_blue", obj, minimum=50, maximum=90)
cmd.ray(2400, 1800)
cmd.png(os.path.expanduser("~/Desktop/design_grid.png"), dpi=300)
cmd.set("grid_mode", 0)
```

## Tips

- Grid mode (`grid_mode=1`) is essential for screening >5 designs
- Sort by pLDDT descending + RMSD ascending for combined ranking
- Self-consistency RMSD < 1.5 A AND pLDDT > 80 is the standard pass filter
- Color by pLDDT in grid view for instant visual screening
- For motif scaffolding, always check motif RMSD separately from full-structure RMSD
- Export grid views at high resolution for lab presentations
- Use consistent colors: gray=template/target, marine=best design, green=AF2 prediction
- See @publication-figures for detailed export settings

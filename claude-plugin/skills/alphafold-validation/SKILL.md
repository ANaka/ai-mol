---
name: alphafold-validation
description: Use when validating protein designs with AlphaFold2/AlphaFold3/ESMFold predictions, coloring by pLDDT or pAE, computing self-consistency RMSD, or screening design candidates through PyMOL.
version: 0.1.0
---

# AlphaFold / ESMFold Validation Visualization

Workflows for validating designed proteins using structure prediction confidence metrics in PyMOL. Composes with @proteinmpnn-viz (upstream sequence design) and @design-comparison (batch screening).

> **Send all `cmd.*` code via:** `~/.pymol-agent-bridge/bin/pymol-agent-bridge exec "..."` (or heredoc for multi-line). See @pymol-fundamentals for details.

## pLDDT Coloring

AlphaFold and ESMFold store per-residue confidence (pLDDT) in the B-factor column of output PDBs. Higher = more confident.

### Standard pLDDT Spectrum

```python
cmd.load("af2_prediction.pdb", "af2")
cmd.show("cartoon", "af2")

# Continuous spectrum: blue=high confidence, red=low
cmd.spectrum("b", "red_yellow_green_cyan_blue", "af2", minimum=50, maximum=90)
```

### AlphaFold Database Color Scheme

The official AF color scheme uses discrete confidence bands:

```python
# AlphaFold Database official colors
cmd.color("blue", "af2 and b > 90")           # Very high confidence
cmd.color("cornflowerblue", "af2 and b > 70 and b <= 90")  # High confidence
cmd.color("yellow", "af2 and b > 50 and b <= 70")          # Low confidence
cmd.color("orange", "af2 and b <= 50")         # Very low confidence
```

### Interpretation

| pLDDT Range | Color | Interpretation |
|-------------|-------|---------------|
| > 90 | Blue | Very high confidence — well-folded |
| 70-90 | Cornflower blue | Confident — expect correct fold |
| 50-70 | Yellow | Low confidence — may be disordered or flexible |
| < 50 | Orange | Very low — likely disordered, unstructured |

## Self-Consistency RMSD

The gold-standard design validation: does the designed sequence fold back into the intended structure?

### Single Design Validation

```python
cmd.load("rfdiffusion_output.pdb", "design")
cmd.load("af2_prediction.pdb", "af2_pred")

# Align on backbone
rms = cmd.align("af2_pred and name CA", "design and name CA")
print("Self-consistency CA-RMSD: %.2f A" % rms[0])

# Visualize both
cmd.color("cyan", "design")
cmd.color("green", "af2_pred")
cmd.show("cartoon")
```

### Color by Per-Residue Deviation

```python
# After alignment, color AF2 prediction by deviation from design
cmd.align("af2_pred", "design")

# Use pair_fit to get per-residue distances, or approximate with:
cmd.select("good_match", "af2_pred within 1.5 of design")
cmd.select("poor_match", "af2_pred and not good_match")
cmd.color("green", "good_match")
cmd.color("red", "poor_match")
```

### Pass/Fail Table

| Metric | Pass | Marginal | Fail |
|--------|------|----------|------|
| CA-RMSD (full) | < 1.5 A | 1.5-2.5 A | > 2.5 A |
| CA-RMSD (interface) | < 2.0 A | 2.0-3.0 A | > 3.0 A |
| Mean pLDDT | > 80 | 60-80 | < 60 |
| pLDDT at interface | > 70 | 50-70 | < 50 |

## pAE (Predicted Aligned Error)

pAE measures the expected position error of residue j when aligned on residue i. Low pAE between domains indicates confident relative positioning.

### Interpreting pAE for Design

AlphaFold outputs pAE as a JSON matrix. Low inter-domain pAE indicates the model is confident about the relative arrangement.

```python
# pAE is not directly loadable into PyMOL — it's a 2D matrix
# Useful checks from pAE:
# - Low intra-chain pAE: chain folds well
# - Low inter-chain pAE: confident about binding mode
# - High inter-chain pAE: AF2 is unsure about the complex — design may not bind

# For visualization, focus on pLDDT and RMSD in PyMOL
# pAE is best viewed as a heatmap (matplotlib, ChimeraX, or AF2 notebook)
```

## AF2-Multimer Validation (Binder Design)

For designed binders, validate the complex with AF2-Multimer.

### Load and Inspect Complex

```python
cmd.load("af2_multimer_prediction.pdb", "af2_complex")
cmd.show("cartoon")

chains = cmd.get_chains("af2_complex")
# Typically: target=chain A, binder=chain B

cmd.color("gray70", "chain A")    # target
cmd.color("marine", "chain B")    # designed binder
```

### Interface pLDDT

```python
# Check confidence specifically at the binding interface
cmd.select("interface_A", "chain A and byres (chain A within 5 of chain B)")
cmd.select("interface_B", "chain B and byres (chain B within 5 of chain A)")

# Color interface by pLDDT
cmd.spectrum("b", "red_yellow_green_cyan_blue", "interface_A", minimum=50, maximum=90)
cmd.spectrum("b", "red_yellow_green_cyan_blue", "interface_B", minimum=50, maximum=90)
cmd.show("sticks", "interface_A or interface_B")
```

### Interface Metrics

```python
# Count interface contacts
n_contacts = cmd.count_atoms("chain B and byres (chain B within 4 of chain A) and name CA")
print("Interface residues (binder): %d" % n_contacts)

# H-bonds across interface
cmd.distance("interface_hbonds", "chain A", "chain B", mode=2)
# Count H-bonds from the distance object (each bond = 2 pseudoatoms)
n_hbonds = cmd.count_atoms("interface_hbonds") // 2
print("Interface H-bonds: ~%d" % n_hbonds)
```

## Batch Screening

Screen many designs at once using pLDDT and RMSD.

### Load and Score All Predictions

```python
import glob, os

pred_dir = "/path/to/af2_predictions"
design_dir = "/path/to/rfdiffusion_outputs"

results = []
for f in sorted(glob.glob(os.path.join(pred_dir, "*.pdb"))):
    name = os.path.splitext(os.path.basename(f))[0]
    cmd.load(f, name)

    # Mean pLDDT
    stored.bfactors = []
    cmd.iterate("%s and name CA" % name, "stored.bfactors.append(b)")
    mean_plddt = sum(stored.bfactors) / len(stored.bfactors) if stored.bfactors else 0

    # Self-consistency RMSD (if design file exists)
    design_file = os.path.join(design_dir, name.replace("_pred", "") + ".pdb")
    if os.path.exists(design_file):
        cmd.load(design_file, "tmp_design")
        rms = cmd.align("%s and name CA" % name, "tmp_design and name CA")
        rmsd = rms[0]
        cmd.delete("tmp_design")
    else:
        rmsd = -1

    results.append((name, mean_plddt, rmsd))
    print("%s: pLDDT=%.1f, RMSD=%.2f" % (name, mean_plddt, rmsd))

# Summary
passing = [(n, p, r) for n, p, r in results if p > 80 and 0 < r < 1.5]
print("\nPassing designs: %d / %d" % (len(passing), len(results)))
```

### Grid View with pLDDT Coloring

```python
# After batch loading, apply pLDDT coloring to all and tile
for obj in cmd.get_object_list():
    cmd.spectrum("b", "red_yellow_green_cyan_blue", obj, minimum=50, maximum=90)

cmd.set("grid_mode", 1)
cmd.show("cartoon")
```

## ESMFold-Specific

ESMFold is ~60x faster than AF2 — ideal for rapid first-pass screening of hundreds of designs.

```python
# ESMFold outputs are identical in format (pLDDT in B-factor)
# Same coloring commands apply:
cmd.load("esmfold_prediction.pdb", "esm")
cmd.spectrum("b", "red_yellow_green_cyan_blue", "esm", minimum=50, maximum=90)
cmd.show("cartoon")
```

### ESMFold vs. AF2 Comparison

```python
cmd.load("esmfold_pred.pdb", "esm_pred")
cmd.load("af2_pred.pdb", "af2_pred")

cmd.align("esm_pred and name CA", "af2_pred and name CA")
rms = cmd.rms_cur("esm_pred and name CA", "af2_pred and name CA")
print("ESMFold vs AF2 RMSD: %.2f A" % rms)

cmd.color("salmon", "esm_pred")
cmd.color("marine", "af2_pred")
```

## Tips

- pLDDT is in the B-factor column — `spectrum b` is your primary tool
- Self-consistency RMSD < 1.5 A is the standard pass threshold
- AF2-Multimer interface pLDDT > 70 suggests confident binding prediction
- ESMFold is great for rapid screening; use AF2 for final validation
- Low inter-chain pAE in AF2-Multimer is a strong positive signal for binder design
- ProteinMPNN outputs have idealized sidechains — AF2 predictions show realistic packing
- Always check both pLDDT AND RMSD — high pLDDT with high RMSD means AF2 is confident in a *different* fold

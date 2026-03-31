---
name: proteinmpnn-viz
description: Use when visualizing ProteinMPNN or LigandMPNN sequence design results, inspecting designed vs. fixed residues, viewing per-position confidence, or analyzing sequence design outputs through PyMOL.
version: 0.1.0
---

# ProteinMPNN / LigandMPNN Visualization

Workflows for inspecting sequence design outputs in PyMOL. Composes with @rfdiffusion-viz (upstream backbone) and @alphafold-validation (downstream validation).

> **Send all `cmd.*` code via:** `~/.pymol-agent-bridge/bin/pymol-agent-bridge exec "..."` (or heredoc for multi-line). See @pymol-fundamentals for details.

## Loading ProteinMPNN Outputs

ProteinMPNN outputs PDB files with designed sequences threaded onto the input backbone. Sidechains are idealized — expect them to look "strange" until relaxed or validated by AF2.

```python
cmd.load("seqs/design_0_dldesign_0.pdb", "mpnn_design")
cmd.remove("resn HOH+WAT")
cmd.show("cartoon")
cmd.orient()
```

### Batch Loading Sequence Variants

```python
import glob, os
seq_dir = "/path/to/proteinmpnn/seqs"
for f in sorted(glob.glob(os.path.join(seq_dir, "*.pdb"))):
    name = os.path.splitext(os.path.basename(f))[0]
    cmd.load(f, name)
```

## Designed vs. Fixed Residues

In most ProteinMPNN runs, some positions are fixed (e.g., catalytic residues, motif) while others are redesigned.

### Coloring by Design Status

```python
# If you know which residues were fixed (e.g., from the design_residues input)
fixed_resi = "10+15+20+45+73"  # residues that were NOT designed
cmd.select("fixed", "mpnn_design and resi %s" % fixed_resi)
cmd.select("designed", "mpnn_design and not fixed")

cmd.color("cyan", "fixed")       # fixed = cyan (matches @rfd3 scheme)
cmd.color("magenta", "designed")  # designed = magenta

cmd.show("sticks", "fixed")
cmd.show("cartoon", "designed")
```

### Showing Designed Sidechains

```python
# Show sidechains only for designed residues
cmd.show("sticks", "designed and sidechain")
cmd.hide("sticks", "fixed and sidechain")

# Color by element for designed sidechains
cmd.util.cbag("designed")  # carbons green
```

## Per-Position Confidence

ProteinMPNN outputs per-position log-probabilities. These can be mapped to B-factors for visualization.

### If Scores Are in B-Factor Column

```python
# ProteinMPNN score (lower = more confident for that position)
cmd.spectrum("b", "green_white_red", "mpnn_design", minimum=-3, maximum=0)
# Green = high confidence, Red = low confidence
```

### Manual Score Loading

If you have a separate score file (e.g., from `--score_only` mode or parsed output):

```python
# Load per-residue scores into B-factors
# scores is a dict: {resi_number: score}
scores = {1: -2.5, 2: -1.8, 3: -0.5}  # example
for resi, score in scores.items():
    cmd.alter("mpnn_design and resi %d" % resi, "b=%f" % score)
cmd.rebuild()
cmd.spectrum("b", "green_white_red", "mpnn_design")
```

## Sequence Recovery Analysis

Compare designed sequence to the original (wild-type) sequence to see what changed.

```python
# Load both original and designed
cmd.load("original.pdb", "wildtype")
cmd.load("seqs/design_0.pdb", "designed")

# Align
cmd.align("designed", "wildtype")

# Identify mutations by comparing residue names at each position
stored.wt_seq = []
stored.des_seq = []
cmd.iterate("wildtype and name CA", "stored.wt_seq.append((resi, resn))")
cmd.iterate("designed and name CA", "stored.des_seq.append((resi, resn))")

# Select mutated positions
mutated = []
for (r1, n1), (r2, n2) in zip(stored.wt_seq, stored.des_seq):
    if n1 != n2:
        mutated.append(r1)

if mutated:
    mut_sel = "+".join(mutated)
    cmd.select("mutations", "designed and resi %s" % mut_sel)
    cmd.show("sticks", "mutations")
    cmd.color("orange", "mutations")
    print("Mutated positions: %s" % mut_sel)
    print("Sequence recovery: %.1f%%" % (100 * (1 - len(mutated)/len(stored.wt_seq))))
```

## Multi-Sequence Comparison

Compare multiple ProteinMPNN sequence designs on the same backbone.

### Grid View

```python
# Load all sequences, then tile
cmd.set("grid_mode", 1)
cmd.show("cartoon")

# Color mutations relative to first design
# (useful for spotting consensus positions)
```

### Consensus Visualization

```python
# After loading multiple designs, identify consensus positions
# (positions where all designs agree)
stored.all_seqs = {}
stored.all_resi = {}
for obj in cmd.get_object_list():
    stored.all_seqs[obj] = []
    stored.all_resi[obj] = []
    cmd.iterate("%s and name CA" % obj, "stored.all_seqs['%s'].append(resn); stored.all_resi['%s'].append(resi)" % (obj, obj))

n_designs = len(stored.all_seqs)
ref_obj = cmd.get_object_list()[0]
ref_resi = stored.all_resi[ref_obj]
n_positions = len(ref_resi)
consensus = []
variable = []
for i in range(n_positions):
    residues = set(seq[i] for seq in stored.all_seqs.values())
    if len(residues) == 1:
        consensus.append(ref_resi[i])
    else:
        variable.append(ref_resi[i])

# Color: consensus = blue, variable = red
if consensus:
    cmd.color("marine", "%s and resi %s" % (ref_obj, "+".join(consensus)))
if variable:
    cmd.color("salmon", "%s and resi %s" % (ref_obj, "+".join(variable)))
print("Consensus positions: %d/%d (%.0f%%)" % (len(consensus), n_positions, 100*len(consensus)/n_positions))
```

## Tied Positions

ProteinMPNN supports "tied positions" — residues constrained to have the same amino acid across chains (e.g., symmetric interfaces).

```python
# Highlight tied positions
tied_groups = [(("A", "10"), ("B", "10")), (("A", "25"), ("B", "25"))]
for i, group in enumerate(tied_groups):
    sels = " or ".join("(chain %s and resi %s)" % (c, r) for c, r in group)
    cmd.select("tied_%d" % i, sels)
    cmd.show("sticks", "tied_%d" % i)
    # Each group gets a distinct color
cmd.color("tv_blue", "tied_0")
cmd.color("tv_red", "tied_1")
```

## LigandMPNN-Specific

LigandMPNN designs sequences in the context of a bound ligand. Visualize the ligand context.

```python
# Load LigandMPNN output
cmd.load("ligandmpnn_output.pdb", "lig_design")

# Show ligand
cmd.select("ligand", "organic")
cmd.show("sticks", "ligand")
cmd.color("yellow", "ligand")

# Show designed residues near ligand
cmd.select("near_lig", "byres (polymer.protein within 4 of ligand)")
cmd.show("sticks", "near_lig")
cmd.color("magenta", "near_lig and elem C")

# H-bonds to ligand
cmd.distance("lig_hbonds", "ligand", "near_lig", mode=2)
cmd.set("dash_color", "yellow", "lig_hbonds")
```

## Tips

- ProteinMPNN outputs have idealized sidechains — they look "wrong" until relaxed or predicted by AF2. This is expected.
- Use `grid_mode=1` to compare multiple sequence designs at a glance
- Designed residues = magenta, fixed = cyan (matches @rfd3 scheme)
- For ligand-aware design, use LigandMPNN and visualize ligand contacts
- Sequence recovery % is a useful metric but low recovery is not necessarily bad — it means the design found a better solution
- Always validate with AF2/ESMFold (see @alphafold-validation)

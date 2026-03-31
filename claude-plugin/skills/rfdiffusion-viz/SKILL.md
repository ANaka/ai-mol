---
name: rfdiffusion-viz
description: Use when inspecting RFdiffusion/RFdiffusion2/RFdiffusion3 outputs, viewing diffusion trajectories, tiling scaffold candidates, or performing visual QC on generated backbones through PyMOL.
version: 0.1.0
---

# RFdiffusion Output Visualization

Workflows for inspecting and QC'ing RFdiffusion backbone outputs in PyMOL. Composes with @rfd3 (config building) and @proteinmpnn-viz (sequence design step).

> **Send all `cmd.*` code via:** `~/.pymol-agent-bridge/bin/pymol-agent-bridge exec "..."` (or heredoc for multi-line). See @pymol-fundamentals for details.

## Loading Outputs

### Single Design

```python
cmd.load("/path/to/output/design_0.pdb", "design_0")
cmd.remove("resn HOH+WAT")
cmd.show("cartoon")
cmd.orient()
```

### Batch Loading

```python
import glob, os
output_dir = "/path/to/rfdiffusion/output"
for f in sorted(glob.glob(os.path.join(output_dir, "*.pdb"))):
    name = os.path.splitext(os.path.basename(f))[0]
    cmd.load(f, name)
```

## Trajectory Visualization

RFdiffusion outputs trajectory files in a `/traj/` subdirectory as multi-state PDBs showing the diffusion process from noise to structure.

### Load and Play Trajectory

```python
cmd.load("/path/to/output/traj/design_0_pX0_traj.pdb", "trajectory")
cmd.show("cartoon", "trajectory")
cmd.spectrum("count", "blue_white_red", "trajectory")

# Play through states
cmd.mset("1 -%d" % cmd.count_states("trajectory"))
cmd.mplay()
```

### View Specific Steps

```python
# First frame (noise)
cmd.frame(1)

# Last frame (final structure)
cmd.frame(cmd.count_states("trajectory"))

# Midpoint
n = cmd.count_states("trajectory")
cmd.frame(n // 2)
```

## Grid Tiling for Batch QC

Tile all designs in a grid for rapid visual screening.

```python
# Load all outputs first, then:
cmd.set("grid_mode", 1)
cmd.show("cartoon")

# Optional: color each by chain
for obj in cmd.get_object_list():
    cmd.do("util.cbc " + obj)
```

### Exit Grid Mode

```python
cmd.set("grid_mode", 0)
```

## Contig Region Coloring

Color designed vs. fixed regions using the standard design color scheme (see @rfd3 for full scheme).

```python
# Color scheme: cyan=fixed/motif, magenta=designed, yellow=ligand
# Assuming the contig was: [5-25/A10-30/30-50]
# Residues 1-25 are designed, 26-46 are from motif (A10-30), 47-71 are designed

cmd.color("magenta", "design_0 and resi 1-25")   # designed
cmd.color("cyan", "design_0 and resi 26-46")      # fixed motif
cmd.color("magenta", "design_0 and resi 47-71")   # designed

cmd.show("sticks", "design_0 and resi 26-46")     # show motif as sticks
```

### Automated Region Identification

```python
# If you know the motif residues from the input PDB:
cmd.select("motif_region", "design_0 and resi 26-46")
cmd.select("designed_region", "design_0 and not motif_region")

cmd.color("cyan", "motif_region")
cmd.color("magenta", "designed_region")
cmd.show("sticks", "motif_region")
cmd.show("cartoon", "designed_region")
```

## Self-Consistency Check

Align the RFdiffusion output to the AlphaFold2 prediction of the designed sequence to validate designability. See @alphafold-validation for the AF2 side.

```python
# Load both
cmd.load("rfdiffusion_output.pdb", "design")
cmd.load("af2_prediction.pdb", "af2_pred")

# Align on CA atoms
rms = cmd.align("af2_pred and name CA", "design and name CA")
print("Self-consistency RMSD: %.2f A" % rms[0])

# Color by deviation
cmd.color("green", "af2_pred")
cmd.color("cyan", "design")
```

### Pass/Fail Criteria

| Metric | Pass | Marginal | Fail |
|--------|------|----------|------|
| CA-RMSD | < 1.5 A | 1.5-2.5 A | > 2.5 A |
| pLDDT (AF2) | > 80 | 60-80 | < 60 |

## Motif RMSD (Scaffolding QC)

For motif scaffolding designs, verify the motif geometry is preserved.

```python
# Align only the motif residues
# Suppose motif is residues 26-46 in the design, 10-30 in the original
cmd.align("design and resi 26-46 and name CA", "original and chain A and resi 10-30 and name CA")

# Per-atom RMSD for motif
rms = cmd.rms_cur("design and resi 26-46 and name CA", "original and chain A and resi 10-30 and name CA")
print("Motif RMSD: %.2f A" % rms)
```

### Motif Fidelity Criteria

| RMSD | Interpretation |
|------|---------------|
| < 0.5 A | Excellent motif preservation |
| 0.5-1.0 A | Good — minor backbone shifts |
| 1.0-2.0 A | Marginal — check contacts |
| > 2.0 A | Poor — motif geometry distorted |

## Binder Design Outputs

For binder design runs (target + designed binder), visualize the complex.

```python
cmd.load("binder_design.pdb", "complex")

# Identify chains
chains = cmd.get_chains("complex")
# Typically: target=chain A, binder=chain B

cmd.color("gray80", "chain A")       # target
cmd.color("marine", "chain B")       # designed binder
cmd.show("surface", "chain A")
cmd.set("transparency", 0.7, "chain A")
cmd.show("cartoon", "chain B")
```

### Hotspot Contacts

```python
# Show designed binder residues contacting the target
cmd.select("interface_binder", "byres (chain B within 4 of chain A)")
cmd.select("interface_target", "byres (chain A within 4 of chain B)")
cmd.show("sticks", "interface_binder")
cmd.show("sticks", "interface_target")

# H-bonds across the interface
cmd.distance("interface_hbonds", "chain A", "chain B", mode=2)
cmd.set("dash_color", "yellow", "interface_hbonds")
```

## Symmetric Assembly Outputs

```python
cmd.load("symmetric_design.pdb", "assembly")
cmd.do("util.cbc assembly")  # color by chain
cmd.show("cartoon")

# Show inter-subunit contacts
chains = cmd.get_chains("assembly")
if len(chains) >= 2:
    cmd.select("interface_AB", "byres (chain %s within 4 of chain %s)" % (chains[0], chains[1]))
    cmd.show("sticks", "interface_AB")
```

## Tips

- Always remove waters before inspecting: `cmd.remove("resn HOH+WAT")`
- Grid mode (`grid_mode=1`) is essential for screening >5 designs
- Trajectory files can be large — load one at a time for smooth playback
- Self-consistency RMSD < 1.5 A is the standard designability threshold
- Color scheme matches @rfd3: cyan=fixed, magenta=designed, yellow=ligand

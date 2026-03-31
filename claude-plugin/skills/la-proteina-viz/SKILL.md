---
name: la-proteina-viz
description: Use when setting up, configuring, running, or inspecting La-Proteina protein generation tasks including unconditional design and motif scaffolding. Helps build configs and visualize outputs through PyMOL.
version: 0.1.0
---

# La-Proteina: Config Builder + Visualization

This skill guides Claude through setting up, configuring, and running [La-Proteina](https://github.com/NVIDIA-Digital-Bio/la-proteina) (NVIDIA) atomistic protein generation, and visualizing results in PyMOL. La-Proteina jointly generates backbone AND sidechains via partially latent flow matching.

Composes with @alphafold-validation (design validation), @design-comparison (batch QC), and @proteina-complexa-viz (binder design extension).

> **Send all `cmd.*` code via:** `~/.pymol-agent-bridge/bin/pymol-agent-bridge exec "..."` (or heredoc for multi-line). See @pymol-fundamentals for details.

## Key Difference from RFdiffusion

- **Full atomistic output** — generates backbone + sidechains jointly (no separate ProteinMPNN step needed)
- **Latent representation** — side chains encoded as per-residue latent variables
- **Supports 100-800 residues** across three model variants

---

## Setup

### Environment

```bash
mamba env create -f environment.yaml
mamba activate laproteina_env
pip install torch==2.7.0 --index-url https://download.pytorch.org/whl/cu118
pip install graphein==1.7.7 --no-deps
pip install torch_geometric torch_scatter torch_sparse torch_cluster
```

### Required Files

Create `.env` in the repo root:
```
DATA_PATH=/path/to/your/dataset
```

Checkpoints go in `./checkpoints_laproteina/`.

---

## Model Selection Guide

### Unconditional Generation

| Model | Checkpoint | Features | Length Range |
|-------|-----------|----------|-------------|
| **LD1** | `LD1_ucond_notri_512.ckpt` | No triangular layers | Up to 500 |
| **LD2** | `LD2_ucond_tri_512.ckpt` | Triangular multiplicative layers | Up to 500 |
| **LD3** | `LD3_ucond_notri_800.ckpt` | No triangular layers | 300-800 |

**Autoencoder pairing:**
- LD1, LD2 → `AE1_ucond_512.ckpt`
- LD3 → `AE2_ucond_800.ckpt`

### Motif Scaffolding

| Model | Checkpoint | Motif Type | Atom Detail |
|-------|-----------|------------|-------------|
| **LD4** | `LD4_motif_idx_aa.ckpt` | Indexed | All-atom |
| **LD5** | `LD5_motif_idx_tip.ckpt` | Indexed | Tip-atom |
| **LD6** | `LD6_motif_uidx_aa.ckpt` | Unindexed | All-atom |
| **LD7** | `LD7_motif_uidx_tip.ckpt` | Unindexed | Tip-atom |

**All motif models use:** `AE3_motif.ckpt`

**Indexed vs. Unindexed:**
- **Indexed** — motif position in the final sequence is specified (e.g., residues 10-25)
- **Unindexed** — motif can appear anywhere in the generated protein

**All-atom vs. Tip-atom:**
- **All-atom** — condition on complete sidechain atoms of motif residues
- **Tip-atom** — condition only on functional tip atoms (less restrictive, more diverse scaffolds)

---

## Config Reference

### Base Config

All configs derive from `configs/experiment_config/inference_base_release.yaml`. Key parameters:

| Parameter | Type | Description |
|-----------|------|-------------|
| `ckpt_name` | string | Latent diffusion checkpoint filename |
| `autoencoder_ckpt_path` | path | Full path to autoencoder checkpoint |
| `self_cond` | bool | Enable self-conditioning during sampling |
| `sc_scale_noise` | float/dict | Noise scale for backbone and latents |

### Noise Scale Defaults

| Model | Backbone noise | Latent noise |
|-------|---------------|-------------|
| LD1/LD2 | 0.1 | 0.1 |
| LD3 | 0.15 | 0.05 |

### Generation Codes

Defined in `configs/generation/uncod_codes.yaml`:
- Controls length distribution and sample count
- Default: 100 samples per length

### Motif Task Definition

Motif tasks are defined in `configs/generation/motif_dict.yaml` with contig-style specifications.

- Tasks **without** `_TIP` suffix → use all-atom models (LD4/LD6)
- Tasks **with** `_TIP` suffix → use tip-atom models (LD5/LD7)

---

## Running Generation

### Unconditional Generation

```bash
# LD1 — no triangular, up to 500 residues
python proteinfoundation/generate.py --config_name inference_ucond_notri

# LD2 — triangular layers, up to 500 residues
python proteinfoundation/generate.py --config_name inference_ucond_tri

# LD3 — no triangular, 300-800 residues
python proteinfoundation/generate.py --config_name inference_ucond_notri_long
```

### Motif Scaffolding

```bash
# Indexed all-atom
python proteinfoundation/generate.py --config_name inference_motif_idx_aa

# Indexed tip-atom
python proteinfoundation/generate.py --config_name inference_motif_idx_tip

# Unindexed all-atom
python proteinfoundation/generate.py --config_name inference_motif_uidx_aa

# Unindexed tip-atom
python proteinfoundation/generate.py --config_name inference_motif_uidx_tip
```

### Evaluation

```bash
# Download ProteinMPNN weights first
bash script_utils/download_pmpnn_weights.sh

# Run evaluation (co-designability, diversity, RMSD for motif tasks)
python proteinfoundation/evaluate.py --config_name <same_config_name>
```

---

## Deciding Which Model to Use

Ask the user:

1. **What's the task?**
   - "Generate a novel protein fold" → Unconditional (LD1/LD2/LD3)
   - "Scaffold a functional motif" → Motif (LD4-LD7)

2. **If unconditional — how long?**
   - ≤500 residues → LD1 (fast) or LD2 (higher quality with triangular layers)
   - 300-800 residues → LD3

3. **If motif scaffolding — do you know where the motif goes?**
   - "Yes, at specific positions" → Indexed (LD4/LD5)
   - "No, anywhere is fine" → Unindexed (LD6/LD7)

4. **If motif — how strict on sidechain geometry?**
   - "Must preserve exact sidechain positions" → All-atom (LD4/LD6)
   - "Just the functional groups" → Tip-atom (LD5/LD7) — more scaffold diversity

---

## Visualizing Outputs in PyMOL

### Load and Inspect

```python
cmd.load("/path/to/output/sample_0.pdb", "lp_design")
cmd.remove("resn HOH+WAT")
cmd.show("cartoon")
cmd.show("sticks", "sidechain")  # La-Proteina generates real sidechains
cmd.orient()
```

### Fold Quality Check

```python
cmd.dss("lp_design")  # assign secondary structure
cmd.color("marine", "lp_design and ss h")
cmd.color("yellow", "lp_design and ss s")
cmd.color("gray70", "lp_design and ss l+")
n_res = cmd.count_atoms("lp_design and name CA")
print("Design length: %d residues" % n_res)
```

### Sidechain Packing Quality

```python
# La-Proteina generates full sidechains — check packing
cmd.show("sticks", "lp_design and sidechain")
cmd.util.cbag("lp_design")  # color by element, green carbons

# Hydrophobic core
cmd.select("core_hp", "lp_design and resn ALA+VAL+LEU+ILE+MET+PHE+TRP+PRO")
cmd.show("sticks", "core_hp and sidechain")
cmd.color("yellow", "core_hp and elem C")
cmd.show("surface", "lp_design")
cmd.set("transparency", 0.7)
```

### Motif Scaffolding Visualization

```python
motif_resi = "10-25"  # from your motif_dict.yaml config
cmd.select("motif", "lp_design and resi %s" % motif_resi)
cmd.select("scaffold", "lp_design and not motif")

cmd.color("cyan", "motif")       # fixed motif
cmd.color("magenta", "scaffold") # generated scaffold
cmd.show("sticks", "motif")
cmd.show("cartoon", "scaffold")
```

### Motif RMSD (All-Atom)

```python
cmd.load("original_motif.pdb", "motif_ref")
cmd.align("lp_design and resi %s" % motif_resi, "motif_ref")

rms_bb = cmd.rms_cur("lp_design and resi %s and name CA" % motif_resi, "motif_ref and name CA")
rms_all = cmd.rms_cur("lp_design and resi %s and not name H*" % motif_resi, "motif_ref and not name H*")
print("Motif backbone RMSD: %.2f A" % rms_bb)
print("Motif all-atom RMSD: %.2f A" % rms_all)
```

| Metric | Pass | Marginal | Fail |
|--------|------|----------|------|
| Backbone RMSD | < 0.5 A | 0.5-1.0 A | > 1.0 A |
| All-atom RMSD | < 1.0 A | 1.0-2.0 A | > 2.0 A |

### Grid Tiling for Batch QC

```python
cmd.set("grid_mode", 1)
cmd.show("cartoon")
for obj in cmd.get_object_list():
    cmd.dss(obj)
    cmd.color("marine", "%s and ss h" % obj)
    cmd.color("yellow", "%s and ss s" % obj)
    cmd.color("gray70", "%s and ss l+" % obj)
```

### Co-Designability Check

```python
cmd.load("lp_design.pdb", "design")
cmd.load("af2_prediction.pdb", "af2")
cmd.align("af2 and name CA", "design and name CA")
rms = cmd.rms_cur("af2 and name CA", "design and name CA")
print("Co-designability CA-RMSD: %.2f A" % rms)

# Also check sidechain agreement (unique to atomistic generators)
rms_all = cmd.rms_cur("af2 and not name H*", "design and not name H*")
print("All-atom RMSD: %.2f A" % rms_all)
```

## Tips

- **No ProteinMPNN step needed** — La-Proteina co-generates sequence and structure. But you CAN still run ProteinMPNN if you want alternative sequences.
- **All-atom RMSD is more informative** than backbone-only for La-Proteina outputs.
- **Tip-atom models** (LD5/LD7) give more diverse scaffolds at the cost of less strict sidechain geometry.
- **LD2** is the highest-quality unconditional model (triangular layers) but slower.
- Color scheme: cyan=motif, magenta=scaffold (matches @rfd3).
- For validation, see @alphafold-validation. For batch ranking, see @design-comparison.

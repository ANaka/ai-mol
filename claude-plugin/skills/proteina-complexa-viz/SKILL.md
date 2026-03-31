---
name: proteina-complexa-viz
description: Use when setting up, configuring, running, or inspecting Proteina-Complexa protein binder design, ligand binder design, AME motif scaffolding, or monomer motif scaffolding. Helps build configs, select targets, and visualize outputs through PyMOL.
version: 0.1.0
---

# Proteina-Complexa: Config Builder + Visualization

This skill guides Claude through setting up, configuring, and running [Proteina-Complexa](https://github.com/NVIDIA-Digital-Bio/Proteina-Complexa) (NVIDIA) design pipelines, and visualizing results in PyMOL. Proteina-Complexa extends La-Proteina with inference-time optimization for binder design.

Composes with @la-proteina-viz (base model), @alphafold-validation (validation), @design-interface-analysis (interface QC), and @design-comparison (batch ranking).

> **Send all `cmd.*` code via:** `~/.pymol-agent-bridge/bin/pymol-agent-bridge exec "..."` (or heredoc for multi-line). See @pymol-fundamentals for details.

---

## Setup

### Installation

```bash
# UV (recommended, Ubuntu 22.04+)
./env/build_uv_env.sh
source .venv/bin/activate

# Or Docker
docker build -t proteina-complexa -f env/docker/Dockerfile .
```

### Initialize Environment

```bash
complexa init       # creates .env with paths
complexa download   # fetches model weights
```

### Required Environment Variables (.env)

```bash
# Structure predictors
AF2_DIR=/path/to/AF2                    # AlphaFold2 parameters
ESM_DIR=/path/to/ESM2                   # ESM2 weights
RF3_CKPT_PATH=/path/to/rf3.ckpt        # RoseTTAFold3 checkpoint
RF3_EXEC_PATH=/path/to/rf3             # RF3 executable

# Bioinformatics tools
SC_EXEC=/path/to/sc                     # Shape complementarity (CCP4)
FOLDSEEK_EXEC=/path/to/foldseek
MMSEQS_EXEC=/path/to/mmseqs
DSSP_EXEC=/path/to/dssp

# Paths
LOCAL_CODE_PATH=/path/to/Proteina-Complexa
COMMUNITY_MODELS_PATH=${LOCAL_CODE_PATH}/community_models
DATA_PATH=/path/to/PFM_data
```

---

## Pipeline Selection Guide

Ask the user:

1. **What are you designing against?**
   - "A protein target" → **Protein Binder** pipeline
   - "A small molecule" → **Ligand Binder** pipeline
   - "A motif near a ligand" → **AME** pipeline
   - "Just scaffold a motif (no ligand)" → **Monomer Motif** pipeline

### Pipeline → Config → Checkpoint Mapping

| Pipeline | Config File | Model | AE | NGC Collection |
|----------|-------------|-------|----|----|
| **Protein Binder** | `search_binder_local_pipeline.yaml` | `complexa.ckpt` | `complexa_ae.ckpt` | proteina_complexa |
| **Ligand Binder** | `search_ligand_binder_local_pipeline.yaml` | `complexa_ligand.ckpt` | `complexa_ligand_ae.ckpt` | proteina_complexa_ligand |
| **AME** | `search_ame_local_pipeline.yaml` | `complexa_ame.ckpt` | `complexa_ame_ae.ckpt` | proteina_complexa_ame |
| **Monomer Motif** | `search_motif_local_pipeline.yaml` | `complexa_ame.ckpt` | `complexa_ame_ae.ckpt` | proteina_complexa_ame |

---

## Config Structure

Each pipeline config has these sections:

```yaml
# Checkpoint paths (REQUIRED — set these first)
ckpt_path: /path/to/checkpoints
ckpt_name: complexa.ckpt
autoencoder_ckpt_path: /path/to/checkpoints/complexa_ae.ckpt

# Generation
generation:
  task_name: "02_PDL1"          # target identifier
  num_samples: 100              # designs to generate
  num_steps: 100                # diffusion steps
  hotspots: [12, 45, 67]        # optional: target residues to contact

# Reward models
af2folding:
  af_params_dir: ${oc.env:AF2_DIR}
rf3folding:
  ckpt_path: ${oc.env:RF3_CKPT_PATH}
  rf3_path: ${oc.env:RF3_EXEC_PATH}

# Parallelization
gen_njobs: 1                    # generation parallel jobs (1 GPU each)
eval_njobs: 1                   # evaluation parallel jobs

# Run metadata
run_name: my_experiment
```

---

## Target Definition

Targets are defined in YAML files under `configs/design_tasks/`.

### Protein Binder Targets (`binder_dict_v2.yaml`)

```yaml
"02_PDL1":
  pdb_file: path/to/pdl1.pdb
  chains: ["A"]                 # target chains
  motif_chains: []              # empty for pure binder design
```

### Ligand Binder Targets (`ligand_binder_dict_v2.yaml`)

```yaml
"39_7V11_LIGAND":
  pdb_file: path/to/7v11.pdb
  ligand_chain: "A"             # chain containing the ligand
```

### AME Targets (`ame_dict_v2.yaml`)

```yaml
"M0024_1nzy_v3":
  pdb_file: path/to/ame_input.pdb
  # IMPORTANT: Chain A = ligand (residue name "L:0")
  #            Chain B = motif protein residues
```

**Critical AME input rules:**
- Ligands MUST be on chain A with residue name `L:0`
- Motif protein residues on chain B
- Rename ligand residues to `L:0` before RF3 evaluation

### Monomer Motif Targets (`motif_dict_v2.yaml`)

```yaml
"1YCR_AA":
  pdb_file: path/to/motif.pdb
```

### Adding a Custom Target

Use the CLI or add to the appropriate `*_dict_v2.yaml`:

```bash
complexa target add --name "my_target" --pdb /path/to/target.pdb --chains A
complexa target list
complexa target show my_target
```

---

## Running Pipelines

### Full Pipeline (Recommended)

```bash
# Protein binder
complexa design configs/search_binder_local_pipeline.yaml \
  ++run_name=pdl1_binders \
  ++generation.task_name=02_PDL1

# Ligand binder
complexa design configs/search_ligand_binder_local_pipeline.yaml \
  ++run_name=ligand_binders \
  ++generation.task_name=39_7V11_LIGAND

# AME (motif + ligand scaffolding)
complexa design configs/search_ame_local_pipeline.yaml \
  ++run_name=ame_design \
  ++generation.task_name=M0024_1nzy_v3

# Monomer motif scaffolding
complexa design configs/search_motif_local_pipeline.yaml \
  ++run_name=motif_design \
  ++generation.task_name=1YCR_AA
```

### Individual Stages

```bash
complexa generate config.yaml   # generation only
complexa filter config.yaml     # filter by reward scores
complexa evaluate config.yaml   # structure prediction validation
complexa analyze config.yaml    # aggregate results + metrics
```

### Common Overrides

```bash
# More samples
++generation.num_samples=500

# More diffusion steps (higher quality, slower)
++generation.num_steps=200

# Specify hotspots on target
++generation.hotspots=[12,45,67]

# Parallelize
++gen_njobs=4 ++eval_njobs=4

# Custom checkpoint paths
++ckpt_path=/my/checkpoints
++ckpt_name=complexa.ckpt
++autoencoder_ckpt_path=/my/checkpoints/complexa_ae.ckpt
```

### Validate Config Before Running

```bash
complexa validate design configs/search_binder_local_pipeline.yaml
```

### Check Pipeline Status

```bash
complexa status
```

---

## Critical Warnings

- **TMOL reward** is NOT supported for ligand binder/AME pipelines — will fail if enabled
- **AME inputs**: ligands must be chain A, residue name `L:0`; motif protein on chain B
- **RF3 ligand handling**: rename ligand residues to `L:0` before RF3 evaluation

---

## Preparing Targets in PyMOL

### Extract Target Chain for Binder Design

```python
cmd.fetch("7v11")
cmd.remove("resn HOH+WAT+NA+CL+MG+CA+ZN+K+GOL+PEG+EDO+SO4+PO4+ACT+DMS")

# Inspect chains
chains = cmd.get_chains("7v11")
print("Chains: %s" % ", ".join(chains))
for c in chains:
    n = cmd.count_atoms("chain %s and name CA" % c)
    print("  Chain %s: %d residues" % (c, n))

# Extract target chain
cmd.create("target", "7v11 and chain A")
cmd.save("/path/to/target.pdb", "target")
```

### Identify Hotspot Residues

```python
# If you have a known binder, identify contact residues on target
cmd.select("interface", "byres (chain A within 4 of chain B)")
cmd.show("sticks", "interface")
cmd.color("red", "interface")

# List hotspot residue numbers
stored.hotspots = []
cmd.iterate("interface and name CA", "stored.hotspots.append(resi)")
print("Hotspot residues: [%s]" % ",".join(stored.hotspots))
# Use these in: ++generation.hotspots=[...]
```

### Prepare AME Input

```python
# Load structure with both protein motif and ligand
cmd.fetch("1nzy")
cmd.remove("resn HOH+WAT")

# Rename ligand to L:0 on chain A (REQUIRED for AME)
cmd.alter("organic", "chain='A'")
cmd.alter("organic", "resn='L'")
cmd.alter("organic", "resi='0'")

# Motif protein goes on chain B
cmd.alter("polymer.protein and resi 25-40", "chain='B'")

cmd.save("/path/to/ame_input.pdb", "all")
print("AME input saved — verify chain A=ligand(L:0), chain B=motif")
```

### Truncate Large Target

```python
# Proteina-Complexa scales with target size — truncate if large
cmd.remove("chain A and resi 200-400")  # remove distant regions
cmd.save("/path/to/target_truncated.pdb", "chain A")
```

---

## Visualizing Pipeline Outputs

### Load Top Designs

```python
import glob, os
results_dir = "/path/to/complexa/output/generation"
for f in sorted(glob.glob(os.path.join(results_dir, "*.pdb")))[:20]:
    name = os.path.splitext(os.path.basename(f))[0]
    cmd.load(f, name)
cmd.remove("resn HOH+WAT")
cmd.show("cartoon")
```

### Protein Binder Complex

```python
cmd.load("binder_design.pdb", "complex")
chains = cmd.get_chains("complex")
target_chain = chains[0]
binder_chain = chains[-1]

cmd.color("gray80", "chain %s" % target_chain)
cmd.color("marine", "chain %s" % binder_chain)
cmd.show("surface", "chain %s" % target_chain)
cmd.set("transparency", 0.7, "chain %s" % target_chain)
cmd.show("cartoon", "chain %s" % binder_chain)
cmd.show("sticks", "chain %s and sidechain" % binder_chain)
```

### Interface Analysis

```python
cmd.select("interface_target", "byres (chain %s within 4 of chain %s)" % (target_chain, binder_chain))
cmd.select("interface_binder", "byres (chain %s within 4 of chain %s)" % (binder_chain, target_chain))
cmd.show("sticks", "interface_target or interface_binder")
cmd.distance("hbonds", "chain %s" % target_chain, "chain %s" % binder_chain, mode=2)
cmd.set("dash_color", "yellow", "hbonds")
```

### Ligand Binder

```python
cmd.load("ligand_binder.pdb", "lig_complex")
cmd.select("ligand", "organic")
cmd.select("pocket", "byres (polymer.protein within 4 of ligand)")
cmd.show("sticks", "ligand")
cmd.color("yellow", "ligand and elem C")
cmd.show("sticks", "pocket and sidechain")
cmd.color("cyan", "pocket and elem C")
cmd.distance("lig_hbonds", "ligand", "pocket", mode=2)
```

### AME Design

```python
cmd.load("ame_design.pdb", "ame")
cmd.select("ligand", "organic")
motif_resi = "25-40"
cmd.select("motif", "polymer.protein and resi %s" % motif_resi)
cmd.select("scaffold", "polymer.protein and not motif")

cmd.color("cyan", "motif")
cmd.color("magenta", "scaffold")
cmd.color("yellow", "ligand and elem C")
cmd.show("sticks", "motif")
cmd.show("sticks", "ligand")
cmd.show("cartoon", "scaffold")
```

### Batch Grid View

```python
cmd.set("grid_mode", 1)
for obj in cmd.get_object_list():
    chains = cmd.get_chains(obj)
    if len(chains) >= 2:
        cmd.color("gray80", "%s and chain %s" % (obj, chains[0]))
        cmd.color("marine", "%s and chain %s" % (obj, chains[-1]))
cmd.show("cartoon")
```

### Load Metrics from CSV and Rank

```python
import csv, os
results_csv = "/path/to/output/analysis/results.csv"
pdb_dir = "/path/to/output/generation"

with open(results_csv) as f:
    reader = csv.DictReader(f)
    rows = sorted(reader, key=lambda r: -float(r.get("score", 0)))

# Load top 10
for row in rows[:10]:
    name = row.get("name", row.get("design_id", ""))
    pdb_path = os.path.join(pdb_dir, name + ".pdb")
    if os.path.exists(pdb_path):
        cmd.load(pdb_path, name)
        print("%s: score=%.3f" % (name, float(row.get("score", 0))))
```

---

## Tips

- Use `complexa validate` before `complexa design` to catch config errors early
- `complexa design` runs the full pipeline — use individual stages only for debugging
- Hotspots significantly improve binder quality — always identify them from known complexes when possible
- AME is unique to Proteina-Complexa — no other tool does motif + ligand scaffolding jointly
- TMOL reward is NOT supported for ligand/AME pipelines
- For interface analysis, see @design-interface-analysis
- For AF2 validation, see @alphafold-validation
- For batch ranking, see @design-comparison
- Color scheme: gray=target, marine=binder, cyan=motif, magenta=scaffold, yellow=ligand

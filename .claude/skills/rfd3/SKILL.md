# RFD3 Interactive Config Builder with PyMOL

This document guides Claude Code + PyMOL (pymol-agent-bridge) through interactive construction and visualization of RFD3 protein design configurations.

## Prerequisites

- PyMOL running with the pymol-agent-bridge socket plugin (run `pymol-agent-bridge setup`)
- Structure file (PDB or CIF) to design around

## Quick Reference: Color Scheme

| Config Element | Color | Representation |
|---------------|-------|----------------|
| Fixed residues (motif) | cyan | sticks |
| Design regions | magenta | cartoon (transparent) |
| Ligand (RET) | yellow | spheres |
| Hotspots | red | spheres |
| Unindexed motifs | orange | sticks |
| Backbone only | marine | cartoon |
| Target protein (binder design) | gray | surface |
| ORI marker | green | sphere (large) |
| H-bond donors | blue | sticks |
| H-bond acceptors | red | sticks |


PyMOL one-liner:
```python
remove resn HOH+WAT+NA+CL+MG+CA+ZN+K+GOL+PEG+EDO+SO4+PO4+ACT+DMS
```

---

## Interactive Workflow

### Step 1: Load and Inspect Structure

```python
# Load structure
fetch 1ABC  # or: load /path/to/structure.pdb
# Show as cartoon with sequence
as cartoon
color gray
# Show sequence panel
set seq_view, 1
# Label residues
label n. CA, "%s%s" % (resn, resi)
```

**CRITICAL: Verify Residue Numbering**

Before designing contigs, always check the actual residue numbers in your structure. PDB/CIF files often don't start at residue 1 (N-terminal residues may be missing or disordered).

```python
# Check residue range for chain A
stored.resids = []
iterate chain A and name CA, stored.resids.append(int(resi))
print(f"Chain A residues: {min(stored.resids)} to {max(stored.resids)}")
```

For CIF files, be aware of two numbering schemes:
- `label_seq_id`: Sequential numbering used by RFD3 (what you see in PyMOL)
- `auth_seq_id`: Original author numbering from the deposited structure

RFD3 uses `label_seq_id`. If your contig references residues that don't exist (e.g., `A1-19` when the structure starts at residue 8), you'll get an error like:
```
Error: [component=A1] Residue A1 not found in atom array.
```

**Fix**: Adjust your contig to use residue numbers that actually exist in the structure.

### Step 2: Identify Regions

Ask the user what they want to:
- **Fix**: Residues/atoms that should remain unchanged (motifs, active sites)
- **Design**: Regions to be redesigned by RFD3
- **Unindex**: Motifs whose sequence position is unknown to the model

### Step 3: Visualize Selections

#### Fixed Residues (Motif)
```python
# Select and show fixed residues
select fixed_motif, resi 44+80+102+103+105+106
show sticks, fixed_motif
color cyan, fixed_motif
```

#### Design Regions
```python
# Select design region
select design_region, resi 51-79
show cartoon, design_region
color magenta, design_region
set cartoon_transparency, 0.5, design_region
```

#### Ligand
```python
# Show ligand (e.g., retinal RET, or other 3-letter code)
select ligand, resn RET
show spheres, ligand
color yellow, ligand
```

#### Hotspots (for binder design)
```python
# Hotspots on target protein
select hotspots, chain B and resi 10-20+45-50
show spheres, hotspots
color red, hotspots
set sphere_scale, 0.5, hotspots
```

#### Distance from Ligand
```python
# Show residues within 5Å of ligand
select near_ligand, byres (all within 5 of ligand)
show sticks, near_ligand
color tv_orange, near_ligand
```

### Step 4: Review and Confirm

```python
# Center on motif
center fixed_motif
zoom fixed_motif, 10

# Show distances between key residues
distance d1, /struct//A/102/CA, /struct//A/106/CA

# Ray trace for clear view
ray 1200, 900
```

### Step 5: Generate Config

After user confirms the selections, generate the RFD3 config in JSON or Python format.

---

## RFD3 Config Schema

### Core Fields

| Field | Type | Description |
|-------|------|-------------|
| `input` | str | Path to PDB/CIF structure file |
| `contig` | str | Indexed motif specification (see Contig Syntax below) |
| `length` | str | Total length: "min-max" or int |
| `ligand` | str | Ligand 3-letter code(s), comma-separated |
| `unindex` | str or dict | Unindexed motifs (position unknown to model) |

### Selection Fields (InputSelection type)

These accept: `bool`, contig string `"A1-10,B5-8"`, or dict `{"A1-2": "BKBN", "A3": "N,CA,C,O"}`

| Field | Description |
|-------|-------------|
| `select_fixed_atoms` | Atoms with fixed 3D coordinates |
| `select_unfixed_sequence` | Regions where sequence can change |
| `select_buried` | RASA conditioning: buried residues |
| `select_partially_buried` | RASA conditioning: partially buried |
| `select_exposed` | RASA conditioning: exposed residues |
| `select_hotspots` | Target residues for binder design |
| `select_hbond_donor` | H-bond donors (dict only) |
| `select_hbond_acceptor` | H-bond acceptors (dict only) |

**IMPORTANT: No Comment Keys in Selection Dicts**

RFD3 does NOT support underscore-prefixed "comment" keys inside `select_fixed_atoms`, `select_hbond_donor`, or `select_hbond_acceptor` dictionaries. Every key is parsed as a residue selector.

❌ **Invalid** (will fail with "Invalid contig format: '_comment'"):
```json
"select_fixed_atoms": {
    "_comment": "49 fixed residues",
    "_category_pore": "M20, Y22",
    "A20": "ALL",
    "A22": "ALL"
}
```

✅ **Valid** (comments only outside the selection dicts, or omit entirely):
```json
"select_fixed_atoms": {
    "A20": "ALL",
    "A22": "ALL"
}
```

If you need documentation, add comments at the top level of the JSON or in a separate notes file.

### Atom Selection Shortcuts

| Shortcut | Atoms |
|----------|-------|
| `ALL` | All atoms in residue |
| `BKBN` | N, CA, C, O (backbone) |
| `TIP` | Functional tip atoms (varies by residue) |

### Design Options

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `partial_t` | float | None | Partial diffusion noise (Å), recommended 5-15 |
| `symmetry` | dict | None | Symmetry config (id, is_unsym_motif) |
| `redesign_motif_sidechains` | bool | False | Keep backbone, redesign sidechains |
| `ori_token` | list[float] | None | [x, y, z] origin override |
| `infer_ori_strategy` | str | None | "com" or "hotspots" |
| `plddt_enhanced` | bool | True | Enable pLDDT enhancement |
| `is_non_loopy` | bool | True | Fewer loops, more helices |

---

## Contig String Syntax

Contig strings specify which residues to keep vs design.

### Format Rules
- Comma-separated components
- `ChainResid` or `ChainStart-End` = keep from input (e.g., `A1-80`, `A102`)
- Integer or `min-max` = design new residues (e.g., `10` for exactly 10, `50-70` for 50-70 residues)
- `\0` = chain break

**IMPORTANT**: The chain ID goes directly before the residue number with NO dash between them.
- ✅ `A1-80` = keep residues 1-80 from chain A
- ❌ `A-1-80` = INVALID (dash between chain and residue number)
- ✅ `10-20` = design 10-20 new residues (no chain ID = design region)
- ❌ `A-10-20` = INVALID (this is not "design 10-20 residues from chain A")

### Examples

```
A1-80,10,A91-120       # Keep A1-80, design 10, keep A91-120
50-70,A10-30,20        # Design 50-70 residues, keep A10-30, design 20
A1-50,\0,B1-50         # Two chains from input
A40-60,70,A120-170     # Keep 40-60, design exactly 70, keep 120-170
```

### Reading a Contig

For `A40-60,70,A120-170,A203,\0,B3-45,60-80`:
1. `A40-60`: residues 40-60 from chain A (fixed)
2. `70`: design exactly 70 new residues
3. `A120-170`: residues 120-170 from chain A (fixed)
4. `A203`: single residue 203 from chain A (fixed)
5. `\0`: chain break (no peptide bond)
6. `B3-45`: residues 3-45 from chain B (fixed)
7. `60-80`: design 60-80 residues at the end

---

## Output Formats

### JSON Format (for direct RFD3 CLI)

```json
{
    "design_name": {
        "input": "/path/to/structure.pdb",
        "contig": "A1-43,20-30,A74-126",
        "ligand": "RET",
        "length": "150-180",
        "select_fixed_atoms": {
            "A44": "ALL",
            "A80": "BKBN",
            "A102-106": "TIP"
        },
        "is_non_loopy": true,
        "plddt_enhanced": true
    }
}
```

### Python Format (using RFD3ConfigBuilder)

```python
from rfd3_config_builder import RFD3ConfigBuilder

config = (
    RFD3ConfigBuilder.from_structure(
        "/path/to/structure.pdb",
        name="design_name"
    )
    .fix_residues([44, 80, 102, 103, 105, 106])
    .fix_range(1, 43)
    .design_range(44, 73, length=(20, 30))
    .fix_range(74, 126)
    .with_ligand("RET")
    .with_total_length((150, 180))
    .build()
)

spec = config.spec.to_foundry_dict()  # Dict ready for RFD3 JSON input
```

---

## Structure Preparation and Sanitization

Before using a structure with RFD3, it often needs to be cleaned up. The pymol-agent-bridge tool should help identify and remove unwanted components.

### Validating Residue Numbering (CRITICAL)

**This is the most common source of RFD3 errors.** Crystal structures often have:
- Missing N-terminal residues (signal peptides, disordered regions)
- Missing C-terminal residues
- Internal gaps (disordered loops)
- Non-standard numbering (insertions like 45A, 45B)

Before writing any contig string, verify the actual residue range:

```python
# Check residue range in PyMOL
stored.resids = []
iterate chain A and name CA, stored.resids.append(int(resi))
print(f"Chain A: {min(stored.resids)} to {max(stored.resids)}, {len(stored.resids)} residues")

# Check for gaps (missing residues)
resids = sorted(stored.resids)
gaps = [(resids[i], resids[i+1]) for i in range(len(resids)-1) if resids[i+1] - resids[i] > 1]
if gaps:
    print("Gaps found:", gaps)
```

For CIF files specifically, check from command line:
```bash
# Extract residue numbers from CIF (label_seq_id is what RFD3 uses)
grep "^ATOM" structure.cif | awk '{print $7, $9}' | sort -t' ' -k2 -n | uniq | head -5
grep "^ATOM" structure.cif | awk '{print $7, $9}' | sort -t' ' -k2 -n | uniq | tail -5
```

**Common Error:**
```
Error: [component=A1] Residue A1 not found in atom array.
```
This means your contig references `A1` but the structure starts at a higher number.

**Fix:** Adjust contig to match actual residue numbers:
- Original (wrong): `"contig": "A1-19,10-18,A34-80"`
- Fixed: `"contig": "A8-19,10-18,A34-80"` (if structure starts at 8)

### Biological Assembly Issues (Homomers)

CIF files often contain **biological assembly information** that RFD3 will auto-expand, causing errors like:
```
AssertionError: Mismatch in number of residues: expected 1, got 3
```

Check for assembly info:
```bash
grep -i "_pdbx_struct_assembly\|oligomeric" structure.cif
```

If you see `oligomeric_count 3` (or similar), the CIF defines a trimer/multimer that RFD3 will expand.

**Fix:** Convert to PDB format (which strips assembly info):
```python
import biotite.structure.io.pdbx as pdbx
import biotite.structure.io.pdb as pdb
import biotite.structure as struc

# Load CIF (single model, no assembly expansion)
cif_file = pdbx.CIFFile.read("structure.cif")
structure = pdbx.get_structure(cif_file, model=1)

# Filter to protein + ligand
protein_mask = struc.filter_amino_acids(structure)
ligand_mask = structure.res_name == "RET"  # or your ligand
filtered = structure[protein_mask | ligand_mask]

# Save as PDB
pdb_file = pdb.PDBFile()
pdb_file.set_structure(filtered)
pdb_file.write("structure_monomer.pdb")
```

**Note:** PDB files use `auth_seq_id` numbering which may differ from `label_seq_id`. Check residue numbers after conversion and adjust your contig accordingly.

### Identifying Components to Remove

```python
# List all unique residue names (ligands, waters, ions, etc.)
iterate all, stored.resnames.add(resn)
print(sorted(stored.resnames))

# Or visually:
select hetero, hetatm
show spheres, hetero
label hetero and name CA+C1, resn
```

Common components to **remove**:
- Waters: `HOH`, `WAT`, `DOD`
- Ions: `NA`, `CL`, `MG`, `CA`, `ZN`, `K`
- Crystallization additives: `GOL`, `PEG`, `EDO`, `SO4`, `PO4`, `ACT`
- Detergents: `LMT`, `OLC`, `DMS`

Components to **keep** (for opsins):
- Retinal: `RET` (all-trans), `LYR` (Schiff base linked)
- Other functional ligands specific to your protein

### Using remove_ccds in Config

The `cif_parser_args.remove_ccds` field removes unwanted CCD (Chemical Component Dictionary) entries:

```json
{
    "design_with_retinal": {
        "input": "structure.cif",
        "contig": "A1-300",
        "ligand": "RET",
        "cif_parser_args": {
            "remove_ccds": ["HOH", "NA", "CL", "GOL", "PEG", "EDO", "SO4"]
        }
    }
}
```

**Rule of thumb for opsins**: Remove everything except `RET` (or your specific ligand).

### Structure Sanitization in PyMOL

If you need to create a cleaned structure file:

```python
# Load original
load structure.cif, orig

# Remove unwanted components
remove resn HOH+WAT+NA+CL+GOL+PEG+EDO+SO4+PO4+MG+CA+ZN

# Verify only desired components remain
select remaining_het, hetatm
iterate remaining_het, print(resn)  # Should only show RET

# Save cleaned structure
save structure_clean.pdb, all
```

### Handling Multi-chain Structures

For homotrimers/homodimers, decide early:
1. **Use single chain** for simpler design (RFD3 handles symmetry internally)
2. **Keep all chains** for explicit symmetric design

```python
# Extract single chain for monomer design
select chain_a, chain A
save monomer.pdb, chain_a

# Or keep all for symmetric design
# but remove duplicate ligands if needed
remove (resn RET and not chain A)
save trimer_single_ret.pdb, all
```

---

## Origin Token and Centering

The **ORI token** controls where RFD3 places the center of mass of the designed structure. This is critical for:
- Binder design (placing the binder relative to target)
- Symmetric design (placing subunits around origin)
- Motif scaffolding (controlling where new structure grows)

### Understanding ORI Behavior

| `infer_ori_strategy` | Behavior |
|---------------------|----------|
| `"com"` (default) | ORI placed at center of mass of input structure |
| `"hotspots"` | ORI placed 10Å outward from hotspot center of mass |
| (not set) | Inferred based on input type |

The designed structure's center of mass will typically be **within ~5Å of the ORI token**.

### Visualizing Current Center of Mass

```python
# Calculate and show center of mass
com all, state=1
# Creates pseudoatom at COM

# Or manually:
stored.coords = []
iterate_state 1, all and name CA, stored.coords.append([x,y,z])
import numpy as np
com = np.mean(stored.coords, axis=0)
pseudoatom com_marker, pos=list(com)
show spheres, com_marker
color red, com_marker
```

### When to Set ORI Manually

Set `ori_token` explicitly when:
1. **Designing around a ligand**: Place ORI near the ligand
2. **Off-center motifs**: When your motif isn't at the structure's COM
3. **Symmetric design**: Place ORI at symmetry axis (usually [0, 0, 0])
4. **Binder design**: Control where the binder should be placed

```python
# Find ligand center for ORI placement
stored.coords = []
iterate_state 1, resn RET, stored.coords.append([x,y,z])
import numpy as np
ret_com = np.mean(stored.coords, axis=0)
print("Suggested ori_token:", list(ret_com))

# Visualize
pseudoatom ori_marker, pos=list(ret_com)
show spheres, ori_marker
color green, ori_marker
set sphere_scale, 1.5, ori_marker
```

### Recentering Structures

If your structure needs to be recentered (e.g., for symmetric design):

```python
# Recenter on origin
translate [-com_x, -com_y, -com_z], all

# Or recenter on ligand
stored.coords = []
iterate_state 1, resn RET, stored.coords.append([x,y,z])
import numpy as np
ret_com = np.mean(stored.coords, axis=0)
translate list(-ret_com), all

# Verify
com all  # Should show position near [0, 0, 0]

# Save recentered structure
save structure_centered.pdb, all
```

### ORI Config Examples

#### Binder Design (ORI from hotspots)
```json
{
    "binder_design": {
        "input": "target.pdb",
        "contig": "A1-150,/0,80-100",
        "select_hotspots": "A50-60,A75-85",
        "infer_ori_strategy": "hotspots"
    }
}
```

#### Ligand-centered Design (explicit ORI)
```json
{
    "ligand_centered": {
        "input": "opsin.pdb",
        "contig": "A1-126,20-30,A157-300",
        "ligand": "RET",
        "ori_token": [12.5, -3.2, 8.7]
    }
}
```

#### Symmetric Design (ORI at origin)
```json
{
    "symmetric_c3": {
        "input": "trimer_centered.pdb",
        "contig": "A1-300",
        "symmetry": {"id": "C3"},
        "ori_token": [0.0, 0.0, 0.0]
    }
}
```

---

## Symmetry for Multimeric Proteins

Many proteins (including channelrhodopsins) are homotrimers or homodimers. RFD3 supports symmetric design through the `symmetry` field.

### Monomer vs Symmetric Design

| Approach | When to Use |
|----------|-------------|
| **Monomer only** | Simpler; good for initial exploration; RFD3 designs a single chain |
| **Symmetric (C2, C3, D2...)** | Preserves oligomeric interfaces; designs all subunits consistently |

### Symmetry Types

| ID | Description | Subunits |
|----|-------------|----------|
| `C2` | Cyclic 2-fold (dimer) | 2 |
| `C3` | Cyclic 3-fold (trimer) | 3 |
| `C4` | Cyclic 4-fold | 4 |
| `D2` | Dihedral 2-fold | 4 |
| `D3` | Dihedral 3-fold | 6 |

### Preparing for Symmetric Design

**Critical**: Input structure must be pre-centered and pre-symmetrized around the origin.

```python
# Load multimer
load homotrimer.pdb

# Check if centered on origin
com all
# Should be near [0, 0, 0]

# If not, recenter
stored.coords = []
iterate_state 1, name CA, stored.coords.append([x,y,z])
import numpy as np
current_com = np.mean(stored.coords, axis=0)
translate list(-current_com), all

# Verify symmetry axis
# For C3: chains should be ~120° apart around z-axis
select chain_a, chain A and name CA and resi 1
select chain_b, chain B and name CA and resi 1
select chain_c, chain C and name CA and resi 1
# Check positions manually

# Save centered structure
save homotrimer_centered.pdb, all
```

### Symmetric Motif Design

For a C3 homotrimer where you want to redesign a loop in all three chains:

```python
# Visualize what will be symmetric
# Load and show all chains
as cartoon
util.cbc  # Color by chain

# Select the region to redesign (appears in all chains)
select design_loop, resi 50-70
color magenta, design_loop

# The motif (fixed) - symmetric across chains
select motif, resi 80+85+90
show sticks, motif
color cyan, motif
```

Config for symmetric design:
```json
{
    "symmetric_trimer_design": {
        "input": "homotrimer_centered.pdb",
        "contig": "A1-49,15-25,A71-150",
        "symmetry": {
            "id": "C3",
            "is_symmetric_motif": true
        },
        "is_non_loopy": true
    }
}
```

### Asymmetric Components (is_unsym_motif)

When some components should NOT be symmetrized (e.g., a single DNA molecule bound to a symmetric protein):

```python
# Protein is symmetric (chains A, B, C)
# DNA is asymmetric (chains Y, Z)
select protein, chain A+B+C
select dna, chain Y+Z
color gray, protein
color yellow, dna
```

Config:
```json
{
    "symmetric_with_asymm_dna": {
        "input": "protein_dna_complex.pdb",
        "contig": "150-150,/0,Y1-11,/0,Z16-25",
        "symmetry": {
            "id": "C3",
            "is_unsym_motif": "Y1-11,Z16-25"
        },
        "is_non_loopy": true
    }
}
```

### Monomer Design for Symmetric Proteins

Sometimes it's easier to design on a single chain and rely on natural symmetry:

```python
# Extract just chain A
select monomer, chain A
# Also get the ligand
select monomer, monomer or resn RET

save monomer_with_ret.pdb, monomer
```

Config (no symmetry, just design the monomer):
```json
{
    "monomer_design": {
        "input": "monomer_with_ret.pdb",
        "contig": "A1-49,15-25,A71-300",
        "ligand": "RET",
        "cif_parser_args": {
            "remove_ccds": ["HOH", "NA", "CL", "GOL"]
        }
    }
}
```

### Symmetry Workflow

1. **Decide**: Monomer or symmetric?
   - Monomer if: exploring, interface not critical, simpler
   - Symmetric if: interface matters, designing oligomer-specific features

2. **Prepare structure**:
   - Remove unwanted components (`remove_ccds`)
   - Center on origin (for symmetric)
   - Verify symmetry alignment

3. **Configure symmetry**:
   - Set `symmetry.id` (C2, C3, D2, etc.)
   - Mark asymmetric components with `is_unsym_motif`
   - Place ORI at origin for symmetric designs

4. **Memory considerations**:
   - Symmetric designs use more memory
   - Set `diffusion_batch_size=1` for large symmetric structures
   - Consider `low_memory_mode=True`

---

## Hydrogen Bond Analysis and Protection

A critical part of protein design is identifying and preserving important hydrogen bonds. RFD3 supports H-bond conditioning via `select_hbond_donor` and `select_hbond_acceptor` fields.

### Step 1: Identify H-bonds in PyMOL

```python
# Method 1: Use PyMOL's built-in H-bond finder
# Shows all H-bonds in structure
h_add  # Add hydrogens first
distance hbonds, (all), (all), mode=2

# Method 2: Find H-bonds to specific selection (e.g., ligand)
distance ligand_hbonds, (resn RET), (protein), mode=2

# Method 3: Find H-bonds in a region
distance region_hbonds, (resi 80-120), (resi 80-120), mode=2
```

### Step 2: Identify Critical H-bonds

Look for H-bonds that are:
- **Ligand-coordinating**: Between protein and ligand (substrate, cofactor, chromophore)
- **Structural**: Stabilizing key secondary structure elements
- **Functional**: Part of active site or binding pocket
- **Cross-region**: Connecting the design region to fixed regions

```python
# Show H-bonds to ligand with distances
select ligand, resn RET
select protein_near_ligand, byres (protein within 4 of ligand)
distance lig_hbonds, ligand, protein_near_ligand, mode=2

# Color H-bond donors (typically N, sometimes O)
select donors, (elem N and neighbor elem H) or (resn SER+THR+TYR and name OG+OG1+OH)
color blue, donors and protein_near_ligand

# Color H-bond acceptors (typically O, sometimes N)
select acceptors, elem O or (elem N and not neighbor elem H)
color red, acceptors and protein_near_ligand
```

### Step 3: List H-bond Atoms

```python
# Iterate through H-bond pairs to get atom names
# After running h_add and creating hbonds distance object:

# Get residues involved in H-bonds to ligand
iterate (byres (protein within 3.5 of resn RET) and (elem N or elem O)), print("%s%s %s" % (chain, resi, name))
```

Common H-bond atoms by residue type:

| Residue | Donors | Acceptors |
|---------|--------|-----------|
| Backbone | N | O |
| Ser | OG | OG |
| Thr | OG1 | OG1, O |
| Tyr | OH | OH, O |
| Asn | ND2 | OD1 |
| Gln | NE2 | OE1 |
| Asp | - | OD1, OD2 |
| Glu | - | OE1, OE2 |
| Lys | NZ | - |
| Arg | NE, NH1, NH2 | - |
| His | ND1, NE2 | ND1, NE2 |
| Trp | NE1 | - |

### Step 4: Visualize H-bonds to Protect

```python
# Create a clear visualization of H-bonds to protect
hide everything
show cartoon, all
color gray, all

# Show the design region
select design_region, resi 50-80
color magenta, design_region

# Show residues with H-bonds crossing into/out of design region
select hbond_anchors, resi 48+49+81+82  # residues flanking design region
show sticks, hbond_anchors
color cyan, hbond_anchors

# Show the specific H-bonds
distance protected_hbonds, resi 48+49, resi 50-52, mode=2
distance protected_hbonds2, resi 78-80, resi 81+82, mode=2

# Label the atoms involved
label hbond_anchors and (name N or name O or name OG*), "%s-%s" % (resi, name)
```

### Step 5: Specify H-bond Protection in Config

The `select_hbond_donor` and `select_hbond_acceptor` fields tell RFD3 to preserve these interactions.

**Important**: These fields only accept dict format, not bool or contig strings.

```json
{
    "hbond_protected_design": {
        "input": "structure.pdb",
        "contig": "A1-49,25-35,A81-150",
        "select_hbond_donor": {
            "A48": "N",
            "A49": "N",
            "A81": "N",
            "A82": "N,NZ"
        },
        "select_hbond_acceptor": {
            "A48": "O",
            "A49": "O",
            "A81": "O",
            "A82": "O"
        }
    }
}
```

### H-bond Conditioning Examples

#### Example 1: Protect Ligand Coordination

For a channelrhodopsin with retinal (RET), protect the Schiff base and counterion H-bonds:

```python
# Visualize Schiff base region
select schiff_base, resi 292  # Lys forming Schiff base
select counterion, resi 123+253  # Glu/Asp counterions
show sticks, schiff_base or counterion
color cyan, schiff_base or counterion
distance sb_hbonds, schiff_base, counterion, mode=2
```

Config:
```json
{
    "select_hbond_donor": {
        "A292": "NZ"
    },
    "select_hbond_acceptor": {
        "A123": "OE1,OE2",
        "A253": "OD1,OD2"
    }
}
```

#### Example 2: Protect Helix Capping

When designing a loop that connects to helices, protect the helix capping H-bonds:

```python
# N-cap of helix (first 4 residues have unsatisfied backbone N)
select helix_start, resi 81-84
# C-cap of helix (last 4 residues have unsatisfied backbone O)
select helix_end, resi 45-48

show sticks, helix_start or helix_end
distance cap_hbonds, helix_start, helix_end, mode=2
```

Config:
```json
{
    "select_hbond_donor": {
        "A81": "N",
        "A82": "N",
        "A83": "N"
    },
    "select_hbond_acceptor": {
        "A45": "O",
        "A46": "O",
        "A47": "O"
    }
}
```

#### Example 3: Protect Beta Sheet H-bonds

For designs near beta sheets, protect the strand-strand H-bonds:

```python
# Adjacent beta strands
select strand1, resi 20-25
select strand2, resi 40-45
show cartoon, strand1 or strand2
distance sheet_hbonds, strand1, strand2, mode=2
```

Config:
```json
{
    "select_hbond_donor": {
        "A21": "N",
        "A23": "N",
        "A25": "N",
        "A41": "N",
        "A43": "N",
        "A45": "N"
    },
    "select_hbond_acceptor": {
        "A21": "O",
        "A23": "O",
        "A25": "O",
        "A41": "O",
        "A43": "O",
        "A45": "O"
    }
}
```

### Workflow: From H-bond Analysis to Config

1. **Load structure** and add hydrogens: `h_add`

2. **Find all H-bonds**: `distance hbonds, all, all, mode=2`

3. **Identify design region** and find H-bonds crossing boundaries:
   ```python
   select design, resi 50-80
   select fixed, not design
   distance boundary_hbonds, design, fixed, mode=2
   ```

4. **List the atoms** involved in boundary H-bonds:
   ```python
   # Get the specific atoms
   iterate (resi 48-52+78-82) and (name N or name O), print("%s %s%s" % (name, chain, resi))
   ```

5. **Build the config** with `select_hbond_donor` and `select_hbond_acceptor`

6. **Visualize the protection** to confirm:
   ```python
   # Show protected H-bonds in green
   color green, (resi 48-52+78-82) and (name N or name O)
   ```

---

## Example Configs by Use Case

### 1. Enzyme Design (Active Site Scaffolding)

Visualize:
```python
# Load enzyme with substrate
load enzyme.pdb
select active_site, resi 108+139+152+156
select substrate, resn NAI+ACT
show sticks, active_site
show spheres, substrate
color cyan, active_site
color yellow, substrate
```

Config:
```json
{
    "enzyme_design": {
        "input": "enzyme.pdb",
        "ligand": "NAI,ACT",
        "unindex": "A108,A139,A152,A156",
        "length": "180-200",
        "select_fixed_atoms": {
            "A108": "ND2,CG",
            "A139": "OG,CB,CA",
            "A152": "OH,CZ",
            "A156": "NZ,CE,CD",
            "ACT": "OXT",
            "NAI": ""
        }
    }
}
```

### 2. Protein Binder Design

Visualize:
```python
# Load target protein
load target.pdb
# Show target surface
select target, chain A
show surface, target
color gray, target
set transparency, 0.7, target

# Highlight hotspots
select hotspots, chain A and resi 50-60+75-85
color red, hotspots
show spheres, hotspots
```

Config:
```json
{
    "binder_design": {
        "input": "target.pdb",
        "contig": "A1-150,/0,80-100",
        "select_hotspots": "A50-60,A75-85",
        "infer_ori_strategy": "hotspots",
        "is_non_loopy": true
    }
}
```

### 3. Partial Diffusion (Structure Refinement)

Visualize:
```python
# Load structure to refine
load structure.pdb
# Highlight residues to constrain
select constraints, resi 431+572+573
show sticks, constraints
color orange, constraints
```

Config:
```json
{
    "partial_diffusion": {
        "input": "structure.pdb",
        "ligand": "RET",
        "partial_t": 10.0,
        "unindex": "A431,A572-573",
        "select_fixed_atoms": {
            "A431": "TIP",
            "A572": "BKBN",
            "A573": "BKBN"
        }
    }
}
```

### 4. Symmetric Design (Cyclic)

Visualize:
```python
# Load symmetric structure
load symmetric.pdb
# Color by chain
util.cbc
# Show symmetry axis
pseudoatom symmetry_axis, pos=[0, 0, 0]
```

Config:
```json
{
    "symmetric_C3": {
        "length": "100",
        "is_non_loopy": true,
        "symmetry": {
            "id": "C3"
        }
    }
}
```

### 5. Channelrhodopsin Infill Design

Visualize:
```python
# Load opsin structure
load opsin.cif

# Check what's in the structure
stored.resnames = set()
iterate hetatm, stored.resnames.add(resn)
print("Non-protein:", stored.resnames)  # e.g., RET, HOH, NA, CL

# Clean up
remove resn HOH+NA+CL+GOL+PEG+EDO

# Show retinal
select retinal, resn RET
show spheres, retinal
color yellow, retinal

# Fixed residues (key functional sites)
select key_residues, resi 85+90+123+253+257+292
show sticks, key_residues
color cyan, key_residues

# Design region (loop to redesign)
select design_loop, resi 127-145
color magenta, design_loop
```

Config:
```json
{
    "opsin_infill": {
        "input": "opsin.cif",
        "contig": "A1-126,15-25,A146-300",
        "ligand": "RET",
        "cif_parser_args": {
            "remove_ccds": ["HOH", "NA", "CL", "GOL", "PEG", "EDO", "SO4"]
        },
        "select_fixed_atoms": {
            "A85": "ALL",
            "A90": "ALL",
            "A123": "TIP",
            "A253": "TIP",
            "A257": "TIP",
            "A292": "TIP"
        },
        "is_non_loopy": true,
        "plddt_enhanced": true
    }
}
```

### 6. Channelrhodopsin with C3 Symmetry

For designing a homotrimeric channelrhodopsin:

Visualize:
```python
# Load trimer
load chr_trimer.cif

# Check centering
com all  # Should be near [0, 0, 0]

# If not centered, recenter
stored.coords = []
iterate_state 1, name CA, stored.coords.append([x,y,z])
import numpy as np
current_com = np.mean(stored.coords, axis=0)
translate list(-current_com), all

# Color by chain to see symmetry
util.cbc

# Show retinal in each chain
select retinal, resn RET
show spheres, retinal
color yellow, retinal

# Design loop (same in all chains)
select design_loop, resi 127-145
color magenta, design_loop
```

Config:
```json
{
    "opsin_trimer_symmetric": {
        "input": "chr_trimer_centered.cif",
        "contig": "A1-126,15-25,A146-300",
        "ligand": "RET",
        "symmetry": {
            "id": "C3",
            "is_symmetric_motif": true
        },
        "cif_parser_args": {
            "remove_ccds": ["HOH", "NA", "CL", "GOL", "PEG"]
        },
        "ori_token": [0.0, 0.0, 0.0],
        "is_non_loopy": true
    }
}
```

---

## PyMOL Utility Commands

### Save Current View
```python
# Save view for later
get_view
# Restore view
set_view (...)
```

### Measure Distances
```python
# Distance between atoms
distance d1, /obj//A/102/CA, /obj//A/106/CA

# All distances < 4Å to ligand
select contacts, byres (protein within 4 of ligand)
```

### Export Selection as Residue List
```python
# Get residue numbers in selection
iterate (fixed_motif and n. CA), print(resi)
```

### Create Session for Review
```python
# Save session
save design_review.pse

# Save image
ray 1600, 1200
png design_preview.png
```

### Reset and Start Over
```python
# Reset all
reinitialize

# Or just clear selections and colors
delete all_selections
color gray, all
hide everything
show cartoon
```

---

## Conversation Patterns

### Starting a Design Session

User: "I want to design a new loop in my channelrhodopsin"

Claude should:
1. Ask for structure path or PDB ID
2. Load into PyMOL: `load structure.cif`
3. **Check structure contents**:
   ```python
   # List all components
   stored.resnames = set()
   iterate all, stored.resnames.add(resn)
   print(sorted(stored.resnames))
   ```
4. **Ask about symmetry**: "This looks like a trimer - should we design as monomer or use C3 symmetry?"
5. Ask which region to redesign
6. Visualize: select and color the region
7. Ask about constraints (fixed residues, ligand)
8. Visualize constraints
9. Confirm with user
10. Generate config

### Structure Cleanup

User: "Load 6EID from the PDB"

Claude should:
1. Fetch: `fetch 6EID`
2. List components:
   ```python
   stored.resnames = set()
   iterate hetatm, stored.resnames.add(resn)
   print("Non-protein components:", stored.resnames)
   ```
3. Report: "Found: RET, HOH, NA, CL, GOL. I'll keep RET and remove the rest."
4. Clean and visualize:
   ```python
   remove resn HOH+NA+CL+GOL
   show spheres, resn RET
   color yellow, resn RET
   ```
5. Note in config:
   ```json
   "cif_parser_args": {"remove_ccds": ["HOH", "NA", "CL", "GOL"]}
   ```

### Symmetry Decision

User: "Should I use symmetry?"

Claude should:
1. Check structure:
   ```python
   # How many protein chains?
   stored.chains = set()
   iterate polymer, stored.chains.add(chain)
   print("Chains:", stored.chains)
   ```
2. Explain tradeoffs:
   - **Monomer**: Simpler, faster, good for exploration
   - **Symmetric**: Preserves interfaces, consistent across subunits
3. If symmetric, check centering:
   ```python
   com all  # Should be near origin
   ```
4. Recommend: "For a first pass, let's try monomer. We can add C3 symmetry later if the design looks good."

### ORI Placement

User: "Where should the origin be?"

Claude should:
1. Find current COM:
   ```python
   com all
   ```
2. Find ligand center (for opsins):
   ```python
   stored.coords = []
   iterate_state 1, resn RET, stored.coords.append([x,y,z])
   import numpy as np
   ret_com = np.mean(stored.coords, axis=0)
   print("Retinal center:", ret_com)
   pseudoatom ret_center, pos=list(ret_com)
   show spheres, ret_center
   color green, ret_center
   ```
3. Recommend based on design type:
   - Motif scaffolding: "ORI near the motif/ligand works well"
   - Symmetric: "ORI should be at [0, 0, 0] - we may need to recenter"
   - Binder: "Use `infer_ori_strategy: hotspots`"

### Analyzing H-bonds

User: "What H-bonds should I protect?"

Claude should:
1. Add hydrogens: `h_add`
2. Find H-bonds at design region boundaries:
   ```python
   select design, resi 50-80
   distance boundary_hbonds, (resi 48-52), (resi 78-82), mode=2
   ```
3. Find H-bonds to ligand/cofactor:
   ```python
   distance ligand_hbonds, resn RET, protein, mode=2
   ```
4. List the specific atoms:
   ```python
   iterate (byres boundary_hbonds) and (name N or name O), print("%s%s %s" % (chain, resi, name))
   ```
5. Show which are donors vs acceptors
6. Recommend `select_hbond_donor` and `select_hbond_acceptor` entries

### Iterating on Design

User: "Actually, also fix residue 85"

Claude should:
1. Add to fixed selection: `select fixed_motif, fixed_motif or resi 85`
2. Update visualization: `show sticks, fixed_motif; color cyan, fixed_motif`
3. Check for new H-bonds to protect: `distance new_hbonds, resi 85, design, mode=2`
4. Update config and show diff

### Finalizing

User: "That looks good, generate the config"

Claude should:
1. Summarize the design:
   - Fixed residues: [list]
   - Design region: start-end, length constraint
   - Ligand: name
   - H-bond protection: donors and acceptors
   - Other options
2. Generate JSON config
3. Optionally save PyMOL session for reference

---

## H-bond Analysis Tips

### Quick H-bond Checklist

Before finalizing a design config, verify:

- [ ] All H-bonds between design region and fixed regions identified
- [ ] Ligand-coordinating H-bonds included in donor/acceptor lists
- [ ] Helix/sheet capping H-bonds at design boundaries protected
- [ ] Functional H-bonds (active site, binding pocket) preserved
- [ ] Visualization confirms coverage of critical interactions

### Common Mistakes

1. **Missing backbone H-bonds**: The backbone N and O are often the most important H-bond atoms at region boundaries

2. **Forgetting both donor AND acceptor**: An H-bond has two ends - specify both the donor residue and acceptor residue

3. **Wrong atom names**: Use standard PDB atom names (OG not OG1 for Ser, but OG1 for Thr)

4. **Over-constraining**: Don't specify H-bonds for residues in the middle of design regions - only at boundaries or for functional sites

---

## References

- [RFD3 README (Getting Started)](https://github.com/RosettaCommons/foundry/blob/production/models/rfd3/README.md)
- [RFD3 Input Specification](https://github.com/RosettaCommons/foundry/blob/production/models/rfd3/docs/input.md)
- [RFD3 Enzyme Design](https://github.com/RosettaCommons/foundry/blob/production/models/rfd3/docs/enzyme_design.md)
- [RFD3 Symmetry](https://github.com/RosettaCommons/foundry/blob/production/models/rfd3/docs/symmetry.md)
- [RFD3 Protein Binder Design](https://github.com/RosettaCommons/foundry/blob/production/models/rfd3/docs/protein_binder_design.md)
- [RFD3 Small Molecule Binder Design](https://github.com/RosettaCommons/foundry/blob/production/models/rfd3/docs/sm_binder_design.md)
- [RFD3 Nucleic Acid Binder Design](https://github.com/RosettaCommons/foundry/blob/production/models/rfd3/docs/na_binder_design.md)
- [pymol-agent-bridge PyMOL Integration](https://github.com/ANaka/pymol-agent-bridge)

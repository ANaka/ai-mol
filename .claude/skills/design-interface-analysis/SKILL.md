---
name: design-interface-analysis
description: Use when analyzing protein-protein or protein-ligand interfaces in designed complexes, computing buried surface area, identifying hotspot contacts, or characterizing binding interfaces through PyMOL.
version: 0.1.0
---

# Design Interface Analysis

Workflows for characterizing interfaces in designed protein complexes. Composes with @rfdiffusion-viz (binder outputs), @alphafold-validation (AF2-Multimer), and @binding-site-visualization (existing ligand analysis).

> **Send all `cmd.*` code via:** `~/.pymol-agent-bridge/bin/pymol-agent-bridge exec "..."` (or heredoc for multi-line). See @pymol-fundamentals for details.

## Interface Identification

### Define Interface Residues

```python
# Standard: residues with any atom within 4A of the partner chain
cmd.select("interface_A", "byres (chain A within 4 of chain B)")
cmd.select("interface_B", "byres (chain B within 4 of chain A)")

# Tighter cutoff for direct contacts
cmd.select("contacts_A", "byres (chain A within 3.5 of chain B)")
cmd.select("contacts_B", "byres (chain B within 3.5 of chain A)")
```

### Count Interface Residues

```python
n_A = cmd.count_atoms("interface_A and name CA")
n_B = cmd.count_atoms("interface_B and name CA")
print("Interface residues: %d (chain A) + %d (chain B) = %d total" % (n_A, n_B, n_A + n_B))
```

### Visualize Interface

```python
# Standard interface view
cmd.color("gray80", "chain A")
cmd.color("marine", "chain B")
cmd.show("cartoon")

cmd.show("sticks", "interface_A or interface_B")
cmd.color("tv_red", "interface_A and elem C")
cmd.color("tv_blue", "interface_B and elem C")
```

## Hydrogen Bonds

### Detect Interface H-Bonds

```python
cmd.distance("hbonds", "chain A", "chain B", mode=2)
cmd.set("dash_color", "yellow", "hbonds")
cmd.set("dash_width", 2.0, "hbonds")
cmd.set("dash_gap", 0.2, "hbonds")
```

### Count H-Bonds

```python
# Get H-bond distances
stored.hbond_list = []
cmd.iterate("hbonds", "stored.hbond_list.append(1)")
# Note: each H-bond creates multiple pseudoatoms in the distance object
# A more reliable count:
hbond_count = cmd.count_atoms("hbonds") // 2
print("Interface H-bonds: ~%d" % hbond_count)
```

### Donor/Acceptor Annotation

```python
# Highlight H-bond donors (N-H) and acceptors (O, N)
cmd.select("donors", "(interface_A or interface_B) and (elem N and neighbor elem H)")
cmd.select("acceptors", "(interface_A or interface_B) and (elem O or (elem N and not neighbor elem H))")
cmd.color("blue", "donors")
cmd.color("red", "acceptors")
```

## Salt Bridges

```python
# Identify charged residue pairs across the interface
cmd.select("pos_A", "chain A and (resn ARG+LYS) and name NZ+NH1+NH2")
cmd.select("neg_B", "chain B and (resn ASP+GLU) and name OD1+OD2+OE1+OE2")
cmd.select("neg_A", "chain A and (resn ASP+GLU) and name OD1+OD2+OE1+OE2")
cmd.select("pos_B", "chain B and (resn ARG+LYS) and name NZ+NH1+NH2")

# Salt bridges (< 4A between charged groups)
cmd.distance("salt_bridges_1", "pos_A", "neg_B", cutoff=4.0, mode=0)
cmd.distance("salt_bridges_2", "neg_A", "pos_B", cutoff=4.0, mode=0)
cmd.set("dash_color", "magenta", "salt_bridges_1")
cmd.set("dash_color", "magenta", "salt_bridges_2")
```

## Hydrophobic Contacts

```python
# Hydrophobic residues at the interface
cmd.select("hydrophobic_A", "interface_A and resn ALA+VAL+LEU+ILE+MET+PHE+TRP+PRO")
cmd.select("hydrophobic_B", "interface_B and resn ALA+VAL+LEU+ILE+MET+PHE+TRP+PRO")

n_hp_A = cmd.count_atoms("hydrophobic_A and name CA")
n_hp_B = cmd.count_atoms("hydrophobic_B and name CA")
print("Hydrophobic interface residues: %d (A) + %d (B)" % (n_hp_A, n_hp_B))

cmd.show("sticks", "hydrophobic_A or hydrophobic_B")
cmd.color("yellow", "(hydrophobic_A or hydrophobic_B) and elem C")
```

## Buried Surface Area (BSA)

### Compute BSA

```python
# SASA of each chain alone vs. in complex
cmd.set("dot_solvent", 1)
cmd.set("dot_density", 3)

sasa_A_alone = cmd.get_area("chain A")
sasa_B_alone = cmd.get_area("chain B")
sasa_complex = cmd.get_area("chain A or chain B")

bsa = (sasa_A_alone + sasa_B_alone - sasa_complex) / 2.0
print("Buried surface area: %.0f A^2" % bsa)
```

### BSA Interpretation for Design

| BSA (A^2) | Interpretation |
|-----------|---------------|
| < 500 | Very small interface — likely weak/transient |
| 500-1000 | Small interface — typical for designed mini-binders |
| 1000-2000 | Medium interface — good for designed binders |
| > 2000 | Large interface — typical for natural complexes |

### Color by Burial

```python
# Color interface residues by how buried they are
cmd.set("dot_solvent", 1)
stored.burial = {}

# Get per-residue SASA in complex
cmd.iterate("chain B and name CA", "stored.burial[int(resi)] = 0")
for resi in stored.burial:
    sasa_alone = cmd.get_area("chain B and resi %d" % resi)
    sasa_complex = cmd.get_area("chain B and resi %d and not (chain B and byres(chain B within 4 of chain A))" % resi)
    # Approximate: fully buried residues at interface
```

## Hotspot Identification

Identify key interface residues that contribute most to binding.

### By Contact Density

```python
# Rank interface residues by number of cross-chain contacts
stored.contacts = {}
cmd.iterate("interface_B and name CA", "stored.contacts[int(resi)] = 0")
for resi in stored.contacts:
    n = cmd.count_atoms("chain A within 4 of (chain B and resi %d)" % resi)
    stored.contacts[resi] = n

# Sort by contact count
ranked = sorted(stored.contacts.items(), key=lambda x: -x[1])
print("Top hotspot residues (binder):")
for resi, n in ranked[:10]:
    stored.resn = []
    cmd.iterate("chain B and resi %d and name CA" % resi, "stored.resn.append(resn)")
    print("  %s%d: %d contacts" % (stored.resn[0] if stored.resn else "?", resi, n))

# Color top hotspots
top_resi = "+".join(str(r) for r, _ in ranked[:5])
cmd.select("hotspots", "chain B and resi %s" % top_resi)
cmd.show("spheres", "hotspots and name CA")
cmd.color("red", "hotspots")
```

### From Known Complex (Binder Design Input)

```python
# Identify target hotspots from a known binder-target complex
# These become RFdiffusion hotspot inputs
cmd.load("known_complex.pdb", "reference")
cmd.select("ref_interface", "byres (chain A within 4 of chain B)")

stored.ref_contacts = {}
cmd.iterate("ref_interface and name CA", "stored.ref_contacts[int(resi)] = 0")
for resi in stored.ref_contacts:
    n = cmd.count_atoms("chain B within 3.5 of (chain A and resi %d)" % resi)
    stored.ref_contacts[resi] = n

ranked = sorted(stored.ref_contacts.items(), key=lambda x: -x[1])
hotspot_resi = [str(r) for r, n in ranked[:10]]
print("Hotspot residues for RFdiffusion: %s" % ",".join(hotspot_resi))

cmd.select("hotspots", "chain A and resi %s" % "+".join(hotspot_resi))
cmd.show("spheres", "hotspots")
cmd.color("red", "hotspots")
```

## Shape Complementarity

### Visual Assessment

```python
# Show surfaces at interface colored by electrostatics proxy
cmd.show("surface", "interface_A")
cmd.show("surface", "interface_B")

# Color by charge (crude electrostatics)
cmd.color("blue", "interface_A and resn ARG+LYS")
cmd.color("red", "interface_A and resn ASP+GLU")
cmd.color("white", "interface_A and not resn ARG+LYS+ASP+GLU")
cmd.color("blue", "interface_B and resn ARG+LYS")
cmd.color("red", "interface_B and resn ASP+GLU")
cmd.color("white", "interface_B and not resn ARG+LYS+ASP+GLU")

cmd.set("transparency", 0.4)
```

### Gap Analysis

```python
# Check for voids at the interface
# Show surface of one chain, cartoon of the other
cmd.show("surface", "chain A")
cmd.set("transparency", 0.3, "chain A")
cmd.show("cartoon", "chain B")
cmd.show("sticks", "interface_B")
# Visually inspect for gaps between the surface and sticks
```

## Interface Comparison (Design vs. Reference)

```python
# Compare designed interface to a natural complex
cmd.load("natural_complex.pdb", "natural")
cmd.load("designed_complex.pdb", "designed")

# Align on target chain
cmd.align("designed and chain A", "natural and chain A")

# Compare binder positioning
cmd.color("gray70", "chain A")
cmd.color("green", "natural and chain B")
cmd.color("marine", "designed and chain B")
cmd.show("cartoon")
```

## Tips

- Interface cutoff of 4A is standard; use 3.5A for stringent direct contacts
- BSA > 1000 A^2 is a good target for designed binders
- Hotspot residues with > 5 cross-chain contacts are strong anchors
- Charge complementarity across the interface is a positive design signal
- Always check H-bonds AND hydrophobic packing — good interfaces have both
- For binder design, extract hotspots from known complexes to feed into RFdiffusion (see @rfd3)
- See @binding-site-visualization for protein-ligand interface analysis (small molecule focus)

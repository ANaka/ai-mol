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

## Metal and Cofactor Visualization

### Select Metals

```python
cmd.select("metals", "elem Cu+Fe+Zn+Mg+Mn+Ca")
cmd.show("spheres", "metals")
cmd.color("orange", "metals")
```

### Select Heme Groups

```python
cmd.select("heme", "resn HEM+HEC+HEA")
cmd.show("sticks", "heme")
```

### Coordination Sphere

```python
cmd.select("coord_sphere", "byres (polymer.protein within 3 of metals)")
cmd.show("sticks", "coord_sphere")
cmd.color("yellow", "coord_sphere and elem C")
```

## Residue Property Selection

### By Charge

```python
cmd.select("basic", "resn ARG+LYS+HIS")
cmd.select("acidic", "resn ASP+GLU")
cmd.select("charged", "resn ARG+LYS+HIS+ASP+GLU")
```

### By Hydrophobicity

```python
cmd.select("hydrophobic", "resn ALA+VAL+ILE+LEU+MET+PHE+TRP+PRO")
cmd.select("polar", "resn SER+THR+CYS+TYR+ASN+GLN")
```

### Color by Property

```python
cmd.color("blue", "resn ARG+LYS+HIS")      # Basic (positive)
cmd.color("red", "resn ASP+GLU")            # Acidic (negative)
cmd.color("yellow", "hydrophobic")          # Hydrophobic
cmd.color("cyan", "polar")                   # Polar uncharged
```

---

## NMR Ensemble Handling

### Check Number of States

```python
states = cmd.count_states("object_name")
print("States: " + str(states))
```

### Show All States Overlaid

```python
cmd.set("all_states", 1)  # Overlay all states
cmd.set("all_states", 0)  # Show one state at a time
```

### Create Movie Through States

```python
n_states = cmd.count_states("object_name")
cmd.mset("1 -" + str(n_states))  # Each frame = one state
cmd.mplay()  # Start playback
```

### Style for Ensemble Visualization

```python
cmd.set("all_states", 1)
cmd.show("lines", "all")
cmd.set("line_width", 1)
cmd.color("gray70", "all")
# Highlight specific state
cmd.set("state", 1)
cmd.color("red", "all")
```

## Programmatic Measurements

### Get Distance (Returns Value)

```python
d = cmd.get_distance("sel1", "sel2")
print("Distance: " + str(round(d, 2)) + " A")
```

### Get Angle

```python
a = cmd.get_angle("atom1", "atom2", "atom3")
print("Angle: " + str(round(a, 1)) + " degrees")
```

### Get Dihedral

```python
# Backbone psi angle example
d = cmd.get_dihedral(
    "resi 10 and name N",
    "resi 10 and name CA",
    "resi 10 and name C",
    "resi 11 and name N"
)
print("Psi: " + str(round(d, 1)) + " degrees")
```

### Pair Fit (Align Specific Atoms)

```python
# Align first 30 CA atoms and return RMSD
rmsd = cmd.pair_fit(
    "mobile and resi 1-30 and name CA",
    "target and resi 1-30 and name CA"
)
print("Pair fit RMSD: " + str(round(rmsd, 2)) + " A")
```

## Finding Contacts

### Select Contacting Residues

```python
# Select residues from A that contact B
cmd.select("contact_A", "byres (chain A within 4 of chain B)")
cmd.select("contact_B", "byres (chain B within 4 of chain A)")
```

### Iterate to Get Contact List

```python
contacts = []
cmd.iterate(
    "chain A within 4 of chain B",
    "contacts.append((resi, resn))",
    space={"contacts": contacts}
)
unique = list(set(contacts))
print("Contact residues: " + str(len(unique)))
```

### Visualize Contacts

```python
cmd.select("interface", "byres (chain A within 4 of chain B) or byres (chain B within 4 of chain A)")
cmd.show("sticks", "interface")
cmd.color("orange", "interface and chain A")
cmd.color("purple", "interface and chain B")
```

---

## Known Limitations

- **cmd.morph()** may not work reliably through socket connection
- **Electrostatic surfaces** require APBS or similar external tools
- **Some wizard operations** may need interactive PyMOL

---

## Solvent Accessible Surface Area

### Calculate Total SASA

```python
total_area = cmd.get_area("selection")
print("SASA: " + str(round(total_area, 1)) + " sq A")
```

### Color by SASA

```python
# Load SASA into B-factor column
cmd.get_area("selection", load_b=1)
# Color by SASA value
cmd.spectrum("b", "blue_white_red", "selection")
```

### Find Buried Residues

```python
cmd.get_area("protein", load_b=1)
buried = []
cmd.iterate(
    "protein and name CA",
    "buried.append((resi, resn)) if b < 10 else None",
    space={"buried": buried}
)
print("Buried residues: " + str(len(buried)))
```

### Select by Exposure

```python
cmd.get_area("protein", load_b=1)
cmd.select("exposed", "protein and name CA and b > 50")
cmd.select("buried", "protein and name CA and b < 10")
```

---

## Salt Bridges

### Select Salt Bridge Atoms

```python
# Basic nitrogen atoms
cmd.select("basic_atoms",
    "(resn ARG and name NH1+NH2+NE) or "
    "(resn LYS and name NZ) or "
    "(resn HIS and name ND1+NE2)")

# Acidic oxygen atoms
cmd.select("acidic_atoms",
    "(resn ASP and name OD1+OD2) or "
    "(resn GLU and name OE1+OE2)")
```

### Find and Display Salt Bridges

```python
cmd.distance("salt_bridges", "basic_atoms", "acidic_atoms",
             cutoff=4.0, mode=0)
cmd.set("dash_color", "yellow", "salt_bridges")
```

## Aromatic Interactions

### Select Aromatic Residues

```python
cmd.select("aromatic", "resn PHE+TYR+TRP")
cmd.select("aromatic_HIS", "resn HIS")  # Sometimes aromatic
```

### Visualize Aromatic Rings

```python
cmd.show("sticks", "resn PHE+TYR+TRP")
cmd.color("purple", "resn PHE+TYR+TRP and elem C")
```

---

## Data Extraction

### Get FASTA Sequence

```python
seq = cmd.get_fastastr("object_name")
print(seq)  # Full FASTA with header
```

### Get Residue List

```python
residues = []
cmd.iterate(
    "object and name CA",
    "residues.append((resi, resn))",
    space={"residues": residues}
)
print("Residues: " + str(len(residues)))
```

### Get Coordinates

```python
# Returns numpy array of shape (N, 3)
coords = cmd.get_coords("selection")
print("First atom: " + str(coords[0]))
```

### Center of Mass

```python
com = cmd.centerofmass("selection")
print("Center: " + str([round(c, 2) for c in com]))
```

### Get Model Object (Full Atom Data)

```python
model = cmd.get_model("selection")
for atom in model.atom:
    print(f"{atom.resn} {atom.resi} {atom.name}")
```

---

## TODO: Patterns to Add

- Map fitting and isosurface
- Custom CGO objects
- Cation-pi interactions

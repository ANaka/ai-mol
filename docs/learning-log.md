# PyMOL MCP Learning Log

Tracking experiments, discoveries, and issues during autodidact mission.

---

## Session: 2026-01-28

### Starting State
- On branch: skill-dev
- MCP server: pymol_mcp_server.py with 88 commands
- Goal: Learn PyMOL MCP through experimentation

---

## Experiments

### Experiment 1: Connection Test
**Time:** 2026-01-28
**Goal:** Verify MCP connection works
**Commands tried:** Direct socket connection with test print
**Result:** SUCCESS - Connected to PyMOL on port 9876
**Learned:** Connection protocol uses JSON with `type: pymol_command` and `code` field

---

### Experiment 2: Basic Visualization Commands
**Time:** 2026-01-28
**Goal:** Test fetch, show, color commands
**Commands tried:**
- `cmd.fetch("1ubq")` - SUCCESS, loaded ubiquitin
- `cmd.show("cartoon", "1ubq")` - SUCCESS
- `cmd.hide("lines", "1ubq")` - SUCCESS
- `cmd.color("red", "ss h")` - SUCCESS (helix coloring)
- `cmd.do("util.ss 1ubq")` - DEPRECATED, use `cmd.dss()` instead
- `cmd.spectrum("count", "rainbow", "1ubq")` - SUCCESS (rainbow by residue)
- `cmd.spectrum("b", "blue_white_red", "1ubq")` - SUCCESS (B-factor coloring)

**Result:** All basic visualization commands work via socket
**Learned:**
- `util.ss` is deprecated → use `cmd.dss()` for secondary structure assignment
- Spectrum palette options: rainbow, blue_white_red, etc.
- Can color by secondary structure type: `ss h` (helix), `ss s` (sheet), `ss l+` (loop)

---

### Experiment 3: Selection Syntax
**Time:** 2026-01-28
**Goal:** Test selection algebra through MCP
**Commands tried:**
- `cmd.select("name", "resi 1-10")` - SUCCESS (residue range)
- `cmd.select("ligand", "organic")` - SUCCESS (selects small molecules)
- `cmd.select("protein", "polymer.protein")` - SUCCESS
- `cmd.select("binding_site", "byres (protein within 5 of ligand)")` - SUCCESS (proximity selection)
- `cmd.count_atoms("selection")` - SUCCESS (returns atom count)

**Result:** Selection algebra works fully through socket
**Learned:**
- `organic` selects ligands/small molecules
- `polymer.protein` selects protein chains
- `byres (X within N of Y)` expands to full residues within distance
- `elem C` selects carbon atoms

---

### Experiment 4: Structure Alignment
**Time:** 2026-01-28
**Goal:** Test align and super commands
**Commands tried:**
- `cmd.fetch("1ubi")` then `cmd.align("1ubi", "1ubq")` - SUCCESS, RMSD 0.10 Å / 520 atoms
- `cmd.super("1ubi", "1ubq")` - SUCCESS, RMSD 0.10 Å / 520 atoms

**Result:** Alignment works, returns tuple with (RMSD, atoms_aligned, ...)
**Learned:**
- `align` uses sequence alignment first, then structure
- `super` uses structure-only alignment (good for different sequences)
- Both return results that can be captured: `result[0]` = RMSD, `result[1]` = atom count

---

### Experiment 5: Ligand and Binding Site Visualization
**Time:** 2026-01-28
**Goal:** Test protein-ligand visualization workflow
**Structure:** 1HSG (HIV protease with inhibitor)
**Commands tried:**
- Select ligand: `cmd.select("ligand", "organic")` → 45 atoms
- Select protein: `cmd.select("protein", "polymer.protein")` → 1514 atoms
- Binding site: `cmd.select("binding_site", "byres (protein within 5 of ligand)")` → 236 atoms
- Polar contacts: `cmd.distance("polar_contacts", "ligand", "binding_site", mode=2)` - SUCCESS

**Result:** Full ligand binding site workflow works
**Learned:**
- `mode=2` in distance command shows polar contacts (H-bonds)
- `util.cbag` colors by atom with green carbons
- Workflow: select ligand → select binding site → show interactions

---

### Experiment 6: Scenes and Movies
**Time:** 2026-01-28
**Goal:** Test scene storage and movie creation
**Commands tried:**
- `cmd.scene("F1", "store", message="Label")` - SUCCESS
- `cmd.scene("F1", "recall")` - SUCCESS
- `cmd.mset("1 x90")` - SUCCESS (90 frames)
- `cmd.mview("store")` at keyframes - SUCCESS

**Result:** Scene and movie commands work
**Learned:**
- Scenes store view, representations, and colors
- Movie workflow: mset → frame → scene recall → mview store

---

### Experiment 7: Rendering for Publication
**Time:** 2026-01-28
**Goal:** Test ray tracing and image export settings
**Commands tried:**
- `cmd.bg_color("white")` - SUCCESS
- `cmd.set("ray_opaque_background", 1)` - SUCCESS
- `cmd.ray(800, 600)` - SUCCESS (ray tracing takes ~2-3 seconds)

**Result:** Rendering works through socket
**Learned:**
- `ray_opaque_background` ensures solid background for publication
- Ray takes width, height as arguments
- For publication: white background, ray traced images

---

## Key Discoveries

### Working Selection Keywords
| Keyword | Selects |
|---------|---------|
| `organic` | Small molecules (ligands) |
| `polymer.protein` | Protein chains |
| `ss h` | Alpha helices |
| `ss s` | Beta sheets |
| `ss l+` | Loops |
| `elem X` | Element X (C, N, O, etc.) |
| `name CA` | Alpha carbons |
| `resi N-M` | Residue range |
| `byres (X within N of Y)` | Full residues within N Å |

### Useful Patterns
1. **Load and style protein:** `fetch → show cartoon → hide lines → color`
2. **Binding site view:** `select organic → select within → show sticks → polar contacts`
3. **Publication figure:** `bg_color white → set ray_opaque_background → ray`
4. **Multi-structure comparison:** `fetch both → align/super → color differently`

### Deprecated Commands
- `util.ss` → use `cmd.dss()` for secondary structure assignment

---

## Session 2: Continued Experiments

### Experiment 8: Alignment Methods
**Time:** 2026-01-28
**Goal:** Test align, super, and cealign differences
**Structures:** 1tim, 8tim (TIM barrel)
**Results:**
- `cmd.align()` - RMSD 0.78 Å, 3109 atoms, 5 cycles
- `cmd.super()` - RMSD 0.78 Å, 3089 atoms
- `cmd.cealign()` - RMSD 0.87 Å, 488 residues aligned

**Learned:**
- All three methods work through socket
- `align` returns tuple: (RMSD, atoms, cycles, pre_RMSD, pairs, score, length)
- `super` returns similar tuple
- `cealign` returns dict with "RMSD" and "alignment_length" keys
- `cealign` has REVERSED argument order: (target, mobile)
- `rms_cur()` calculates RMSD of current positions without transformation

---

### Experiment 9: Publication Figure Settings
**Time:** 2026-01-28
**Goal:** Test rendering and export settings
**Commands tried:**
- `cmd.set("antialias", 2)` - SUCCESS
- `cmd.set("ray_shadows", 0)` - SUCCESS
- `cmd.set("depth_cue", 0)` - SUCCESS
- `cmd.viewport(1200, 900)` - SUCCESS
- `cmd.png(path, 1200, 900, dpi=300, ray=1)` - SUCCESS

**Result:** Full publication workflow works
**Learned:**
- PNG export with ray tracing: `cmd.png(path, w, h, dpi=300, ray=1)`
- Key settings: antialias, ray_shadows, depth_cue
- Use `os.path.expanduser("~")` for home directory
- Ray tracing is slow but high quality

---

### Experiment 10: Binding Pocket Labels
**Time:** 2026-01-28
**Goal:** Add residue labels to binding site
**Commands tried:**
- `cmd.label("pocket and name CA", "resn+resi")` - SUCCESS
- `cmd.set("label_size", 14)` - SUCCESS
- `cmd.set("label_color", "black", "pocket")` - SUCCESS

**Result:** Labels work well
**Learned:**
- Label expression `resn+resi` gives "ALA45" format
- Label settings: label_size, label_color
- Labels only show on visible representations

---

## Skills Created

1. **pymol-fundamentals** - Core operations (selections, representations, colors, camera)
2. **binding-site-visualization** - Protein-ligand interaction visualization
3. **structure-alignment-analysis** - Structure comparison and RMSD
4. **publication-figures** - Ray tracing and export settings

---

## Server Improvements Identified

### Pattern Issues Found
1. `cealign` not in PYMOL_COMMANDS - cannot be used via MCP parse_and_execute
2. `rms_cur` not in PYMOL_COMMANDS
3. `viewport` not in PYMOL_COMMANDS (pattern exists but limited)
4. `dss` not in PYMOL_COMMANDS (newer alternative to util.ss)

### Missing Commands for Common Workflows
- `png` with dpi and ray parameters
- `label` with expression
- `cealign` for structural alignment

### Notes for Future
- Direct socket communication bypasses MCP server patterns
- For complex workflows, building Python code directly is more flexible
- MCP server patterns good for simple commands but limited for advanced use

---

## Server Improvements Made

Branch: `autodidact-improvements`

### Commands Added to PYMOL_COMMANDS

1. **cealign** - Combinatorial Extension structure alignment
   - Pattern: `cealign target, mobile`
   - Returns dict with RMSD and alignment_length

2. **rms** - RMSD without transformation
   - Pattern: `rms mobile, target`

3. **rms_cur** - RMSD at current positions
   - Pattern: `rms_cur mobile, target`

4. **dss** - Secondary structure assignment
   - Pattern: `dss selection`
   - Replaces deprecated util.ss

5. **mview** - Movie view storage
   - Pattern: `mview store|recall|clear|interpolate`

6. **count_atoms** - Atom counting
   - Pattern: `count_atoms selection`

7. **count_states** - State counting for NMR/MD
   - Pattern: `count_states object`

8. **get_names** - Object/selection listing
   - Pattern: `get_names type`

### Code Changes
- Added command definitions to PYMOL_COMMANDS dict
- Added handlers in build_pymol_code() for proper output

